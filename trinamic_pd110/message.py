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
        return [(value & 0xFF000000), (value & 0x00FF0000), (value & 0x0000FF00), (value & 0x000000FF)]

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

    @classmethod
    def from_raw(cls, raw_data):
        assert isinstance(raw_data, bytearray)

        if not len(raw_data) == cls.RESPONSE_BYTES:
            raise RuntimeError("input length must be 9")

        addr = raw_data[0]
        mod  = raw_data[1]
        stat = raw_data[2]
        cmd  = raw_data[3]
        val  = (raw_data[4] << 3*8) | (raw_data[5] << 2*8) | (raw_data[6] << 1*8) | raw_data[7]
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

class Message(object):

    TERMINATOR = '\r'
    SPACE = ' '

    def __init__(self):
        self._type = ""
        self._instruction = ""
        self._bank = ""
        self._value = ""
        self._address = ""

    def _check_input(self, input):
        if not isinstance(input, basestring):
            raise TypeError('input must be of type string')

    def set_type(self, type):
        self._check_input(type)
        self._type = type

    def set_instruction(self, instruction):
        self._check_input(instruction)
        self._instruction = instruction

    def set_bank(self, bank):
        self._check_input(bank)
        self._bank = bank

    def set_address(self, address):
        self._check_input(address)
        self._address = address

    def get_type(self):
        return self._type

    def get_instruction(self):
        return self._instruction

    def get_bank(self):
        return self._bank

    def get_address(self):
        return self._address

    def set_value(self, value):
        self._value = str(value)

    def get_value(self):
        return self._value

    def get_raw(self):
        # remove all empty values
        parameters = ", ".join(filter(lambda x: x != "", [self._type, self._bank, self._value]))
        return "".join([self._address, self.SPACE, self._instruction, self.SPACE, parameters, self.TERMINATOR])

class Response(object):

    STATUS_SUCCESS = '100'
    STATUS_LOADED = '101'
    STATUS_WRONG_CHKSUM = '1'
    STATUS_INVALID_COMMAND = '2'
    STATUS_WRONG_TYPE = '3'
    STATUS_INVALID_VALUE = '4'
    STATUS_CONFIGURATION_LOCKED = '5'
    STATUS_COMMAND_NOT_AVAILABLE = '6'

    def __init__(self):
        self._host = 'B'
        self._client = 'A'
        self._status = '100'
        self._value = '0'

    def read_response(self, response):
        m = re.search('([a-z])\s*([a-z])\s*([0-9]{1,3})\s*(-?\d{1,})', response, re.IGNORECASE)
        if m is None:
            raise ValueError("Malformed response given")

        self._host = m.group(1)
        self._client = m.group(2)
        self._status = m.group(3)
        self._value = m.group(4)

    def get_host(self):
        return self._host

    def get_client(self):
        return self._client

    def get_status(self):
        return self._status

    def get_value(self):
        return self._value

class AbstractMessage(object):
    def __init__(self):
        self._msg = Message()
        self.initialize()

    def initialize(self):
        pass

    def get_message(self):
        return self._msg

    def get_raw(self):
        return self._msg.get_raw()

    def set_address(self, addr):
        self._msg.set_address(addr)    
