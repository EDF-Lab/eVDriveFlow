
import sys
sys.path.append("..")
import time
from charge_controller_tcp_driver.charge_controller_tcp_client_helper import *

if __name__ == '__main__':

    helper = ChargeControllerTCPClientHelper("169.254.43.3", 12500)

    time.sleep(3)
    helper.set_pwm(100)
    print("PWM:", helper.get_pwm())
    #time.sleep(10)
    #helper.set_ev_state("A")
    #print("EV State: ", helper.get_ev_state())
    time.sleep(10)
    helper.set_pwm(50)
    time.sleep(2)
    print("PWM:", helper.get_pwm())
    #print("EV State: ", helper.get_ev_state())
    time.sleep(1)
    #helper.set_pwm(50)
    #print("PWM:", helper.get_pwm())
    time.sleep(10)
    helper.set_pwm(30)
    time.sleep(2)
    print("PWM:", helper.get_pwm())
    
    # print("EV State: ", helper.get_ev_state())

