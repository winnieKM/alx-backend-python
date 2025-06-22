#!/usr/bin/python3
import sys
stream_age = __import__('4-stream_ages')

try:
    stream_age.calculate_average_age()
except BrokenPipeError:
    sys.stderr.close()
