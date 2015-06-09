#!/usr/bin/python
"""

 Copyright 2013 Paul Willworth <ioscode@gmail.com>

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
from xml.dom import minidom
import ghNames
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

numRows = form.getfirst("numRows", "")
# Get form info
galaxy = form.getfirst("galaxy", "")
planet = form.getfirst("planet", "")
spawnID = form.getfirst("resID", "")
spawnName = form.getfirst("resName", "")
resType = form.getfirst("resType", "")
forceOp = form.getfirst("forceOp", "")
sourceRow = form.getfirst("sourceRow", "")
CR = form.getfirst("CR", "")
CD = form.getfirst("CD", "")
DR = form.getfirst("DR", "")
FL = form.getfirst("FL", "")
HR = form.getfirst("HR", "")
MA = form.getfirst("MA", "")
PE = form.getfirst("PE", "")
OQ = form.getfirst("OQ", "")
SR = form.getfirst("SR", "")
UT = form.getfirst("UT", "")
ER = form.getfirst("ER", "")
# escape input to prevent sql injection
sid = dbShared.dbInsertSafe(sid)
numRows = dbShared.dbInsertSafe(numRows)
galaxy = dbShared.dbInsertSafe(galaxy)
planet = dbShared.dbInsertSafe(planet)
spawnID = dbShared.dbInsertSafe(spawnID)
spawnName = dbShared.dbInsertSafe(spawnName)
resType = dbShared.dbInsertSafe(resType)
forceOp = dbShared.dbInsertSafe(forceOp)
sourceRow = dbShared.dbInsertSafe(sourceRow)
CR = dbShared.dbInsertSafe(CR)
CD = dbShared.dbInsertSafe(CD)
DR = dbShared.dbInsertSafe(DR)
FL = dbShared.dbInsertSafe(FL)
HR = dbShared.dbInsertSafe(HR)
MA = dbShared.dbInsertSafe(MA)
PE = dbShared.dbInsertSafe(PE)
OQ = dbShared.dbInsertSafe(OQ)
SR = dbShared.dbInsertSafe(SR)
UT = dbShared.dbInsertSafe(UT)
ER = dbShared.dbInsertSafe(ER)

  
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


def addResource(resName, galaxy, resType, CR, CD, DR, FL, HR, MA, PE, OQ, SR, UT, ER):
	# Add new resource
	returnStr = ""
	conn = dbShared.ghConn()
	cursor = conn.cursor()
	# clear invalid stat values incase type was switched in the UI
	tempSQL = "SELECT CRmin, CRMax, CDmin, CDmax, DRmin, DRmax, FLmin, FLmax, HRmin, HRmax, MAmin, MAmax, PEmin, PEmax, OQmin, OQmax, SRmin, SRmax, UTmin, UTmax, ERmin, ERmax FROM tResourceType WHERE resourceType='" + resType + "';"
	cursor.execute(tempSQL)
	row = cursor.fetchone()
	if row != None:
		if row[0] == 0: CR = ''
		if row[2] == 0: CD = ''
		if row[4] == 0: DR = ''
		if row[6] == 0: FL = ''
		if row[8] == 0: HR = ''
		if row[10] == 0: MA = ''
		if row[12] == 0: PE = ''
		if row[14] == 0: OQ = ''
		if row[16] == 0: SR = ''
		if row[18] == 0: UT = ''
		if row[20] == 0: ER = ''
			

	tempSQL = "INSERT INTO tResources (spawnName, galaxy, entered, enteredBy, resourceType, CR, CD, DR, FL, HR, MA, PE, OQ, SR, UT, ER) VALUES ('" + resName + "'," + n2n(galaxy) + ",NOW(),'" + currentUser + "','" + resType + "'," + n2n(CR) + "," + n2n(CD) + "," + n2n(DR) + "," + n2n(FL) + "," + n2n(HR) + "," + n2n(MA) + "," + n2n(PE) + "," + n2n(OQ) + "," + n2n(SR) + "," + n2n(UT) + "," + n2n(ER) + ");"
	cursor.execute(tempSQL)
	result = cursor.rowcount
	if (result < 1):
		returnStr = "Error: resource not added."
	else:
		returnStr = "1st entry."
	# add event for add if stats included
	if OQ.isdigit():
		spawnID = dbShared.getSpawnID(resName,galaxy)
		dbShared.logEvent("INSERT INTO tResourceEvents (spawnID, userID, eventTime, eventType) VALUES (" + str(spawnID) + ",'" + currentUser + "',NOW(),'a');","a",currentUser, galaxy,spawnID)

	cursor.close()
	conn.close()
	return returnStr

def addResPlanet(spawn, planet, spawnName):
	# Add resource to a planet
	returnStr = ""
	conn = dbShared.ghConn()
	cursor = conn.cursor()
	cursor.execute("SELECT trp.enteredBy, trp.unavailable, tr.unavailable AS tru, trp.planetID, tr.enteredBy, trp.verified, trp.verifiedBy FROM tResources tr LEFT JOIN (SELECT * FROM tResourcePlanet WHERE tResourcePlanet.spawnID=" + str(spawn) + " AND tResourcePlanet.planetID=" + str(planet) + ") trp ON tr.spawnID = trp.spawnID WHERE tr.spawnID=" + str(spawn) + ";")
	row = cursor.fetchone()
	if row[3] == None:
		# insert spawn planet record
		tempSQL = "INSERT INTO tResourcePlanet (spawnID, planetID, entered, enteredBy) VALUES (" + str(spawn) + "," + str(planet) + ",NOW(),'" + currentUser + "');"
		cursor.execute(tempSQL)
		result = cursor.rowcount
		if (result < 1):
			returnStr = "Error: Could not add resource to planet."
		else:
			returnStr = spawnName + " added to " + str(ghNames.getPlanetName(planet))
		# add resource planet add event
		dbShared.logEvent("INSERT INTO tResourceEvents (spawnID, userID, eventTime, eventType, planetID) VALUES (" + str(spawn) + ",'" + currentUser + "',NOW(),'p'," + str(planet) + ");",'p',currentUser, galaxy, spawn)
		if row[2] != None:
			# update main resource table when becoming re-available
			tempSQL = "UPDATE tResources SET unavailable=NULL WHERE spawnID = " + str(spawn) + ";"
			cursor.execute(tempSQL)
			returnStr += " and marked re-available"
	else:
		if (row[1] == None and row[2] == None):
			if ((row[0] == None) or (row[0].lower() != currentUser.lower() and row[4].lower() != currentUser.lower())):
				if (row[6] == None or row[6].lower() != currentUser.lower()):
					tempSQL = "UPDATE tResourcePlanet SET verified=NOW(), verifiedBy='" + currentUser + "' WHERE spawnID=" + str(spawn) + " AND planetID=" + str(planet) + ";"
					result = cursor.execute(tempSQL)
					if (result < 1):
						returnStr = "Error: Resource " + spawnName + " was marked available on " + str(ghNames.getPlanetName(planet)) + " by " + row[0] + " and there was an error entering your verification."
					else:
						returnStr = "Resource " + spawnName + " has been verified by you.  It was marked available on " + str(ghNames.getPlanetName(planet)) + " by " + row[0] + "."
						# add event for verification
						dbShared.logEvent("INSERT INTO tResourceEvents (spawnID, userID, eventTime, eventType, planetID) VALUES (" + str(spawn) + ",'" + currentUser + "',NOW(),'v'," + str(planet) + ");",'v',currentUser,galaxy,spawn)
						# update main resource table when verifying
						tempSQL = "UPDATE tResources SET verified=NOW(), verifiedBy='" + currentUser + "' WHERE spawnID = " + str(spawn) + ";"
						cursor.execute(tempSQL)
				else:
					returnStr = "You already verified " + spawnName + " on " + str(row[5]) + "."
			else:
				returnStr = "You already entered resource " + spawnName
		else:
			# update resource status available for planet
			tempSQL = "UPDATE tResourcePlanet SET unavailable = NULL WHERE spawnID=" + str(spawn) + " AND planetID=" + str(planet) + ";"
			cursor.execute(tempSQL)
			result = cursor.rowcount

			# update main resource table when becoming re-available
			tempSQL = "UPDATE tResources SET unavailable=NULL WHERE spawnID = " + str(spawn) + ";"
			cursor.execute(tempSQL)
			returnStr = spawnName + " marked re-available on " + ghNames.getPlanetName(planet)
    
	cursor.close()
	conn.close()
	return returnStr

def addResStats(spawn, resType, CR, CD, DR, FL, HR, MA, PE, OQ, SR, UT, ER, forceOp):
	# Update stats for a spawn
	returnStr = ""
	needStat = 0
	hasStats = 0
	resStats = [CR,CD,DR,FL,HR,MA,PE,OQ,SR,UT,ER]

	conn = dbShared.ghConn()
	cursor = conn.cursor()
	cursor.execute("SELECT CR, CD, DR, FL, HR, MA, PE, OQ, SR, UT, ER, CRmax, CDmax, DRmax, FLmax, HRmax, MAmax, PEmax, OQmax, SRmax, UTmax, ERmax, tResources.resourceType FROM tResources INNER JOIN tResourceType ON tResources.resourceType=tResourceType.resourceType WHERE spawnID=" + str(spawn) + ";")
	row = cursor.fetchone()
	if row != None:
		for i in range(11):
			if row[i+11] > 0 and row[i] == None:
				needStat = 1
			if (resStats[i]>0 and resStats[i] != "" and resStats[i] != None):
				hasStats = 1
		# override normal behavior of only updating
		# when there are no stats if forceOp is set to edit
		if ( (not needStat) and forceOp != "edit"):
			returnStr = "Resource stats already entered."
		else:
			# update resource stats
			if hasStats:
				tempSQL = "UPDATE tResources SET enteredBy='" + currentUser + "', CR=" + n2n(CR) + ", CD=" + n2n(CD) + ", DR=" + n2n(DR) + ", FL=" + n2n(FL) + ", HR=" + n2n(HR) + ", MA=" + n2n(MA) + ", PE=" + n2n(PE) + ", OQ=" + n2n(OQ) + ", SR=" + n2n(SR) + ", UT=" + n2n(UT) + ", ER=" + n2n(ER) + " WHERE spawnID=" + str(spawn) + ";"
				#sys.stderr.write("sql: " + tempSQL + "\n")
				cursor.execute(tempSQL)
				result = cursor.rowcount
				returnStr = str(spawnName) + " stats updated"
				# add resource edit event
				if needStat:
					dbShared.logEvent("INSERT INTO tResourceEvents (spawnID, userID, eventTime, eventType) VALUES (" + str(spawn) + ",'" + currentUser + "',NOW(),'a');",'a',currentUser,galaxy,spawn)
				else:
					dbShared.logEvent("INSERT INTO tResourceEvents (spawnID, userID, eventTime, eventType) VALUES (" + str(spawn) + ",'" + currentUser + "',NOW(),'e');",'e',currentUser,galaxy,spawn)

		if (row[22] != resType and len(resType)>0):
			tempSQL = "UPDATE tResources SET resourceType='" + resType + "' WHERE spawnID=" + str(spawn) + ";"
			cursor.execute(tempSQL)
			returnStr = returnStr + " type updated"

	else:
		returnStr = "Error: could not find that resource " + str(spawnName) + "."
    
	cursor.close()
	conn.close()
	return returnStr


#  Check for errors
errstr = ""
if (len(spawnName) < 1 and spawnID == ""):
	errstr = errstr + "Error: no resource name. \r\n"
if ((resType == "none" or len(resType) < 1) and spawnID == "" and forceOp != "verify"):
	errstr = errstr + "Error: no resource type. \r\n"
if (spawnID == "" and galaxy == ""):
	errstr = errstr + "Error: no galaxy selected. \r\n"
else:
	# try to look up spawnID for editing and verifying
	if (spawnID == ""):
		spawnID = dbShared.getSpawnID(spawnName, galaxy)
if re.search('\W', spawnName):
	errstr = errstr + "Error: spawn name contains illegal characters."
if (forceOp != "edit" and planet.isdigit() == False):
	# attempt to lookup planet by name
	if planet != "":
		planet = dbShared.getPlanetID(planet)
	if planet.isdigit() == False:
		errstr = errstr + "Error: planet must be provided to post resource unless editing."

if (errstr == ""):
	result = ""
	galaxyState = dbShared.galaxyState(galaxy)
	if (logged_state > 0 and galaxyState == 1):
		if (spawnName == "" or spawnName == None):
			spawnName = ghNames.getSpawnName(spawnID)

		if (spawnID>-1):
			# spawn already entered
			if (forceOp == "edit"):
				result = "edit: "
				result = result + addResStats(spawnID, resType, CR, CD, DR, FL, HR, MA, PE, OQ, SR, UT, ER, forceOp)
			else:
				result = addResPlanet(spawnID, planet, spawnName)
				result = result + '  ' + addResStats(spawnID, resType, CR, CD, DR, FL, HR, MA, PE, OQ, SR, UT, ER, forceOp)
		else:
			# new spawn
			result = addResource(spawnName, galaxy, resType, CR, CD, DR, FL, HR, MA, PE, OQ, SR, UT, ER)
			spawnID = dbShared.getSpawnID(spawnName, galaxy)
			result = addResPlanet(spawnID, planet, spawnName) + '  ' + result

	else:
		if logged_state > 0:
			result = "Error: You cannot add resource data for an Inactive Galaxy."
		else:
			result = "Error: must be logged in to add resources"
else:
	result = errstr

print 'Content-type: text/xml\n'
doc = minidom.Document()
eRoot = doc.createElement("result")
doc.appendChild(eRoot)

eName = doc.createElement("spawnName")
tName = doc.createTextNode(spawnName)
eName.appendChild(tName)
eRoot.appendChild(eName)
eText = doc.createElement("resultText")
tText = doc.createTextNode(result)
eText.appendChild(tText)
eRoot.appendChild(eText)
eSource = doc.createElement("sourceRow")
tSource = doc.createTextNode(sourceRow)
eSource.appendChild(tSource)
eRoot.appendChild(eSource)
print doc.toxml()

if (result.find("Error:") > -1):
	sys.exit(500)
else:
	sys.exit(200)
