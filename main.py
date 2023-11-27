# импорт необходимых модулей
import sys

import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication


# создание класса окна входа в аккаунт
class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('login_widget.ui', self)
        self.signin_button.clicked.connect(self.sign_in)

    # функция проверки пароля и логина и входа в аккаунт
    def sign_in(self):
        con = sqlite3.connect('app_username.db')
        cur = con.cursor()
        self.login = self.login_input.text()
        self.password = self.password_input.text()
        request = cur.execute("""SELECT name FROM userdata WHERE 
        password = ? AND login = ?""", (self.password, self.login)).fetchone()
        if len(request) == 0:
            # если такого пользователя не найдено, предлагаем создать аккаунт и добавляем в бд
            pass
        else:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = LoginWidget()
    form.show()
    sys.exit(app.exec())