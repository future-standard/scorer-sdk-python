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
pushd doc
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

popd

# Install Javascript related files
JQUERY_VERSION=2.2.4
JQUERY_URL=https://code.jquery.com/jquery-${JQUERY_VERSION}.min.js

JQUERY_FILE=`basename $JQUERY_URL`
wget -q "$JQUERY_URL" -O /tmp/$JQUERY_FILE
cp /tmp/$JQUERY_FILE samples/scripts/

# Obtain the jabric.js stable release and install
FABRICJS_VERSION=1.7.0
FABRICJS_URL=http://cdnjs.cloudflare.com/ajax/libs/fabric.js/${FABRICJS_VERSION}/fabric.min.js

FABRICJS_FILE=`basename $FABRICJS_URL`
wget -q "$FABRICJS_URL" -O /tmp/$FABRICJS_FILE
cp /tmp/$FABRICJS_FILE samples/scripts/

# Install Tesseract English Dictionary
TESSERACT_ENG_DIC_URL=https://github.com/tesseract-ocr/tessdata/raw/master/eng.traineddata
TESSERACT_ENG_DIC=`basename $TESSERACT_ENG_DIC_URL`

wget -q "$TESSERACT_ENG_DIC_URL" -O /tmp/$TESSERACT_ENG_DIC
mv /tmp/$TESSERACT_ENG_DIC samples/Tesseract/tessdata/

echo "install script successfully completed."
exit 0
