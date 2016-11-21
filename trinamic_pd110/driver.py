from slave.driver import Driver, Command
from slave.types import Integer
import time
from protocol import TrinamicProtocol

class ShutterDriver(Driver):

    def __init__(self, transport, protocol=None):
        if protocol is None:
            protocol = TrinamicProtocol()

        super(ShutterDriver, self).__init__(transport, protocol)

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
            rotate = (12800 / 2) / 180 * degree  # 12800/2 steps are half rotation
            return self.move_rel(rotate)
        except:
            pass

    def sputter(self, sputter_time):
        x = raw_input("Is the shutter closed? (yes/no) : ")
        if x != "yes":
            return 'Shutter: Command aborted!'
        cmd = [4, 1, 0], Integer
        try:
            self.move(180)
            #self._write(cmd, 12800 / 2)
        except:
            print("Exception...")

        time.sleep(sputter_time)

        try:
            self.move(180)
            #self._write(cmd, 12800 / 2)
        except:
            print("Exception....")

        print('Shutter: Sputtered for ' + str(sputter_time) + ' seconds!')
