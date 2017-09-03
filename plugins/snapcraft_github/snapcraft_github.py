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

import json
import fileinput
import glob
import subprocess
import tempfile

import errbot
import git
import github


_TELEGRAM_ID_SNAPCRAFT_TEAM_ROOM = -132110793


class SnapcraftGithub(errbot.BotPlugin):
    """Handle GitHub webhooks from the snapcraft repository."""

    def activate(self):
        super().activate()
        self['subscriptions'] = {}

    @errbot.arg_botcmd('pull_request_number', type=int)
    def github_subscribe(self, message, pull_request_number):
        """Subscribe to the results of pull request tests."""
        from_nick = message.frm.nick
        snapcraft = self._get_snapcraft_repo()
        pull_request = snapcraft.get_pull(int(pull_request_number))
        with self.mutable('subscriptions') as subscriptions:
            if pull_request_number not in subscriptions:
                subscriptions[pull_request_number] = {from_nick}
            else:
                subscriptions[pull_request_number].add(from_nick)
        return (
            "@{}: I'll send you a message if a test fails in the pull request "
            "#{} ({}).".format(
                from_nick, pull_request.number, pull_request.title))

    def _get_snapcraft_repo(self):
        return github.Github().get_user('snapcore').get_repo('snapcraft')

    @errbot.webhook
    def github(self, incoming_request):
        """A webhook to handle messages from GitHub."""
        payload = json.loads(incoming_request['payload'])
        if payload['state'] == 'failure':
            self._handle_failure(payload)

    def _handle_failure(self, payload):
        snapcraft = self._get_snapcraft_repo()
        for pull_request in snapcraft.get_pulls():
            if pull_request.head.sha == payload['sha']:
                self._notify_failure(
                    pull_request, payload['target_url'])
                break

    def _notify_failure(self, pull_request, url):
        if pull_request.number in self['subscriptions']:
            nicks = ' '.join(
                '@' + nick for nick in self['subscriptions'][pull_request.number])
            self.send(
                self.build_identifier(_TELEGRAM_ID_SNAPCRAFT_TEAM_ROOM),
                '{}: a test failed in pull request #{} ({}): {}'.format(
                    nicks, pull_request.number, pull_request.title, url))

    @errbot.arg_botcmd('pull_request_number', type=int)
    def github_build(self, message, pull_request_number):
        """Build the snapcraft snap from a pull request."""
        from_nick = message.frm.nick
        snapcraft = self._get_snapcraft_repo()
        pull_request = snapcraft.get_pull(int(pull_request_number))
        with tempfile.TemporaryDirectory() as tmp:
            git.Repo.clone_from(
                'https://github.com/{}'.format(pull_request.head.repo.full_name),
                tmp, branch=pull_request.head.ref)
            with fileinput.FileInput(
                    os.path.join(tmp, 'snap', 'snapcraft.yaml'),
                    inplace=True, backup='.bak') as yaml:
                for line in yamll:
                    print(line.replace(
                        'name: snapcraft', 'name: snapcraft-m-o').replace(
                            'snapcraft:', 'snapcraft-m-o:'), end='')
            subprocess.check_call('snapcraft', cwd=tmp)
            subprocess.check_call(
                ['snapcraft', 'push', glob.glob(os.path.join(tmp, '*.snap'))[0],
                 '--release', 'edge/pr{}'.format(pull_request_number)])
        return (
            '@{}: You can install your snapcraft snap with '
            'sudo snap install snapcraft-m-o --channel=edge/pr{}'.format(
                from_nick, pull_request_number))
