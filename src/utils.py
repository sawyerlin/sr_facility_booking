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