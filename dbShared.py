#!/usr/bin/python
"""

 Copyright 2010 Paul Willworth <ioscode@gmail.com>

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


import MySQLdb
import sys
sys.path.append("../")
import dbInfo
import subprocess
import ghObjects


def ghConn():
	conn = MySQLdb.connect(host = dbInfo.DB_HOST,
		db = dbInfo.DB_NAME,
		user = dbInfo.DB_USER,
		passwd = dbInfo.DB_PASS)
	conn.autocommit(True)
	return conn

def dbInsertSafe(insertStr):
	newStr = ""
	if (insertStr != None):
		for i in range(len(insertStr)):
			if (insertStr[i] == "'"):
				newStr = newStr + "'"
			newStr = newStr + insertStr[i]
	return newStr

def n2n(inVal):
	if (inVal == '' or inVal == None or inVal == 'undefined' or inVal == 'None'):
		return 'NULL'
	else:
		return str(inVal)

# update resource activity stats tracking
def logEvent(sqlStr, eventType, user, galaxy, spawnID):
	conn = ghConn()
	cursor = conn.cursor()
	if (cursor):
		cursor.execute(sqlStr)

		cursor.execute("SELECT userID FROM tUserStats WHERE userID='" + user + "' AND galaxy=" + str(galaxy) + ";")
		row = cursor.fetchone()
		if (row == None):
			cursor.execute("INSERT INTO tUserStats (userID, galaxy, added, planet, edited, removed, verified, waypoint, repGood, repBad) VALUES ('" + user + "'," + str(galaxy) + ",0,0,0,0,0,0,0,0);")
		if eventType == 'a':
			cursor.execute("UPDATE tUserStats SET added = added + 1 WHERE userID = '" + user + "' AND galaxy=" + str(galaxy) + ";")
			subprocess.call(["python","../checkAlerts.py", "-s " + str(spawnID)])
		elif eventType == 'p':
			cursor.execute("UPDATE tUserStats SET planet = planet + 1 WHERE userID = '" + user + "' AND galaxy=" + str(galaxy) + ";")
		elif eventType == 'e':
			cursor.execute("UPDATE tUserStats SET edited = edited + 1 WHERE userID = '" + user + "' AND galaxy=" + str(galaxy) + ";")
		elif eventType == 'r':
			cursor.execute("UPDATE tUserStats SET removed = removed + 1 WHERE userID = '" + user + "' AND galaxy=" + str(galaxy) + ";")
		elif eventType == 'v':
			cursor.execute("UPDATE tUserStats SET verified = verified + 1 WHERE userID = '" + user + "' AND galaxy=" + str(galaxy) + ";")
		elif eventType == 'w':
			cursor.execute("UPDATE tUserStats SET waypoint = waypoint + 1 WHERE userID = '" + user + "' AND galaxy=" + str(galaxy) + ";")
		elif eventType == '+':
			cursor.execute("UPDATE tUserStats SET repGood = repGood + 1 WHERE userID = '" + user + "' AND galaxy=" + str(galaxy) + ";")
		elif eventType == '-':
			cursor.execute("UPDATE tUserStats SET repBad = repBad + 1 WHERE userID = '" + user + "' AND galaxy=" + str(galaxy) + ";")
		cursor.close()
	conn.close()
	# Also log a user event for verifications
	if eventType == 'v':
		logUserEvent(user, galaxy, 'r', spawnID, eventType)

def logUserEvent(user, galaxy, targetType, targetID, eventType):
	conn = ghConn()
	cursor = conn.cursor()
	if (cursor):
		# add the event record
		cursor.execute("INSERT INTO tUserEvents (userID, targetType, targetID, eventType, eventTime) VALUES ('" + user + "','" + targetType + "'," + str(targetID) + ",'" + eventType + "',NOW());")
		# Check if user is experienced enough to give rep bonus
		expGood = False
		cursor.execute("SELECT added, repBad FROM tUserStats WHERE userID='" + user + "' AND galaxy=" + galaxy + ";")
		row = cursor.fetchone()
		if (row != None and row[0] != None):
			if (row[0] > (row[1] + 5)):
				expGood = True

		if eventType == "v" and expGood == True:
			# Get target User if target is resource
			if targetType == "r":
				cursor.execute("SELECT enteredBy FROM tResources WHERE spawnID=" + str(targetID) + ";")
				row = cursor.fetchone()
				if (row != None):
					targetUser = row[0]
			# Get target user if target is waypoint
			elif targetType == "w":
				cursor.execute("SELECT owner FROM tWaypoint WHERE waypointID=" + str(targetID) + ";")
				row = cursor.fetchone()
				if (row != None):
					targetUser = row[0]
			# Increment rep on target user for verification of their entry
			if targetUser != None:
				logEvent("SELECT userID FROM tUsers WHERE 1=2;","+",targetUser,galaxy,targetID)
		cursor.close()
	conn.close()

def getUserAttr(user, attr):
	conn = ghConn()
	cursor = conn.cursor()
	cursor.execute('SELECT pictureName, emailAddress, themeName, created, inGameInfo, paidThrough FROM tUsers WHERE userID="' + user + '"')
	row = cursor.fetchone()
	if (row != None):
		if attr == 'themeName':
			retAttr = row[2]
		elif attr == 'emailAddress':
			retAttr = row[1]
		elif attr == 'pictureName':
			if (row[0] == '' or row[0] == None):
				retAttr = 'default'
			else:
				retAttr = row[0]
		elif attr == 'created':
			retAttr = row[3]
		elif (attr == 'inGameInfo' and row[4] != None):
			retAttr = row[4]
		elif (attr == 'paidThrough' and row[5] != None):
			retAttr = row[5]
		else:
			retAttr = ''
	else:
		retAttr = ''

	cursor.close()
	conn.close()
	return retAttr

# Returns total amount user has donated to the site
def getUserDonated(user):
	conn = ghConn()
	cursor = conn.cursor()
	cursor.execute('SELECT Sum(paymentGross) FROM tPayments WHERE payerEmail = (SELECT emailAddress FROM tUsers WHERE userID=%s)', (user))
	row = cursor.fetchone()
	if (row != None and row[0] != None):
		retAttr = str(row[0])
	else:
		retAttr = ''

	cursor.close()
	conn.close()
	return retAttr

# Returns honor badge title for user based on stats
def getUserTitle(user):
	conn = ghConn()
	cursor = conn.cursor()
	cursor.execute('SELECT Sum(added), Sum(planet), Sum(edited), Sum(removed), Sum(verified), Sum(waypoint), Sum(repGood), Sum(repBad) FROM tUserStats WHERE userID = %s', (user))
	row = cursor.fetchone()
	if (row != None and row[0] != None):
		# build composite scores
		resScore = (float(row[0]) * 2) + (float(row[1]) / 2) + float(row[2]) + float(row[3]) + (float(row[4]) / 2)
		mapScore = float(row[5])
		repScore = float(row[6]) - float(row[7])
		# set resource title part
		if resScore > 2000:
			resTitle = "Reaper"
		elif resScore > 500:
			resTitle = "Hound"
		elif resScore > 25:
			resTitle = "Harvester"
		else:
			resTitle = "Seeker"
		# set mapping title part
		if mapScore > 400:
			mapTitle = "Cartographer"
		elif mapScore > 100:
			mapTitle = "Mapper"
		elif mapScore > 5:
			mapTitle = "Finder"
		else:
			mapTitle = "Seeker"
		# set reputation title part
		if repScore > 100:
			repTitle = "Revered "
		elif repScore > 50:
			repTitle = "Honored "
		elif repScore > 25:
			repTitle = "Verified "
		else:
			repTitle = ""

		# Determine Style
		if (resScore > 2000 or mapScore > 400) and repScore > 100:
			retAttr = '<span class="statMax">'
		elif (resScore > 500 or mapScore > 100) and repScore > 25:
			retAttr = '<span class="statHigh">'
		else:
			retAttr = '<span class="statNormal">'
		# build full title
		if (resScore / 5) > mapScore:
			retAttr = retAttr + repTitle + resTitle + '</span>'
		else:
			retAttr = retAttr + repTitle + mapTitle + '</span>'
	else:
		retAttr = '<span>Lurker</span>'

	cursor.close()
	conn.close()
	return retAttr

def getLastResourceChange():
	conn = ghConn()
	cursor = conn.cursor()
	cursor.execute('SELECT Max(entered) FROM tResources')
	row = cursor.fetchone()
	if (row != None):
		retDate = row[0]
	else:
		retDate = ''

	cursor.close()
	conn.close()
	return retDate

def getLastExport(galaxy):
	conn = ghConn()
	cursor = conn.cursor()
	cursor.execute('SELECT lastExport FROM tGalaxy WHERE galaxyID=' + str(galaxy))
	row = cursor.fetchone()
	if (row != None and row[0] != None):
		retDate = row[0]
	else:
		retDate = 'never'

	cursor.close()
	conn.close()
	return retDate

def getPlanetID(planetName):
	conn = ghConn()
	cursor = conn.cursor()
	cursor.execute('SELECT planetID FROM tPlanet WHERE LOWER(REPLACE(planetName," ","")) = "' + planetName + '";')
	row = cursor.fetchone()
	if (row != None and row[0] != None):
		retVal = str(row[0])
	else:
		retVal = ""

	cursor.close()
	conn.close()
	return retVal

def galaxyState(galaxyID):
	# 0 = Unlaunched, 1 = Active, 2 = Retired
	conn = ghConn()
	cursor = conn.cursor()
	cursor.execute('SELECT galaxyState FROM tGalaxy WHERE galaxyID = ' + str(galaxyID) + ';')
	row = cursor.fetchone()
	if (row != None and row[0] != None):
		retVal = row[0]
	else:
		retVal = 0

	cursor.close()
	conn.close()
	return retVal

def friendStatus(uid, ofUser):
	# 0 = None, 1 = Added, 2 = Reciprocated
	conn = ghConn()
	cursor = conn.cursor()
	cursor.execute('SELECT uf1.added, uf2.added FROM tUserFriends uf1 LEFT JOIN tUserFriends uf2 ON uf1.friendID=uf2.userID AND uf1.userID=uf2.friendID WHERE uf1.userID = \'' + ofUser + '\' AND uf1.friendID = \'' + uid + '\';')
	row = cursor.fetchone()
	if (row != None and row[0] != None):
		if row[1] != None:
			retVal = 2
		else:
			retVal = 1
	else:
		retVal = 0

	cursor.close()
	conn.close()
	return retVal

def getSpawnID(resName, galaxy):
	conn = ghConn()
	cursor = conn.cursor()
	cursor.execute("SELECT spawnID FROM tResources WHERE galaxy=" + galaxy + " AND spawnName='" + resName + "';")
	row = cursor.fetchone()
	if row == None:
		newid = -1
	else:
		newid = row[0]

	cursor.close()
	conn.close()
	return newid

def getSpawnPlanets(conn, spawnID, availableOnly):
	criteriaStr = ''
	planets = []
	cursor = conn.cursor()
	if (cursor):
		if availableOnly:
			criteriaStr = ' AND unavailable IS NULL'
		sqlStr = 'SELECT tPlanet.planetID, planetName, enteredBy FROM tPlanet LEFT JOIN (SELECT planetID, enteredBy FROM tResourcePlanet WHERE spawnID='+str(spawnID)+criteriaStr+') trp ON tPlanet.planetID=trp.planetID;'
		cursor.execute(sqlStr)
		row = cursor.fetchone()
		while (row != None):
			p = ghObjects.resourcePlanet(row[0], row[1], row[2])
			planets.append(p)
			row = cursor.fetchone()
	cursor.close()
	return planets

