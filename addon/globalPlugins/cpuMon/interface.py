#interface.py
# Copyright (C) 2022 Beqa Gozalishvili <beqaprogger@gmail.com>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import addonHandler
import gui
from gui.settingsDialogs import SettingsPanel
import wx

from .const import *

addonHandler.initTranslation()


class CPUMonSettingsPanel(SettingsPanel):
    title = addonSummary

    def makeSettings(self, sizer):
        sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=sizer)
        self.enableAddonChk = sHelper.addItem(wx.CheckBox(self, label=_("Enable addon")))
        self.enableAddonChk.SetValue(self.addonConf["enabled"])
        self.cpuThresholdSpin = sHelper.addLabeledControl(_("CPU load threshold (in percents):"), gui.nvdaControls.SelectOnFocusSpinCtrl, min=5, max=100, initial=self.addonConf["cpuThreshold"])
        self.timeIntervalSpin = sHelper.addLabeledControl(_("Measuring interval (in seconds):"), gui.nvdaControls.SelectOnFocusSpinCtrl, min=5, initial=self.addonConf["timeInterval"])
        beepGroupSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=_("CPU load notification beep options"))
        beepGroupBox = beepGroupSizer.GetStaticBox()
        beepGroup = gui.guiHelper.BoxSizerHelper(self, sizer=beepGroupSizer)
        sHelper.addItem(beepGroup)
        self.beepFreqSpin = beepGroup.addLabeledControl(_("Frequency (in HZ):"), gui.nvdaControls.SelectOnFocusSpinCtrl, min=10, max=3000, initial=self.addonConf["beepFreq"])
        self.beepLenSpin = beepGroup.addLabeledControl(_("Length (in milliseconds):"), gui.nvdaControls.SelectOnFocusSpinCtrl, min=10, max=5000, initial=self.addonConf["beepLen"])
        self.beepVolSlider = beepGroup.addLabeledControl(_("Volume:"), gui.nvdaControls.EnhancedInputSlider, minValue=0, maxValue=100, value=self.addonConf["beepVol"])
        self.donateBtn = sHelper.addItem(wx.Button(self, label=_("Support an author...")))
        self.donateBtn.Bind(wx.EVT_BUTTON, self.onDonate)

    def onDonate(self, evt):
        from .donate_dialog import requestDonations
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
