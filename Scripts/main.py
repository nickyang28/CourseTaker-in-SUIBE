# -*- coding:utf-8 -*-
import warnings

warnings.filterwarnings('ignore')
import wx
import global_variable as gb_v
import guiManager as FrameManager

locale = wx.Locale.GetSystemLanguage()


class MainAPP(wx.App):
    def OnInit(self):
        self.manager = FrameManager.GuiManager(self.UpdateUI, self)
        self.locale = wx.Locale(locale)
        self.frame = self.manager.GetFrame(0)
        self.frame.Show()
        return True

    def UpdateUI(self, type):
        self.frame.Destroy()
        self.frame = self.manager.GetFrame(type)
        self.frame.Show()


def main():
    app = MainAPP()
    app.MainLoop()


if __name__ == '__main__':
    main()
    if gb_v.DRIVER is not None:
        gb_v.DRIVER.close()
        gb_v.DRIVER.quit()
