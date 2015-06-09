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
import cgi
import Cookie
import dbSession
import dbShared
import MySQLdb
import ghShared
import ghLists
import ghObjects
from jinja2 import Environment, FileSystemLoader

def getResourceHistory(conn, spawnID):
	# generate table of resource event history
	resHistory = ''
	sqlStr = 'SELECT eventTime, userID, eventType, planetName FROM tResourceEvents INNER JOIN tResources ON tResourceEvents.spawnID = tResources.spawnID LEFT JOIN tPlanet ON tResourceEvents.planetID = tPlanet.planetID WHERE tResources.spawnID="' + str(spawnID) + '" ORDER BY eventTime DESC;'
	try:
		cursor = conn.cursor()
	except Exception:
		resHistory = '<div class="error">Error: could not connect to database</div>'

	if (cursor):
		cursor.execute(sqlStr)
		row = cursor.fetchone()
		resHistory += '<table class="userData">'
		resHistory += '<thead><tr class="tableHead"><td>Time</td><td>User</td><td>Action</td><td width="50">Planet</td></th></thead>'
		while (row != None):
			resHistory += '  <tr class="statRow"><td>' + str(row[0]) + '</td><td>' + row[1] + '</td><td>' + ghShared.getActionName(row[2]) + '</td><td>' + str(row[3]) + '</td>'
			resHistory += '  </tr>'
			row = cursor.fetchone()   
		resHistory += '  </table>'
		cursor.close()

	return resHistory

def getResource(conn, logged_state, currentUser, spawnID, galaxy, spawnName):
	if logged_state == 1:
		favJoin = ' LEFT JOIN (SELECT itemID, favGroup FROM tFavorites WHERE userID="' + currentUser + '" AND favType=1) favs ON tResources.spawnID = favs.itemID'
		favCols = ', favGroup'
	else:
		favJoin = ''
		favCols = ', NULL'
	if spawnID != None:
		criteriaStr = 'spawnID=' + str(spawnID)
	else:
		criteriaStr = 'galaxy=' + galaxy + ' AND spawnName="' + spawnName + '"'

	try:
		cursor = conn.cursor()
	except Exception:
		errorstr = "Error: could not connect to database"

	if (cursor):
		sqlStr = 'SELECT spawnID, spawnName, galaxy, entered, enteredBy, tResources.resourceType, rt1.resourceTypeName, rt1.resourceGroup,'
		sqlStr += ' CR, CD, DR, FL, HR, MA, PE, OQ, SR, UT, ER,'
		sqlStr += ' CASE WHEN rt1.CRmax > 0 THEN ((CR-rt1.CRmin) / (rt1.CRmax-rt1.CRmin))*100 ELSE NULL END AS CRperc, CASE WHEN rt1.CDmax > 0 THEN ((CD-rt1.CDmin) / (rt1.CDmax-rt1.CDmin))*100 ELSE NULL END AS CDperc, CASE WHEN rt1.DRmax > 0 THEN ((DR-rt1.DRmin) / (rt1.DRmax-rt1.DRmin))*100 ELSE NULL END AS DRperc, CASE WHEN rt1.FLmax > 0 THEN ((FL-rt1.FLmin) / (rt1.FLmax-rt1.FLmin))*100 ELSE NULL END AS FLperc, CASE WHEN rt1.HRmax > 0 THEN ((HR-rt1.HRmin) / (rt1.HRmax-rt1.HRmin))*100 ELSE NULL END AS HRperc, CASE WHEN rt1.MAmax > 0 THEN ((MA-rt1.MAmin) / (rt1.MAmax-rt1.MAmin))*100 ELSE NULL END AS MAperc, CASE WHEN rt1.PEmax > 0 THEN ((PE-rt1.PEmin) / (rt1.PEmax-rt1.PEmin))*100 ELSE NULL END AS PEperc, CASE WHEN rt1.OQmax > 0 THEN ((OQ-rt1.OQmin) / (rt1.OQmax-rt1.OQmin))*100 ELSE NULL END AS OQperc, CASE WHEN rt1.SRmax > 0 THEN ((SR-rt1.SRmin) / (rt1.SRmax-rt1.SRmin))*100 ELSE NULL END AS SRperc, CASE WHEN rt1.UTmax > 0 THEN ((UT-rt1.UTmin) / (rt1.UTmax-rt1.UTmin))*100 ELSE NULL END AS UTperc, CASE WHEN rt1.ERmax > 0 THEN ((ER-rt1.ERmin) / (rt1.ERmax-rt1.ERmin))*100 ELSE NULL END AS ERperc,'
		sqlStr += ' rt1.containerType, verified, verifiedBy, unavailable, unavailableBy, rg1.groupName, rt1.resourceCategory, rg2.groupName AS categoryName' + favCols + ', (SELECT GROUP_CONCAT(resourceGroup SEPARATOR ",") FROM tResourceTypeGroup rtg WHERE rtg.resourceType=tResources.resourceType) FROM tResources INNER JOIN tResourceType rt1 ON tResources.resourceType = rt1.resourceType INNER JOIN tResourceGroup rg1 ON rt1.resourceGroup = rg1.resourceGroup INNER JOIN tResourceGroup rg2 ON rt1.resourceCategory = rg2.resourceGroup' + favJoin + ' WHERE ' + criteriaStr + ';'
		cursor.execute(sqlStr)
		row = cursor.fetchone()

		# get resource box if the spawn was found
		if (row != None):
			s = ghObjects.resourceSpawn()
			s.spawnID = row[0]
			s.spawnName = row[1]
			s.spawnGalaxy = row[2]
			s.resourceType = row[5]
			s.resourceTypeName = row[6]
			s.containerType = row[30]
			s.stats.CR = row[8]
			s.stats.CD = row[9]
			s.stats.DR = row[10]
			s.stats.FL = row[11]
			s.stats.HR = row[12]
			s.stats.MA = row[13]
			s.stats.PE = row[14]
			s.stats.OQ = row[15]
			s.stats.SR = row[16]
			s.stats.UT = row[17]
			s.stats.ER = row[18]
		
			s.percentStats.CR = row[19]
			s.percentStats.CD = row[20]
			s.percentStats.DR = row[21]
			s.percentStats.FL = row[22]
			s.percentStats.HR = row[23]
			s.percentStats.MA = row[24]
			s.percentStats.PE = row[25]
			s.percentStats.OQ = row[26]
			s.percentStats.SR = row[27]
			s.percentStats.UT = row[28]
			s.percentStats.ER = row[29]

			s.entered = row[3]
			s.enteredBy = row[4]
			s.verified = row[31]
			s.verifiedBy = row[32]
			s.unavailable = row[33]
			s.unavailableBy = row[34]
			if row[38] != None:
				s.favorite = 1
			s.groupList = ',' + row[39] + ','
			s.planets = dbShared.getSpawnPlanets(conn, row[0], True)
		else:
			s = None

		cursor.close()

	return s

