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
import Cookie
import dbSession
import dbShared
import cgi
import MySQLdb
#
form = cgi.FieldStorage()

galaxy = form.getfirst('galaxy', '')
statID = form.getfirst('statID', '')
# escape input to prevent sql injection
galaxy = dbShared.dbInsertSafe(galaxy)

# Main program
rowCount = 0
print 'Content-type: text/html\r\n\r\n'

conn = dbShared.ghConn()
cursor = conn.cursor()
if (cursor):
	if statID == 'currentSpawns':
		sqlStr = 'SELECT Count(spawnID) FROM tResources WHERE galaxy=' + galaxy + ' AND unavailable IS NULL;'
	elif statID == 'totalSpawns':
		sqlStr = 'SELECT Count(spawnID) FROM tResources WHERE galaxy=' + galaxy + ';'
	elif statID == 'currentWaypoints':
		sqlStr = 'SELECT Count(*) FROM tWaypoint INNER JOIN tResources ON tWaypoint.spawnID = tResources.spawnID WHERE galaxy=' + galaxy + ' AND tWaypoint.unavailable IS NULL AND tResources.unavailable IS NULL;'
	else:
		sqlStr = 'SELECT \'Unknown statID\';'

	cursor.execute(sqlStr)
	row = cursor.fetchone()

	if (row != None):
		print str(row[0])
        
	cursor.close()
conn.close()

