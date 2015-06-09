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
import cgi
import Cookie
import dbSession
import dbShared
import MySQLdb
import ghShared
import ghLists

# Get current url
try:
	url = os.environ['SCRIPT_NAME']
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
else:
	currentUser = ''
	loginResult = form.getfirst('loginAttempt', '')
	sid = form.getfirst('gh_sid', '')

# Get a session
logged_state = 0
linkappend = ''
disableStr = ''
# escape input to prevent sql injection
sid = dbShared.dbInsertSafe(sid)

if loginResult == None:
	loginResult = 'success'

sess = dbSession.getSession(sid, 2592000)
if (sess != ''):
	logged_state = 1
	currentUser = sess
	if (uiTheme == ''):
		uiTheme = dbShared.getUserAttr(currentUser, 'themeName')
	if (useCookies == 0):
		linkappend = 'gh_sid=' + sid
	userPadded = ' ' + currentUser
else:
	disableStr = ' disabled="disabled"'
	if (uiTheme == ''):
		uiTheme = 'crafter'
	userPadded = ''

messageAction = form.getfirst('action', '')

if (messageAction == 'canceldonate'):
	theMessage = 'Donation Cancelled'
elif (messageAction == 'donedonate'):
	theMessage = 'Donation Completed, Thank You' + userPadded + '!'
else:
	theMessage = ''

print 'Content-type: text/html\n'
print '<!DOCTYPE html'
print '        PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"'
print '         "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
print '<html xmlns="http://www.w3.org/1999/xhtml" lang="en-US" xml:lang="en-US"><head><title>Waypoint Maps - Galaxy Harvester</title>'
print '<link rel="stylesheet" href="/style/ghCore.css" type="text/css" />'
print '<link rel="stylesheet" href="/style/themes/'+uiTheme+'.css" type="text/css" />'
print '<script type="text/javascript" src="/js/jquery.min.js"></script>'
print '<script src="/js/ghShared.js" type="text/javascript"></script>'
print '<script type="text/javascript">'
print '$(document).ready(function() {'
print '    $("#galaxySel").val(getCookie("galaxy",defaultGalaxy));'
print '    $(".window .close").click(function(e) {'
print '        e.preventDefault();'
print '        $("#mask, .window").hide();'
print '    });'
print '    $("#mask").click(function() {'
print '        $(this).hide();'
print '        $(".window").hide();'
print '    });'
print '});'
print '</script>'
ghShared.printPageTracker()
print '<body>'
ghShared.printHeaderSection(logged_state, currentUser, loginResult, linkappend, url)

print '<div id="mainContent" class="wrapper">'
print '  <div id="leftNavContent" class="ghCol">'
print '    <div id="sideBox" class="ghWidgetBox">'
print '    </div>'
print '  </div>'
print '  <div id="rightMainContent" class="ghCol">'
print '    <div id="messageBox" class="ghWidgetBox">'
print '    <div class="standOut">' + theMessage + '</div>'
print '    Go back to the <a href="/ghHome.py" title="Home Page">home</a> page.'
print '    </div>'
print '  </div>'
print '</div>'
ghShared.printPageFooter()
ghShared.printJoinForm(logged_state, '?src_url=waypointMaps.py&' + linkappend, url)
print '<div id="mask"> </div>'
print '</body></html>'
