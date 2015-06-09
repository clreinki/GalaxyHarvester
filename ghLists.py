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
import MySQLdb
import dbShared


def getThemeList():
	result = ''
	result += '      <option value="ghAlpha">Alpha Blue</option>'
	result += '      <option value="crafter">Crafter Grey</option>'
	result += '      <option value="Destroyer">Destroyer</option>'
	result += '      <option value="FSJediGray">FS Jedi</option>'
	result += '      <option value="Hutt">Hutt</option>'
	result += '      <option value="Imperial">Imperial</option>'
	result += '      <option value="ghOriginal">Original</option>'
	result += '      <option value="Rebel">Rebel</option>'
	result += '      <option value="rebelFlightSuits">Rebel Flight Suits</option>'
	result += '      <option value="WinduPurple">Windu Purple</option>'
	return result

def getSchematicTabList():
	result = ''
	result += '    <option value="1">Weapon</option>'
	result += '    <option value="2">Armor</option>'
	result += '    <option value="4">Food</option>'
	result += '    <option value="8">Clothing</option>'
	result += '    <option value="16">Vehicle</option>'
	result += '    <option value="32">Droid</option>'
	result += '    <option value="64">Chemical</option>'
	result += '    <option value="128">Bio-Chemical</option>'
	result += '    <option value="256">Creature</option>'
	result += '    <option value="512">Furniture</option>'
	result += '    <option value="1024">Installation</option>'
	result += '    <option value="2048">Jedi</option>'
	result += '    <option value="8192">Genetics</option>'
	result += '    <option value="131072">Starship Components</option>'
	result += '    <option value="262144">Ship Tools</option>'
	result += '    <option value="524288">Misc</option>'
	return result

def getOptionList(sqlStr):
	result = ""
	conn = dbShared.ghConn()
	cursor = conn.cursor()
	if (cursor):
		cursor.execute(sqlStr)
		row = cursor.fetchone()
		while (row != None):
			if len(row)>2:
				result = result + '  <option value="' + str(row[0]) + '" group="' + str(row[2]) + '">' + row[1] + '</option>'
			elif len(row)>1:
				result = result + '  <option value="' + str(row[0]) + '">' + row[1] + '</option>'
			else:
				result = result + '  <option>' + row[0] + '</option>'
			row = cursor.fetchone()
		cursor.close()
	conn.close()
	return result

def getResourceTypeList():
	listStr = getOptionList('SELECT resourceType, resourceTypeName FROM tResourceType ORDER BY resourceTypeName;')
	return listStr

def getResourceGroupList():
	listStr = getOptionList('SELECT resourceGroup, groupName FROM tResourceGroup WHERE groupLevel > 1 ORDER BY groupName;')
	return listStr

def getResourceGroupListShort():
	listStr = getOptionList('SELECT resourceGroup, groupName FROM tResourceGroup WHERE groupLevel < 4 AND groupLevel > 1 ORDER BY groupName;')
	return listStr

def getGalaxyList():
	listStr = getOptionList('SELECT galaxyID, galaxyName, galaxyState FROM tGalaxy WHERE galaxyState < 3 ORDER BY galaxyState, galaxyName;')
	return listStr

def getPlanetList():
	listStr = getOptionList('SELECT planetID, planetName FROM tPlanet ORDER BY planetName;')
	return listStr

def getProfessionList():
	listStr = getOptionList('SELECT profID, profName FROM tProfession ORDER BY profName;')
	return listStr

def getObjectTypeList():
	listStr = getOptionList('SELECT objectType, typeName, craftingTab FROM tObjectType ORDER BY typeName;')
	return listStr


