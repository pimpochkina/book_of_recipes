# импорт необходимых модулей
import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication


# создание класса окна входа в аккаунт
class LoginWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect('userdatas.sqlite')
        self.cur = self.con.cursor()
        uic.loadUi('login_widget.ui', self)
        self.signin_button.clicked.connect(self.sign_in)

    # функция проверки пароля и логина и входа в аккаунт
    def sign_in(self):
        self.login = self.login_input.text()
        self.password = self.password_input.text()
        request = self.cur.execute("""SELECT * FROM userdata WHERE login = ? AND password = ?""", (self.login, self.password)).fetchall()
        self.con.close()
        if len(request) == 0:
            # если такого пользователя не найдено, предлагаем создать аккаунт и добавляем в бд
            self.question_form = CreateAccWidget(self.login, self.password)
            self.question_form.show()
            self.close()
        else:
            # если есть - заходим в аккаунт
            pass


# создание класса виджета с запросом создания аккаунта
class CreateAccWidget(QWidget):
    def __init__(self, login, password):
        super().__init__()
        uic.loadUi('create_acc_widget.ui', self)
        self.password = password
        self.login = login
        self.createacc_btn.clicked.connect(self.create_acc)
        self.dontcreateacc_btn.clicked.connect(self.cancel)

    def create_acc(self):
        self.acc_creating_form = CreatingAccForm(self.login, self.password)
        self.acc_creating_form.show()
        self.close()

    def cancel(self):
        self.close()


class CreatingAccForm(QWidget):
    def __init__(self, login, password):
        super().__init__()
        uic.loadUi('create_acc_form.ui', self)
        self.password = password
        self.login = login
        self.con = sqlite3.connect('userdatas.sqlite')
        self.cur = self.con.cursor()
        self.create_btn.clicked.connect(self.create_account)

    def create_account(self):
        if self.check_info.isChecked():
            self.name = self.name_input.text()
            self.cur.execute("""INSERT INTO userdata(login,password,name) VALUES(?, ?, ?)""",
            (self.login, self.password, self.name))
            self.con.close()
            self.close()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = LoginWidget()
    form.show()
    sys.exit(app.exec())