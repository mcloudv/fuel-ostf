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


class CinderWorkersTest(cloudvalidation.CloudValidationTest):
    """TestClass contains test that checks number of cinder workers."""

    def test_cinder_workers_number(self):
        """Check: Cinder worker count
        Target component: Cinder

        Scenario:
            1. Check configured number of cinder workers on controller nodes
        Duration: 20 s.
        """
        cmd = (
            'grep -E "^\s*osapi_volume_workers\s*=\s*[0-9]*\s*(#.*)?$"'
            ' /etc/cinder/cinder.conf '
            ' | sed -r "s/^[^0-9]*([0-9]+)([^0-9]+.*)?$/\\1/"'
        )

        fail_msg = 'Less than two cinder workers configured on node(s) %s'
        failed = set()
        for host in self.controllers:
            try:
                stdout, stderr = self.verify(
                    5, self._run_ssh_cmd, 1, fail_msg % host,
                    'checking cinder workers number', host, cmd)
            except AssertionError:
                failed.add(host)
                continue
            try:
                if int(stdout) < 2 or stderr:
                    failed.add(host)
            except Exception:  # Failed to convert stdout to int
                failed.add(host)
        failed_hosts = ', '.join(failed)
        self.verify_response_true(len(failed) == 0, fail_msg % failed_hosts, 1)
