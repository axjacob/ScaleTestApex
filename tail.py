from pygtail import Pygtail
import sys
import logmonitor
pagename = {}
pyt = Pygtail("eptlog.log")
for line in pyt.readlines():
    ed = line.split(",")
    #clog.append(ed)
    if int(ed[9]) == 200:
        pagename['pagename__c'] = ed[6]
        pagename['ept__c'] = int(ed[7])
        pagename['status_code__c'] = int(ed[9])

    else:
        pagename[ed[6]] = "error"
 
if len(pagename.keys()) > 0:
    print(pagename)
    logmonitor.sendEvent(pagename)


