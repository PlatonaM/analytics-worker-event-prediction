"""
   Copyright 2021 InfAI (CC SES)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

__all__ = ("Jobs",)


from ..logger import getLogger
from .. import models
from .. import event_prediction_pipeline
from . import Storage
import threading
import queue
import typing
import time
import uuid
import datetime
import base64
import gzip
import multiprocessing
import signal
import sys


logger = getLogger(__name__.split(".", 1)[-1])


def handle_sigterm(signo, stack_frame):
    logger.debug("got signal '{}' - exiting ...".format(signo))
    sys.exit(0)


class Result:
    def __init__(self):
        self.job: typing.Optional[models.Job] = None
        self.error = False


class Worker(multiprocessing.Process):
    def __init__(self, job: models.Job):
        super().__init__(name="jobs-worker-{}".format(job.id), daemon=True)
        self.__job = job
        self.result = multiprocessing.Queue()

    def run(self) -> None:
        signal.signal(signal.SIGTERM, handle_sigterm)
        signal.signal(signal.SIGINT, handle_sigterm)
        result_obj = Result()
        try:
            logger.debug("starting job '{}' ...".format(self.__job.id))
            self.__job.status = models.JobStatus.running
            predictions = dict()
            for model in self.__job.models:
                config = event_prediction_pipeline.config.config_from_dict(model.config)
                logger.debug(
                    "{}: predicting '{}' for '{}' ...".format(
                        self.__job.id, config["target_errorCode"],
                        config["target_col"]
                    )
                )
                logger.debug("model id '{}' created '{}'".format(model.id, model.created))
                prediction = event_prediction_pipeline.pipeline.run_pipeline(
                    df=event_prediction_pipeline.pipeline.df_from_csv(
                        self.__job.data_source,
                        model.time_field,
                        self.__job.sorted_data
                    ),
                    config=config,
                    clf=event_prediction_pipeline.pipeline.clf_from_pickle_bytes(
                        gzip.decompress(base64.standard_b64decode(model.data))
                    )
                )
                result = {
                    "target": config["target_errorCode"],
                    "result": prediction.tolist()[0]
                }
                if config["target_col"] not in predictions:
                    predictions[config["target_col"]] = [result]
                else:
                    predictions[config["target_col"]].append(result)
            self.__job.result = predictions
            self.__job.status = models.JobStatus.finished
            logger.debug("{}: completed successfully".format(self.__job.id))
        except Exception as ex:
            self.__job.status = models.JobStatus.failed
            self.__job.reason = str(ex)
            logger.error("{}: failed - {}".format(self.__job.id, ex))
            result_obj.error = True
        result_obj.job = self.__job
        self.result.put(result_obj)


class Jobs(threading.Thread):
    def __init__(self, stg_handler: Storage, check_delay: typing.Union[int, float], max_jobs: int):
        super().__init__(name="jobs-handler", daemon=True)
        self.__stg_handler = stg_handler
        self.__check_delay = check_delay
        self.__max_jobs = max_jobs
        self.__job_queue = queue.Queue()
        self.__job_pool: typing.Dict[str, models.Job] = dict()
        self.__worker_pool: typing.Dict[str, Worker] = dict()

    def create(self, data: dict) -> str:
        job = models.Job(data, id=uuid.uuid4().hex)
        job.created = '{}Z'.format(datetime.datetime.utcnow().isoformat())
        job.models = [models.Model(item) for item in job.models]
        self.__job_pool[job.id] = job
        return job.id

    def add_data_source(self, job_id: str, data_source: str):
        job = self.__job_pool[job_id]
        job.data_source = data_source
        job.status = models.JobStatus.pending
        self.__job_queue.put_nowait(job_id)

    def get_job(self, job_id: str) -> models.Job:
        return self.__job_pool[job_id]

    def run(self):
        while True:
            try:
                if len(self.__worker_pool) < self.__max_jobs:
                    try:
                        job_id = self.__job_queue.get(timeout=self.__check_delay)
                        worker = Worker(self.__job_pool[job_id])
                        self.__worker_pool[job_id] = worker
                        worker.start()
                    except queue.Empty:
                        pass
                else:
                    time.sleep(self.__check_delay)
                for job_id in list(self.__worker_pool.keys()):
                    if not self.__worker_pool[job_id].is_alive():
                        try:
                            res = self.__worker_pool[job_id].result.get(timeout=5)
                            self.__job_pool[job_id] = res.job
                        except queue.Empty:
                            logger.error("job '{}' quit with exitcode '{}'".format(job_id, self.__worker_pool[job_id].exitcode))
                            self.__job_pool[job_id].status = models.JobStatus.failed
                        self.__worker_pool[job_id].close()
                        del self.__worker_pool[job_id]
                        try:
                            self.__stg_handler.remove(self.__job_pool[job_id].data_source)
                        except Exception as ex:
                            logger.error("cleanup after job '{}' failed - {}".format(job_id, ex))
            except Exception as ex:
                logger.error("job handling failed - {}".format(ex))
