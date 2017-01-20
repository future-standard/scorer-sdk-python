#!/bin/bash
# Install Shell Script for SCORER Python SDK

#Copyright 2017 Future Standard Co., Ltd.
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

# SCORER Python SDK pip install
pip3 install -U --user .
if [ $? -ne 0 ]; then
   echo "SCORER Python SDK install failed."
   exit 1
fi
echo "SCORER Python SDK install succeeded."

# Sphinx Document Make
cd doc
if [ ! -d _static ]; then
    mkdir _static
fi

if [ ! -d _templates ]; then
    mkdir _templates
fi

make clean; make html
if [ ! -d _build/html ]; then
    echo "html build failed."
    exit 1
fi
echo "SCORER Python SDK Document Created."

# Update API DOC 
rm -rf $HOME/html/SDK_API
cp -r _build/html $HOME/html/SDK_API

echo "install script successfully completed."
exit 0
