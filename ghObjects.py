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

import ghShared

class resourceStats:
	def __init__(self):
		self.CR = 0
		self.CD = 0
		self.DR = 0
		self.FL = 0
		self.HR = 0
		self.MA = 0
		self.PE = 0
		self.OQ = 0
		self.SR = 0
		self.UT = 0
		self.ER = 0

class resourcePlanet:
	def __init__(self, planetID=0, planetName="", enteredBy=""):
		self.planetID = planetID
		self.planetName = planetName
		self.enteredBy = enteredBy

class resourceSpawn:
	def __init__(self):
		self.spawnID = 0
		self.spawnName = ""
		self.spawnGalaxy = 0
		self.resourceType = ""
		self.resourceTypeName = ""
		self.containerType = ""
		self.favorite = 0
		self.favGroup = ""
		self.units = 0
		self.inventoryType = ""
		self.groupName = ""
		self.groupList = ""
		self.stats = resourceStats()
		self.percentStats = resourceStats()
		self.overallScore = 0

		self.entered = None
		self.enteredBy = ""
		self.verified = None
		self.verifiedBy = ""
		self.unavailable = None
		self.unavailableBy = ""
		self.planets = []

		self.maxWaypointConc = None

	def getPlanetBar(self):
		result = '<ul class="planetBar">'
		criteriaStr = ''

		for planet in self.planets:
			result = result + '    <li class="planetBarBox'
			if (planet.enteredBy != None):
				result = result + ' ' + planet.planetName.replace(' ','')
				result +='"'
			if (planet.enteredBy != None):
				result = result + ' title="'+planet.planetName+' marked available by '+planet.enteredBy+'"'
				result = result + ' onclick="planetRemove(this,'+str(planet.planetID)+','+str(self.spawnID)+',\''+planet.planetName+'\');"'
			else:
				result = result + ' title="'+planet.planetName+' - not available"'
				result = result + ' onclick="planetAdd(this,'+str(planet.planetID)+','+str(self.spawnID)+',\''+planet.planetName+'\');"'
			result = result + '>'+planet.planetName[0]+'</li>'

		result += '</ul>'
		return result

	def getHTML(self, editable, formatStyle, resBoxMargin):
		result = ''
		unPlanetStr = ",'all'"
		statHeads = ""
		statVals = ""
		titleStr = ""

		# style 0 is wide format
		if formatStyle == 0:
			resBoxStyle = "margin-left:" + resBoxMargin + ";min-width:500px;"
		# style 2 is survey tool format
		elif formatStyle == 2:
			resBoxStyle = "padding-left:" + resBoxMargin + ";"
		else:
			# other is compact style
			resBoxStyle = ""

		# prepare stat value table contents
		if (self.percentStats.ER != None or formatStyle == 0):
			statHeads = statHeads + "<td class='header'><span>ER</span></td>"
			if (self.stats.ER != None and self.percentStats.ER != None):
				statVals = statVals + "<td class='"+ghShared.percOfRangeColor(self.percentStats.ER)+"'><span>" + str(self.stats.ER) + "<br />(" + ("%.0f" % float(self.percentStats.ER)) + "%)</span></td>"
			elif (self.percentStats.ER != None):
				statVals = statVals + "<td>?</td>"
			else:
				statVals = statVals + "<td></td>"
		
		if (self.percentStats.CR != None or formatStyle == 0):
			statHeads = statHeads + "<td class='header'><span>CR</span></td>"
			if (self.stats.CR != None and self.percentStats.CR != None):
				statVals = statVals + "<td class='"+ghShared.percOfRangeColor(self.percentStats.CR)+"'><span>" + str(self.stats.CR) + "<br />(" + ("%.0f" % float(self.percentStats.CR)) + "%)</span></td>"
			elif (self.percentStats.CR != None):
				statVals = statVals + "<td>?</td>"
			else:
				statVals = statVals + "<td></td>"

		if (self.percentStats.CD != None or formatStyle == 0):
			statHeads = statHeads + "<td class='header'><span>CD</span></td>"
			if (self.stats.CD != None and self.percentStats.CD != None):
				statVals = statVals + "<td class='"+ghShared.percOfRangeColor(self.percentStats.CD)+"'><span>" + str(self.stats.CD) + "<br />(" + ("%.0f" % float(self.percentStats.CD)) + "%)</span></td>"
			elif (self.percentStats.CD != None):
				statVals = statVals + "<td>?</td>"
			else:
				statVals = statVals + "<td></td>"

		if (self.percentStats.DR != None or formatStyle == 0):
			statHeads = statHeads + "<td class='header'><span>DR</span></td>"
			if (self.stats.DR != None and self.percentStats.DR != None):
				statVals = statVals + "<td class='"+ghShared.percOfRangeColor(self.percentStats.DR)+"'><span>" + str(self.stats.DR) + "<br />(" + ("%.0f" % float(self.percentStats.DR)) + "%)</span></td>"
			elif (self.percentStats.DR != None):
				statVals = statVals + "<td>?</td>"
			else:
				statVals = statVals + "<td></td>"

		if (self.percentStats.FL != None or formatStyle == 0):
			statHeads = statHeads + "<td class='header'><span>FL</span></td>"
			if (self.stats.FL != None and self.percentStats.FL != None):
				statVals = statVals + "<td class='"+ghShared.percOfRangeColor(self.percentStats.FL)+"'><span>" + str(self.stats.FL) + "<br />(" + ("%.0f" % float(self.percentStats.FL)) + "%)</span></td>"
			elif (self.percentStats.FL != None):
				statVals = statVals + "<td>?</td>"
			else:
				statVals = statVals + "<td></td>"

		if (self.percentStats.HR != None or formatStyle == 0):
			statHeads = statHeads + "<td class='header'><span>HR</span></td>"
			if (self.stats.HR != None and self.percentStats.HR != None):
				statVals = statVals + "<td class='"+ghShared.percOfRangeColor(self.percentStats.HR)+"'><span>" + str(self.stats.HR) + "<br />(" + ("%.0f" % float(self.percentStats.HR)) + "%)</span></td>"
			elif (self.percentStats.HR != None):
				statVals = statVals + "<td>?</td>"
			else:
				statVals = statVals + "<td></td>"

		if (self.percentStats.MA != None or formatStyle == 0):
			statHeads = statHeads + "<td class='header'><span>MA</span></td>"
			if (self.stats.MA != None and self.percentStats.MA != None):
				statVals = statVals + "<td class='"+ghShared.percOfRangeColor(self.percentStats.MA)+"'><span>" + str(self.stats.MA) + "<br />(" + ("%.0f" % float(self.percentStats.MA)) + "%)</span></td>"
			elif (self.percentStats.MA != None):
				statVals = statVals + "<td>?</td>"
			else:
				statVals = statVals + "<td></td>"

		if (self.percentStats.PE != None or formatStyle == 0):
			statHeads = statHeads + "<td class='header'><span>PE</span></td>"
			if (self.stats.PE != None and self.percentStats.PE != None):
				statVals = statVals + "<td class='"+ghShared.percOfRangeColor(self.percentStats.PE)+"'><span>" + str(self.stats.PE) + "<br />(" + ("%.0f" % float(self.percentStats.PE)) + "%)</span></td>"
			elif (self.percentStats.PE != None):
				statVals = statVals + "<td>?</td>"
			else:
				statVals = statVals + "<td></td>"

		if (self.percentStats.OQ != None or formatStyle == 0):
			statHeads = statHeads + "<td class='header'><span>OQ</span></td>"
			if (self.stats.OQ != None and self.percentStats.OQ != None):
				statVals = statVals + "<td class='"+ghShared.percOfRangeColor(self.percentStats.OQ)+"'><span>" + str(self.stats.OQ) + "<br />(" + ("%.0f" % float(self.percentStats.OQ)) + "%)</span></td>"
			elif (self.percentStats.OQ != None):
				statVals = statVals + "<td>?</td>"
			else:
				statVals = statVals + "<td></td>"

		if (self.percentStats.SR != None or formatStyle == 0):
			statHeads = statHeads + "<td class='header'><span>SR</span></td>"
			if (self.stats.SR != None and self.percentStats.SR != None):
				statVals = statVals + "<td class='"+ghShared.percOfRangeColor(self.percentStats.SR)+"'><span>" + str(self.stats.SR) + "<br />(" + ("%.0f" % float(self.percentStats.SR)) + "%)</span></td>"
			elif (self.percentStats.SR != None):
				statVals = statVals + "<td>?</td>"
			else:
				statVals = statVals + "<td></td>"

		if (self.percentStats.UT != None or formatStyle == 0):
			statHeads = statHeads + "<td class='header'><span>UT</span></td>"
			if (self.stats.UT != None and self.percentStats.UT != None):
				statVals = statVals + "<td class='"+ghShared.percOfRangeColor(self.percentStats.UT)+"'><span>" + str(self.stats.UT) + "<br />(" + ("%.0f" % float(self.percentStats.UT)) + "%)</span></td>"
			elif (self.percentStats.UT != None):
				statVals = statVals + "<td>?</td>"
			else:
				statVals = statVals + "<td></td>"

		# construct resource container
		if self.overallScore != None and self.overallScore > 0:
			titleStr = ' title="' + str("%.0f" % (float(self.overallScore))) + '"'
		if formatStyle == 2:
			result += '  <div id="cont_'+self.spawnName+'" class="boxBorderHidden" style="' + resBoxStyle + '"' + titleStr + ' onmouseover="$(this).removeClass(\'boxBorderHidden\');$(this).addClass(\'listSelected\');" onmouseout="$(this).removeClass(\'listSelected\');$(this).addClass(\'boxBorderHidden\');">'
		else:
			result += '  <div id="cont_'+self.spawnName+'" class="resourceBox" style="' + resBoxStyle + '"' + titleStr + '>'
		if self.overallScore != None and self.overallScore > 0:
			result += '  <div class="compareInfo"><span>Quality: ' + str("%.0f" % (float(self.overallScore))) + '</span></div>'
		
		# resource title row
		if formatStyle == 0:
			result += '  <div style="text-align:left;"><div class="inlineBlock" style="width:55%;text-align:left;float:left;"><span style="font-size: 12px;font-weight: bold;"><a href="' + ghShared.BASE_SCRIPT_URL + 'resource.py/'+str(self.spawnGalaxy)+'/'+self.spawnName+'" class="nameLink">'+self.spawnName+'</a></span>'
		elif formatStyle == 2:
			result += '    <div style="margin-bottom:4px;text-align:left;"><span style="font-size: 12px;"><a href="' + ghShared.BASE_SCRIPT_URL + 'resource.py/'+str(self.spawnGalaxy)+'/'+self.spawnName+'" class="nameLink">'+self.spawnName+'</a></span>'
		else:
			result += '    <div style="margin-bottom:4px;text-align:left;"><span style="font-size: 12px;font-weight: bold;"><a href="' + ghShared.BASE_SCRIPT_URL + 'resource.py/'+str(self.spawnGalaxy)+'/'+self.spawnName+'" class="nameLink">'+self.spawnName+'</a></span>'
		if (editable > 0):
			if formatStyle != 2:
				result += '  <a alt="Edit Stats" style="cursor: pointer;" onclick="editStats(this, \''+self.spawnName+'\');">[Edit]</a>'
			if formatStyle != 1:
				if formatStyle == 2:
					result += '  <div style="width:100px;float:right;"><input type="checkbox" id="chkRemove_' + self.spawnName + '" />Remove</div>'
				else:
					result += '  <a alt="Mark Unavailable" style="cursor: pointer;" onclick="markUnavailable(this, \''+self.spawnName+'\', '+str(self.spawnGalaxy)+unPlanetStr+');"> [X]</a>'

		# non-stat info
		if formatStyle == 0:
			result += '  <span style="color:#000033;"><a href="' + ghShared.BASE_SCRIPT_URL + 'resourceType.py/'+self.resourceType+'" title="View recent spawns of this type" class="nameLink">'+self.resourceTypeName+'</a></span></div>'
			result += '  <div class="inlineBlock" style="margin-top:2px;margin-right:4px;width:44%;text-align:right;float:right;">'+self.getPlanetBar()+'</div>'
			result += '  </div><div><div style="height:32px;float:left;"><img src="/images/resources/'+self.containerType+'.png"/></div>'
		elif formatStyle == 1:
			result += '&nbsp;'+ghShared.timeAgo(self.entered)+' ago by <a href="user.py?uid='+self.enteredBy+'" class="nameLink">'+self.enteredBy+'</a>'
			result += '    </div>'
			result += '    <div>'
			result += '      <div style="height:32px;float:left;"><img src="/images/resources/'+self.containerType+'.png" /></div>'
			result += '      <div style="width:90px;float:left;"><a href="' + ghShared.BASE_SCRIPT_URL + 'resourceType.py/'+self.resourceType+'" title="View schematics and recent spawns of this type" class="nameLink">'+self.resourceTypeName+'</a></div>'
		else:
			result += ''
			
		# favorite indicator
		if editable > 0:
			if self.favorite > 0:
				result += '  <div class="inlineBlock" style="width:3%;float:left;"><a alt="Favorite" title="Favorite" style="cursor: pointer;" onclick="toggleFavorite(this, \''+str(self.spawnID)+'\');"><img src="/images/favorite16On.png" /></a></div>'
			else:
				result += '  <div class="inlineBlock" style="width:3%;float:left;"><a alt="Favorite" title="Favorite" style="cursor: pointer;" onclick="toggleFavorite(this, \''+str(self.spawnID)+'\');"><img src="/images/favorite16Off.png" /></a></div>'

		# stats information table
		if formatStyle == 0:
			result += '  <div style="width:275px;float:left;">'
		elif formatStyle == 1:
			result += '  <div style="float:left;">'
		else:
			result += ''

		if formatStyle != 2:
			result += '  <table class="resAttr"><tr>' + statHeads + '</tr><tr>' + statVals + '</tr>'
			result += '  </table></div></div>'

			if formatStyle == 0:
				# resource update information

				result += '  <div style="clear:both;">'
				# add waypoints indicator
				if self.maxWaypointConc != None:
					result += '<div style="float:right;"><a href="' + ghShared.BASE_SCRIPT_URL + 'resource.py/'+str(self.spawnGalaxy)+'/'+self.spawnName+'"><img src="/images/waypointMarker.png" alt="waypoint marker" title="waypoint(s) available (best is ' + str(self.maxWaypointConc) + '%)" width="20" /></a></div>'
				# entered
				result += '  <div class="inlineBlock" style="width:33%;float:right;"><img src="/images/circleBlue16.png" alt="Entered" title="Entered" /><span style="vertical-align:4px;">' + ghShared.timeAgo(self.entered)+' ago by <a href="/user.py?uid='+self.enteredBy+'">'+self.enteredBy+'</a></span></div>'
				# verified
				result += '  <div class="inlineBlock" style="width:33%;float:right;">'
				if (self.verified != None):
					result += '  <img src="/images/checkGreen16.png" alt="Verified" title="Verified" /><span style="vertical-align:4px;">' + ghShared.timeAgo(self.verified) + ' ago by <a href="/user.py?uid='+self.verifiedBy+'">'+self.verifiedBy+'</a></span>'
				else:
					if (self.unavailable == None and editable > 0):
						result += '  <span id="cont_verify_'+self.spawnName+'"><img src="/images/checkGrey16.png" alt="Not Verified" title="Not Verified" /><span style="vertical-align:4px;"><a alt="Verify Resource" style="cursor: pointer;" onclick="quickAdd(null, \''+self.spawnName+'\');">[Verify]</a></span></span>'
				# unavailable
				result += '  </div><div class="inlineBlock" style="width:32%;float:right;">'
				if (self.unavailable != None):
					result += '  <img src="/images/xRed16.png" alt="Unavailable" title="Unavailable" /><span style="vertical-align:4px;">' + ghShared.timeAgo(self.unavailable) + ' ago by <a href="/user.py?uid='+self.unavailableBy+'">'+self.unavailableBy+'</a></span>'
				result += '  </div>'
			else:
				result += '    <div style="width: 180px;clear:both;margin-left:64px;">'+self.getPlanetBar()+'</div>'

		else:
			if (self.unavailable == None and editable > 0 and ghShared.timeAgo(self.verified).find('minute') == -1):
				result += '  <div id="cont_verify_'+self.spawnName+'" style="width:100px;float:right;"><input type="checkbox" id="chkVerify_' + self.spawnName + '" />Verify</div>'
				
		result += '  </div>'
		return result

	def getMobileHTML(self, editable):
		result = ''
		statHeads = ""
		statVals = ""
		titleStr = ""

		# prepare stat value table contents
		if (self.stats.ER != None and self.percentStats.ER != None):
			statVals = statVals + "<span class='"+ghShared.percOfRangeColor(self.percentStats.ER)+"'> ER: " + str(self.stats.ER) + "(" + ("%.0f" % float(self.percentStats.ER)) + "%)</span>"
		
		if (self.stats.CR != None and self.percentStats.CR != None):
			statVals = statVals + "<span class='"+ghShared.percOfRangeColor(self.percentStats.CR)+"'> CR: " + str(self.stats.CR) + "(" + ("%.0f" % float(self.percentStats.CR)) + "%)</span>"

		if (self.stats.CD != None and self.percentStats.CD != None):
			statVals = statVals + "<span class='"+ghShared.percOfRangeColor(self.percentStats.CD)+"'> CD: " + str(self.stats.CD) + "(" + ("%.0f" % float(self.percentStats.CD)) + "%)</span>"

		if (self.stats.DR != None and self.percentStats.DR != None):
			statVals = statVals + "<span class='"+ghShared.percOfRangeColor(self.percentStats.DR)+"'> DR: " + str(self.stats.DR) + "(" + ("%.0f" % float(self.percentStats.DR)) + "%)</span>"

		if (self.stats.FL != None and self.percentStats.FL != None):
			statVals = statVals + "<span class='"+ghShared.percOfRangeColor(self.percentStats.FL)+"'> FL: " + str(self.stats.FL) + "(" + ("%.0f" % float(self.percentStats.FL)) + "%)</span>"

		if (self.stats.HR != None and self.percentStats.HR != None):
			statVals = statVals + "<span class='"+ghShared.percOfRangeColor(self.percentStats.HR)+"'> HR: " + str(self.stats.HR) + "(" + ("%.0f" % float(self.percentStats.HR)) + "%)</span>"

		if (self.stats.MA != None and self.percentStats.MA != None):
			statVals = statVals + "<span class='"+ghShared.percOfRangeColor(self.percentStats.MA)+"'> MA: " + str(self.stats.MA) + "(" + ("%.0f" % float(self.percentStats.MA)) + "%)</span>"

		if (self.stats.PE != None and self.percentStats.PE != None):
			statVals = statVals + "<span class='"+ghShared.percOfRangeColor(self.percentStats.PE)+"'> PE: " + str(self.stats.PE) + "(" + ("%.0f" % float(self.percentStats.PE)) + "%)</span>"

		if (self.stats.OQ != None and self.percentStats.OQ != None):
			statVals = statVals + "<span class='"+ghShared.percOfRangeColor(self.percentStats.OQ)+"'> OQ: " + str(self.stats.OQ) + "(" + ("%.0f" % float(self.percentStats.OQ)) + "%)</span>"

		if (self.stats.SR != None and self.percentStats.SR != None):
			statVals = statVals + "<span class='"+ghShared.percOfRangeColor(self.percentStats.SR)+"'> SR: " + str(self.stats.SR) + "(" + ("%.0f" % float(self.percentStats.SR)) + "%)</span>"

		if (self.stats.UT != None and self.percentStats.UT != None):
			statVals = statVals + "<span class='"+ghShared.percOfRangeColor(self.percentStats.UT)+"'>" + str(self.stats.UT) + "(" + ("%.0f" % float(self.percentStats.UT)) + "%)</span>"

		# construct resource container
		if self.overallScore != None and self.overallScore > 0:
			titleStr = ' title="' + str("%.0f" % (float(self.overallScore))) + '"'
		result += '  <a href="' + ghShared.BASE_SCRIPT_URL + 'resource.py/'+str(self.spawnGalaxy)+'/'+self.spawnName+'" class="nameLink">'
		result += '  <div id="cont_'+self.spawnName+'" class="control"' + titleStr + ' style="text-align:left;">'

		# resource title row
		result += '    <div style="margin-bottom:4px;">'
		result += '    '+self.resourceTypeName+' ('+self.spawnName + ')'

		# non-stat info
		result += '&nbsp;entered&nbsp;'+ghShared.timeAgo(self.entered)+' ago by '+self.enteredBy
		if (editable > 0):
			result += '  <span title="Mark Unavailable" style="cursor: pointer;float:right;" onclick="markUnavailable(this, \''+self.spawnName+'\', '+str(self.spawnGalaxy)+',\'all\');"> [X]</span>'
		result += '    </div>'

		# stats information
		result += '  <div>'
		result += statVals
		result += '  </div></div></a>'
		return result

	def getRow(self, editable):
		result = ''
		statVals = ""
		titleStr = ""

		result += '<tr id="cont_'+self.spawnName+'" name="cont_'+self.spawnName+'" class="statRow ui-draggable">'

		# favorite indicator
		if editable > 0:
			if self.favorite > 0:
				result += '  <td class="dragColumn" style="width:20px;"><a alt="Favorite" title="Favorite" style="cursor: pointer;" onclick="toggleFavorite(this, \''+str(self.spawnID)+'\');"><img src="/images/favorite16On.png" /></a></td>'
			else:
				result += '  <td class="dragColumn" style="width:20px;"><a alt="Favorite" title="Favorite" style="cursor: pointer;" onclick="toggleFavorite(this, \''+str(self.spawnID)+'\');"><img src="/images/favorite16Off.png" /></a></td>'

		# resource title row
		if self.unavailable != None:
			styleAdd = "background-image:url(/images/xRed16.png);background-repeat:no-repeat;background-position:2px 2px;"
		elif self.verified != None:
			styleAdd = "background-image:url(/images/checkGreen16.png);background-repeat:no-repeat;background-position:2px 2px;"
		else:
			styleAdd = "background-image:url(/images/circleBlue16.png);background-repeat:no-repeat;background-position:2px 2px;"

		result += '    <td class="dragColumn" style="width:90px;' + styleAdd + '"><span style="font-size: 12px;font-weight: bold;"><a href="' + ghShared.BASE_SCRIPT_URL + 'resource.py/'+str(self.spawnGalaxy)+'/'+self.spawnName+'" class="nameLink">'+self.spawnName+'</a></td>'

		result += '  <td class="dragColumn" style="width:160px"><a href="' + ghShared.BASE_SCRIPT_URL + 'resourceType.py/'+self.resourceType+'" title="View recent spawns of this type" class="nameLink">'+self.resourceTypeName+'</a></td>'

		# prepare stat value table contents
		if (self.stats.ER != None and self.percentStats.ER != None):
			statVals = statVals + "<td style='width:30px;' class='"+ghShared.percOfRangeColor(self.percentStats.ER)+"'><span title='(" + ("%.0f" % float(self.percentStats.ER)) + "%)'>" + str(self.stats.ER) + "</span></td>"
		elif (self.percentStats.ER != None):
			statVals = statVals + "<td style='width:30px;'>?</td>"
		else:
			statVals = statVals + "<td style='width:30px;'></td>"
		
		if (self.stats.CR != None and self.percentStats.CR != None):
			statVals = statVals + "<td style='width:30px;' class='"+ghShared.percOfRangeColor(self.percentStats.CR)+"'><span title='(" + ("%.0f" % float(self.percentStats.CR)) + "%)'>" + str(self.stats.CR) + "</span></td>"
		elif (self.percentStats.CR != None):
			statVals = statVals + "<td style='width:30px;'>?</td>"
		else:
			statVals = statVals + "<td style='width:30px;'></td>"

		if (self.stats.CD != None and self.percentStats.CD != None):
			statVals = statVals + "<td style='width:30px;' class='"+ghShared.percOfRangeColor(self.percentStats.CD)+"'><span title='(" + ("%.0f" % float(self.percentStats.CD)) + "%)'>" + str(self.stats.CD) + "</span></td>"
		elif (self.percentStats.CD != None):
			statVals = statVals + "<td style='width:30px;'>?</td>"
		else:
			statVals = statVals + "<td style='width:30px;'></td>"

		if (self.stats.DR != None and self.percentStats.DR != None):
			statVals = statVals + "<td style='width:30px;' class='"+ghShared.percOfRangeColor(self.percentStats.DR)+"'><span title='(" + ("%.0f" % float(self.percentStats.DR)) + "%)'>" + str(self.stats.DR) + "</span></td>"
		elif (self.percentStats.DR != None):
			statVals = statVals + "<td style='width:30px;'>?</td>"
		else:
			statVals = statVals + "<td style='width:30px;'></td>"

		if (self.stats.FL != None and self.percentStats.FL != None):
			statVals = statVals + "<td style='width:30px;' class='"+ghShared.percOfRangeColor(self.percentStats.FL)+"'><span title='(" + ("%.0f" % float(self.percentStats.FL)) + "%)'>" + str(self.stats.FL) + "</span></td>"
		elif (self.percentStats.FL != None):
			statVals = statVals + "<td style='width:30px;'>?</td>"
		else:
			statVals = statVals + "<td style='width:30px;'></td>"

		if (self.stats.HR != None and self.percentStats.HR != None):
			statVals = statVals + "<td style='width:30px;' class='"+ghShared.percOfRangeColor(self.percentStats.HR)+"'><span title='(" + ("%.0f" % float(self.percentStats.HR)) + "%)'>" + str(self.stats.HR) + "</span></td>"
		elif (self.percentStats.HR != None):
			statVals = statVals + "<td style='width:30px;'>?</td>"
		else:
			statVals = statVals + "<td style='width:30px;'></td>"

		if (self.stats.MA != None and self.percentStats.MA != None):
			statVals = statVals + "<td style='width:30px;' class='"+ghShared.percOfRangeColor(self.percentStats.MA)+"'><span title='(" + ("%.0f" % float(self.percentStats.MA)) + "%)'>" + str(self.stats.MA) + "</span></td>"
		elif (self.percentStats.MA != None):
			statVals = statVals + "<td style='width:30px;'>?</td>"
		else:
			statVals = statVals + "<td style='width:30px;'></td>"

		if (self.stats.PE != None and self.percentStats.PE != None):
			statVals = statVals + "<td style='width:30px;' class='"+ghShared.percOfRangeColor(self.percentStats.PE)+"'><span title='(" + ("%.0f" % float(self.percentStats.PE)) + "%)'>" + str(self.stats.PE) + "</span></td>"
		elif (self.percentStats.PE != None):
			statVals = statVals + "<td style='width:30px;'>?</td>"
		else:
			statVals = statVals + "<td style='width:30px;'></td>"

		if (self.stats.OQ != None and self.percentStats.OQ != None):
			statVals = statVals + "<td style='width:30px;' class='"+ghShared.percOfRangeColor(self.percentStats.OQ)+"'><span title='(" + ("%.0f" % float(self.percentStats.OQ)) + "%)'>" + str(self.stats.OQ) + "</span></td>"
		elif (self.percentStats.OQ != None):
			statVals = statVals + "<td style='width:30px;'>?</td>"
		else:
			statVals = statVals + "<td style='width:30px;'></td>"

		if (self.stats.SR != None and self.percentStats.SR != None):
			statVals = statVals + "<td style='width:30px;' class='"+ghShared.percOfRangeColor(self.percentStats.SR)+"'><span title='(" + ("%.0f" % float(self.percentStats.SR)) + "%)'>" + str(self.stats.SR) + "</span></td>"
		elif (self.percentStats.SR != None):
			statVals = statVals + "<td style='width:30px;'>?</td>"
		else:
			statVals = statVals + "<td style='width:30px;'></td>"

		if (self.stats.UT != None and self.percentStats.UT != None):
			statVals = statVals + "<td style='width:30px;' class='"+ghShared.percOfRangeColor(self.percentStats.UT)+"'><span title='(" + ("%.0f" % float(self.percentStats.UT)) + "%)'>" + str(self.stats.UT) + "</span></td>"
		elif (self.percentStats.UT != None):
			statVals = statVals + "<td style='width:30px;'>?</td>"
		else:
			statVals = statVals + "<td style='width:30px;'></td>"

		result += statVals
		result += "<td><input type='text' id='units_" + str(self.spawnID) + "' size='10' maxlength='13' tag='" + str(self.units) + "' value='" + str(self.units) + "' onblur='updateFavoriteAmount(this, \"" + str(self.spawnID) + "\",this.value);' onkeyup='if($(this).attr(\"tag\")==this.value){$(this).css(\"color\",\"black\");}else{$(this).css(\"color\",\"red\");}' /></td>"
		result += "<td style='width:20px'><input type='checkbox' id='chkMove_" + str(self.spawnID) + "' /></td>"

		return result
	
	def getStatList(self):
		statList = ""
		if self.stats.ER != None:
			statList += "<span class='altText'>Entangle Resistance:</span> " + str(self.stats.ER) + "<br />"
		if self.stats.CR != None:
			statList += "<span class='altText'>Cold Resistance:</span> " + str(self.stats.CR) + "<br />"
		if self.stats.CD != None:
			statList += "<span class='altText'>Conductivity:</span> " + str(self.stats.CD) + "<br />"
		if self.stats.DR != None:
			statList += "<span class='altText'>Decay Resistance:</span> " + str(self.stats.DR) + "<br />"
		if self.stats.FL != None:
			statList += "<span class='altText'>Flavor:</span> " + str(self.stats.FL) + "<br />"
		if self.stats.HR != None:
			statList += "<span class='altText'>Heat Resistance:</span> " + str(self.stats.HR) + "<br />"
		if self.stats.MA != None:
			statList += "<span class='altText'>Malleability:</span> " + str(self.stats.MA) + "<br />"
		if self.stats.PE != None:
			statList += "<span class='altText'>Potential Energy:</span> " + str(self.stats.PE) + "<br />"
		if self.stats.OQ != None:
			statList += "<span class='altText'>Overall Quality:</span> " + str(self.stats.OQ) + "<br />"
		if self.stats.SR != None:
			statList += "<span class='altText'>Shock Resistance:</span> " + str(self.stats.SR) + "<br />"
		if self.stats.UT != None:
			statList += "<span class='altText'>Unit Toughness:</span> " + str(self.stats.UT) + "<br />"
		return statList

	def getInventoryObject(self):
		# Return HTML of resource in inventory box
		result = "<div id='resInventory" + str(self.spawnName) + "' class='inventoryItem inlineBlock' style='background-image:url(/images/resources/inventory/inv_" + self.inventoryType + ".png);background-size:64px 64px;' tag='" + self.groupList + "," + self.resourceType + ",'>"
		result += "<div style='float:right;'>" + ghShared.getNumberAbbr(self.units) + "</div>"
		result += "<p style='display:none;'>Loaded with: " + self.spawnName + ", " + self.resourceTypeName + "<br />"
		result += self.getStatList()
		result += "</p>"
		result += "<div id='stackDetails" + str(self.spawnID) + "' style='display:none;' class='resourceDetails' tag='ER:" + str(self.stats.ER) + ",CR:" + str(self.stats.CR) + ",CD:" + str(self.stats.CD) + ",DR:" + str(self.stats.DR) + ",FL:" + str(self.stats.FL) + ",HR:" + str(self.stats.HR) + ",MA:" + str(self.stats.MA) + ",PE:" + str(self.stats.PE) + ",OQ:" + str(self.stats.OQ) + ",SR:" + str(self.stats.SR) + ",UT:" + str(self.stats.UT) + "'>"
		result += "  <div style='text-align:center;width:100%;margin-bottom:14px;'>" + self.groupName + "</div>"
		result += "  <span class='altText'>Resource Type:</span> " + self.spawnName + "<br />"
		result += "  <span class='altText'>Resource Quantity:</span> " + str(self.units) + "<br />"
		result += "  <span class='altText'>Resource Class:</span> " + self.resourceTypeName + "<br />"
		result += self.getStatList()		
		result += "</div>"
		result += "<div style='position: absolute;bottom:0;width:100%'>" + self.groupName + "</div>"
		result += "</div>"
		return result

