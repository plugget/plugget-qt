# import site
# site.addsitedir("C:\\Users\\hanne\\OneDrive\\Documents\\repos\\plugget")
# site.addsitedir("C:\\Users\\hanne\\OneDrive\\Documents\\repos\\detect-app")

import PySide2.QtWidgets as QtWidgets
import plugget.commands as cmd


class PackageWidget(QtWidgets.QWidget):
    def __init__(self, package, parent=None):
        super().__init__(parent)
        self.package = package

        # Create the UI elements
        self.name_label = QtWidgets.QLabel(self.package.package_name)
        self.version_label = QtWidgets.QLabel(self.package.version)
        self.install_button = QtWidgets.QPushButton("Install")
        self.install_button.clicked.connect(self.install_package)

        # Lay out the elements horizontally
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.name_label)
        layout.addWidget(self.version_label)
        layout.addWidget(self.install_button)

    def install_package(self):
        cmd.install(self.package.package_name)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Package Manager")

        # Create the UI elements
        self.search_field = QtWidgets.QLineEdit()
        self.search_field.returnPressed.connect(self.search_packages)

        self.package_layout = QtWidgets.QVBoxLayout()
        self.package_scroll_area = QtWidgets.QScrollArea()
        self.package_scroll_area.setWidgetResizable(True)
        self.package_scroll_widget = QtWidgets.QWidget()
        self.package_scroll_widget.setLayout(self.package_layout)
        self.package_scroll_area.setWidget(self.package_scroll_widget)

        # Lay out the elements vertically
        central_widget = QtWidgets.QWidget()
        central_layout = QtWidgets.QVBoxLayout(central_widget)
        central_layout.addWidget(self.search_field)
        central_layout.addWidget(self.package_scroll_area)
        self.setCentralWidget(central_widget)

    def search_packages(self):
        # Clear the existing package widgets
        for i in reversed(range(self.package_layout.count())):
            widget = self.package_layout.itemAt(i).widget()
            widget.setParent(None)

        # Search for packages and create widgets for each result
        results = cmd.search(self.search_field.text())
        for package in results:
            package_widget = PackageWidget(package)
            self.package_layout.addWidget(package_widget)
        self.package_layout.addStretch()


app = QtWidgets.QApplication.instance
window = MainWindow()
window.show()

