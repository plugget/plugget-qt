# local hack for IDE
import sys
# sys.path.append("C:\\Users\\hanne\\OneDrive\\Documents\\repos\\plugget")
# sys.path.append("C:\\Users\\hanne\\OneDrive\\Documents\\repos\\detect-app")

try:
    from contextlib import suppress
    QtWidgets = None
    with suppress(ImportError):
        import PySide6.QtWidgets as QtWidgets
    with suppress(ImportError):
        import PyQt6.QtWidgets as QtWidgets
except:
    try:
        import PyQt5.QtWidgets as QtWidgets
    except ImportError:
        pass
    try:
        import PySide2.QtWidgets as QtWidgets
    except ImportError:
        import qtpy.QtWidgets as QtWidgets

import plugget.commands as cmd
import logging

INSTALLED = "Installed"
INSTALL = "Install"
NOT_INSTALLED = "Not installed"
UNINSTALL = "Uninstall"

LABELS = ["Package Name", INSTALLED, UNINSTALL, "versions", INSTALL]

INDEX_PACKAGE_NAME = 0
INDEX_INSTALLED = 1
INDEX_UNINSTALL = 2
INDEX_VERSIONS = 3
INDEX_INSTALL = 4


class PluggetWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(objectName="plugget_qt_main_window", parent=parent, *args, **kwargs)
        self.setWindowTitle("Package Manager")

        self.current_packages = []

        # Create the UI elements
        self.search_field = QtWidgets.QLineEdit()
        self.search_field.returnPressed.connect(self.search_packages)
        self.search_field.setPlaceholderText("Search packages")

        self.search_text = QtWidgets.QLabel("")

        # self.list_button = QtWidgets.QPushButton("Refresh")
        # self.list_button.clicked.connect(self.list_packages)

        # Create the table widget and set its properties
        self.package_list = QtWidgets.QTableWidget()
        self.package_list.setColumnCount(len(LABELS))
        self.package_list.setHorizontalHeaderLabels(LABELS)
        self.package_list.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.package_list.verticalHeader().setVisible(False)
        self.package_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.package_list.cellDoubleClicked.connect(self.package_double_clicked)

        # Create the tab widget
        self.tab_widget = QtWidgets.QTabWidget(parent=self)

        # Create the search widget and add UI elements
        self.search_widget = QtWidgets.QWidget(parent=self)
        search_layout = QtWidgets.QVBoxLayout()
        search_layout.addWidget(self.search_field)
        # search_layout.addWidget(self.search_text)
        self.search_widget.setLayout(search_layout)

        # Create the list widget and add UI elements
        self.list_widget = QtWidgets.QWidget(parent=self)
        list_layout = QtWidgets.QVBoxLayout()
        # list_layout.addWidget(self.list_button)
        self.list_widget.setLayout(list_layout)

        # Create the list widget and add UI elements
        self.toolbox_widget = QtWidgets.QWidget(parent=self)
        list_layout = QtWidgets.QVBoxLayout()
        # list_layout.addWidget(self.package_list)
        self.toolbox_widget.setLayout(list_layout)

        # Add the search and list widgets to the tab widget
        self.tab_widget.addTab(self.search_widget, "Search")
        self.tab_widget.addTab(self.list_widget, "Installed")
        self.tab_widget.addTab(self.toolbox_widget, "Preset")
        self.tab_widget.setTabToolTip(0, "Search for packages")
        self.tab_widget.setTabToolTip(1, "List installed packages")
        self.tab_widget.setTabToolTip(2, "Selected packages from a config")

        # Add the tab widget to the main layout
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.tab_widget)
        layout.addWidget(self.package_list)

        # when i go to select tab, run self.list_packages
        self.tab_widget.currentChanged.connect(self.tab_logic)

        # # tab widget should take up least space possible
        # self.tab_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        # self.search_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        # self.list_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        # self.toolbox_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        # # package list should take up all space possible
        # self.package_list.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # # Add the UI elements to the layout
        # layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(self.search_field)
        # layout.addWidget(self.search_text)
        # layout.addWidget(self.list_button)
        # layout.addWidget(self.package_list)
        # self.setLayout(layout)

        # self.list_packages()
        # set tab to list
        self.tab_widget.setCurrentIndex(1)

    def tab_logic(self):
        # if tab is select, run self.list_packages

        # clear package list
        self.package_list.clearContents()
        self.package_list.setRowCount(0)

        if self.tab_widget.currentIndex() == 0:
            self.search_packages(use_cache=True)
            # todo load previous search results
            pass
        elif self.tab_widget.currentIndex() == 1:
            self.list_packages()
        elif self.tab_widget.currentIndex() == 2:
            self.list_config_packages()

    def try_except(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                import traceback
                traceback.print_exc()
                QtWidgets.QMessageBox.critical(self, "Error", str(e))

        return wrapper

    def load_packages(self, packages: "list[cmd.PackagesMeta]"):
        print("load packages", packages)

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
            self.package_list.setItem(row, INDEX_PACKAGE_NAME, QtWidgets.QTableWidgetItem(package_meta.package_name))

            # installed version
            if package_meta.installed_package:
                self.package_list.setItem(row, INDEX_INSTALLED, QtWidgets.QTableWidgetItem(package_meta.installed_package.version))

            # uninstall button
            if package_meta.installed_package:
                uninstall_button = QtWidgets.QPushButton(UNINSTALL)
                uninstall_button.clicked.connect(lambda _=None, r=row: self.uninstall_package(r))
                self.package_list.setCellWidget(row, INDEX_UNINSTALL, uninstall_button)
                uninstall_button.setStyleSheet("background-color: tomato;color: black;")

            # versions dropdown
            versions = package_meta.versions
            version_dropdown = QtWidgets.QComboBox()
            version_dropdown.addItems(versions)
            # version_dropdown.currentTextChanged.connect(self.version_changed)
            self.package_list.setCellWidget(row, INDEX_VERSIONS, version_dropdown)
            # set version to latest
            version_dropdown.setCurrentText(package_meta.latest.version)

            # install button
            install_button = QtWidgets.QPushButton(INSTALL)
            install_button.clicked.connect(lambda _=None, r=row: self.install_package(r))
            self.package_list.setCellWidget(row, INDEX_INSTALL, install_button)

    @try_except
    def install_package(self, row):
        package_meta = self.current_packages[row]
        version = self.package_list.cellWidget(row, INDEX_VERSIONS).currentText()
        cmd.install(package_meta.package_name, version=version)
        self.list_packages()

    @try_except
    def uninstall_package(self, row):
        package_meta = self.current_packages[row]
        package_meta.installed_package.uninstall()
        self.list_packages()

    def package_double_clicked(self, row, column):
        pass
        # # Get the package metadata for the selected row
        # package_meta = cmd.search(self.table_widget.item(row, INDEX_PACKAGE_NAME).text())[0]

        # # Create a package dialog and show it
        # package_dialog = PackageDialog(package_meta)
        # package_dialog.exec_()

    def _get_app(self):
        app = cmd._detect_app_id()
        if not app:
            logging.warning("could not detect app, will list all packages")
            app = "all"
        return app

    @try_except
    def search_packages(self, use_cache=False):
        # self.search_text.setText(f"Search results for '{self.search_field.text()}':")
        app = self._get_app()
        packages = cmd.search(self.search_field.text(), use_cache=use_cache, app=app)
        self.load_packages(packages)

    @try_except
    def list_packages(self):
        """list installed packages"""
        # self.search_text.setText("Installed packages:")
        app = self._get_app()
        packages = cmd.search(installed=True, app=app)  # todo remove need for app
        self.load_packages(packages)

    @try_except
    def list_config_packages(self):
        """list packages from a config file"""
        #todo
        # if not found, show a red warning or something.

        # self.search_text.setText("Installed packages:")
        packages = cmd.packages_from_config_file(path=r"C:\Users\hanne\OneDrive\Documents\repos\plugget-qt-search\sample_config.txt")
        self.load_packages(packages)

    def set_tab(self, index):
        self.tab_widget.setCurrentIndex(index)

    def hide_tabs(self, hide_tabs=False):
        self.tab_widget.setVisible(not hide_tabs)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        central_widget = PluggetWidget(parent=self)
        self.setCentralWidget(central_widget)
        self.setWindowTitle(central_widget.windowTitle())

    def set_tab(self, index):
        self.centralWidget().set_tab(index)

    def hide_tabs(self, hide_tabs=False):
        self.centralWidget().hide_tabs(hide_tabs)


def show(tab_index=0, hide_tabs=False):
    app = QtWidgets.QApplication.instance()

    exec = False
    if not app:
        exec = True
        app = QtWidgets.QApplication()

    global window
    window = MainWindow()
    window.set_tab(tab_index)
    window.hide_tabs(hide_tabs)
    window.show()

    if exec:
        app.exec_()

    return window


if __name__ == "__main__":
    show()
