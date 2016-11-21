# Copyright (C) 2016, see AUTHORS.md
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from trinamic_pd110.message import AbstractMessage

class MVPMessage(AbstractMessage):
    TYPE_ABSOLUTE = 'ABS'
    TYPE_RELATIVE = 'REL'
    TYPE_COORDINATE = 'COORD'

    def initialize(self):
        self._msg.set_instruction('MVP')
        self._msg.set_type(self.TYPE_ABSOLUTE)

    def set_type(self, type):
        if not type in [self.TYPE_ABSOLUTE, self.TYPE_COORDINATE, self.TYPE_RELATIVE]:
            raise ValueError("unknown type")

        self._msg.set_type(type)

    def set_value(self, value):
        self._msg.set_value(value)