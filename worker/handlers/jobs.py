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
from .. import model
from .. event_prediction_pipeline.config import configs_pipeline
from ..event_prediction_pipeline.pipeline import run_pipeline
from . import Storage
import threading
import queue
import typing
import time
import uuid
import datetime
import base64
import gzip
import pickle
import dask.dataframe


logger = getLogger(__name__.split(".", 1)[-1])


class Worker(threading.Thread):
    def __init__(self, job: dict):
        super().__init__(name="jobs-worker-{}".format(job[model.Job.id]), daemon=True)
        self.job = job
        self.done = False

    def run(self) -> None:
        try:
            self.job[model.Job.status] = model.JobStatus.running
            df = dask.dataframe.read_csv(self.job[model.Job.data_source])
            df['time'] = dask.dataframe.to_datetime(df['time'])
            df = df.set_index('time')
            clf = pickle.loads(gzip.decompress(base64.standard_b64decode(self.job[model.Job.model][model.Model.data])))
            self.job[model.Job.result] = str(run_pipeline(df, configs_pipeline[0], clf))
            self.job[model.Job.status] = model.JobStatus.finished
        except Exception as ex:
            self.job[model.Job.status] = model.JobStatus.failed
            self.job[model.Job.reason] = str(ex)
            logger.error("job '{}' failed - {}".format(self.job[model.Job.id], ex))
        self.done = True


class Jobs(threading.Thread):
    def __init__(self, stg_handler: Storage, check_delay: typing.Union[int, float], max_jobs: int):
        super().__init__(name="jobs-handler", daemon=True)
        self.__stg_handler = stg_handler
        self.__check_delay = check_delay
        self.__max_jobs = max_jobs
        self.__job_queue = queue.Queue()
        self.__job_pool = dict()
        self.__worker_pool = dict()

    def create(self, data: dict):
        job_id = uuid.uuid4().hex
        self.__job_pool[job_id] = {
            model.Job.id: job_id,
            model.Job.created: '{}Z'.format(datetime.datetime.utcnow().isoformat()),
            model.Job.status: model.JobStatus.no_data,
            model.Job.model: data[model.Job.model],
            model.Job.config: data[model.Job.config],
            model.Job.data_source: None,
            model.Job.result: None,
            model.Job.reason: None
        }
        return {model.Job.id: job_id}

    def add_data_source(self, job_id: str, data_source: str):
        self.__job_pool[job_id][model.Job.data_source] = data_source
        self.__job_pool[job_id][model.Job.status] = model.JobStatus.pending
        self.__job_queue.put_nowait(job_id)

    def get_job(self, job_id: str):
        return self.__job_pool[job_id].copy()

    def run(self):
        while True:
            time.sleep(self.__check_delay)
            if len(self.__worker_pool) < self.__max_jobs:
                job_id = self.__job_queue.get()
                worker = Worker(self.__job_pool[job_id])
                self.__worker_pool[job_id] = worker
                worker.start()
            for job_id in list(self.__worker_pool.keys()):
                if self.__worker_pool[job_id].done:
                    del self.__worker_pool[job_id]
                    try:
                        self.__stg_handler.remove(self.__job_pool[job_id][model.Job.data_source])
                    except Exception as ex:
                        logger.error(ex)
