import sys
sys.path.append("..")
import cmd
import argparse

from charge_controller_tcp_driver.charge_controller_tcp_client_helper import ChargeControllerTCPClientHelper

# Delay between commands
TEMPO = 1

CHAR_GREEN = "\033[32m"
CHAR_RED = "\033[31m"
CHAR_CLEAR = "\033[0m"

helper = None


def print_results() -> None:
    global helper
    if helper.is_ok():
        print(CHAR_GREEN, end="")  # Green escape character
    else:
        print(CHAR_RED, end="")  # Red escape character
    print("Return ->", helper.get_value(), CHAR_CLEAR)


def parse(arg, t: type = str):
    """Convert a series of zero or more arguments to a tuple"""
    return tuple(map(t, arg.split()))


def check_valid_state(arg):
    state = parse(arg)[0].upper()
    if state not in ["OPEN", "CLOSE"]:
        print(CHAR_RED + "Error ! Unknown state:", state, CHAR_CLEAR)
        return False, state
    return True, state


class CCShell(cmd.Cmd):
    intro = """
 _____ ____  _____    ____ ____   ____  _          _ _
| ____|  _ \|  ___|  / ___/ ___| / ___|| |__   ___| | |
|  _| | | | | |_    | |  | |     \___ \| '_ \ / _ \ | |
| |___| |_| |  _|   | |__| |___   ___) | | | |  __/ | |
|_____|____/|_|      \____\____| |____/|_| |_|\___|_|_|\n\n"""\
            "Welcome to the Charge Controller TCP client shell. Type help or ? to list commands.\n"
    prompt = '(Charge Controller) '

    def do_get_pwm(self, arg):
        """\
Retrieve the currently set PWM
Usage: GET_PWM\
        """
        helper.get_pwm()
        print_results()

    def do_set_pwm(self, arg):
        """\
Modify the current PWM
Usage: SET_PWM <VALUE>
Example:
    SET_PWM 10
    Sets the PWM to 10\
        """
        try:
            int_arg = parse(arg, int)
            helper.set_pwm(int_arg)
            print_results()
        except (TypeError, IndexError):
            print(CHAR_RED + "Error! Not enough arguments!\nUsage: SET_PWM <VALUE>", CHAR_CLEAR)
        except ValueError:
            print(CHAR_RED + "Error! Argument is not an int.\nUsage: SET_PWM <VALUE>", CHAR_CLEAR)

    def do_get_ev_state(self, arg):
        """\
Retrieve the current 61851-1 state
Usage: GET_EV_STATE\
        """
        helper.get_ev_state()
        print_results()

    def do_set_ev_state(self, arg):
        """\
Modify the current 61851-1 state
Usage: SET_EV_STATE <A-D>
Example:
    SET_EV_STATE A
    Sets the 61851-1 state to A\
        """
        try:
            value = parse(arg, str)[0].upper()
            if value not in ["A", "B", "C", "D"]:
                print(CHAR_RED + "Error! Unknown state:", value, CHAR_CLEAR)
                return
            helper.set_ev_state(value)
            print_results()
        except (TypeError, IndexError):
            print(CHAR_RED + "Error! Not enough arguments!\nUsage: SET_EV_STATE <A|B|C|D>", CHAR_CLEAR)

    def do_set_c1(self, arg):
        """\
Modify the primary contactor's position
Usage: SET_C1 <OPEN/CLOSE>
Example:
    SET_C1 OPEN
    Sets the primary contactor to an open position\
        """
        try:
            state = check_valid_state(arg)
            if not state[0]:
                return
            helper.set_c1(state[1])
            print_results()
        except (TypeError, IndexError):
            print(CHAR_RED + "Error! Not enough arguments!\nUsage: SET_C1 <OPEN|CLOSE>", CHAR_CLEAR)


    def do_get_c1(self, arg):
        """\
Retrieve the primary contactor's driving signal state (OPEN/CLOSE)
Usage: GET_C1\
        """
        helper.get_c1()
        print_results()

    def do_get_c1_real(self, arg):
        """\
Retrieve the primary contactor's physical state (OPEN/CLOSE)
Usage: GET_C1\
        """
        helper.get_c1_real()
        print_results()

    def do_set_c2(self, arg):
        """\
Modify the secondary contactor's position
Usage: SET_C2 <OPEN/CLOSE>
Example:
    SET_C2 CLOSE
    Sets the primary contactor to a closed position\
        """
        try:
            state = check_valid_state(arg)
            if not state[0]:
                return
            helper.set_c2(state[1])
            print_results()
        except (TypeError, IndexError):
            print(CHAR_RED + "Error! Not enough arguments!\nUsage: SET_C2 <OPEN|CLOSE>", CHAR_CLEAR)

    def do_get_c2(self, arg):
        """\
Retrieve the secondary contactor's state (OPEN/CLOSE)
Usage: GET_C2\
        """
        helper.get_c2()
        print_results()

    def do_get_max_current(self, arg):
        """\
Get the cable's maximum possible current (either 13, 20, 32 or 63 A)
Usage: GET_MAX_CURRENT\
        """
        helper.get_max_current()
        print_results()

    def precmd(self, line):
        return line.lower()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", help="The IP address of the Charge Controller card", type=str, required=True)
    parser.add_argument("-p", "--port", help="The port address of the Charge Controller card", type=int, required=True)
    args = parser.parse_args()
    if args.ip and args.port:
        helper = ChargeControllerTCPClientHelper(ip_address=args.ip, port=args.port)
        cc = CCShell()
        try:
            cc.cmdloop()
        except KeyboardInterrupt:
            pass
