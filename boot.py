from _env import HOSTNAME
import network
import os
print(os.uname())

network.hostname(HOSTNAME)