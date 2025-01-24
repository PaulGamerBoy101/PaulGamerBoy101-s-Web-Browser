import wx
import wx.html2


class Browser(wx.Frame):
    def __init__(self):
        super().__init__(None, title="PaulGamerBoy101's Web Browser", size=(1200, 800))

        # Main panel
        self.panel = wx.Panel(self)

        # Layouts
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        nav_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Back Button
        self.back_btn = wx.Button(self.panel, label="🢀")
        self.back_btn.Bind(wx.EVT_BUTTON, self.on_back)
        nav_sizer.Add(self.back_btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Forward Button
        self.forward_btn = wx.Button(self.panel, label="🢂")
        self.forward_btn.Bind(wx.EVT_BUTTON, self.on_forward)
        nav_sizer.Add(self.forward_btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Refresh Button
        self.refresh_btn = wx.Button(self.panel, label="🗘")
        self.refresh_btn.Bind(wx.EVT_BUTTON, self.on_refresh)
        nav_sizer.Add(self.refresh_btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Home Button
        self.home_btn = wx.Button(self.panel, label="⌂")
        self.home_btn.Bind(wx.EVT_BUTTON, self.on_home)
        nav_sizer.Add(self.home_btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # URL Bar
        self.url_bar = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.url_bar.Bind(wx.EVT_TEXT_ENTER, self.on_url_enter)
        nav_sizer.Add(self.url_bar, 1, wx.ALL | wx.EXPAND, 5)

        # Add navigation bar to main layout
        main_sizer.Add(nav_sizer, 0, wx.EXPAND)

        # Web view
        self.browser = wx.html2.WebView.New(self.panel)
        self.browser.Bind(wx.html2.EVT_WEBVIEW_NAVIGATING, self.on_navigating)
        self.browser.Bind(wx.html2.EVT_WEBVIEW_LOADED, self.on_loaded)
        main_sizer.Add(self.browser, 1, wx.EXPAND)

        # Set the initial homepage
        self.browser.LoadURL("https://custom-new-tab-page-12935782.codehs.me/")

        # Finalize layout
        self.panel.SetSizer(main_sizer)
        self.Show()

    def on_back(self, event):
        if self.browser.CanGoBack():
            self.browser.GoBack()

    def on_forward(self, event):
        if self.browser.CanGoForward():
            self.browser.GoForward()

    def on_refresh(self, event):
        self.browser.Reload()

    def on_home(self, event):
        self.browser.LoadURL("https://custom-new-tab-page-12935782.codehs.me/")

    def on_url_enter(self, event):
        url = self.url_bar.GetValue()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        self.browser.LoadURL(url)

    def on_navigating(self, event):
        url = event.GetURL()
        self.url_bar.SetValue(url)

    def on_loaded(self, event):
        self.SetTitle(self.browser.GetCurrentTitle())


if __name__ == "__main__":
    app = wx.App(False)
    frame = Browser()
    app.MainLoop()
