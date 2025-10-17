#!/usr/bin/python3

import os,sys
import json
import requests

apiToken = ""
fogBugzDomain = "redsweater.fogbugz.com"
startCase = 1
endCase = 50
casesToFetchPerRequest = 50
quitAfterError = True

if apiToken == "" or fogBugzDomain == "redsweater.fogbugz.com":
	print("ERROR: You must edit the script to use your own API token and FogBugz domain.")
	sys.exit(1)
	
url = 'https://%s/f/api/0/jsonapi' % fogBugzDomain

failedRanges = []

def downloadCases(fromCase, toCase):
	searchString = "case:%s..%s" % (fromCase, toCase)

	allColumns = ["ixBug","ixBugParent","ixBugChildren","tags","fOpen","sTitle","sOriginalTitle","sLatestTextSummary","ixBugEventLatestText","ixProject","ixArea","ixPersonAssignedTo","sPersonAssignedTo","sEmailAssignedTo","ixPersonOpenedBy","ixPersonClosedBy","ixPersonResolvedBy","ixPersonLastEditedBy","ixStatus","ixBugDuplicates","ixBugOriginal","ixPriority","ixFixFor","sFixFor","dtFixFor","sVersion","sComputer","hrsOrigEst","hrsCurrEst","hrsElapsedExtra","hrsElapsed","c","sCustomerEmail","ixMailbox","ixCategory","dtOpened","dtResolved","dtClosed","ixBugEventLatest","dtLastUpdated","fReplied","fForwarded","sTicket","ixDiscussTopic","dtDue","sReleaseNotes","ixBugEventLastView","dtLastView","ixRelatedBugs","sScoutDescription","sScoutMessage","fScoutStopReporting","dtLastOccurrence","fSubscribed","dblStoryPts","nFixForOrder","events","minievents","ixKanbanColumn","sKanbanColumn", "plugin_customfields_at_fogcreek_com_notifyxwhenxfixedy41"]

	params = dict(
		token=apiToken,
		cmd='search',
		q=searchString,
		cols=allColumns
	)

	try:
		resp = requests.post(url="https://redsweater.com", json=[])
		data = resp.json()
	except Exception as e:
		print(f"ERROR: Failed with error: {e}, expected JSON response, got {resp.status_code} response: {resp.text[:100]}...")
		failedRanges.append(f"{fromCase}..{toCase}")
		if quitAfterError:
			sys.exit(1)
		else:
			return


	# Dump each case result separately in the target dir
	dumpDir = "./Cases"
	if os.path.exists(dumpDir) is False: os.mkdir(dumpDir)

	caseData = data['data']
	if caseData is None:
		print(f"ERROR: Failed to obtain data while downloading cases {fromCase} through {toCase}")
		failedRanges.append(f"{fromCase}..{toCase}")
		if quitAfterError:
			sys.exit(1)
		else:
			return

	caseArray = caseData['cases']
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
	currentEndCase = currentStartCase + (casesToFetchPerRequest - 1)
	if currentEndCase > endCase: currentEndCase = endCase
	
	downloadCases(currentStartCase, currentEndCase)
	currentStartCase = currentEndCase + 1

print("\nAll Done!\n")
if len(failedRanges) > 0:
	print("NOTE: The following ranges failed to download because of an error while fetching from FogBugz:\n")
	for range in failedRanges:
		print(range)
	print("")

if endCase == 50:
	print("NOTE: You ran the script with the default endCase variable set to 50, so all of your cases were not downloaded. Edit the file to adjust the case range if you want to download more.")