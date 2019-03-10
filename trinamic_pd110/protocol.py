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

from e21_util.interface import Loggable
from e21_util.serial_connection import AbstractTransport, SerialTimeoutException

from trinamic_pd110.message import BinaryCommand, BinaryResponse

class TrinamicPD110Protocol(Loggable):
    def __init__(self, transport, logger):
        super(TrinamicPD110Protocol, self).__init__(logger)
        assert isinstance(transport, AbstractTransport)

        self._transport = transport

    def clear(self):
        with self._transport:
            try:
                while True:
                    self._transport.read(9)
            except SerialTimeoutException:
                pass

    def _write(self, message):
        assert isinstance(message, BinaryCommand)


        raw_msg = message.get_raw()

        self._logger.debug("Sending message {}".format(raw_msg))
        self._transport.write(raw_msg)

    def _read(self):

        raw_response = self._transport.read_bytes(BinaryResponse.RESPONSE_BYTES)

        return BinaryResponse.from_raw(raw_response)

    def execute(self, message):
        with self._transport:
            self._write(message)
            return self._read()