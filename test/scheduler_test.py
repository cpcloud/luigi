# Copyright (c) 2014 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import tempfile
import luigi.scheduler
import pickle
import unittest
import time

luigi.notifications.DEBUG = True


class SchedulerTest(unittest.TestCase):
    def test_load_old_state(self):
        tasks = {}
        active_workers = {'Worker1': 1e9, 'Worker2': time.time()}

        with tempfile.NamedTemporaryFile(delete=True) as fn:
            with open(fn.name, 'w') as fobj:
                state = (tasks, active_workers)
                pickle.dump(state, fobj)

            scheduler = luigi.scheduler.CentralPlannerScheduler(
                state_path=fn.name)
            scheduler.load()

            scheduler.prune()

            self.assertEquals(list(scheduler._active_workers.keys()),
                              ['Worker2'])

    def test_load_broken_state(self):
        with tempfile.NamedTemporaryFile(delete=True) as fn:
            with open(fn.name, 'w') as fobj:
                print >> fobj, "b0rk"

            scheduler = luigi.scheduler.CentralPlannerScheduler(
                state_path=fn.name)
            scheduler.load()  # bad if this crashes

            self.assertEquals(list(scheduler._active_workers.keys()), [])


if __name__ == '__main__':
    unittest.main()
