#
#	LHSPNservice
#	Little Hedgehog Server
#
#	Created by James Barrow on 09/07/2013.
#

#!/usr/bin/env python

import logging

__author__ = 'James Barrow'
__auther_email__ = 'james@pigonahill.com'
__version__ = '1.0'
__copyright__ = 'Copyright (c) 2013 James Barrow'
__license__ = 'MIT'

__all__ = ['APNservice', 'PushNotificationDeviceHandler']

logFileHandler = '../log/LHSPNservice.log'
logLevel = logging.WARNING

# Setup Logging
logging.basicConfig(level=logLevel,
						 format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
						 filename=logFileHandler,
						 filemode='a')
console = logging.StreamHandler()
console.setLevel(logLevel)
formatter = logging.Formatter('%(name)-12s %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logger = logging.getLogger('LHSPNservice')
logger.addHandler(console)
