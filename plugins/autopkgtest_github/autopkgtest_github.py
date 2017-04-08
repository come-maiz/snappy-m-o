#!/usr/bin/python3
# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2017 Canonical Ltd
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
import subprocess
import stat
import tempfile
from urllib import request

import errbot


RETRY_AUTOPKGTEST_SCRIPT_URL = (
    'https://raw.githubusercontent.com/snapcore/snapcraft/master/tools/'
    'retry_autopkgtest.sh')

class AutopkgtestsGithub(errbot.BotPlugin):
    """Trigger the autopkgtests for GitHub pull requests."""

    @errbot.botcmd(split_args_with=None)
    def autopkgtest(self, message, args):
        with tempfile.TemporaryDirectory() as tmp_dir:
            retry_script_path = os.path.join(tmp_dir, 'retry_autopkgtest.sh')
            request.urlretrieve(
                RETRY_AUTOPKGTEST_SCRIPT_URL,
                retry_script_path)
            os.chmod(
                retry_script_path,
                os.stat(retry_script_path).st_mode | stat.S_IEXEC)
            subprocess.check_call([retry_script_path, *args])
        from_nick = message.frm.nick
        return "@{}: I've just triggered your test.".format(from_nick)
