from datetime import datetime

from time import sleep
from random import uniform

MIN_RAND = 0.64
MAX_RAND = 1.27
LONG_MIN_RAND = 4.78
LONG_MAX_RAND = 11.1

def short_wait():
    rand=uniform(MIN_RAND, MAX_RAND)
    sleep(rand)

def long_wait():
    rand=uniform(LONG_MIN_RAND, LONG_MAX_RAND)
    sleep(rand)

def get_strtime(format: str = "%Y-%m-%d_%H-%M-%S"):
    now = datetime.now()
    current_time = now.strftime(format)
    return current_time

def wait_until(wait_until: str):
    wait_until_datetime = datetime.strptime(wait_until, "%Y-%m-%d %H:%M:%S")
    while datetime.now() < wait_until_datetime:
        sleep(0.01)