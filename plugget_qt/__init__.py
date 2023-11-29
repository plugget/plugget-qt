# import site
# site.addsitedir("C:\\Users\\hanne\\OneDrive\\Documents\\repos\\plugget")
# site.addsitedir("C:\\Users\\hanne\\OneDrive\\Documents\\repos\\detect-app")

from qtpy import QtWidgets
import plugget.commands as cmd


INSTALLED = "Installed"
INSTALL = "Install"
NOT_INSTALLED = "Not installed"
UNINSTALL = "Uninstall"

INDEX_INSTALLED = 1
INDEX_UNINSTALL = 2
INDEX_VERSIONS = 3
INDEX_INSTALL = 4


class PluggetWidget(QtWidgets.QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(objectName="plugget_qt_main_window", parent=parent, *args, **kwargs)
        self.setWindowTitle("Package Manager")

        self.current_packages = []

        # Create the UI elements
        self.search_field = QtWidgets.QLineEdit()
        self.search_field.returnPressed.connect(self.search_packages)
        self.search_field.setPlaceholderText("Search packages")

        self.search_text = QtWidgets.QLabel("")

        self.list_button = QtWidgets.QPushButton("List")
        self.list_button.clicked.connect(self.list_packages)

        # Create the table widget and set its properties
        self.package_list = QtWidgets.QTableWidget()
        self.package_list.setColumnCount(5)
        self.package_list.setHorizontalHeaderLabels(["Package Name", "installed", "uninstall", "versions", "Install"])
        self.package_list.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.package_list.verticalHeader().setVisible(False)
        self.package_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.package_list.cellDoubleClicked.connect(self.package_double_clicked)

        # Add the UI elements to the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.search_field)
        layout.addWidget(self.search_text)
        layout.addWidget(self.list_button)
        layout.addWidget(self.package_list)
        self.setLayout(layout)

        self.list_packages()
        
    @staticmethod
    def try_except(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                import traceback
                traceback.print_exc()

                QtWidgets.QMessageBox.critical(self, "Error", str(e))

        return wrapper

    def load_packages(self, packages):

        self.current_packages = packages

        # Clear the table widget
        self.package_list.clearContents()

        # Get the list of available packages
        # packages = cmd.search(self.search_field.text())

        # Set the number of rows in the table widget
        self.package_list.setRowCount(len(packages))

        # Add each package to the table widget
        for row, package_meta in enumerate(packages):
            # package name
            self.package_list.setItem(row, 0, QtWidgets.QTableWidgetItem(package_meta.package_name))
            
            # installed version
            if package_meta.installed_package:
                self.package_list.setItem(row, INDEX_INSTALLED, QtWidgets.QTableWidgetItem(package_meta.installed_package.version))

            # uninstall button
            if package_meta.installed_package:
                uninstall_button = QtWidgets.QPushButton(UNINSTALL)
                uninstall_button.clicked.connect(self.uninstall_package)
                self.package_list.setCellWidget(row, INDEX_UNINSTALL, uninstall_button)
                uninstall_button.setStyleSheet("background-color: tomato;color: black;")

            # versions dropdown
            versions = package_meta.versions
            version_dropdown = QtWidgets.QComboBox()
            version_dropdown.addItems(versions)
            # version_dropdown.currentTextChanged.connect(self.version_changed)
            self.package_list.setCellWidget(row, 3, version_dropdown)

            # install button
            install_button = QtWidgets.QPushButton(INSTALL)
            install_button.clicked.connect(self.install_package)
            self.package_list.setCellWidget(row, INDEX_INSTALL, install_button)

    @try_except
    def install_package(self):
        row = self.package_list.currentRow()
        package_meta = self.current_packages[row]
        version = self.package_list.cellWidget(row, INDEX_VERSIONS).currentText()
        cmd.install(package_meta.package_name, version=version)
        self.list_packages()
        
    @try_except
    def uninstall_package(self):
        row = self.package_list.currentRow()
        package_meta = self.current_packages[row]
        package_meta.installed_package.uninstall()
        self.list_packages()

    def package_double_clicked(self, row, column):
        pass
        # # Get the package metadata for the selected row
        # package_meta = cmd.search(self.table_widget.item(row, 0).text())[0]

        # # Create a package dialog and show it
        # package_dialog = PackageDialog(package_meta)
        # package_dialog.exec_()
    
    @try_except
    def search_packages(self):
        self.search_text.setText(f"Search results for '{self.search_field.text()}':")
        packages = cmd.search(self.search_field.text())
        self.load_packages(packages)

    @try_except
    def list_packages(self):
        self.search_text.setText("Installed packages:")
        packages = cmd.list(app="blender")  # todo remove need for app
        self.load_packages(packages)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(args, **kwargs)
        central_widget = PluggetWidget()
        self.setCentralWidget(central_widget)


def show():
    app = QtWidgets.QApplication.instance()
    
    exec = False
    if not app:
        exec = True
        app = QtWidgets.QApplication()
    
    global window
    window = MainWindow()
    window.show()

    if exec:
        app.exec_()

    return window


if __name__ == "__main__":
    show()
