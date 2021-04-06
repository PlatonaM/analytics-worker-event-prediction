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

__all__ = ("Jobs", "Job")


from .logger import getLogger
from . import handlers, models
import falcon
import json


logger = getLogger(__name__.split(".", 1)[-1])


def reqDebugLog(req):
    logger.debug("method='{}' path='{}' content_type='{}'".format(req.method, req.path, req.content_type))


def reqErrorLog(req, ex):
    logger.error("method='{}' path='{}' - {}".format(req.method, req.path, ex))


class Jobs:
    def __init__(self, job_handler: handlers.Jobs):
        self.__job_handler = job_handler

    def on_post(self, req: falcon.request.Request, resp: falcon.response.Response):
        reqDebugLog(req)
        try:
            data = json.load(req.bounded_stream)
            resp.body = self.__job_handler.create(data)
            resp.content_type = falcon.MEDIA_TEXT
            resp.status = falcon.HTTP_200
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)


class Job:
    def __init__(self, job_handler: handlers.Jobs, stg_handler: handlers.Storage):
        self.__job_handler = job_handler
        self.__stg_handler = stg_handler

    def on_get(self, req: falcon.request.Request, resp: falcon.response.Response, job):
        reqDebugLog(req)
        try:
            resp.content_type = falcon.MEDIA_JSON
            data = dict(self.__job_handler.get_job(job))
            del data["models"]
            resp.body = json.dumps(data)
            resp.status = falcon.HTTP_200
        except KeyError as ex:
            resp.status = falcon.HTTP_404
            reqErrorLog(req, ex)
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)

    def on_post(self, req: falcon.request.Request, resp: falcon.response.Response, job):
        reqDebugLog(req)
        try:
            self.__job_handler.add_data_source(job, self.__stg_handler.save(req.stream))
            resp.status = falcon.HTTP_200
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)

    # def on_delete(self, req: falcon.request.Request, resp: falcon.response.Response, job):
    #     reqDebugLog(req)
    #     try:
    #
    #         resp.status = falcon.HTTP_200
    #     except Exception as ex:
    #         resp.status = falcon.HTTP_500
    #         reqErrorLog(req, ex)
