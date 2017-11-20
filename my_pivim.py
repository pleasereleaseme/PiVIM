"""DocString"""
import sys
import time
import logging as log
from pivim import mobile_broadband as mb
from pivim import control_panel as cp
from pivim import data_portal as dp
from pivim import temperature as t

def main(access_key):
    """Evolving picture of how all the different code modules will work together"""

    log.basicConfig(filename='/home/pi/PiVIM-py/my_pivim.log', level=log.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    log.debug("Starting up")

    highest_temp = 0
    lowest_temp = 100

    cp.display_config()

    mobile = mb.MobileBroadband()

    while True:
        try:
            mobile.get_status()
            log.debug("Signal strength: %s", mobile.signalbar)
            log.debug("Network type: %s", mobile.network_type)
            signalbar = mobile.signalbar
            network_type = mobile.network_type

            #latest_temp = round(t.read_temp() -0.5)
            latest_temp = round(t.read_temp() 1)
            lowest_temp = latest_temp if latest_temp < lowest_temp else lowest_temp
            highest_temp = latest_temp if latest_temp > highest_temp else highest_temp

            cp.clear_screen()
            cp.message_right_top(network_type)
            cp.message_right_middle('*' * int(signalbar))
            cp.message_left_top("L: " + str(lowest_temp))
            cp.message_left_middle("N: " + str(latest_temp))
            cp.message_left_bottom("H: " + str(highest_temp))

            dp.upload_temperature_data(access_key, latest_temp)

            time.sleep(10)

        except KeyboardInterrupt:
            cp.display_off()

if __name__ == '__main__':
    main(sys.argv[1])
