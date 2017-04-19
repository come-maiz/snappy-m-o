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

import errbot
import github


class SnapcraftGithub(errbot.BotPlugin):
    """Handle GitHub webhooks from the snapcraft repository."""

    def activate(self):
        super().activate()
        self['subscriptions'] = {}

    @errbot.arg_botcmd('pull_request_number', type=int)
    def github_subscribe(self, message, pull_request_number):
        """Subscribe to the results of pull request tests."""
        from_nick = message.frm.nick
        with self.mutable('subscriptions') as subscriptions:
            if pull_request_number not in subscriptions:
                subscriptions[pull_request_number] = {from_nick}
            else:
                subscriptions[pull_request_number].add(from_nick)
        return (
            "@{}: I'll send you a message if a test fails in the pull request "
            "#{}".format(from_nick, pr_number))

    @errbot.webhook
    def github(self, incoming_request):
        """A webhook to handle messages from GitHub."""
        payload = json.loads(incoming_request['payload'])
        if payload['state'] == 'failure':
            self._handle_failure(payload)

    def _handle_failure(self, payload):
        snapcraft = github.Github().get_user('snapcore').get_repo('snapcraft')
        for pull_request in snapcraft.get_pulls():
            if pull_request.head.sha == payload['sha']:
                self._notify_failure(
                    pull_request.number, payload['target_url'])
                break

    def _notify_failure(self, pull_request_number, url):
        if pull_request_number in self['subscriptions']:
            nicks = ' '.join(
                '@' + nick for nick in self['subscriptions'][pull_request_number])
            self.send(
                self.build_identifier(43624396),
                '{}: a test in pull request #{} failed: {}'.format(
                    nicks, pull_request_number, url))
