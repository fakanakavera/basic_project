#!/usr/bin/env python
# coding=utf-8

#
# F1 Telemetry - Main application
# Written in Python by Martijn van Kekem
# URL: https://www.vankekem.com/
#
# Receives F1 Telemetry data for the custom F1 steering wheel, designed by Martijn van Kekem
#
# This work was made possible thanks to the following sources:
# -- https://github.com/gmaslowski/f1game-telemetry/wiki/udp-packet-1237-structure
# -- http://forums.codemasters.com/discussion/53139/f1-2017-d-box-and-udp-output-specification
#
# This work is licensed under a "Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License"
# License URL: https://creativecommons.org/licenses/by-nc-nd/4.0/
#

import time
from vars import *  # Import everything from vars
from struct import *  # Import everything from struct
from ArrayStructure import *  # Import everything from array structure
from f1_22_decoder import f1_22_decoder  # Import everything from f1_22_decoder
import sys  # Import libraries
sys.path.append('ArrayStructure.py')  # Include array structure

decoder = f1_22_decoder()  # Create decoder object

decoder.decoder_loop()  # Start the decoder loop
