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

from slave.driver import Driver, Command
from slave.types import Integer
from protocol import TrinamicPD110Protocol

class TrinamicPD110Driver(Driver):

    def __init__(self, transport, protocol=None):
        if protocol is None:
            protocol = TrinamicPD110Protocol()

        super(TrinamicPD110Driver, self).__init__(transport, protocol)

        # Commands:

        self.position = Command(  # Command: def __init__(self, query=None, write=None, type_=None, protocol=None):
            '[6,1,0]',  # query
            '[5,0,0]',  # write
            Integer
        )

        self.speed_max = Command(
            '[6,4,0]',  # query
            '[5,4,0]',  # write
            # [Integer,Integer,Integer,Integer]
            Integer
        )

        self.speed = Command(
            '[6,3,0]',  # query
            '[5,2,0]',  # write
            # [Integer,Integer,Integer,Integer]
            Integer
        )

        self.acceleration = Command(
            '[6,5,0]',  # query
            '[5,5,0]',  # write
            # [Integer,Integer,Integer,Integer]
            Integer
        )

        # Functions:

    def move_right(self, value):  # max_value = 500
        cmd = [1, 0, 0], Integer  # first entry: Instruction number, second entry: Type; third entry: Motor/Bank
        return self._write(cmd, value)

    def move_left(self, value):
        cmd = [2, 0, 0], Integer
        return self._write(cmd, value)

    def stop(self):
        cmd = [1, 3, 0], Integer  # Motor stop
        return self._write(cmd, 0)

    def move_abs(self, value):
        cmd = [4, 0, 0], Integer  # Absolute movement
        return self._write(cmd, value)

    def move_rel(self, value):
        cmd = [4, 1, 0], Integer  # relative movement
        return self._write(cmd, value)

    def move_coord(self, value):
        cmd = [4, 2, 0], Integer  # move to coordinate
        return self._write(cmd, value)

    def mode(self, value):
        cmd = [6, 138, 0], Integer  # value = 0: position mode; value = 2: velocity mode
        return self._write(cmd, value)

    def move(self, degree=180):
        try:
            rotate = (25990 / 2) * degree / 360  # 25990 / 2 steps are full rotation
            return self.move_rel(rotate)
        except:
            pass