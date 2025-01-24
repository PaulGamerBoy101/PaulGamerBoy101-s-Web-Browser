import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QVBoxLayout,
    QHBoxLayout, QWidget, QPushButton, QLineEdit, QTabWidget,
    QMenuBar, QAction, QLabel
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl, Qt


class AdBlocker:
    def __init__(self):
        self.blocked_domains = [
            "ads.example.com",
            "ads1.example.net",
            "doubleclick.net",
            "googlesyndication.com",
            "pagead2.googlesyndication.com",
            "adservice.google.com",
            "amazon-adsystem.com"
        ]

    def is_ad(self, url):
        for domain in self.blocked_domains:
            if domain in url:
                return True
        return False


class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None, popup_blocking_enabled=True, adblocking_enabled=True):
        super().__init__(parent)
        self.popup_blocking_enabled = popup_blocking_enabled
        self.adblocking_enabled = adblocking_enabled
        self.ad_blocker = AdBlocker()
        self.trusted_domains = []  # Domains always allowed
        self.blocked_domains = []  # Domains always blocked

def createWindow(self, _type):
    """Intercept popup creation."""
    request_url = self.requestedUrl().toString()
    domain = QUrl(request_url).host() if request_url else ""

    if not self.popup_blocking_enabled or domain in self.trusted_domains:
        new_view = QWebEngineView()
        new_page = CustomWebEnginePage(popup_blocking_enabled=self.popup_blocking_enabled, adblocking_enabled=self.adblocking_enabled)
        new_view.setPage(new_page)
        new_view.show()
        return new_page

    if domain in self.blocked_domains:
        return None

    msg = QMessageBox()
    msg.setWindowTitle("Popup Blocked")
    msg.setText(f"A popup was blocked from {domain}. What would you like to do?")
    trust_button = msg.addButton("Trust", QMessageBox.AcceptRole)
    deny_button = msg.addButton("Deny", QMessageBox.RejectRole)
    ignore_button = msg.addButton("Ignore", QMessageBox.DestructiveRole)
    msg.setDefaultButton(ignore_button)

    result = msg.exec()

    if msg.clickedButton() == trust_button:
        if domain not in self.trusted_domains:
            self.trusted_domains.append(domain)
        new_view = QWebEngineView()
        new_page = CustomWebEnginePage(popup_blocking_enabled=self.popup_blocking_enabled, adblocking_enabled=self.adblocking_enabled)
        new_view.setPage(new_page)
        new_view.show()
        return new_page

    elif msg.clickedButton() == deny_button:
        if domain not in self.blocked_domains:
            self.blocked_domains.append(domain)
        return None

    elif msg.clickedButton() == ignore_button:
        return None


    def acceptNavigationRequest(self, url, type, is_main_frame):
        """Block ads and manage trusted/blocked domains."""
        domain = url.host()
        if self.adblocking_enabled and self.ad_blocker.is_ad(url.toString()):
            return False
        if domain in self.blocked_domains:
            return False
        return super().acceptNavigationRequest(url, type, is_main_frame)


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PaulGamerBoy101's Web Browser")
        self.resize(1200, 800)

        # Popup blocker and adblocker state
        self.popup_blocking_enabled = True
        self.adblocking_enabled = True

        # Main layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        # Navigation bar
        self.nav_bar = QWidget()
        self.nav_layout = QHBoxLayout()
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.nav_layout.addWidget(self.url_bar)

        # Back button
        self.back_button = QPushButton("🢀")
        self.back_button.clicked.connect(self.navigate_back)
        self.nav_layout.insertWidget(0, self.back_button)

        # Forward button
        self.forward_button = QPushButton("🢂")
        self.forward_button.clicked.connect(self.navigate_forward)
        self.nav_layout.insertWidget(1, self.forward_button)

        # Reload button
        self.refresh_button = QPushButton("🗘")
        self.refresh_button.clicked.connect(self.refresh_page)
        self.nav_layout.insertWidget(2, self.refresh_button)

        # Home button
        self.home_button = QPushButton("⌂")
        self.home_button.clicked.connect(self.navigate_home)
        self.nav_layout.insertWidget(3, self.home_button)

        self.nav_bar.setLayout(self.nav_layout)
        self.main_layout.addWidget(self.nav_bar)

        # Hover URL display
        self.hover_url_label = QLabel("")
        self.hover_url_label.setAlignment(Qt.AlignLeft)
        self.hover_url_label.setStyleSheet("color: gray; font-size: 12px;")
        self.main_layout.addWidget(self.hover_url_label)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.main_layout.addWidget(self.tabs)

        # Menu Bar
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Popup Blocker Menu
        popup_blocker_menu = self.menu_bar.addMenu("Popup Blocker")
        toggle_popup_blocker_action = QAction("Enable Popup Blocking", self, checkable=True)
        toggle_popup_blocker_action.setChecked(True)
        toggle_popup_blocker_action.triggered.connect(self.toggle_popup_blocker)
        popup_blocker_menu.addAction(toggle_popup_blocker_action)

        # Adblocker Menu
        adblocker_menu = self.menu_bar.addMenu("Adblocker")
        toggle_adblocker_action = QAction("Enable Adblocker", self, checkable=True)
        toggle_adblocker_action.setChecked(True)
        toggle_adblocker_action.triggered.connect(self.toggle_adblocker)
        adblocker_menu.addAction(toggle_adblocker_action)

        # New Tab Button
        self.new_tab_button = QPushButton("+")
        self.new_tab_button.clicked.connect(self.add_tab)
        self.tabs.setCornerWidget(self.new_tab_button)

        # Add initial tab
        self.add_tab()

    def toggle_popup_blocker(self, state):
        self.popup_blocking_enabled = state

    def toggle_adblocker(self, state):
        self.adblocking_enabled = state

    def add_tab(self, url="https://custom-new-tab-page-12935782.codehs.me/"):
        browser = QWebEngineView()
        custom_page = CustomWebEnginePage(browser, self.popup_blocking_enabled, self.adblocking_enabled)
        browser.setPage(custom_page)
        browser.setUrl(QUrl(url))
        browser.urlChanged.connect(lambda url: self.update_hover_url(url))
        index = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentWidget(browser)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def navigate_to_url(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            url = self.url_bar.text()
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url
            current_tab.setUrl(QUrl(url))

    def navigate_back(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.back()

    def navigate_forward(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.forward()

    def refresh_page(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.reload()

    def navigate_home(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.setUrl(QUrl("https://custom-new-tab-page-12935782.codehs.me/"))

    def update_hover_url(self, url):
        self.hover_url_label.setText(url.toString())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec())
