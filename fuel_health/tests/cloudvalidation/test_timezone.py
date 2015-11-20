# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2015 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging

from fuel_health import cloudvalidation

LOG = logging.getLogger(__name__)


class TimezoneTest(cloudvalidation.CloudValidationTest):
    """Cloud Validation Test class for Timezone."""

    def _check_timezone(self, host):
        """Checks timezone on host."""

        err_msg = "Cannot check timezone at host %s."
        cmd = "date +%Z"

        out, err = self.verify(5, self._run_ssh_cmd, 1,
                               err_msg % host,
                               'check timezone', host, cmd)

        return out.replace('\n', '')

    def test_timezone_on_nodes(self):
        """Check Timezone on all nodes
        Target component: Time

        Scenario:
            1. Check timezone on all nodes

        Duration: 20 s.
        """

        LOG.info('Testing up timezones on nodes.')
        tz_list = dict()

        for host in self.controllers + self.computes:
            tz = self._check_timezone(host)
            LOG.info("Host '%s', timezone: '%s'." % (host, tz))
            tz_list[host] = tz

        tz_set = set(tz_list.values())
        self.verify_response_true(len(tz_set) == 1,
                                  "There are different timezones on nodes", 1)

        LOG.info('Finish testing timezone.')
