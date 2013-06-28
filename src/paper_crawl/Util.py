#! /usr/bin/env python
from time import sleep
import random
from Constants import *

def random_sleep():
	sleep_time = SLEEPMAXTIME * (random.random() + 1)
	sleep(sleep_time)

