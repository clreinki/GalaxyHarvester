#!/usr/bin/python
"""

 Copyright 2012 Paul Willworth <ioscode@gmail.com>

 This file is part of Galaxy Harvester.

 Galaxy Harvester is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Galaxy Harvester is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Affero General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 along with Galaxy Harvester.  If not, see <http://www.gnu.org/licenses/>.

"""

import os
import sys
import re
import Cookie
import dbSession
import dbShared
import cgi
import MySQLdb
import re

#
# Get current url
try:
	url = os.environ['SCRIPT_NAME']
except KeyError:
	url = ''

form = cgi.FieldStorage()
# Get Cookies
useCookies = 1
cookies = Cookie.SimpleCookie()
try:
	cookies.load(os.environ['HTTP_COOKIE'])
except KeyError:
	useCookies = 0

if useCookies:
	try:
		currentUser = cookies['userID'].value
	except KeyError:
		currentUser = ''
	try:
		loginResult = cookies['loginAttempt'].value
	except KeyError:
		loginResult = 'success'
	try:
		sid = cookies['gh_sid'].value
	except KeyError:
		sid = form.getfirst('gh_sid', '')
else:
	currentUser = ''
	loginResult = 'success'
	sid = form.getfirst('gh_sid', '')

# Get form info
itemID = form.getfirst("itemID", "")
favType = form.getfirst("favType", "")
favGroup = form.getfirst("favGroup", "")
itemName = form.getfirst("itemName", "")
galaxyID = form.getfirst("galaxy", "")
operation = form.getfirst("op", "")
units = form.getfirst("units", "")

# escape input to prevent sql injection
sid = dbShared.dbInsertSafe(sid)
itemID = dbShared.dbInsertSafe(itemID)
favType = dbShared.dbInsertSafe(favType)
favGroup = dbShared.dbInsertSafe(favGroup)
itemName = dbShared.dbInsertSafe(itemName)
galaxyID = dbShared.dbInsertSafe(galaxyID)
operation = dbShared.dbInsertSafe(operation)
units = dbShared.dbInsertSafe(units)


result = ""
# Get a session
logged_state = 0

sess = dbSession.getSession(sid, 2592000)
if (sess != ''):
	logged_state = 1
	currentUser = sess

def n2n(inVal):
	if (inVal == '' or inVal == None or inVal == 'undefined' or inVal == 'None'):
		return 'NULL'
	else:
		return str(inVal)

units = units.replace(",","")
#  Check for errors
errstr = ""

if (itemID.isdigit() == False) and (galaxyID.isdigit() == False or itemName == ""):
	errstr = errstr + "Error: no spawnID or galaxy + name provided. \r\n"
if (favType.isdigit() == False):
	errstr = errstr + "Error: no item type provided. \r\n"
if not re.match('^[\w ]+$', favGroup) and favGroup != "":
	errstr = errstr + "Error: group name contains illegal characters (only alpha numeric and spaces allowed)."
if len(favGroup) > 255:
	errstr = errstr + "Error: Group name must not be longer than 255 characters."
if (units != "" and units.isdigit() == False):
	errstr = errstr + "Error: The value you entered for units contains non-numeric characters."
if (units != "" and units.isdigit() == True):
	try:
		unitsTest = int(units)
		if unitsTest > 2147483648 or unitsTest < -2147483648:
			errstr = errstr + "Error: That value for units is outside the range I can store."
	except:
		errstr = errstr + "Error: The value you entered for units could not be converted to a number."

# Only process if no errors
if (errstr == ""):
	result = ""
	favGroup = favGroup.replace(" ", "_")
	if (logged_state > 0):
		# Find favorite record and update/add as needed
		conn = dbShared.ghConn()
		# Lookup spawn id if we dont have it
		if itemID.isdigit() == False:
			#sys.stderr.write("__" + itemName + "__" + galaxyID)
			itemID = dbShared.getSpawnID(itemName, galaxyID)
			if itemID == -1:
				result = "Error: The spawn name you entered cannot be found in this galaxy."
		else:
			itemID = int(itemID)

		if itemID > -1:
			cursor = conn.cursor()
			cursor.execute("SELECT favGroup FROM tFavorites WHERE itemID=" + str(itemID) + " AND userID='" + currentUser + "' AND favType=" + str(favType) + ";")
			row = cursor.fetchone()
			cursor2 = conn.cursor()
			if row != None:
				if operation != "2" and units == "":
					if operation != "1":
						# not changing group, must be removing
						tempSQL = "DELETE FROM tFavorites WHERE itemID=" + str(itemID) + " AND userID='" + currentUser + "' AND favType=" + str(favType) + ";"
						cursor2.execute(tempSQL)
						result = "Favorite removed."
					else:
						result = "Error: You already have that resource set as a favorite."
				else:
					# set update str
					if operation != "2":
						udStr = "units=" + str(units)
					else:
						udStr = "favGroup='" + favGroup + "'"

					# group passed so they want to update that
					tempSQL = "UPDATE tFavorites SET " + udStr + " WHERE itemID=" + str(itemID) + " AND userID='" + currentUser + "' AND favType=" + str(favType) + ";"
					cursor2.execute(tempSQL)
					result = "Update complete"
			else:
				# does not exist, adding as new favorite
				tempSQL = "INSERT INTO tFavorites (userID, favType, itemID, favGroup) VALUES ('" + currentUser + "', " + str(favType) + ", " + str(itemID) + ", '" + favGroup + "');"
				cursor2.execute(tempSQL)
				result = "New favorite added."

			cursor2.close()

		conn.close()
	else:
		result = "Error: must be logged in to change favorites"
else:
	result = errstr

print 'Content-type: text/html\n'
print result

if (result.find("Error:") > -1):
	sys.exit(500)
else:
	sys.exit(200)

