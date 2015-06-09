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
import cgi
import re
import Cookie
import hashlib
import MySQLdb
import dbSession
import dbShared

cookies = Cookie.SimpleCookie()
useCookies = 1
errorstr = ''
try:
    cookies.load(os.environ["HTTP_COOKIE"])
except KeyError:
    useCookies = 0

form = cgi.FieldStorage()

uname = form.getfirst("uname")
email = form.getfirst("email")
userpass = form.getfirst("userpass")
src_url = form.getfirst("src_url")
# escape input to prevent sql injection
uname = dbShared.dbInsertSafe(uname)
email = dbShared.dbInsertSafe(email)
userpass = dbShared.dbInsertSafe(userpass)

if uname == None or email == None or userpass == None:
    errorstr = "Missing user parameters"
else:
    if len(uname) < 3:
        errorstr = errorstr + "The login name must be at least 3 characters.\n"
    if len(email) < 6:
        errorstr = errorstr + "That was not a valid email address.\n"
    if len(userpass) < 6:
        errorstr = errorstr + "The password must be at least 6 characters.\n"
    if re.search('\W', uname):
        errorstr = errorstr + "Error: user name contains illegal characters.\n"
    if re.search('[><"&\']', email):
        errorstr = errorstr + "Error: email address contains illegal characters.\n"

if errorstr != "":
    result = "fail"
else:
    crypt_pass = hashlib.sha1(uname + userpass).hexdigest()

    conn = dbShared.ghConn()
    cursor = conn.cursor()
    cursor.execute("SELECT userID FROM tUsers WHERE userID='" + uname + "';")
    row = cursor.fetchone()
    if row != None:
        result = "fail"
        errorstr = "That login name is already used, please try another."
    else:
        updatestr = "INSERT INTO tUsers (userID, emailAddress, userPassword, created, lastLogin) VALUES ('" + uname + "','" + email + "','" + crypt_pass + "', Now(), Now());"
	cursor.execute(updatestr)
	result = "success"

    cursor.close()
    conn.close()

if useCookies:
    cookies["create_result"] = result
    cookies["create_error"] = errorstr
    print cookies

print "Content-Type: text/html\n"
if errorstr != "":
    print errorstr, "\n"
else:
    if src_url == None:
        src_url = 'ghHome.py'
    print '<html><head><script type=text/javascript>document.location.href="authUser.py?src_url=' + src_url + '&loginu=' + uname + '&passc=' + crypt_pass + '"</script></head><body></body></html>'


