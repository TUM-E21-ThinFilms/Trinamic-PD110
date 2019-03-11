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

import re

class AbstractMessage(object):
    @classmethod
    def compute_checksum(cls, raw_msg):
        return sum([i for i in raw_msg]) & 0xFF

    @classmethod
    def _parse_value(cls, value):
        return [(value >> 3*8) & 0xFF, (value >> 2*8) & 0xFF, (value >> 1*8) & 0xFF, value & 0xFF]

    @classmethod
    def _generate_value(cls, value_array):
        return (value_array[0] << 3 * 8) | (value_array[1] << 2 * 8) | (value_array[2] << 1 * 8) | value_array[3]

    def get_value(self):
        return self._generate_value(self._value)

class BinaryCommand(AbstractMessage):
    IGNORE = 0

    def __init__(self, module_address, cmd_id, type_number, motor_or_bank_number, value):
        self._addr = module_address & 0xFF
        self._cmd = cmd_id & 0xFF
        self._type = type_number & 0xFF
        self._motor = motor_or_bank_number & 0xFF
        self._value = self._parse_value(value & 0xFFFFFFFF) # 4 bytes

    def get_raw(self):
        raw_msg = [self._addr, self._cmd, self._type, self._motor] + self._value
        checksum = self.compute_checksum(raw_msg)
        return bytearray(raw_msg + [checksum])

class BinaryResponse(AbstractMessage):
    RESPONSE_BYTES = 9

    def __init__(self, reply_address, module_address, status, cmd_id, value, checksum):
        self._addr = reply_address & 0xFF
        self._module = module_address & 0xFF
        self._status = status & 0xFF
        self._cmd = cmd_id & 0xFF
        self._value = self._parse_value(value & 0xFFFFFFFF) # 4 bytes
        self._checksum = checksum & 0xFF

        self._check_checksum()

    def _check_checksum(self):
        raw = [self._addr, self._module, self._status, self._cmd] + self._value
        checksum = self.compute_checksum(raw)

        if not checksum == self._checksum:
            raise RuntimeError("Checksum mismatch")

    def get_status(self):
        return self._status

    def is_successful(self):
        return self._status == Status.SUCCESS or self._status == Status.CMD_LOADED

    @classmethod
    def from_raw(cls, raw_data):
        assert isinstance(raw_data, bytearray)

        if not len(raw_data) == cls.RESPONSE_BYTES:
            raise RuntimeError("input length must be 9")

        addr = raw_data[0]
        mod  = raw_data[1]
        stat = raw_data[2]
        cmd  = raw_data[3]
        val  = cls._generate_value(raw_data[4:8])
        chk  = raw_data[8]

        return cls(addr, mod, stat, cmd, val, chk)

class Status(object):
    SUCCESS = 100
    CMD_LOADED = 101
    CHECKSUM_WRONG = 1
    COMMAND_INVALID = 2
    TYPE_WRONG = 3
    VALUE_INVALID = 4
    EEPROM_LOCKED = 5
    COMMAND_UNAVAILABLE = 6