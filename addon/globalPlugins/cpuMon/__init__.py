#__init__.py
# Copyright (C) 2022 Beqa Gozalishvili <beqaprogger@gmail.com>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import addonHandler
import config
import globalPluginHandler
import os
from . import psutil
import queueHandler
import threading
import time
import tones
import ui

from . import interface
from .const import *

addonHandler.initTranslation()

config.conf.spec[addonName]=confspec


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addonConf = config.conf[addonName]
        self.cpuThread = None
        self.thEvent = threading.Event()
        if self.addonConf["enabled"]:
            self.initialize()
        interface.addSettingsPanel(self.addonConf, self.onSave)

    def initialize(self, restart=False):
        if restart:
            self.tearDown()
        self.cpuThread = threading.Thread(target=self.cpuMonitor)
        self.thEvent.clear()
        self.cpuThread.start()

    def onSave(self, enabled):
        if not enabled:
            self.tearDown()
            return
        self.initialize(True)

    def tearDown(self):
        if self.cpuThread is not None:
            self.thEvent.set()
            self.cpuThread.join()
            self.cpuThread = None

    def terminate(self):
        super().terminate()
        self.tearDown()
        interface.removeSettingsPanel()

    def cpuMonitor(self):
        while not self.thEvent.is_set():
            wait = self.thEvent.wait(self.addonConf["timeInterval"])
            if wait:
                break
            cpuPercent = psutil.cpu_percent(0.1)
            if cpuPercent < self.addonConf["cpuThreshold"]:
                continue
            volume = self.addonConf["beepVol"]
            tones.beep(self.addonConf["beepFreq"], self.addonConf["beepLen"], left=volume, right=volume)
            processes = []
            pids = psutil.pids()[2:]
            for pid in pids:
                time.sleep(0.001)
                try:
                    proc = psutil.Process(pid)
                except psutil.NoSuchProcess:
                    continue
                proc.cpu_percent()
                processes.append(proc)
            time.sleep(0.1)
            try:
                pData = [(p.name(), p.cpu_percent()) for p in processes]
            except psutil.NoSuchProcess:
                continue
            pData = sorted(pData, key=lambda k: k[1])
            highest = round(pData[-1][1] / os.cpu_count(), 2)
            if highest == 0.0:
                continue
            queueHandler.queueFunction(queueHandler.eventQueue, ui.message, _("{processName} loaded CPU by {processLoadPercent}%").format(processName=pData[-1][0], processLoadPercent=highest))
