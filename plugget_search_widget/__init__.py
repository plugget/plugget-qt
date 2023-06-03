# import site
# site.addsitedir("C:\\Users\\hanne\\OneDrive\\Documents\\repos\\plugget")
# site.addsitedir("C:\\Users\\hanne\\OneDrive\\Documents\\repos\\detect-app")

import PySide2.QtWidgets as QtWidgets
import plugget.commands as cmd
import logging


INSTALLED = "Installed"
INSTALL = "Install"
NOT_INSTALLED = "Not installed"
UNINSTALL = "Uninstall"


class PackageWidget(QtWidgets.QWidget):
    def __init__(self, packageMeta, parent=None):
        super().__init__(parent)
        self.package_meta = packageMeta

        # Create the UI elements
        self.name_label = QtWidgets.QLabel(self.package_meta.package_name)

        if self.package_meta.installed_package:
            version = self.package_meta.installed_package.version
        else:
            version = ""
        self.version_label = QtWidgets.QLabel(version)

        # dropdown with all versions
        versions = self.package_meta.versions
        self.version_dropdown = QtWidgets.QComboBox()
        self.version_dropdown.addItems(versions)
        # connect
        self.version_dropdown.currentTextChanged.connect(self.version_changed)

        self.install_button = QtWidgets.QPushButton(INSTALL)
        self.install_button.clicked.connect(self.install_package)

        self.uninstall_button = QtWidgets.QPushButton(UNINSTALL)
        self.uninstall_button.clicked.connect(self.uninstall_package)
        # bold uninstall_button
        self.uninstall_button.setStyleSheet("background-color: tomato;")


        # Lay out the elements horizontally
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.name_label)
        layout.addWidget(self.version_label)
        layout.addWidget(self.version_dropdown)
        layout.addWidget(self.install_button)
        layout.addWidget(self.uninstall_button)
        self.setLayout(layout)

        self.version_changed(self.version_dropdown.currentText())  # init state
        # todo
        # show version dropwon
        # show app


    def install_package(self):
        cmd.install(self.package_meta.package_name, version=self.version_dropdown.currentText())
        # todo update UI

    def uninstall_package(self):
        self.package_meta.installed_package.uninstall()
        # todo update UI

    def version_changed(self, version):
        # disable install button if version is installed
        installed = self.package_meta.get_version(version).is_installed
        # hide
        self.uninstall_button.setVisible(installed)
        # self.install_button.setVisible(not installed)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Package Manager")

        # Create the UI elements
        self.search_field = QtWidgets.QLineEdit()
        self.search_field.returnPressed.connect(self.search_packages)
        self.search_field.setPlaceholderText("Search packages")

        self.search_text = QtWidgets.QLabel("")

        self.list_button = QtWidgets.QPushButton("List")
        self.list_button.clicked.connect(self.list_packages)

        # self.package_list = QtWidgets.QListWidget()

        # todo move package_scroll_widget to own widget, package layout too.
        # make it so we can just just clear and additems similar to list
        self.package_layout = QtWidgets.QVBoxLayout()
        self.package_scroll_area = QtWidgets.QScrollArea()
        self.package_scroll_area.setWidgetResizable(True)
        self.package_scroll_widget = QtWidgets.QWidget()
        self.package_scroll_widget.setLayout(self.package_layout)
        # self.package_scroll_area.setWidget(self.package_scroll_widget)
        self.package_scroll_area.setWidget(self.package_scroll_widget)


        # central_layout.addWidget(self.package_list)


        # Lay out the elements vertically
        central_widget = QtWidgets.QWidget()
        central_layout = QtWidgets.QVBoxLayout(central_widget)
        central_layout.addWidget(self.list_button)
        central_layout.addWidget(self.search_field)
        central_layout.addWidget(self.search_text)

        central_layout.addWidget(self.package_scroll_area)
        self.setCentralWidget(central_widget)


    def list_packages(self):
        # Clear the package list
        # self.package_list.clear()
# 
        # List all installed packages
        packages = cmd.list(app="blender")  # todo remove need for app

        # Add the installed packages to the list
        # self.package_list.addItems(packages)

        for package in packages:
            package_widget = PackageWidget(package, parent=self)
            self.package_layout.addWidget(package_widget)

    def search_packages(self):
        # Clear the existing package widgets
        
        # self.package_list.clear()

        count = self.package_layout.count()
        print(count)
        for i in reversed(range(count)):
            widget = self.package_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
            else:
                logging.warning(f"widget None, index {i}")
        # todo this is a hack for second search, fix it

        # Search for packages and create widgets for each result
        input = self.search_field.text()
        self.search_text.setText(f"Searching for '{input}':")
        QtWidgets.QApplication.processEvents()
        packages = cmd.search(input, app="blender")  # todo remove need for app
        self.search_text.setText(f"Found {len(packages)} results for '{input}':")

        # self.package_list.addItems(packages)

        for packageMeta in packages:
            package_widget = PackageWidget(packageMeta)
            self.package_layout.addWidget(package_widget)
        self.package_layout.addStretch()

if __name__ == "__main__":
    app = QtWidgets.QApplication.instance()
    
    exec = False
    if not app:
        exec = True
        app = QtWidgets.QApplication()

    window = MainWindow()
    window.show()

    if exec:
        app.exec_()

