"""
 log_writer.py

 Copyright (c) 2017 Future Standard Co., Ltd.

 This software is released under the MIT License.
 http://opensource.org/licenses/mit-license.php
"""

import os
from threading import Lock

FILE_NAME = "log.txt"
MAX_LINES = 1000

class LogWriter:
    
    def __init__(self):
        self.lock = Lock()

    def write(self, text):
        with self.lock:
            lines = []
            if os.path.exists(FILE_NAME):
                with open(FILE_NAME, "r") as f:
                    lines = f.readlines()
    
            with open(FILE_NAME, "w") as f:
                f.write(text)
                f.write('\n')
    
            del_index = MAX_LINES - len(lines)
            if del_index < 0:
                del lines[del_index:]
    
            with open(FILE_NAME, "a") as f:
                f.writelines(lines)
