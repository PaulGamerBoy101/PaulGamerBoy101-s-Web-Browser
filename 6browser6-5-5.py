import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QLineEdit,
    QTabWidget,
    QMenuBar,
    QAction,
    QLabel,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile
from PyQt5.QtCore import QUrl


class AdBlocker:
    def __init__(self):
        self.blocked_domains = [
            "ads.example.com",
            "ads1.example.net",
            "doubleclick.net",
            "googlesyndication.com",
            "pagead2.googlesyndication.com",
            "adservice.google.com",
            "amazon-adsystem.com",
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

    def set_popup_blocking(self, enabled):
        self.popup_blocking_enabled = enabled

    def set_adblocking(self, enabled):
        self.adblocking_enabled = enabled

    def createWindow(self, _type):
        if not self.popup_blocking_enabled:
            new_view = QWebEngineView()
            new_view.setPage(CustomWebEnginePage())
            new_view.show()
            return new_view.page()

        msg = QMessageBox()
        msg.setWindowTitle("Popup Blocked")
        msg.setText("A popup was blocked. What would you like to do?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Ignore)
        msg.setDefaultButton(QMessageBox.Ignore)

        result = msg.exec()

        if result == QMessageBox.Yes:
            new_view = QWebEngineView()
            new_view.setPage(CustomWebEnginePage())
            new_view.show()
            return new_view.page()
        elif result == QMessageBox.No or result == QMessageBox.Ignore:
            return None

    def acceptNavigationRequest(self, url, type, is_main_frame):
        if self.adblocking_enabled and self.ad_blocker.is_ad(url.toString()):
            return False
        return super().acceptNavigationRequest(url, type, is_main_frame)


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PaulGamerBoy101's Web Browser")
        self.resize(1200, 800)

        self.popup_blocking_enabled = True
        self.adblocking_enabled = True

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.nav_bar = QWidget()
        self.nav_layout = QHBoxLayout()
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.nav_layout.addWidget(self.url_bar)

        self.back_button = QPushButton("🢀")
        self.back_button.clicked.connect(self.navigate_back)
        self.nav_layout.insertWidget(0, self.back_button)

        self.forward_button = QPushButton("🢂")
        self.forward_button.clicked.connect(self.navigate_forward)
        self.nav_layout.insertWidget(1, self.forward_button)

        self.refresh_button = QPushButton("🗘")
        self.refresh_button.clicked.connect(self.refresh_page)
        self.nav_layout.insertWidget(2, self.refresh_button)

        # Add the Home Button
        self.home_button = QPushButton("⌂")
        self.home_button.clicked.connect(self.navigate_home)
        self.nav_layout.insertWidget(3, self.home_button)

        self.nav_bar.setLayout(self.nav_layout)
        self.main_layout.addWidget(self.nav_bar)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.main_layout.addWidget(self.tabs)

        self.hover_label = QLabel("")
        self.hover_label.setStyleSheet("color: gray; font-size: 12px; padding: 5px;")
        self.main_layout.addWidget(self.hover_label)

        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        popup_blocker_menu = self.menu_bar.addMenu("Popup Blocker")
        toggle_popup_blocker_action = QAction("Enable Popup Blocking", self, checkable=True)
        toggle_popup_blocker_action.setChecked(True)
        toggle_popup_blocker_action.triggered.connect(self.toggle_popup_blocker)
        popup_blocker_menu.addAction(toggle_popup_blocker_action)

        adblocker_menu = self.menu_bar.addMenu("Adblocker")
        toggle_adblocker_action = QAction("Enable Adblocker", self, checkable=True)
        toggle_adblocker_action.setChecked(True)
        toggle_adblocker_action.triggered.connect(self.toggle_adblocker)
        adblocker_menu.addAction(toggle_adblocker_action)

        self.new_tab_button = QPushButton("+")
        self.new_tab_button.clicked.connect(self.add_tab)
        self.tabs.setCornerWidget(self.new_tab_button)

        self.add_tab()

    def toggle_popup_blocker(self, state):
        self.popup_blocking_enabled = state
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            if isinstance(tab, QWebEngineView):
                tab.page().set_popup_blocking(state)

    def toggle_adblocker(self, state):
        self.adblocking_enabled = state
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            if isinstance(tab, QWebEngineView):
                tab.page().set_adblocking(state)

    def add_tab(self, url="https://custom-new-tab-page-12935782.codehs.me/"):
        if not isinstance(url, str):
            url = "https://custom-new-tab-page-12935782.codehs.me/"
        browser = QWebEngineView()
        custom_page = CustomWebEnginePage(browser, self.popup_blocking_enabled, self.adblocking_enabled)
        browser.setPage(custom_page)
        browser.setUrl(QUrl(url))

        browser.page().linkHovered.connect(self.display_hovered_url)

        index = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentWidget(browser)
        browser.urlChanged.connect(lambda url: self.update_tab_title(index, url))

    def navigate_home(self):
        """Navigate to the home page (default new tab URL)."""
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.setUrl(QUrl("https://custom-new-tab-page-12935782.codehs.me/"))

    def display_hovered_url(self, url):
        self.hover_label.setText(url)

    def update_tab_title(self, index, url):
        self.tabs.setTabText(index, url.toString()[:20])

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec())
