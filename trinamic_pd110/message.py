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

class Message(object):

    TERMINATOR = '\r'#
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
        self._value = value

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