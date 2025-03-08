#!/bin/bash
echo 'qfxStipper is Running Script'> /opt/moneydance/scripts/qfxStripper.log
# jython was failing because it could not find java  .. the error did not show up on /dev/pts/3 .. did show up in qfxStripper.err
export JAVA_HOME=/home/wayne/.sdkman/candidates/java/current
#exec jython /opt/moneydance/scripts/qfxStripper.py $@
/usr/bin/jython -u /opt/moneydance/scripts/qfxStripper.py $@ > /opt/moneydance/scripts/qfxStripper.log 2> /opt/moneydance/scripts/qfxStripper.log
###exit
