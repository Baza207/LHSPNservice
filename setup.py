#
#	LHSPNservice
#	Little Hedgehog Server
#
#	Created by James Barrow on 09/07/2013.
#

#!/usr/bin/env python

from distutils.core import setup

setup(name = 'LHSPNservice',
	    version = '1.0',
	    description = 'Python Push Notification Service',
	    author = 'James Barrow',
	    author_email = 'james@pigonahill.com',
	    url = 'https://github.com/Baza207/LHSPNservice',
	    license = 'MIT',
	    package_dir= {'': 'src'},
	    py_modules = ['APNservice', 'PushNotificationDeviceHandler'],
)
