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

from unittest import mock

import fixtures
from testtools.matchers import Equals

import tests


class FakeTravisRequest(fixtures.Fixture):

    def setUp(self):
        super().setUp()
        patcher = mock.patch('requests.get')
        mock_get = patcher.start()
        self.addCleanup(mock_get.stop)

        mock_get.side_effect = self.side_effect

    def side_effect(self, url, headers, params):
        class Response():
            def __init__(self, body):
                self.body = body

            def json(self):
                return self.body

        if url.endswith('repo/snapcore%2Fsnapcraft/requests'):
            return Response({
                'requests': [{
                    'builds': [{
                        'pull_request_number': 1111,
                        'id': 'test_build_id'
                    }]
                }]
            })
        elif url.endswith('build/test_build_id'):
            return Response({
                'jobs': [
                    (), (), (),
                    {'id': 'test_job_id'}
                ]
            })
        elif url.endswith('job/test_job_id/log'):
            return Response({
                'content': 'Your link is transfer.sh/test'
            })


class TestSnapcraftTravisPlugin(tests.BaseTestCase):

    def test_snapcraft_travis(self):
        self.useFixture(FakeTravisRequest())
        result = self.testbot.exec_command('!travis snapurl 1111')
        self.assertThat(
            result, Equals('Your link is transfer.sh/test'))
