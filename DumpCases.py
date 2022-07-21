#!/usr/bin/python3

import os,sys
import json
import requests

apiToken = ""
fogBugzDomain = "redsweater.fogbugz.com"
startCase = 1
endCase = 50
casesToFetchPerRequest = 50

if apiToken == "" or fogBugzDomain == "redsweater.fogbugz.com":
	print("Error: You must edit the script to use your own API token and FogBugz domain.")
	sys.exit(1)
	
url = 'https://%s/f/api/0/jsonapi' % fogBugzDomain

def downloadCases(fromCase, toCase):
	searchString = "case:%s..%s" % (fromCase, toCase)

	allColumns = ["ixBug","ixBugParent","ixBugChildren","tags","fOpen","sTitle","sOriginalTitle","sLatestTextSummary","ixBugEventLatestText","ixProject","ixArea","ixPersonAssignedTo","sPersonAssignedTo","sEmailAssignedTo","ixPersonOpenedBy","ixPersonClosedBy","ixPersonResolvedBy","ixPersonLastEditedBy","ixStatus","ixBugDuplicates","ixBugOriginal","ixPriority","ixFixFor","sFixFor","dtFixFor","sVersion","sComputer","hrsOrigEst","hrsCurrEst","hrsElapsedExtra","hrsElapsed","c","sCustomerEmail","ixMailbox","ixCategory","dtOpened","dtResolved","dtClosed","ixBugEventLatest","dtLastUpdated","fReplied","fForwarded","sTicket","ixDiscussTopic","dtDue","sReleaseNotes","ixBugEventLastView","dtLastView","ixRelatedBugs","sScoutDescription","sScoutMessage","fScoutStopReporting","dtLastOccurrence","fSubscribed","dblStoryPts","nFixForOrder","events","minievents","ixKanbanColumn","sKanbanColumn", "plugin_customfields_at_fogcreek_com_notifyxwhenxfixedy41"]

	params = dict(
		token=apiToken,
		cmd='search',
		q=searchString,
		cols=allColumns
	)

	resp = requests.post(url=url, json=params)
	data = resp.json()

	# Dump each case result separately in the target dir
	dumpDir = "./Cases"
	if os.path.exists(dumpDir) is False: os.mkdir(dumpDir)

	caseArray = data['data']['cases']
	for caseData in caseArray:
		caseNumber = str(caseData["ixBug"])
		caseDir = os.path.join(dumpDir, caseNumber)
		if os.path.exists(caseDir) is False: os.mkdir(caseDir)
		
		caseDumpPath = os.path.join(caseDir, "data.json")
		caseDumpFile = open(caseDumpPath, "w")
		json.dump(caseData, caseDumpFile)
		caseDumpFile.close()
		print("Wrote %s" % caseDumpPath)
		
# Download cases in batches based on casesToFetchPerRequest
currentStartCase = startCase
while currentStartCase <= endCase:
	caseCount = casesToFetchPerRequest
	currentEndCase = currentStartCase + casesToFetchPerRequest
	if currentEndCase > endCase: currentEndCase = endCase
	
	downloadCases(currentStartCase, currentEndCase)
	currentStartCase = currentEndCase + 1
