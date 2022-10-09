#interface.py
# Copyright (C) 2022 Beqa Gozalishvili <beqaprogger@gmail.com>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import addonHandler
import gui
import wx

from .const import *
from .donatedialog import requestDonations

addonHandler.initTranslation()


class CPUMonSettingsPanel(gui.SettingsPanel):
    title = addonSummary

    def makeSettings(self, sizer):
        sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=sizer)
        self.enableAddonChk = sHelper.addItem(wx.CheckBox(self, label=_("Enable addon")))
        self.enableAddonChk.SetValue(self.addonConf["enabled"])
        self.cpuThresholdSpin = sHelper.addLabeledControl(_("Minimum threshold for monitoring CPU load (in percents):"), gui.nvdaControls.SelectOnFocusSpinCtrl, min=5, max=100, initial=self.addonConf["cpuThreshold"])
        self.timeIntervalSpin = sHelper.addLabeledControl(_("Monitor update interval (in seconds):"), gui.nvdaControls.SelectOnFocusSpinCtrl, min=5, initial=self.addonConf["timeInterval"])
        self.beepFreqSpin = sHelper.addLabeledControl(_("Beep frequency for CPU load indication (in HZ):"), gui.nvdaControls.SelectOnFocusSpinCtrl, min=10, max=3000, initial=self.addonConf["beepFreq"])
        self.beepLenSpin = sHelper.addLabeledControl(_("Beep lenth for CPU load indication (in milliseconds):"), gui.nvdaControls.SelectOnFocusSpinCtrl, min=50, max=5000, initial=self.addonConf["beepLen"])
        self.beepVolSlider = sHelper.addLabeledControl(_("Beep volume for CPU load indication:"), gui.nvdaControls.EnhancedInputSlider, minValue=0, maxValue=100, value=self.addonConf["beepVol"])
        self.donateBtn = sHelper.addItem(wx.Button(self, label=_("Support an author with donation...")))
        self.donateBtn.Bind(wx.EVT_BUTTON, self.onDonate)

    def onDonate(self, evt):
        requestDonations(self)

    def onSave(self):
        enabled = self.enableAddonChk.GetValue()
        self.addonConf["enabled"] = enabled
        self.addonConf["cpuThreshold"] = self.cpuThresholdSpin.GetValue()
        self.addonConf["timeInterval"] = self.timeIntervalSpin.GetValue()
        self.addonConf["beepFreq"] = self.beepFreqSpin.GetValue()
        self.addonConf["beepLen"] = self.beepLenSpin.GetValue()
        self.addonConf["beepVol"] = self.beepVolSlider.GetValue()
        self.onSaveCallback(enabled)


def addSettingsPanel(configSection, onSaveCallback):
        CPUMonSettingsPanel.addonConf = configSection
        CPUMonSettingsPanel.onSaveCallback = onSaveCallback
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(CPUMonSettingsPanel)

def removeSettingsPanel():
	gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(CPUMonSettingsPanel)
