#!/usr/bin/python
"""

 Copyright 2011 Paul Willworth <ioscode@gmail.com>

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
import ghShared
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
alertTypes = form.getfirst("alertTypes", "")
# escape input to prevent sql injection
sid = dbShared.dbInsertSafe(sid)
alertTypes = dbShared.dbInsertSafe(alertTypes)


# Get a session
logged_state = 0

sess = dbSession.getSession(sid, 2592000)
if (sess != ''):
	logged_state = 1
	currentUser = sess

fltCount = 0
result = ""
#  Check for errors
errstr = ""

if (alertTypes == ""):
	errstr = errstr + "Error: no alert types given. \r\n"

print 'Content-type: text/html\n'

# Only process if no errors
if (errstr == ""):
	if (logged_state > 0):
		result = '  <ul class="alert">'
		conn = dbShared.ghConn()
		# open list of users existing filters
		cursor = conn.cursor()
		cursor.execute("SELECT alertID, alertType, alertTime, alertMessage, alertLink FROM tAlerts WHERE userID='" + currentUser + "' AND alertType IN (" + alertTypes + ") AND alertStatus < 2 ORDER BY alertTime DESC LIMIT 10;")
		row = cursor.fetchone()
		while row != None:
			result = result + '<li id="alert_' + str(row[0]) + '"><div><a href="' + row[4] + '"><div class="inlineBlock" style="width:90%;">' + ghShared.timeAgo(row[2]) + ' ago - ' + row[3] + '</div></a><div class="inlineBlock" style="min-width:20px;"><img src="/images/xRed16.png" style="cursor:pointer;" title="Click to remove this alert" alt="Red X" onclick="updateAlertStatus(' + str(row[0]) + ', 2)" /></div></div></li>'
			row = cursor.fetchone()

		cursor.close()
		conn.close()
		if result.find("<li") > -1:
			result = result + "</ul>"
		else:
			result = "No Alerts"

	else:
		result = "Error: must be logged in to get alerts"
else:
	result = errstr

print result

if (result.find("Error:") > -1):
	sys.exit(500)
else:
	sys.exit(200)
