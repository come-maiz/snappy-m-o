# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2018 Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import stat
from unittest import mock

from testtools.matchers import Equals, FileExists

import tests


class TestAutopkgtestGithubPlugin(tests.BaseTestCase):

    def test_autopkgtest_downloads_retry_script(self):
        with mock.patch('tempfile.TemporaryDirectory') as mock_temp:
            mock_temp.return_value.__enter__.return_value = self.path
            # Do not execute the script.
            with mock.patch('subprocess.check_call'):
                self.testbot.exec_command('!autopkgtest')

        retry_script_path = os.path.join(self.path,  'retry_autopkgtest.sh')
        self.assertThat(retry_script_path, FileExists())
        # Assert that the script is executable.
        self.assertEqual(
            os.stat(retry_script_path).st_mode & stat.S_IEXEC, stat.S_IEXEC)

    def test_autopkgtest_executes_retry_script(self):
        with mock.patch('tempfile.TemporaryDirectory') as mock_temp:
            mock_temp.return_value.__enter__.return_value = self.path
            with mock.patch('subprocess.check_call') as mock_call:
                self.testbot.exec_command(
                    '!autopkgtest 1111 xenial:amd64 bionic:armhf')

        retry_script_path = os.path.join(self.path,  'retry_autopkgtest.sh')
        mock_call.assert_called_with([
            retry_script_path, '1111', 'xenial:amd64', 'bionic:armhf'])

    def test_autopkgtest_reports_result(self):
        with mock.patch('subprocess.check_call') as mock_call:
            result = self.testbot.exec_command('!autopkgtest')

        self.assertThat(
            result,
            # TODO figure out how to test the nick. This testbot returns None.
            # --elopio - 20180223
            Equals("None: I've just triggered your test."))
