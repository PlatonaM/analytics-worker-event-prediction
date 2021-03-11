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


__all__ = ("Job", "JobStatus")


class JobStatus:
    pending = "pending"
    running = "running"
    finished = "finished"
    failed = "failed"
    aborted = "aborted"
    no_data = "nodata"


class Job:
    id = "id"
    created = "created"
    status = "status"
    model = "model"
    config = "config"
    data_source = "data_source"
    result = "result"
    reason = "reason"


class Model:
    created = "created"
    data = "data"

