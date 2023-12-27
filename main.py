# импорт необходимых модулей
import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt
from random import *


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
        request = self.cur.execute("""SELECT * FROM userdata WHERE login = ? AND password = ?""",
                                   (self.login, self.password)).fetchall()
        if len(request) == 0:
            # если такого пользователя не найдено, предлагаем создать аккаунт и добавляем в бд
            self.question_form = CreateAccWidget(self.login, self.password)
            self.question_form.show()
            self.close()
        else:
            # если есть - заходим в аккаунт
            self.main_window = MainWindow(request[0])
            self.main_window.show()
            self.close()
            self.con.close()


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
            if self.name:
                # добавляем нового пользователя в базу данных
                self.cur.execute("""INSERT INTO userdata(login, password, name) VALUES(?, ?, ?)""",
                                 (self.login, self.password, self.name))
                self.con.commit()
                self.con.close()
                self.close()
                self.main_window = MainWindow(self.name)
                self.main_window.show()

# создание класса главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self, name):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.con_recipes = sqlite3.connect('RECIPES.SQLITE')
        self.cur_recipes = self.con_recipes.cursor()
        self.con_tips = sqlite3.connect('cookingtips.sqlite')
        self.cur_tips = self.con_tips.cursor()
        self.stackedWidget.setCurrentIndex(0)
        self.today_calories = 0
        self.recipe_names = self.cur_recipes.execute("""SELECT name FROM recipes""").fetchall()
        self.lower_recipe_names = [w[0].lower() for w in self.recipe_names]
        self.ings = []
        self.mainInit()
    # метод поиска рецепта по названию

    def name_search(self):
        self.found_recipe_list.clear()
        name_s = self.name_search_line.text()
        name_s = name_s.lower()
        name = f'%{name_s.capitalize()}%'
        result = self.cur_recipes.execute("""SELECT name FROM recipes WHERE name LIKE ? """, (name, )).fetchall()
        if len(result) != 0:
            for e in result:
                self.found_recipe_list.addItem(e[0])
            self.found_label.setText(f'Найдено рецептов: {len(result)}')
        else:
            self.found_label.setText(f'Найдено рецептов: 0')

    # метод поиска рецепта по ингредиенту
    def search_ings(self):
        self.found_recipe_list.clear()
        ing = self.ing_search_edit.text()
        if ing:
            result = self.cur_recipes.execute("""SELECT name FROM recipes WHERE ingredients LIKE ? """, (f'%{ing.lower()}%',)).fetchall()
            if len(result) != 0:
                for e in result:
                    self.found_recipe_list.addItem(e[0])
                self.found_label.setText(f'Найдено рецептов: {len(result)}')
            else:
                self.found_label.setText(f'Найдено рецептов: 0')

    # метод поиска рецептов по тегам
    def tags_search(self):
        self.found_recipe_list.clear()
        tags = []
        if self.breakfast_box.isChecked():
            tags.append('завтрак,')
        if self.lunch_box.isChecked():
            tags.append('обед,')
        if self.dinner_box.isChecked():
            tags.append('ужин,')
        if self.first_dish_box.isChecked():
            tags.append('первое,')
        if self.second_dish_box.isChecked():
            tags.append('второе,')
        if self.snack_box.isChecked():
            tags.append('закуска,')
        if self.sweet_box.isChecked():
            tags.append('десерт,')
        if self.drink_box.isChecked():
            tags.append('напиток,')
        if self.salad_box.isChecked():
            tags.append('салат,')
        if self.bakery_box.isChecked():
            tags.append('выпечка,')
        if self.hot_box.isChecked():
            tags.append('горячее,')
        if self.fast_box.isChecked():
            tags.append('быстрое,')
        if self.easy_box.isChecked():
            tags.append('легкое,')
        if self.diet_box.isChecked():
            tags.append('диетическое,')
        if len(tags) != 0:
            tags_request = " AND ".join([f"tags LIKE '%{tag}%'" for tag in tags])
            result = self.cur_recipes.execute(f"""SELECT name FROM recipes WHERE {tags_request}""").fetchall()
            if len(result) != 0:
                for e in result:
                    self.found_recipe_list.addItem(e[0])
                self.found_label.setText(f'Найдено рецептов: {len(result)}')
            else:
                self.found_label.setText(f'Найдено рецептов: 0')

    def clear_search(self):
        self.found_recipe_list.clear()
        self.found_label.setText(f'Найдено рецептов: 0')

    def read_searched_recipe(self, item):
        self.read_recipe(item.text())

    def search_pageInit(self):
        self.stackedWidget.setCurrentIndex(1)
        self.search_name_btn.clicked.connect(self.name_search)
        self.search_ings_btn.clicked.connect(self.search_ings)
        self.search_tags_btn.clicked.connect(self.tags_search)
        self.clear_search_btn.clicked.connect(self.clear_search)
        self.found_recipe_list.itemClicked.connect(self.read_searched_recipe)

    def return_on_mainpg(self):
        self.stackedWidget.setCurrentIndex(0)

    def set_random_recipe(self):
        self.random_recipe_label.setWordWrap(True)
        self.random_recipe_label.setAlignment(Qt.AlignCenter)
        self.random_recipe_label.setText(choice(self.recipe_names)[0])

    def set_random_tips(self):
        self.tips = self.cur_tips.execute("""SELECT tip FROM tips""").fetchall()
        self.tips = [w[0] for w in self.tips]
        self.tips = set(self.tips)
        self.tips = list(self.tips)
        self.tip_cur_index = 0
        self.tip_label.setWordWrap(True)
        self.tip_label.setAlignment(Qt.AlignCenter)
        self.tip_label.setText(self.tips[self.tip_cur_index])

    def next_tip(self):
        if self.tip_cur_index + 1 >= len(self.tips):
            self.tip_cur_index = 0
        else:
            self.tip_cur_index += 1
        self.tip_label.setText(self.tips[self.tip_cur_index])

    def read_recipe(self, name):
        self.stackedWidget.setCurrentIndex(2)
        request = self.cur_recipes.execute(f"""SELECT * FROM recipes WHERE name = ?""", (name, )).fetchall()
        self.recipe_name_label.setText(name)
        self.recipe_label.setText(request[0][4])
        ing_list = request[0][3].split(',')
        tags_list = request[0][2].split(',')
        self.ings_table.setRowCount(len(ing_list))
        output_tags = ', '.join(tags_list)
        self.tags_label.setText(f'Теги: {output_tags}')
        row_index = 0
        self.servings.setText(str(request[0][7]))
        self.ccalories.setText(str(request[0][5]))
        self.time.setText(str(request[0][6]))
        for e in ing_list:
            index = e.find('(')
            item1 = QTableWidgetItem(e[:index])
            item2 = QTableWidgetItem(e[index+1:-1])
            self.ings_table.setItem(row_index, 0, item1)
            self.ings_table.setItem(row_index, 1, item2)
            row_index += 1

    def previous_tip(self):
        if self.tip_cur_index == 0:
            self.tip_cur_index = len(self.tips) - 1
        self.tip_cur_index -= 1
        self.tip_label.setText(self.tips[self.tip_cur_index])

    def add_ccal(self):
        calories = int(self.add_dish_ccal.value())
        weight = int(self.add_weight.value())
        self.today_calories += (calories / 100) * weight
        self.today_ccal.display(self.today_calories)

    def clear_ccal(self):
        self.today_calories = 0
        self.today_ccal.display(self.today_calories)

    def read_random_recipe(self):
        name = self.random_recipe_label.text()
        self.read_recipe(name)

    def mainInit(self):
        self.search_page_btn.clicked.connect(self.search_pageInit)
        self.main_page_btn.clicked.connect(self.return_on_mainpg)
        self.next_random_btn.clicked.connect(self.set_random_recipe)
        self.set_random_recipe()
        self.read_btn.clicked.connect(self.read_random_recipe)
        self.set_random_tips()
        self.next_tip_btn.clicked.connect(self.next_tip)
        self.previous_tip_btn.clicked.connect(self.previous_tip)
        self.add_dish_btn.clicked.connect(self.add_ccal)
        self.clear_today_ccal.clicked.connect(self.clear_ccal)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = LoginWidget()
    form.show()
    sys.exit(app.exec())