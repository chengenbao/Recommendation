#! /usr/bin/env python
from time import sleep
import random
from Constants import *

def random_sleep():
	sleep_time = SLEEPMAXTIME * random.random()
	sleep(sleep_time)

