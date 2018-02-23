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

import fixtures
import testtools
from errbot.backends import test


class TesttoolsTestCase():

    def setUp(self, *kwargs):
        super().setUp()


class BaseTestCase(testtools.TestCase):

    def setUp(self):
        super().setUp()
        self.testbot = test.TestBot(
            os.path.join(os.path.dirname(__file__), '..', 'plugins'))
        self.testbot.start()
        self.addCleanup(self.testbot.stop)
        temp_cwd_fixture = TempCWD()
        self.useFixture(temp_cwd_fixture)
        self.path = temp_cwd_fixture.path


class TempCWD(fixtures.TempDir):

    def __init__(self, rootdir=None):
        if rootdir is None and 'TMPDIR' in os.environ:
            rootdir = os.environ.get('TMPDIR')
        super().__init__(rootdir)

    def setUp(self):
        """Create a temporary directory an cd into it for the test duration."""
        super().setUp()
        current_dir = os.getcwd()
        self.addCleanup(os.chdir, current_dir)
        os.chdir(self.path)
