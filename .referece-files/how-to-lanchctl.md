launchctl load: Registers the job to run at the scheduled time
launchctl start: Runs the job now, once
launchctl unload: Unregisters the job (stops future scheduled runs)

launchctl load ~/Library/LaunchAgents/com.ianchang.shadowmorning.plist
launchctl load ~/Library/LaunchAgents/com.ianchang.shadownight.plist

launchctl start com.ianchang.shadownight
launchctl start com.ianchang.shadowmorning