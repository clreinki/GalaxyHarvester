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
import cgi
import Cookie
import hashlib
import time
import MySQLdb
import dbSession
import dbShared
import urllib
import datetime

cookies = Cookie.SimpleCookie()
useCookies = 1
result = ''
linkappend = ''
try:
	cookies.load(os.environ['HTTP_COOKIE'])
except KeyError:
	useCookies = 0

form = cgi.FieldStorage()

src_url = form.getfirst('src_url')
sid = form.getfirst('gh_sid')
loginp = form.getfirst('loginu')
passp = form.getfirst('passu')
passc = form.getfirst('passc')
persist = form.getfirst('persist')
#sessions persist up to 30 days
duration = 2592000
#escape input to prevent sql injection
loginp = dbShared.dbInsertSafe(loginp)
sid = dbShared.dbInsertSafe(sid)

if (loginp == None or (passp == None and passc == None)):
	result = 'no login data'
else:
	if (passc == None):
		crypt_pass = hashlib.sha1(loginp + passp).hexdigest()
	else:
		# already encrypted password was sent
		crypt_pass = passc

	conn = dbShared.ghConn()
	cursor = conn.cursor()
	cursor.execute('SELECT userID, userPassword FROM tUsers WHERE userID="' + loginp + '";')
	row = cursor.fetchone()
	if row == None:
		result = 'bad user'
	else:
		if row[1] == crypt_pass:
			updatestr = 'UPDATE tUsers SET lastLogin=NOW() WHERE userID="' + loginp + '";'
			cursor.execute(updatestr)
			dbSession.verifySessionDB()
			sid = hashlib.sha1(str(time.time()) + loginp).hexdigest()
			updatestr = 'INSERT INTO tSessions (sid, userID, expires) VALUES ("' + sid + '", "' + loginp + '", ' + str(time.time() + duration) + ');'
			cursor.execute(updatestr)
			result = 'success'
		else:
			result = 'bad password'

	cursor.close()
	conn.close()

if sid == None:
	sid = ""
if useCookies:
	cookies['loginAttempt'] = result
	if result == "success":
		# session id cookie expires when browser closes unless we are told to persist
		expiration = datetime.datetime.utcnow() + datetime.timedelta(days=30)
		cookies['gh_sid'] = sid
		if persist != None:
			cookies['gh_sid']['expires'] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
		# userid and theme stay for up to 7 days
		expiration = datetime.datetime.now() + datetime.timedelta(days=7)
		cookies['userID'] = loginp
		cookies['userID']['expires'] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
		cookies['uiTheme'] = dbShared.getUserAttr(loginp, 'themeName')
		cookies['uiTheme']['expires'] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
	print cookies
else:
	# add results to url if not using cookies
	linkappend = 'loginAttempt=' + urllib.quote(result) + '&gh_sid=' + sid

print 'Content-Type: text/html\n'
if src_url != None:
	if src_url.find('?') > -1:
		queryChar = '&'
	else:
		queryChar = '?'
	# go back where they came from
	print '<html><head><script type=text/javascript>document.location.href="' + src_url + queryChar + linkappend + '"</script></head><body></body></html>'
else:
	print sid
