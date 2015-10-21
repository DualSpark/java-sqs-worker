#!/bin/bash
# launch script for BidMaster under Linux and OSX
rm -f nohup.out
if [ "$#" -ne 1 ]; then
  echo "Missing required Parameter or Batch file argument!"
fi
WORKDIR=/home/bidmaster
nohup /usr/lib/jvm/java-1.8.0-openjdk/bin/java -Xmx55g -jar ${WORKDIR}/BidMaster.jar $WORKDIR -h -s http://IP:8080/satfcserver Data ${1} >/dev/null 2>&1 &
