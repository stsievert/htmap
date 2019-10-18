# Copyright 2018 HTCondor Team, Computer Sciences Department,
# University of Wisconsin-Madison, WI.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from pathlib import Path

from htmap.options import get_core_descriptors


def test_job_batch_name_is_tag():
    descriptors = get_core_descriptors('foo', Path.cwd())

    assert descriptors['JobBatchName'] == 'foo'


@pytest.mark.parametrize(
    "key", ["log", "stdout", "stderr", "initialdir"]
)
def test_paths_are_in_map_dir(key, tmp_path):
    map_dir = tmp_path / 'map_dir'
    descriptors = get_core_descriptors('foo', map_dir)

    assert descriptors[key].startswith(map_dir.as_posix())
