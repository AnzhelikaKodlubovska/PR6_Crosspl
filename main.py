import sys
import pickle
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QTabWidget,
                             QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QInputDialog, QMessageBox, QDialog)

from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from edit_client import EditClient
from models import Client


class Branch(QWidget):
    def __init__(self):
        super().__init__()
        self.clients_list = []
        self.loadClientsList()
        self.initializeUI()

    def initializeUI(self):
        self.setMinimumSize(500, 400)
        self.setWindowTitle("Програма з обліку")
        self.setUpMainWindow()
        self.show()

    def setUpMainWindow(self):
        tab_bar = QTabWidget(self)
        self.clients_tab = QWidget()
        self.products_tab = QWidget()
        self.managers_tab = QWidget()

        tab_bar.addTab(self.clients_tab, "Клієнти")
        tab_bar.addTab(self.products_tab, "Продукти")
        tab_bar.addTab(self.managers_tab, "Співробітники")

        self.clientsTab()
        self.productsTab()
        self.managersTab()

        main_h_box = QHBoxLayout()
        main_h_box.addWidget(tab_bar)
        self.setLayout(main_h_box)

    def clientsTab(self):
        self.clients_list_widget = QListWidget()
        for client in self.clients_list:
            item = QListWidgetItem(f"{client.name} - {client.email}")
            self.clients_list_widget.addItem(item)

        button_add_client = QPushButton('Додати клієнта')
        button_add_client.clicked.connect(self.addClientClicked)

        tab_v_box = QVBoxLayout()
        tab_v_box.addWidget(self.clients_list_widget)
        tab_v_box.addWidget(button_add_client)
        self.clients_tab.setLayout(tab_v_box)

        self.clients_list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.clients_list_widget.customContextMenuRequested.connect(self.showContextMenu)

    def productsTab(self):
        self.products_list = ['Ноутбук', 'Смартфон', 'Принтер']
        self.products_list_widget = QListWidget()
        for product in self.products_list:
            self.products_list_widget.addItem(QListWidgetItem(product))

        button_add_product = QPushButton('Додати продукт')
        button_add_product.clicked.connect(self.addProductClicked)

        tab_v_box = QVBoxLayout()
        tab_v_box.addWidget(self.products_list_widget)
        tab_v_box.addWidget(button_add_product)
        self.products_tab.setLayout(tab_v_box)

    def addProductClicked(self):
        product, ok = QInputDialog.getText(self, 'Новий продукт', 'Введіть назву продукту:')
        if ok and product:
            self.products_list.append(product)
            self.products_list_widget.addItem(QListWidgetItem(product))

    def managersTab(self):
        self.managers_list = ['Олександр', 'Ірина', 'Василь']
        self.managers_list_widget = QListWidget()
        for manager in self.managers_list:
            self.managers_list_widget.addItem(QListWidgetItem(manager))

        button_add_manager = QPushButton('Додати співробітника')
        button_add_manager.clicked.connect(self.addManagerClicked)

        tab_v_box = QVBoxLayout()
        tab_v_box.addWidget(self.managers_list_widget)
        tab_v_box.addWidget(button_add_manager)
        self.managers_tab.setLayout(tab_v_box)

    def addManagerClicked(self):
        manager, ok = QInputDialog.getText(self, 'Новий співробітник', "Введіть ім'я:")
        if ok and manager:
            self.managers_list.append(manager)
            self.managers_list_widget.addItem(QListWidgetItem(manager))

    def addClientClicked(self):
        dialog = EditClient(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_client = dialog.getClientData()
            if new_client:
                self.clients_list.append(new_client)
                self.clients_list_widget.addItem(QListWidgetItem(f"{new_client.name} - {new_client.email}"))
                self.saveClientsList()

    def showContextMenu(self, position):
        menu = self.clients_list_widget.createStandardContextMenu()
        edit_action = QAction("Редагувати", self)
        edit_action.triggered.connect(self.editClient)
        menu.addAction(edit_action)
        menu.exec(self.clients_list_widget.mapToGlobal(position))

    def editClient(self):
        selected_item = self.clients_list_widget.currentItem()
        if selected_item:
            index = self.clients_list_widget.row(selected_item)
            client = self.clients_list[index]
            dialog = EditClient(self, client)
            if dialog.exec():
                updated_client = dialog.getClientData()
                self.clients_list[index] = updated_client
                selected_item.setText(f"{updated_client.name} - {updated_client.email}")
                self.saveClientsList()

    def loadClientsList(self):
        try:
            with open("clients.pkl", "rb") as f:
                self.clients_list = pickle.load(f)
                if not isinstance(self.clients_list, list):  
                    self.clients_list = []
        except (FileNotFoundError, pickle.UnpicklingError):
            self.clients_list = []


    def saveClientsList(self):
        with open("clients.pkl", "wb") as f:
            pickle.dump(self.clients_list, f)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Branch()
    sys.exit(app.exec())

