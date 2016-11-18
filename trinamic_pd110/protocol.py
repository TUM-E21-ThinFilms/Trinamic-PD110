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

class TrinamicProtocol(Protocol):
    def __init__(self, address=1, encoding='hex'):
        self.address = address
        self.encoding = encoding

    def checksum(self, msg):
        digit_sum = sum([i for i in msg])  # calculate digit sum from data
        return digit_sum % 256  # format to digit sum modulo 256

    def data_splitter(self, data_in):
        data = []
        data.extend(data_in)  # make data list (out of tuple)
        if data == []:  # if data_in is None (No value was transmitted)
            data = [0]
        data[0] = int(data[0])  # convert data to integer
        msg = []
        if data[0] < 0:  # For negative inputs... First bit is sign bit
            data[0] = (pow(2, 32) - data[0])
        for x in range(0, 4):
            msg.append(data[0] % 256)
            data[0] /= 256
            data[0] = int(data[0])
        return msg[::-1]  # reversed bytearray

    def create_message(self, header, *data):
        msg = []
        msg.append(self.address)
        if header[0] == '[':  # convert back to list if header was transmitted as string...
            header = header[1:-1]
            header = header.split(',')
            for i in range(0, len(header)):
                header[i] = int(header[i])
        msg.extend(header)
        msg.extend(self.data_splitter(data))
        check = self.checksum(msg)  # get checksum
        msg.append(check)  # adding checksum
        # logger.debug('Created Message: "%s"', msg)
        return bytearray(msg)

    def parse_response(self, response, header):
        # logger.debug('Parse response: "%s"', response)
        response_header = []  # create response header list
        response_value = []  # create response value list
        for i in range(0, 4):
            response_header.append(response[i])  # fill response header with information

        # exceptions einfügen!! (checks für header correctness!!...)

        for i in range(4, 8):
            response_value.append(response[i])  # fill response value with information
        check = self.checksum(response[0:-1])  # create checksum
        # if check != response[-1]:
        #    raise ValueError('Shutter: Wrong response checksum!') # check checksum
        value = 0  # calculate real response value
        response_value = response_value[::-1]
        for i in range(0, 4):
            value += response_value[i] * pow(256, i)
        if value > pow(2, 31):  # All values > pow (2,31) are negative (they have a positive sign bit)
            value = pow(2, 32) - value
        return [value]  # Has to be given as list (iterable...)
        # return response_value

    def query(self, transport, header, *data):  # QUERY DOES NOT WORK YET!!
        message = self.create_message(header, *data)
        # logger.debug('Shutter query message []: "%s"', [message])
        with transport:
            transport.write(message)
            response = transport.read_bytes(9)  # reply has always 9 bytes
        # logger.debug('Shutter response []: "%s"', [response])
        return self.parse_response(response, header)

    def write(self, transport, header, *data):
        message = self.create_message(header, *data)
        # logger.debug('Shutter write []: "%s"', [message]) # gibt komisches Meldungen zurück...
        with transport:
            transport.write(message)
            response = transport.read_bytes(9)  # reply has always 9 bytes
        # logger.debug('Shutter response []: "%s"', [response])
        return self.parse_response(response, header)
