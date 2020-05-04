import os
import logging
import sys
import time
try:
    deployment_mode=sys.argv[1]
    if deployment_mode=='prod':
        command='bash manage.sh run-with-daemon-prod snet-aigents-service'
        mode='aigents_server-snet-aigents-service'
    if deployment_mode=='dev':
        command='bash manage.sh run-with-daemon-dev snet_aigents_with_daemon_$USER'
        mode='aigents_server-snet_aigents_with_daemon_$USER'

except:
    deployment_mode=''


try:
    os.system('docker rm -f '+str(mode))
except:
    logging.exception("message")


try:
    os.system(command)
except:
    logging.exception("message")
