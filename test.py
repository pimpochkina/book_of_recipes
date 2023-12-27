import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget, QLabel, QVBoxLayout, QWidget

app = QApplication(sys.argv)

# Создаем экземпляр QStackedWidget
stack = QStackedWidget()

# Создаем несколько виджетов, которые будем добавлять в QStackedWidget
widgets = [QLabel("Page 1"), QLabel("Page 2"), QLabel("Page 3")]

# Добавляем виджеты в QStackedWidget
for widget in widgets:
    stack.addWidget(widget)

# Создаем главный виджет и добавляем QStackedWidget в него
main_widget = QWidget()
main_layout = QVBoxLayout(main_widget)
main_layout.addWidget(stack)

# Отображаем главный виджет
main_widget.show()

# Переключаемся на вторую страницу
stack.setCurrentIndex(1)

# Запускаем приложение
sys.exit(app.exec_())
