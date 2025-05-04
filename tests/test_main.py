import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from PyQt5.QtWidgets import QApplication
from main import ContactManagerApp
import sys

@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance() if QApplication.instance() else QApplication(sys.argv)
    yield app

@pytest.fixture
def app(qapp):  # Pass the qapp fixture here
    window = ContactManagerApp()
    window.show()
    yield window
    window.close()  # Clean up after the test

def test_add_contact_gui(app):
    # WARNING: Это ОЧЕНЬ сложно автоматизировать полностью надежно,
    # так как требует взаимодействия с диалоговыми окнами.
    # В большинстве случаев для GUI используют ручное тестирование или инструменты,
    # имитирующие действия пользователя (например, Selenium, но это для веба).
    # Пример:
    # 1. Найти кнопку "Добавить" и нажать ее.
    # 2. Получить доступ к диалоговым окнам (QInputDialog) и ввести текст.
    # 3. Подтвердить ввод.
    # 4. Проверить, что новый контакт отображается в списке контактов.
    # Это потребует более сложного кода с использованием QtTest.

    # Простой пример (требует адаптации к вашему коду):
    initial_count = app.contacts_list.count()
    # Заглушка - необходимо реализовать взаимодействие с GUI элементами
    # и проверить, что контакт действительно добавился в список
    app.add_contact()  # Запускаем добавление (но ввод данных придется эмулировать)
    assert app.contacts_list.count() > initial_count  # Проверяем, что кол-во увеличилось

    # Реальный пример потребует использования QtTest (pip install pytest-qt)
    # и имитации ввода данных в диалоговые окна.

    # Этот тест показывает направление, но требует глубокой интеграции с QtTest
    # и понимания структуры вашего GUI.
    pass

