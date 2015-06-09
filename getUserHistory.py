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

import dbShared
import cgi
import MySQLdb
import ghShared
import dbShared
#
form = cgi.FieldStorage()

galaxy = form.getfirst('galaxy', '')
uid = form.getfirst('uid', '')
lastTime = form.getfirst('lastTime', '')
# escape input to prevent sql injection
galaxy = dbShared.dbInsertSafe(galaxy)
uid = dbShared.dbInsertSafe(uid)
lastTime = dbShared.dbInsertSafe(lastTime)
timeCriteria = ""
pageSize = 42
# Main program

print 'Content-type: text/html\n'
if (len(lastTime) > 5):
	timeCriteria = " AND eventTime < '" + lastTime + "'"

conn = dbShared.ghConn()
cursor = conn.cursor()
if (cursor):
	if uid != '':
		print '<table class="userData" width="640">'
		print '<thead><tr class="tableHead"><td width="150">Time</td><td width="85">Spawn</td><td width="180">Resource Type</td><td width="75">Action</td><td width="75">Planet</td><td width="75">Galaxy</td></th></thead>'
		sqlStr = 'SELECT eventTime, spawnName, eventType, planetName, galaxyName, tResources.resourceType, tResourceType.resourceTypeName FROM tResourceEvents INNER JOIN tResources ON tResourceEvents.spawnID = tResources.spawnID INNER JOIN tGalaxy ON tResources.galaxy = tGalaxy.galaxyID INNER JOIN tResourceType ON tResources.resourceType = tResourceType.resourceType LEFT JOIN tPlanet ON tResourceEvents.planetID = tPlanet.planetID WHERE userID="' + uid + '"' + timeCriteria + ' ORDER BY eventTime DESC LIMIT ' + str(pageSize) + ';'
	else:
		print '<table class="userData" width="620">'
		print '<thead><tr class="tableHead"><td width="100">Member</td><td width="140">Time</td><td width="85">Spawn</td><td width="175">Resource Type</td><td width="70">Action</td><td width="50">Planet</td></th></thead>'
		sqlStr = 'SELECT userID, eventTime, spawnName, eventType, planetName, tResources.resourceType, tResourceType.resourceTypeName FROM tResourceEvents INNER JOIN tResources ON tResourceEvents.spawnID = tResources.spawnID INNER JOIN tResourceType ON tResources.resourceType = tResourceType.resourceType LEFT JOIN tPlanet ON tResourceEvents.planetID = tPlanet.planetID WHERE galaxy=' + galaxy + timeCriteria + ' ORDER BY eventTime DESC LIMIT ' + str(pageSize) + ';'
    
	cursor.execute(sqlStr)
	row = cursor.fetchone()

	if uid != '':
		while (row != None):
			print '  <tr class="statRow"><td>' + str(row[0]) + '</td><td><a href="' + ghShared.BASE_SCRIPT_URL + 'resource.py/' + str(galaxy) + '/' + row[1] + '" class="nameLink">' + row[1] + '</a></td><td><a href="' + ghShared.BASE_SCRIPT_URL + 'resourceType.py/' + row[5] + '" class="nameLink">' + row[6] + '</a></td><td>' + ghShared.getActionName(row[2]) + '</td><td>' + str(row[3]) + '</td><td>' + row[4] + '</td>'
			print '  </tr>'
			lastTime = row[0]
			row = cursor.fetchone()
	else:
		while (row != None):
			print '  <tr class="statRow"><td>' + row[0] + '</td><td>' + str(row[1]) + '</td><td><a href="' + ghShared.BASE_SCRIPT_URL + 'resource.py/' + str(galaxy) + '/' + row[2] + '" class="nameLink">' + row[2] + '</a></td><td><a href="' + ghShared.BASE_SCRIPT_URL + 'resourceType.py/' + row[5] + '" class="nameLink">' + row[6] + '</a></td><td>' + ghShared.getActionName(row[3]) + '</td><td>' + str(row[4]) + '</td>'
			print '  </tr>'
			lastTime = row[1]
			row = cursor.fetchone()
        
	print '  </table>'
	if (cursor.rowcount == pageSize):
		print '<div style="text-align:center;"><button id="moreButton" class="ghButton" onclick="moreHistory(\''+ str(lastTime) + '\');">More</button></div>'
	cursor.close()
conn.close()

