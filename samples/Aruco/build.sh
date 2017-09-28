#!/bin/bash
g++ readAR.cpp -L/opt/scorer/lib/ -I/opt/scorer/include/ -laruco -lopencv_core -lopencv_highgui -lopencv_imgcodecs -lopencv_calib3d -std=c++11 -o readAR
