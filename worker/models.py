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


import typing
import simple_struct


class JobStatus:
    pending = "pending"
    running = "running"
    finished = "finished"
    failed = "failed"
    aborted = "aborted"
    no_data = "nodata"


@simple_struct.structure
class Model:
    id = None
    created = None
    config = None
    columns = None
    data = None
    default_values = None
    service_id = None
    source_id = None
    time_field = None


@simple_struct.structure
class Job:
    id = None
    created = None
    status = JobStatus.no_data
    data_source = None
    result = None
    reason = None
    sorted_data = None
    models: typing.List[Model] = None
