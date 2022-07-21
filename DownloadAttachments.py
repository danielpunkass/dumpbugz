#!/usr/bin/python3

import os,sys
import json
import requests
import shutil

apiToken = ""
fogBugzDomain = "redsweater.fogbugz.com"
startCase = 1
endCase = 50

if apiToken == "" or fogBugzDomain == "redsweater.fogbugz.com":
	print("Error: You must edit the script to use your own API token and FogBugz domain.")
	sys.exit(1)
	
def downloadAttachments(caseNumber):
	dumpDir = "./Cases"
	caseDir = os.path.join(dumpDir, str(caseNumber))
	
	# Load the JSON for each exported case, and look for items with attachments
	caseDumpPath = os.path.join(caseDir, "data.json")
	if os.path.exists(caseDumpPath) == False:
		print("NOTE: Case dump for case %s does not exist" % str(caseNumber))
		return
		
	caseDumpFile = open(caseDumpPath, "r")
	caseData = json.load(caseDumpFile)
	caseDumpFile.close()

	# Sanity check that the case number matches expectation
	if caseData['ixBug'] != caseNumber:
		print("ERROR: Found bug dump with wrong/missing bug number: %s" % caseNumber)
		
	# attachments are found on the individual events that correlate to the email
	# or edit in which they were attached, so we have to cruise events looking for non-empty
	# rgAttachments
	for event in caseData['events']:
		if 'rgAttachments' in event:
			attachments = event['rgAttachments']
			eventAttachmentIndex = 1
			for attachment in attachments:
				eventID = event['ixBugEvent']
				filename = attachment['sFileName']
				eventAttachmentsPath = os.path.join(caseDir, "%s-attachments" % eventID)
				if os.path.exists(eventAttachmentsPath) == False: os.mkdir(eventAttachmentsPath)

				# Get rid of the unnecessary "unsafe" ending for some files in FogBugz
				suffix = ".unsafe"
				if filename.endswith(suffix):
				   filename = filename[:-len(suffix)]
				
				# Replace slashes to avoid filename errors 
				filename = filename.replace("/", "-")
				
				# Save the file as the event ID with the path extension, if any, to ensure
				# uniqueness and avoid having a file name for example containing slashes 
				# which might not be legal
				(originalName, extension) = os.path.splitext(filename)
				filename = "%s-%s-%d%s" % (originalName, eventID, eventAttachmentIndex, extension)
				attachmentPath = os.path.join(eventAttachmentsPath, filename)
					
				if os.path.exists(attachmentPath):
					eventAttachmentIndex += 1
					continue
				
				attachmentFragment = attachment['sURL'].replace("&amp;", "&")
				attachmentURL = "https://%s/%s&token=%s" % (fogBugzDomain, attachmentFragment, apiToken)
				resp = requests.get(attachmentURL, stream=True)
				if resp.status_code != 200:
					print("ERROR: Failed to download attachment %s" % attachmentURL)
				
				with open(attachmentPath, "wb") as f:
					resp.raw.decode_content = True
					shutil.copyfileobj(resp.raw, f)	
					
				print("Wrote %s" % attachmentPath)
				eventAttachmentIndex += 1
		
for caseNumber in range(startCase, endCase+1):
	downloadAttachments(caseNumber)

print("\nAll Done!\n")

if endCase == 50:
	print("NOTE: You ran the script with the default endCase variable set to 50, so all of your cases were not downloaded. Edit the file to adjust the case range if you want to download more.")