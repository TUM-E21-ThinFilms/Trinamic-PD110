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

from slave.protocol import Protocol
from message import Message, AbstractMessage, Response

class TrinamicPD110Protocol(Protocol):
    def __init__(self, address='A', logger=None):
        self.logger = logger
        self.address = address

    def to_ascii(self, transport):
        transport.write("".join(map(chr, [1, 139, 0, 0, 0, 0, 0, 0, 140])))
        response = transport.read_bytes(9)
        print(response)

    def parse_response(self, raw_response):
        resp = Response()
        resp.read_response(raw_response)
        return resp

    def query(self, transport, message):
        if not isinstance(message, AbstractMessage):
            raise TypeError('message must be an instance of AbstractMessage')

        message.set_address(self.address)
        raw_msg = message.get_raw()

        self.logger.debug("Sending message %s", repr(raw_msg))
        transport.write(raw_msg)
        response = transport.read_until(Message.TERMINATOR)

        self.logger.debug("Read response %s", repr(response))

        return self.parse_response(response)

    def write(self, transport, message):
        self.query(transport, message)

