# dumpbugz
Python scripts for downloading the case history and attachments from a FogBugz account

FogBugz used to support a purpose-built function for downloading an archive of database content from a FogBugz bug-tracking account. That feature is no longer available. Instead, users who want to download an archive either for safe-keeping, or to facilitate transitioning to another platform, must use either the FogBugz JSON or XML API to download the content.

These scripts facilitate a two-step dump, first by downloading the JSON data for each of the cases in your FogBugz account, and then by parsing the downloaded content, determining the list of attachments for each case, and then downloading and storing each attachment file alongside the case data.

To use the scripts:

1. Obtain a [FogBugz API key](https://support.fogbugz.com/hc/en-us/articles/360011330873-Create-API-Token-using-the-FogBugz-UI).
2. Edit the scripts to customize them for your needs:
	- Paste in your API key in place of "xxx" near the top of each script.
	- Change the fogBugzDomain from "redsweater.fogbugz.com" to your account/site's domain.
3. Install the python3 "requests" package by running: `pip3 install requests`
4. Run ./DumpCases.py to download JSON case data and store it in "./Cases"
5. Run ./DownloadAttachments.py to scan the downloaded JSON case data and download referenced attachments.

By default the scripts will only download cases between case 1 and 50. Edit the pertinent variables near the top of the scripts to expand the case range as you gain confidence that you are downloading what you expect.

Enjoy!
