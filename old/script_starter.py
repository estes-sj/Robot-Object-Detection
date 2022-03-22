from subprocess import run
from time import sleep
import os

# File path of program
file_path = "1.1.0.py"

# Time before restart
restart_timer = 2
def start_script():
    try:
        # Run program
        print("Starting Computer Vision...")
        # sudoPassword = 'Rah2022'
        # command = 'python3 ' + file_path
        # p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
        run("python3 "+file_path, check=True)
    except:
        # Script has crashed
        handle_crash()

# Crash Handler
def handle_crash():
    print("Crash Detected Restarting...")
    sleep(restart_timer)
    start_script()

start_script()