def main():
	resHTML = '<h2>That resource does not exist</h2>'
	resHistory = ''
	useCookies = 1
	linkappend = ''
	logged_state = 0
	currentUser = ''
	galaxy = ''
	spawnName = ''
	uiTheme = ''
	galaxyState = 0
	# Get current url
	try:
		url = os.environ['SCRIPT_NAME']
	except KeyError:
		url = ''

	form = cgi.FieldStorage()
	# Get Cookies

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
		loginResult = form.getfirst('loginAttempt', '')
		sid = form.getfirst('gh_sid', '')

	# escape input to prevent sql injection
	sid = dbShared.dbInsertSafe(sid)

	# Get a session
	
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
	else:
		if (uiTheme == ''):
			uiTheme = 'crafter'

	path = ['']
	if os.environ.has_key('PATH_INFO'):
		path = os.environ['PATH_INFO'].split('/')[1:]
		path = [p for p in path if p != '']

	if len(path) > 1:
		galaxy = dbShared.dbInsertSafe(path[0])
		spawnName = dbShared.dbInsertSafe(path[1])
		if galaxy != '':
			conn = dbShared.ghConn()
			spawn = getResource(conn, logged_state, currentUser, None, galaxy, spawnName)
			galaxyState = dbShared.galaxyState(spawn.spawnGalaxy)
			if galaxyState == 1:
				resHTML = spawn.getHTML(logged_state, 0, "")
			else:
				resHTML = spawn.getHTML(0, 0, "")

			resHistory = getResourceHistory(conn, spawn.spawnID)
			conn.close()
		else:
			resHTML = '<h2>No Galaxy/Resource name given</h2>'
	else:
		resHTML = '<h2>No Galaxy/Resource name given</h2>'

	pictureName = dbShared.getUserAttr(currentUser, 'pictureName')
	print 'Content-type: text/html\n'
	env = Environment(loader=FileSystemLoader('templates'))
	env.globals['BASE_SCRIPT_URL'] = ghShared.BASE_SCRIPT_URL
	template = env.get_template('resource.html')
	print template.render(uiTheme=uiTheme, loggedin=logged_state, currentUser=currentUser, loginResult=loginResult, linkappend=linkappend, url=url, pictureName=pictureName, imgNum=ghShared.imgNum, galaxyList=ghLists.getGalaxyList(), planetList=ghLists.getPlanetList(), spawnName=spawnName, resHTML=resHTML, resHistory=resHistory)


if __name__ == "__main__":
	main()

