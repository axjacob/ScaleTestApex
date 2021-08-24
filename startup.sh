#!/bin/bash
####Machine & test startup script##
#VAR scriptsfileId=$1
#curl "https://scalegrail--sgdev.my.salesforce.com/services/data/v49.0/sobjects/ContentVersion/$scriptsfileId/VersionData" -H "Authorization: Bearer $sessionID" -H "Content-Type: application/json" -o scripts.zip
#echo "SF file retrieve:$?" >> startup.log
apt-get -y update
echo "update Apt:$?" >> startup.log
apt-get install -y unzip xvfb libxi6 libgconf-2-4
echo "Libgconf:$?" >> startup.log
curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
echo "Chrome:$?" >> startup.log
echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
echo "Chrome download:$?" >> startup.log
apt-get -y install google-chrome-stable
echo "Chrome Install:$?" >> startup.log
apt-get install python3-pip
echo "PIP Install:$?" >> startup.log
python3 -m pip install selenium
echo "selenium Install:$?" >> startup.log
wget -O chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
echo "chromedriver Download:$?" >> startup.log
unzip chromedriver_linux64.zip
echo "chromedriver Install:$?" >> startup.log
pip install pygtail
echo "pygtail Install:$?" >> startup.log
export PATH=`pwd`/chromedriver:$PATH
watch -n 20 -x python3 
##python3 SFDCLogin.py sgaccouts100.csv
##Write script to update machineId into testrunner.properties
##threads.py will read from there##
##Zip up machineinfo.py
