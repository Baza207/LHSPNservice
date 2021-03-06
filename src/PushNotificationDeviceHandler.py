#
#	PushNotificationDeviceHandler.py
#	Little Hedgehog Server
#
#	Created by James Barrow on 04/07/2013.
#

#!/usr/bin/env python

import MySQLdb, time, binascii, ConfigParser

defaults = {'dbusername': '',
			'dbpassword': '',
			'dbname': '',
			'dbport': '3306',
			'dbtable': ''}

config=ConfigParser.ConfigParser(defaults)
if config.read(['config.cfg']):
	defaults = dict(config.items("Properties"))

username = defaults['dbusername']	# Database username
password = defaults['dbpassword']	# Database password
dbName = defaults['dbname']			# Database name
portNum = int(defaults['dbport'])		# Port Number
dbTable = defaults['dbtable']			# Table Name

def connectToDatabase():
	return MySQLdb.connect(host = "localhost", user = username, passwd = password, db = dbName, port = portNum)

def getDevice(db, token):
	db.query("SELECT * FROM %s WHERE token='%s'" %(dbTable, token))
	result = db.store_result()
	resultsTuple = result.fetch_row(0, 1)

	try:
		result = resultsTuple[0]
	except:
		result = None

	return result

def getDevicesWithOrDict(db, searchDict, sendToDev):
	queryString = "SELECT * FROM %s WHERE " %(dbTable)
	searchArray = []

	for key in searchDict:
		searchString = '"%s":"%s"' %(key, searchDict[key])
		searchString = "userInfo LIKE '%%%s%%'" %(searchString)
		searchArray.append(searchString)

	allSearchStrings = ' OR '.join(searchArray)
	queryString += '('+allSearchStrings+')'
	queryString += " AND isDev = '%d'" %(sendToDev)

	db.query(queryString)
	result = db.store_result()
	data = result.fetch_row(0, 1)

	return data

def getDevicesWithAndDict(db, searchDict, sendToDev):
	queryString = "SELECT * FROM %s WHERE " %(dbTable)
	searchArray = []

	for key in searchDict:
		searchString = '"%s":"%s"' %(key, searchDict[key])
		searchString = "userInfo LIKE '%%%s%%'" %(searchString)
		searchArray.append(searchString)

	allSearchStrings = ' AND '.join(searchArray)
	queryString += allSearchStrings
	queryString += " AND isDev = '%d'" %(sendToDev)

	db.query(queryString)
	result = db.store_result()
	data = result.fetch_row(0, 1)

	return data

def saveDevice(db, token, OSVersion, isDev, userInfo):
	timestamp = int(time.time())
	db.query("INSERT INTO %s (token, badge, OSVersion, isDev, userInfo, createdAt, updatedAt) VALUES ('%s', 0, '%s', '%d', '%d', '%d')" %(dbTable, token, OSVersion, isDev, userInfo, timestamp, timestamp))

def updateDevice(db, token, badge, OSVersion, isDev, userInfo):
	timestamp = int(time.time())
	db.query("UPDATE %s SET badge = '%d', OSVersion = '%s', isDev = '%d', userInfo = '%s', updatedAt = '%s' WHERE token='%s'" %(dbTable, badge, OSVersion, isDev, userInfo, timestamp, token))

def deleteDevice(db, token):
	db.query("DELETE FROM %s WHERE token='%s'" %(dbTable, token))

def incrementBadge(token):
	db = connectToDatabase()

	device = getDevice(db, token)
	if device is not None:
		badge = device['badge']
		if badge <= 0:
			badge = 1
		else:
			badge += 1

		updateDevice(db, token, badge, device['OSVersion'], device['isDev'], device['userInfo'])
	else:
		badge = 1

	db.close()

	return badge

def resetBadge(token):
	db = connectToDatabase()
	db.query("UPDATE %s SET badge='0' WHERE token='%s'" % (dbTable, token))
	db.close()

def removeFeedbackDevice(feedbackTuple):
	db = connectToDatabase()
	token = binascii.hexlify(feedbackTuple[2])
	deviceDict = getDevice(db, token)
	if deviceDict is not None:
		if feedbackTuple[0] >= deviceDict['updatedAt']:
			deleteDevice(db, token)
	db.close()
