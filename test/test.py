# system
from selenium import webdriver
import time
import random
import sys
#
from f24_access_file import f24_read_write_file


class Flightradar24:
    __abc = 'yan ting'


    def main(self, s):
        self.__abc = 'a'

        print('%s -> %s' % (self.__abc, s))


if __name__ == "__main__":
    # Flightradar24().main(sys.argv[1])
    Flightradar24().main('ci202')
