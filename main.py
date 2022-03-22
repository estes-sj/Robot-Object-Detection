# Main File for capstone project

import config
import misc
import detect
import align
import gpio
import os
import atexit
from time import sleep

# Main function
def main():
    while True:
        try:
            # Restart camera drivers
            sudoPassword = 'Rah2022'
            command = 'xrandr --output HDMI-0 --mode 1920x1080'
            os.system('echo %s|sudo -S %s' % (sudoPassword, command))
            command = 'sudo systemctl restart nvargus-daemon'
            os.system('echo %s|sudo -S %s' % (sudoPassword, command))

            # Setup gpio interface
            gpio.setup()

            # Status LEDs
            gpio.set_low(config.PIN_GREEN)
            gpio.set_high(config.PIN_RED)


            # Begin Computer Vision
            detect.detection()

        except:
            print("Computer Vision Crashed ...")

            pid = os.getpid()
            command = 'sudo kill -9 ' +str(pid)
            os.system('echo %s|sudo -S %s' % (sudoPassword, command))

def exit_handler():
	gpio.cleanup()
	print("""
░░░█             █ ▀
░░░░▓█       ▄▄▀▀█
░░░░▒░█    ▄█▒░░▄░█
░░░░░░░▀▄ ▄▀▒▀▀▀▄▄▀  DO
░░░░░░░░░█▒░░░░▄▀    IT
▒▒▒░░░░▄▀▒░░░░▄▀     FOR
▓▓▓▓▒░█▒░░░░░█▄      JERRY
█████▀▒░░░░░█░▀▄
█████▒▒░░░▒█░░░▀▄
███▓▓▒▒▒▀▀▀█▄░░░░█
▓██▓▒▒▒▒▒▒▒▒▒█░░░░█
▓▓█▓▒▒▒▒▒▒▓▒▒█░░░░░█
░▒▒▀▀▄▄▄▄█▄▄▀░░░░░░░█""")

# Run main
if __name__ == '__main__':
    main()
    atexit.register(exit_handler)