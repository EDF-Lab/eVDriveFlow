import time
import socket

TEMPO = 1


class ChargeControllerTCPClientHelper:

    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.last_received_message = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(20)
        self.connect()

    def connect(self):
        self.socket.connect((self.ip_address, self.port))
        print( "conected to adress :", self.ip_address, "and port:",self.port)

    def disconnect(self):
        self.socket.close()

    def send_message(self, msg: str) -> None:
        """
        Send a message over the TCP socket, and display the response
        :param msg: The message to send
        """
        self.socket.sendall(bytes(msg, "ASCII"))
        ret = self.socket.recv(1024)
        print(ret)
        self.last_received_message = ret.decode("ASCII")
        print(self.last_received_message )
        time.sleep(TEMPO)

    def get_command(self):
        if self.last_received_message is None:
            return ""
        return self.last_received_message.split(",")[0]

    def get_value(self):
        if self.last_received_message is None:
            return None
        split = self.last_received_message.split(",")
        if len(split) < 3:
            return None
        return split[-2]

    def get_status(self):
        if self.last_received_message is None:
            return None
        return self.last_received_message.split(",")[-1]

    def is_ok(self):
        return self.get_status() == "OK"

    # ----------Commands----------

    def get_pwm(self):
        self.send_message("GET_PWM")
        return int(self.get_value())

    def set_pwm(self, v: int):
        self.send_message("SET_PWM,%03d" % v)

    def get_ev_state(self):
        self.send_message("GET_EV_STATE")
        return str(self.get_value())

    def set_ev_state(self, v: str):
        self.send_message("SET_EV_STATE,%s" % v)

    def set_c1(self, v: str):
        self.send_message("SET_C1,%s" % v)

    def get_c1(self):
        self.send_message("GET_C1")
        return str(self.get_value())

    def get_c1_real(self):
        self.send_message("GET_C1_REAL")
        return str(self.get_value())

    def set_c2(self, v: str):
        self.send_message("SET_C2,%s" % v)

    def get_c2(self):
        self.send_message("GET_C2")
        return str(self.get_value())

    def get_max_current(self):
        self.send_message("GET_MAX_CURRENT")
        return int(self.get_value())
