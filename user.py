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
import cgi
import Cookie
import dbSession
import MySQLdb
import ghShared
import ghLists
import ghCharts
import dbShared
import time
from datetime import timedelta, datetime
import urllib
from jinja2 import Environment, FileSystemLoader

# Get current url
try:
	url = os.environ['REQUEST_URI']
except KeyError:
	url = ''
uiTheme = ''
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
	try:
		uiTheme = cookies['uiTheme'].value
	except KeyError:
		uiTheme = ''
	try:
		avatarResult = cookies['avatarAttempt'].value
	except KeyError:
		avatarResult = ''
	try:
		galaxy = cookies['galaxy'].value
	except KeyError:
		galaxy = '14'
else:
	currentUser = ''
	loginResult = form.getfirst('loginAttempt', '')
	avatarResult = form.getfirst('avatarAttempt', '')
	sid = form.getfirst('gh_sid', '')
	galaxy = '14'

uid = form.getfirst('uid', '')
# escape input to prevent sql injection
sid = dbShared.dbInsertSafe(sid)
uid = dbShared.dbInsertSafe(uid)

# Get a session
logged_state = 0
linkappend = ''
disableStr = ''
created = datetime.fromtimestamp(time.time())
inGameInfo = ''
pictureName = ''
userPictureName = ''
friendCountStr = ''
donateTotal = ''
userTitle = ''
donorBadge = ''
email = ''
# get user attributes
if uid != '':
	created = dbShared.getUserAttr(uid, 'created')
	inGameInfo = dbShared.getUserAttr(uid, 'inGameInfo')
	userPictureName = dbShared.getUserAttr(uid, 'pictureName')
	donateTotal = dbShared.getUserDonated(uid)
	userTitle = dbShared.getUserTitle(uid)
	if userPictureName == '':
		userPictureName = 'default.jpg'
	if donateTotal != '':
		donorBadge = '<img src="/images/coinIcon.png" width="16" title="This user has donated to the site" alt="coin" />'
	# get friend count
	conn = dbShared.ghConn()
	cursor = conn.cursor()
	cursor.execute('SELECT Count(uf1.added) FROM tUserFriends uf1 INNER JOIN tUserFriends uf2 ON uf1.friendID=uf2.userID AND uf1.userID=uf2.friendID WHERE uf1.userID="' + uid + '"')
	row = cursor.fetchone()
	if (row != None):
		friendCountStr = '(' + str(row[0]) + ')'
	cursor.close()
	conn.close()

if loginResult == None:
	loginResult = 'success'

sess = dbSession.getSession(sid, 2592000)
if (sess != ''):
	logged_state = 1
	currentUser = sess
	if (useCookies == 0):
		linkappend = 'gh_sid=' + sid
	conn = dbShared.ghConn()
	cursor = conn.cursor()
	cursor.execute('SELECT userID, emailAddress, themeName FROM tUsers WHERE userID="' + currentUser + '"')
	row = cursor.fetchone()
	if (row != None):
		email = row[1]
		uiTheme = row[2]
	cursor.close()
	conn.close()
else:
	disableStr = ' disabled="disabled"'
	if (uiTheme == ''):
		uiTheme = 'crafter'

convertGI = ghShared.convertText(inGameInfo, "js")
tmpStat = dbShared.friendStatus(uid, currentUser)
joinedStr = 'Joined ' + ghShared.timeAgo(created) + ' ago'
pictureName = dbShared.getUserAttr(currentUser, 'pictureName')
print 'Content-type: text/html\n'
env = Environment(loader=FileSystemLoader('templates'))
env.globals['BASE_SCRIPT_URL'] = ghShared.BASE_SCRIPT_URL
template = env.get_template('user.html')
print template.render(uiTheme=uiTheme, loggedin=logged_state, currentUser=currentUser, loginResult=loginResult, linkappend=linkappend, url=url, pictureName=pictureName, imgNum=ghShared.imgNum, galaxyList=ghLists.getGalaxyList(), themeList=ghLists.getThemeList(), uid=uid, convertGI=convertGI, sid=sid, avatarResult=avatarResult, email=email, donorBadge=donorBadge, joinedStr=joinedStr, userPictureName=userPictureName, tmpStat=tmpStat, userTitle=userTitle, friendCountStr=friendCountStr, chart1URL=ghCharts.getChartURL('bhs', '200x150', 'a', 'creature_resources', 0, 'user', galaxy), chart2URL=ghCharts.getChartURL('bhs', '200x150', 'a', 'inorganic', 0, 'user', galaxy), chart3URL=ghCharts.getChartURL('bhs', '200x150', 'a', 'flora_resources', 0, 'user', galaxy), chart4URL=ghCharts.getChartURL('bhs', '200x150', 'removed', 'all', 0, 'user', galaxy), chart5URL=ghCharts.getChartURL('bhs', '200x150', 'planet', 'all', 0, 'user', galaxy), chart6URL=ghCharts.getChartURL('bhs', '200x150', 'verified', 'all', 0, 'user', galaxy))

