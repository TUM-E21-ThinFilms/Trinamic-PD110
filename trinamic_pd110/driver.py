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

from trinamic_pd110.protocol import TrinamicPD110Protocol
from trinamic_pd110.message import BinaryCommand


class Parameter(object):
    class Move(object):
        ABSOLUTE = 0
        RELATIVE = 1
        COORDINATE = 2

        VALIDATOR = [ABSOLUTE, RELATIVE, COORDINATE]

    class Axis(object):
        TARGET_POSITION = 0
        ACTUAL_POSITION = 1
        TARGET_SPEED = 2
        ACTUAL_SPEED = 3
        MAX_POSITIONING_SPEED = 4
        MAX_ACCELERATION = 5
        MAX_ABSOLUTE_CURRENT = 6
        STANDBY_CURRENT = 7
        RIGHT_LIMIT_SWITCH_DISABLE = 12
        LEFT_LIMIT_SWITCH_DISABLE = 13
        MIN_SPEED = 130
        RAMP_MODE = 138
        MICROSTEP_RESOLUTION = 140
        REF_SWITCH_TOLERANCE = 141
        SOFT_STOP_FLAG = 149
        RAMP_DIVISOR = 153
        PULSE_DIVISOR = 154
        REFERENCING_MODE = 193
        REFERENCING_SEARCH_SPEED = 194
        REFERENCING_SWITCH_SPEED = 195
        MIXED_DECAY_THRESHOLD = 203
        FREEWHEELING = 204
        STALL_DETECTION_THRESHOLD = 205
        FULLSTEP_THRESHOLD = 211
        POWER_DOWN_DELAY = 214

        _RANGE = [TARGET_POSITION, ACTUAL_POSITION, TARGET_SPEED, ACTUAL_SPEED, MAX_POSITIONING_SPEED,
                  MAX_ACCELERATION, MAX_ABSOLUTE_CURRENT, STANDBY_CURRENT, RIGHT_LIMIT_SWITCH_DISABLE,
                  LEFT_LIMIT_SWITCH_DISABLE, MIN_SPEED, RAMP_MODE, MICROSTEP_RESOLUTION, REF_SWITCH_TOLERANCE,
                  SOFT_STOP_FLAG, RAMP_DIVISOR, PULSE_DIVISOR, REFERENCING_MODE, REFERENCING_SEARCH_SPEED,
                  REFERENCING_SWITCH_SPEED, MIXED_DECAY_THRESHOLD, FREEWHEELING, STALL_DETECTION_THRESHOLD,
                  FULLSTEP_THRESHOLD, POWER_DOWN_DELAY]

        @classmethod
        def validate(cls, parameter):
            return parameter in cls._RANGE

    class Global(object):
        @staticmethod
        def get_parameter(parameter):
            return parameter[1]

        @staticmethod
        def get_bank(parameter):
            return parameter[0]

        EEPROM_MAGIC = (0, 64)
        RS232_BAUD_RATE = (0, 65)
        RS232_SERIAL_ADDRESS = (0, 66)
        ASCII_MODE = (0, 67)
        CAN_BIT_RATE = (0, 69)
        CAN_REPLY_ID = (0, 70)
        CAN_ID = (0, 71)
        EEPROM_LOCK_FLAG = (0, 73)
        TELEGRAM_PAUSE_TIME = (0, 75)
        SERIAL_HOST_ADDRESS = (0, 76)
        AUTO_START_MODE = (0, 77)
        SHUTDOWN_PIN_FUNCTIONALITY = (0, 80)
        TMCL_CODE_PROTECTION = (0, 81)
        CAN_SECONDARY_ADDRESS = (0, 83)
        TICK_TIMER = (0, 132)

        _RANGE = [EEPROM_MAGIC, RS232_BAUD_RATE, RS232_SERIAL_ADDRESS, ASCII_MODE, CAN_BIT_RATE, CAN_REPLY_ID, CAN_ID,
                  EEPROM_LOCK_FLAG, TELEGRAM_PAUSE_TIME, SERIAL_HOST_ADDRESS, AUTO_START_MODE,
                  SHUTDOWN_PIN_FUNCTIONALITY, TMCL_CODE_PROTECTION, CAN_SECONDARY_ADDRESS, TICK_TIMER]

        _GPVAR_RANGE = range(0, 55 + 1)

        @classmethod
        def GENERAL_PURPOSE_VARIABLE(cls, id):
            assert id in cls._GPVAR_RANGE
            return (2, id)

        @classmethod
        def validate(cls, parameter):
            return (parameter in cls._RANGE) or (
                    cls.get_bank(parameter) == 2 and cls.get_parameter(parameter) in cls._GPVAR_RANGE)


class TrinamicPD110Driver(object):
    def __init__(self, protocol, address=1):
        assert isinstance(protocol, TrinamicPD110Protocol)
        self._addr = address & 0xFF
        self._protocol = protocol

    def execute(self, msg):
        return self._protocol.execute(msg)

    def stop(self):
        return self.execute(
            BinaryCommand(self._addr, 3, BinaryCommand.IGNORE, BinaryCommand.IGNORE, BinaryCommand.IGNORE))

    def move(self, pos, type=Parameter.Move.RELATIVE):
        assert (type in Parameter.Move.VALIDATOR)

        return self.execute(BinaryCommand(self._addr, 4, type, BinaryCommand.IGNORE, pos))

    def set_axis_parameter(self, parameter_number, value):
        assert Parameter.Axis.validate(parameter_number)
        return self.execute(BinaryCommand(self._addr, 5, parameter_number, BinaryCommand.IGNORE, value))

    def get_axis_parameter(self, parameter_number):
        assert Parameter.Axis.validate(parameter_number)
        return self.execute(BinaryCommand(self._addr, 6, parameter_number, BinaryCommand.IGNORE, BinaryCommand.IGNORE))

    def store_axis_parameter(self, parameter_number):
        assert Parameter.Axis.validate(parameter_number)
        return self.execute(BinaryCommand(self._addr, 7, parameter_number, BinaryCommand.IGNORE, BinaryCommand.IGNORE))

    def restore_axis_parameter(self, parameter_number):
        assert Parameter.Axis.validate(parameter_number)
        return self.execute(BinaryCommand(self._addr, 8, parameter_number, BinaryCommand.IGNORE, BinaryCommand.IGNORE))

    def set_global_parameter(self, parameter, value):
        assert Parameter.Global.validate(parameter)
        return self.execute(BinaryCommand(self._addr, 9, Parameter.Global.get_parameter(parameter),
                                          Parameter.Global.get_bank(parameter), value))

    def get_global_parameter(self, parameter):
        assert Parameter.Global.validate(parameter)
        return self.execute(BinaryCommand(self._addr, 10, Parameter.Global.get_parameter(parameter),
                                          Parameter.Global.get_bank(parameter), BinaryCommand.IGNORE))

    def store_global_parameter(self, parameter):
        assert Parameter.Global.validate(parameter)
        return self.execute(BinaryCommand(self._addr, 11, Parameter.Global.get_parameter(parameter),
                                          Parameter.Global.get_bank(parameter), BinaryCommand.IGNORE))

    def restore_global_parameter(self, parameter):
        assert Parameter.Global.validate(parameter)
        return self.execute(BinaryCommand(self._addr, 12, Parameter.Global.get_parameter(parameter),
                                          Parameter.Global.get_bank(parameter), BinaryCommand.IGNORE))
