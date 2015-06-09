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

import os
import sys
import MySQLdb
import dbShared
import cgi
import urllib
sys.path.append("../")
import dbInfo
#

form = cgi.FieldStorage()
key1 = form.getfirst('key1', '')
key2 = form.getfirst('key2', '')
key3 = form.getfirst('key3', '')
key4 = form.getfirst('key4', '')
key5 = form.getfirst('key5', '')
iFile = form.getfirst('iFile', '')
iContent = form.getfirst('iContent', '')
# escape input
key1 = dbShared.dbInsertSafe(key1)
key2 = dbShared.dbInsertSafe(key2)
key3 = dbShared.dbInsertSafe(key3)
key4 = dbShared.dbInsertSafe(key4)
key5 = dbShared.dbInsertSafe(key5)
iFile = urllib.unquote(iFile)
iContent = urllib.unquote(iContent)

def n2n(inVal):
	if (inVal == None):
		return '\N'
	else:
		return str(inVal)

# Main program
print 'Content-type: text/html\n'

try:
	conn = MySQLdb.connect(host = dbInfo.DB_HOST,
		db = dbInfo.DB_NAME,
		user = dbInfo.DB_USER,
		passwd = key1)
except:
	if (key3 == dbInfo.DB_KEY3):
		conn = MySQLdb.connect(host = dbInfo.DB_HOST,
			db = dbInfo.DB_NAME,
			user = dbInfo.DB_USER,
			passwd = dbInfo.DB_PASS)

if key5 == dbInfo.DB_KEY5:
	f = open(iFile, 'w')
	f.write(iContent)
	f.close()

galaxyCursor = conn.cursor()
if (galaxyCursor):
	if key4 == dbInfo.DB_KEY4:
		galaxySQL = 'DELETE FROM ' + key2 + ';'
	else:
		galaxySQL = 'SELECT * FROM ' + key2 + ';'

	galaxyCursor.execute(galaxySQL)
	row = galaxyCursor.fetchone()
	while (row != None):
		tmpStr = ''
		# write  line
		for i in range(len(row)):
			tmpStr += n2n(row[i]) + '\t'

		tmpStr = tmpStr[:-1]
		tmpStr = '\\n'.join(tmpStr.split('\n'))
		print tmpStr
		row = galaxyCursor.fetchone()

	galaxyCursor.close()
	
conn.close()



