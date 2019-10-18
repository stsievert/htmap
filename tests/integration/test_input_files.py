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
import itertools

import pytest

import os
from contextlib import contextmanager
from pathlib import Path

import htmap


def test_all_fixed_input_files_are_transferred_to_all_components(tmp_path):
    a = tmp_path / 'a.txt'
    b = tmp_path / 'b.txt'
    for f in (a, b):
        f.touch()

    @htmap.mapped(map_options = htmap.MapOptions(fixed_input_files = [a, b]))
    def are_files_there(_):
        return all(((Path.cwd() / p).exists() for p in ('a.txt', 'b.txt')))

    results = are_files_there.map([None, None])

    assert all(results)


@contextmanager
def change_cwd(path):
    old = Path.cwd()

    os.chdir(path)

    yield

    os.chdir(old)


def test_multiple_input_files_per_component_are_delivered(tmp_path):
    def are_files_there(names):
        return all((Path.cwd() / f).exists() for f in names)

    # this is sort of unnecessary, but its the easiest way to get this done
    with change_cwd(tmp_path):
        files = [['0a', '0b'], ['1a', '1b', '1c']]
        for f in itertools.chain(*files):
            (Path.cwd() / f).touch()

        results = htmap.map(
            are_files_there,
            files,
            map_options = htmap.MapOptions(
                input_files = files
            )
        )

        assert all(results)
