import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout,
    QHBoxLayout, QWidget, QPushButton, QLineEdit, QTabWidget,
    QMenuBar, QAction, QLabel
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl, Qt


class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)

    def acceptNavigationRequest(self, url, type, is_main_frame):
        """
        Handle navigation requests, including clicks and new tabs.
        """
        if type == QWebEnginePage.NavigationTypeLinkClicked:
            if is_main_frame:
                self.view().setUrl(url)
            else:
                self.view().parent().add_tab(url.toString())
            return False
        return super().acceptNavigationRequest(url, type, is_main_frame)


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PaulGamerBoy101's Web Browser")
        self.resize(1200, 800)

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

        # New Tab Button
        self.new_tab_button = QPushButton("+")
        self.new_tab_button.clicked.connect(self.add_tab)
        self.tabs.setCornerWidget(self.new_tab_button)

        # Add initial tab
        self.add_tab()

    def add_tab(self, url="https://custom-new-tab-page-12935782.codehs.me/"):
        browser = QWebEngineView()
        custom_page = CustomWebEnginePage(browser)
        browser.setPage(custom_page)
        browser.setUrl(QUrl.fromUserInput(url))
        browser.urlChanged.connect(lambda url: self.update_url_bar(url))
        index = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentWidget(browser)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()

    def navigate_to_url(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            url = self.url_bar.text()
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url
            current_tab.setUrl(QUrl.fromUserInput(url))

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

    def update_url_bar(self, url):
        self.url_bar.setText(url.toString())
        self.hover_url_label.setText(url.toString())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())
