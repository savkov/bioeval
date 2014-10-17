# This file is part of BIOEval.
#
# BIOEval is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BIOEval is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BIOEval.  If not, see <http://www.gnu.org/licenses/>.
__author__ = 'Aleksandar Savkov'

import bioeval
from unittest import TestCase


class TestBIOEval(TestCase):

    def setUp(self):
        self.data = bioeval.read_file('res/conll.data', ' ')
        self.tagset = None

    def generate_data(self):
        pass

    def test_performance(self):
        pass