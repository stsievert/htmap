# Copyright 2019 HTCondor Team, Computer Sciences Department,
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

import textwrap


class ComponentError:
    def __init__(
        self,
        *,
        map,
        component: int,
        exception_msg: str,
        node_info,
        python_info,
        working_dir_contents,
        stack_summary,
    ):
        self.map = map
        self.component = component
        self.exception_msg = exception_msg
        self.node_info = node_info
        self.python_info = python_info
        self.working_dir_contents = working_dir_contents
        self.stack_summary = stack_summary

    def __repr__(self):
        return f'<ComponentError(map = {self.map}, component = {self.component})>'

    @classmethod
    def _from_error(cls, map, error):
        """Construct a :class:`ComponentError` from a raw component result."""
        return cls(
            map = map,
            component = error.component,
            exception_msg = error.exception_msg,
            node_info = error.node_info,
            python_info = error.python_info,
            working_dir_contents = error.working_dir_contents,
            stack_summary = error.stack_summary,
        )

    def _indent(self, text, multiple = 1):
        return textwrap.indent(text, ' ' * 2 * multiple)

    def _format_stack_trace(self):
        # modified from https://github.com/python/cpython/blob/3.7/Lib/traceback.py
        _RECURSIVE_CUTOFF = 3
        result = []
        last_file = None
        last_line = None
        last_name = None
        count = 0
        for frame in self.stack_summary:
            if (
                last_file is None or last_file != frame.filename or
                last_line is None or last_line != frame.lineno or
                last_name is None or last_name != frame.name
            ):
                if count > _RECURSIVE_CUTOFF:
                    count -= _RECURSIVE_CUTOFF
                    result.append(
                        self._indent(f'  [Previous line repeated {count} more time{"s" if count > 1 else ""}]\n')
                    )
                last_file = frame.filename
                last_line = frame.lineno
                last_name = frame.name
                count = 0
            count += 1
            if count > _RECURSIVE_CUTOFF:
                continue
            row = []
            row.append(self._indent(f'File "{frame.filename}", line {frame.lineno}, in {frame.name}\n'))
            if frame.line:
                row.append(self._indent(f'{frame.line.strip()}\n', multiple = 2))
            row.append(self._indent('\nLocal variables:\n', multiple = 2))
            if frame.locals:
                for name, value in sorted(frame.locals.items()):
                    row.append(self._indent(f'{name} = {value}\n', multiple = 3))
            result.append(''.join(row))
        if count > _RECURSIVE_CUTOFF:
            count -= _RECURSIVE_CUTOFF
            result.append(
                self._indent(f'[Previous line repeated {count} more time{"s" if count > 1 else ""}]\n')
            )
        return result

    def report(self) -> str:
        """
        Return a formatted error report.
        """
        lines = [
            f'  Start error report for component {self.component} of map {self.map.tag}  '.center(80, '='),
            'Landed on execute node {} ({}) at {}'.format(*self.node_info),
        ]

        if self.python_info is not None:
            executable, version, packages = self.python_info
            lines.append(f'\nPython executable is {executable} (version {version})')
            lines.append(f'with installed packages')
            lines.append(self._indent(packages))
        else:
            lines.append('\nPython executable information not available')

        lines.append('\nWorking directory contents are')
        for path in self.working_dir_contents:
            lines.append(self._indent(path))

        lines.append('\nException and traceback (most recent call last):')
        lines.extend(self._format_stack_trace())
        lines.append(self._indent(self.exception_msg, multiple = 1))

        lines.append('')
        lines.append(f'  End error report for component {self.component} of map {self.map.tag}  '.center(80, '='))

        return '\n'.join(lines)