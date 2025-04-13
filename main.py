import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QLineEdit, QPushButton, QLabel,
    QComboBox, QMessageBox, QInputDialog, QFileDialog
)
from manager import ContactManager
from contact import Contact

class ContactManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Менеджер контактов")
        self.setGeometry(100, 100, 600, 400)
        
        self.manager = ContactManager()
        
        self.init_ui()
        self.load_sample_data()
    
    def init_ui(self):
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Поиск
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск...")
        search_button = QPushButton("Найти")
        search_button.clicked.connect(self.search_contacts)
        
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        
        layout.addLayout(search_layout)
        
        # Список контактов
        self.contacts_list = QListWidget()
        self.contacts_list.itemDoubleClicked.connect(self.edit_selected_contact)
        layout.addWidget(self.contacts_list)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        add_button = QPushButton("Добавить")
        add_button.clicked.connect(self.add_contact)
        
        edit_button = QPushButton("Редактировать")
        edit_button.clicked.connect(self.edit_selected_contact)
        
        delete_button = QPushButton("Удалить")
        delete_button.clicked.connect(self.delete_selected_contact)
        
        export_button = QPushButton("Экспорт")
        export_button.clicked.connect(self.export_contacts)
        
        import_button = QPushButton("Импорт")
        import_button.clicked.connect(self.import_contacts)
        
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(edit_button)
        buttons_layout.addWidget(delete_button)
        buttons_layout.addWidget(export_button)
        buttons_layout.addWidget(import_button)
        
        layout.addLayout(buttons_layout)
    
    def load_sample_data(self):
        self.manager.add_contact("Иван Иванов", "+79161234567", "ivan@example.com", "Друзья")
        self.manager.add_contact("Петр Петров", "+79169876543", "petr@example.com", "Работа")
        self.update_contacts_list()
    
    def update_contacts_list(self, contacts=None):
        self.contacts_list.clear()
        contacts = contacts if contacts else self.manager.get_all_contacts()
        for contact in contacts:
            item = QListWidgetItem(str(contact))
            self.contacts_list.addItem(item)
    
    def add_contact(self):
        name, ok = QInputDialog.getText(self, "Добавить контакт", "Имя:")
        if not ok or not name:
            return
        
        phone, ok = QInputDialog.getText(self, "Добавить контакт", "Телефон:")
        if not ok or not phone:
            return
        
        email, ok = QInputDialog.getText(self, "Добавить контакт", "Email:")
        if not ok or not email:
            return
        
        category, ok = QInputDialog.getItem(
            self, "Добавить контакт", "Категория:", 
            self.manager.categories, 0, False
        )
        if not ok or not category:
            return
        
        self.manager.add_contact(name, phone, email, category)
        self.update_contacts_list()
    
    def edit_selected_contact(self):
        index = self.contacts_list.currentRow()
        if index == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите контакт для редактирования")
            return
        
        contact = self.manager.contacts[index]
        
        name, ok = QInputDialog.getText(
            self, "Редактировать контакт", "Имя:", 
            text=contact.name
        )
        if not ok or not name:
            return
        
        phone, ok = QInputDialog.getText(
            self, "Редактировать контакт", "Телефон:", 
            text=contact.phone
        )
        if not ok or not phone:
            return
        
        email, ok = QInputDialog.getText(
            self, "Редактировать контакт", "Email:", 
            text=contact.email
        )
        if not ok or not email:
            return
        
        category, ok = QInputDialog.getItem(
            self, "Редактировать контакт", "Категория:", 
            self.manager.categories, 
            self.manager.categories.index(contact.category), 
            False
        )
        if not ok or not category:
            return
        
        self.manager.edit_contact(index, name, phone, email, category)
        self.update_contacts_list()
    
    def delete_selected_contact(self):
        index = self.contacts_list.currentRow()
        if index == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите контакт для удаления")
            return
        
        reply = QMessageBox.question(
            self, "Подтверждение", 
            "Вы уверены, что хотите удалить этот контакт?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.manager.delete_contact(index)
            self.update_contacts_list()
    
    def search_contacts(self):
        query = self.search_input.text().strip()
        if not query:
            self.update_contacts_list()
            return
        
        found_contacts = self.manager.search_contacts(query)
        self.update_contacts_list(found_contacts)
    
    def export_contacts(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Экспорт контактов", "", "Text Files (*.txt)"
        )
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                for contact in self.manager.get_all_contacts():
                    f.write(f"{contact.name},{contact.phone},{contact.email},{contact.category}\n")
            QMessageBox.information(self, "Успех", "Контакты успешно экспортированы")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось экспортировать контакты: {str(e)}")
    
    def import_contacts(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Импорт контактов", "", "Text Files (*.txt)"
        )
        if not file_path:
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) == 4:
                        self.manager.add_contact(*parts)
            self.update_contacts_list()
            QMessageBox.information(self, "Успех", "Контакты успешно импортированы")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось импортировать контакты: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContactManagerApp()
    window.show()
    sys.exit(app.exec_())
