import os
import sys

# add path to have access to values not exported by the basic library
TESTS_PATH = os.getcwd()
sys.path.append(TESTS_PATH + "../src/ovum_mira_modbus")
