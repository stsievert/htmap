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

import htmap
import htcondor


def test_loaded_map_is_same_object_as_previously_created_map():
    map = htmap.Map('singleton', cluster_ids = [], hashes = (), submit = htcondor.Submit())

    recovered = htmap.load('singleton')

    assert recovered is map


def test_new_map_with_same_map_id_is_same_object():
    map = htmap.Map('singleton', cluster_ids = [], hashes = (), submit = htcondor.Submit())

    again = htmap.Map('singleton', cluster_ids = [], hashes = (), submit = htcondor.Submit())

    assert again is map


def test_new_map_with_same_map_id_does_not_change_data():
    map = htmap.Map('singleton', cluster_ids = [], hashes = (), submit = htcondor.Submit())

    again = htmap.Map('singleton', cluster_ids = [], hashes = (), submit = htcondor.Submit())

    assert again._hashes == ()
