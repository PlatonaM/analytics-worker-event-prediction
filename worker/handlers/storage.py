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

__all__ = ("Storage", )


from ..logger import getLogger
from ..configuration import conf
import uuid
import os

logger = getLogger(__name__.split(".", 1)[-1])


class Storage:
    def __init__(self, st_path):
        self.__st_path = st_path

    def save(self, stream):
        name = uuid.uuid4().hex
        file_path = os.path.join(self.__st_path, name)
        with open(file_path, 'wb') as file:
            while True:
                chunk = stream.read(conf.Storage.chunk_size)
                if not chunk:
                    break
                file.write(chunk)
        logger.debug("saved {} bytes to file '{}'".format(os.path.getsize(file_path), name))
        return file_path

    def remove(self, file_path):
        os.remove(file_path)
