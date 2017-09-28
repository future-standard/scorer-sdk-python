"""
 hvcp2_main.py

 Copyright (c) 2017 Future Standard Co., Ltd.

 This software is released under the MIT License.
 http://opensource.org/licenses/mit-license.php
"""

import sys
import subprocess
from subprocess import Popen

import recv_tracking
import recv_sequential

APP_PATH            = "/opt/scorer/bin/hvcp2_sdk"
DEVICE_NAME         = "/dev/ttyACM0"
TRACKING_SOCK_STR   = "ipc://@/scorer/hvcp2-sdk-tracking"
SEQUENTIAL_SOCK_STR = "ipc://@/scorer/hvcp2-sdk-sequential"
RECV_TIMEOUT        = 1000

args = sys.argv

# Start C++ Program
cmd = APP_PATH + " " + DEVICE_NAME + " " + args[1] + " " + TRACKING_SOCK_STR + " " + SEQUENTIAL_SOCK_STR + " " + args[2] + " " + args[3] + " " + args[4] + " " + args[5] + " " + args[6] + " " + args[7] + " " + args[8] + " " + args[9] + " " + args[10] + " " + args[11] + " " + args[12] + " " + args[13] + " " + \
      args[14] + " " + args[15] + " " + args[16] + " " + args[17] + " " + args[18] + " " + args[19] + " " + args[20] + " " + args[21] + " " + args[22] + " " + args[23] + " " + args[24] + " " + args[25] + " " + \
      args[26] + " " + args[27] + " " + args[28] + " " + args[29] + " " + args[30] + " " + args[31] + " " + args[32] + " " + args[33] + " " + args[34] + " " + args[35] + " " + args[36] + " " + args[37] + " " + args[38] + " " + args[39] + " " + args[40] + " " + args[41]
print(cmd)
proc = Popen(cmd.strip().split(" "))

# Start Receive Sequential Data
sequential_receiver = recv_sequential.SequentialReceiver(SEQUENTIAL_SOCK_STR, RECV_TIMEOUT)
sequential_receiver.start()
# Start Receive Tracking Data
tracking_receiver = recv_tracking.TrackingReceiver(TRACKING_SOCK_STR, RECV_TIMEOUT)
tracking_receiver.start()


# Wait C++ Program Exit
proc.wait()

# Stop Receive
sequential_receiver.stop()
tracking_receiver.stop()
