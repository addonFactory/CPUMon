#const.py
# Copyright (C) 2022 Beqa Gozalishvili <beqaprogger@gmail.com>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import addonHandler

confspec={
    "enabled": 'boolean(default=True)',
    "cpuThreshold": "integer(0,100,default=95)",
    "timeInterval": "integer(default=30)",
    "beepFreq": "integer(default=900)",
    "beepLen": "integer(default=100)",
    "beepVol": "integer(default=50)"
}

addon = addonHandler.getCodeAddon()
addonName = addon.name
addonSummary = addon.manifest["summary"]
