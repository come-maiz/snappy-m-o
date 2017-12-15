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
import requests

import errbot
import git
import github


class SnapcraftTravis(errbot.BotPlugin):
    """Handle Travis requests with the Travis API."""

    @errbot.arg_botcmd('pull_request_number', type=int)
    def travis_snapurl(self, message, pull_request_number):
        try:
            build_id = self._get_build_id(pull_request_number)
        except errbot.ValidationException:
            return ('Could not find build with pull '
                    'request snapcraft#{}'.format(pull_request_number))

        jobs = self._get_travis_jobs(build_id)
        # get the id for the snap job
        try:
            job_id = jobs[3]['id']
        except IndexError:
            return 'Link not present in pull request snapcraft#{}'.format(pull_request_number)

        log = self._get_travis_job_log(job_id)
        log = log.split('\n')
        link = next((line for line in log if 'transfer.sh/' in line), 
                    'Link not present in pull request snapcraft#{}'.format(pull_request_number))
        return link


    def _get_travis_api_resource(self, resource, params):        
        url = 'https://api.travis-ci.org'
        headers = {'Travis-API-Version': '3', 'User-Agent': 'snappy-m-o'}
        response = requests.get(url + '/' + resource, headers=headers, params=params)
        return response.json()

    def _get_build_id(self, pull_request_number):
        limit = 100
        offset = 0

        while True:
            requests = self._get_travis_requests(pull_request_number, limit, offset)
            if (len(requests) == 0):
                raise errbot.ValidationException('Could not find build with pull request '
                                                 'snapcraft#{}'.format(pull_request_number))
                
            for request in requests:
                for build in request['builds']:
                    if build['pull_request_number'] == pull_request_number:
                        return build['id']
                        
            offset += limit

    def _get_travis_requests(self, pull_request_number, limit, offset):
        params = {'limit': limit, 'offset': offset}
        response = self._get_travis_api_resource('repo/snapcore%2Fsnapcraft/requests', params)
        requests = response['requests']
        return requests

    def _get_travis_jobs(self, build_id):
        jobs = self._get_travis_api_resource('build/{}'.format(build_id), {})['jobs']
        return jobs

    def _get_travis_job_log(self, job_id):
        log = self._get_travis_api_resource('job/{}/log'.format(job_id), {})['content']
        return log
