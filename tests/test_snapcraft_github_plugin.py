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
from unittest import mock

from testtools.matchers import Equals

import tests


class TestSnapcraftGithubPlugin(tests.BaseTestCase):

    def test_github_subscribe_gets_title_from_pull_request(self):
        with mock.patch('github.Github') as mock_github:
            mock_github().get_user().get_repo().get_pull.return_value = (
                type('obj', (object,), {
                    'number' : 1111,
                    'title': 'test-title'
                }))
            result = self.testbot.exec_command('!github subscribe 1111')

        mock_github().get_user.assert_called_with('snapcore')
        mock_github().get_user().get_repo.assert_called_with('snapcraft')
        # TODO figure out how to test the nick. This testbot returns None.
        # --elopio - 20180223
        self.assertThat(
            result,
            Equals("None: I'll send you updates as tests complete in pull "
                   "request snapcraft#1111 (test-title)."))

    #def test_github_subscribe_reports_pull_request_result(self):
    # According to the docs, one can trigger a webhook calling the
    # !webhook command. This is not working here, though
    # TODO file a bug in errbot. --elopio - 20180223

    def test_github_build(self):
        with mock.patch('github.Github') as mock_github:
            mock_head = mock_github().get_user().get_repo().get_pull().head
            mock_head.repo.full_name = 'snapcore/snapcraft'
            mock_head.ref = 'test-branch'
            with mock.patch('tempfile.TemporaryDirectory') as mock_temp:
                mock_temp.return_value.__enter__.return_value = self.path
                with mock.patch('git.Repo.clone_from') as mock_clone:
                    with mock.patch('subprocess.check_call') as mock_call:
                        open('test.snap', 'w').close()
                        result = self.testbot.exec_command(
                            '!github build 1111')

        mock_clone.assert_called_with(
            'https://github.com/snapcore/snapcraft',
            self.path,
            branch='test-branch')
        self.assertThat(
            mock_call.mock_calls[0],
            Equals(mock.call('snapcraft', cwd=self.path, env=mock.ANY)))
        self.assertThat(
            mock_call.mock_calls[1],
            Equals(mock.call(
                ['snapcraft', 'push', os.path.join(self.path, 'test.snap'),
                 '--release', 'edge/pr1111'])))
        # TODO figure out how to test the nick. This testbot returns None.
        # --elopio - 20180223
        self.assertThat(
            result,
            Equals('None: You can install your snapcraft snap with '
                   'sudo snap install snapcraft-m-o --channel=edge/pr1111'))
