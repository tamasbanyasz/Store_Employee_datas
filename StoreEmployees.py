import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg

from datetime import datetime
import pandas as pd
import os.path
import sqlite3


def file_is_exist(column_names):  # load datas from csv
    if os.path.exists('employees.csv'):
        return pd.read_csv('employees.csv', skiprows=1, names=column_names)


class MessageBox:
    def __init__(self):
        self.msg = qtw.QMessageBox()
        self.msg.setIcon(qtw.QMessageBox.Warning)

    def incorrect_first_name(self, first_name):
        self.msg.setWindowTitle("Warning MessageBox")
        self.msg.setText(f"Incorrect  'First Name':   ' {first_name} '")
        self.msg.exec_()

    def incorrect_last_name(self, last_name):
        self.msg.setWindowTitle("Warning MessageBox")
        self.msg.setText(f"Incorrect  'Last Name':   ' {last_name} '")
        self.msg.exec_()


class NameValid:
    def __init__(self):
        self.messagebox = MessageBox()

    def first_name_is_valid(self, first_name):
        if not first_name.isalpha():
            self.messagebox.incorrect_first_name(first_name)
        return first_name.isalpha()

    def last_name_is_valid(self, last_name):
        if not last_name.isalpha():
            self.messagebox.incorrect_last_name(last_name)
        return last_name.isalpha()

    def full_name_is_valid(self, first_name, last_name):
        return self.first_name_is_valid(first_name) and self.last_name_is_valid(last_name)


class WorkersPropertiesDataBase:
    def __init__(self):
        self.connection = sqlite3.connect('employees.db')
        self.connection.commit()
        self.cur = self.connection.cursor()

        # create SQL table
        self.cur.execute("create table if not exists employees(id int primary key, ""firstname varchar(20), "
                         "lastname varchar(20),"
                         "age int,"
                         "date DATETIME);")

        self.cur.execute("create table if not exists permissions(id int primary key, worker_id int, ""mobile varchar(20), "
                         "warehouse varchar(5));")

        self.db_employees_length = 0  # length of the loaded db. Use to count db index
        self.db_permissions_length = 0

        self.read_from_employees_table()  # read the database

    def read_from_employees_table(self):

        loaded_sql = pd.read_sql('SELECT id, firstname, lastname, age, date FROM employees', self.connection)

        self.db_employees_length = len(loaded_sql)

        return loaded_sql

    def insert_into_employees_table(self, firstname, lastname, age):

        self.cur.execute(f"insert into employees values({self.db_employees_length}, "
                         f"'{firstname}', "
                         f"'{lastname}', "
                         f"'{age}',"
                         f"'{datetime.now()}')")
        self.connection.commit()

    def show_employees_table(self):
        print(self.read_from_employees_table())

    def insert_into_permissions_table(self, index, mobile, warehouse):

        self.cur.execute(f"insert into permissions values({self.db_permissions_length},"
                         f"'{index}', "
                         f"'{mobile}',"
                         f"'{warehouse}')")
        self.connection.commit()

    def read_from_premission_table(self):
        loaded_sql = pd.read_sql('SELECT id, worker_id, mobile, warehouse FROM permissions', self.connection)

        self.db_permissions_length = len(loaded_sql)

        return loaded_sql

    def show_premission_table(self):
        print(self.read_from_premission_table())


class GetEmployeesData:
    def __init__(self):
        self.name_valid = NameValid()
        self.database = WorkersPropertiesDataBase()

        self.COLUMN_NAMES = ["First Name", "Last Name", "Age", "Date"]

        self.csv = file_is_exist(self.COLUMN_NAMES)  # load datas from csv

        self.df = pd.DataFrame(self.csv, columns=self.COLUMN_NAMES)  # DataFrame to store employee datas
        print(self.df)

    def set_datas(self, firstname, lastname, age):  # add new employee datas to DataFrame
        self.df.loc[len(self.df.index)] = [firstname, lastname, age, datetime.now().strftime('%d/%m/%Y %H:%M:%S')]

    def full_name_is_valid(self, first_name, last_name, age):
        if self.name_valid.full_name_is_valid(first_name, last_name):
            self.database.insert_into_employees_table(first_name, last_name, age)
            self.set_datas(first_name, last_name, age)
            return True


class SetTreeViewBox:
    def __init__(self, model):
        self.datas = GetEmployeesData()
        self.model = model

    def clear_treeview_box(self):  # clear the treeview box for the new datas
        self.model.removeRows(0, self.model.rowCount(qtc.QModelIndex()))

    def insert_items_into_treeview_box(self):

        ages = self.datas.df[
            'Age'].values.tolist()  # store 'Age' values in classic list because the type of the DataFrame column is 'numpy.integer' and it couldnt display
        print(self.datas.df)

        for i in range(len(self.datas.df)):
            self.model.insertRow(i)  # make box rows

            self.model.setData(self.model.index(i, 0), self.datas.df.loc[i, "First Name"])  # insert 'First Name'
            self.model.setData(self.model.index(i, 1), self.datas.df.loc[i, "Last Name"])  # insert 'Last Name'
            self.model.setData(self.model.index(i, 2), ages[i])  # insert 'Age' (from the list)
            self.model.setData(self.model.index(i, 3), self.datas.df.loc[i, "Date"])  # insert 'Date'


class Tabs:
    def __init__(self, parent):
        self.layout = qtw.QVBoxLayout(parent)

        # Initialize tab screen
        self.tabs = qtw.QTabWidget()
        self.tab1 = qtw.QWidget()
        self.tab2 = qtw.QWidget()
        self.tabs.resize(1000, 500)
        self.tabs.setStyleSheet("""QTabBar::tab {border: 1px solid black;background: grey; height: 40px; width: 70px;
                                   border-top-left-radius: 6px;                   
                                   border-top-right-radius: 6px;
                                   border-bottom-left-radius: 6px;}    
                                   QTabWidget::pane {border: 2px solid black;background: white;
                                   border-top-left-radius: 6px;                   
                                   border-top-right-radius: 6px;
                                   border-bottom-left-radius: 6px;}
                                   QTabBar::tab:!selected {margin-top: 2px; background: white}
                                   """)

        # Add tabs
        self.tabs.addTab(self.tab1, "Add worker")
        self.tabs.addTab(self.tab2, "Read from DB")

        # Create first tab
        self.tab1.layout = qtw.QVBoxLayout(parent)
        self.label = qtw.QLabel()

        self.tab1.layout.addWidget(self.label)
        self.tab1.setLayout(self.tab1.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        parent.setLayout(self.layout)


class Tab2:
    def __init__(self, parent):
        self.tab = parent
        self.db = WorkersPropertiesDataBase()

        self.index = None
        self.row_id = None

        self.frame = qtw.QFrame(self.tab)
        # Frame on Tab 2
        self.frame.setFrameShape(qtw.QFrame.StyledPanel)
        self.frame.setGeometry(80, 50, 590, 150)
        self.frame.setStyleSheet("border :1px solid black;")
        self.frame.hide()

        self.label_1 = qtw.QLabel("Mobile", self.tab)
        # Mobile Label settings
        self.label_1.setFont(qtg.QFont('Helvetica', 8))
        self.label_1.setStyleSheet("background-color: White")
        self.label_1.move(115, 163)
        self.label_1.hide()

        self.label_2 = qtw.QLabel("Acces to warehouse", self.tab)
        # Warehouse Label settings
        self.label_2.setFont(qtg.QFont('Helvetica', 8))
        self.label_2.setStyleSheet("background-color: White")
        self.label_2.move(200, 163)
        self.label_2.hide()

        self.dataView2 = qtw.QTreeView(self.tab)
        # TreeView settings on Tab 2
        self.dataView2.setStyleSheet("border :1px solid black")
        self.dataView2.setStyleSheet("background-color: #E0E0E0")
        self.dataView2.setGeometry(80, 50, 590, 110)

        # Button on Tab 2
        self.button_1 = qtw.QPushButton("Load", self.tab)
        # Button settings on Tab 2
        self.button_1.setStyleSheet("background-color: #E0E0E0")
        self.button_1.setGeometry(330, 10, 50, 25)

        self.button_2 = qtw.QPushButton("Send", self.tab)
        # Button settings on Tab 2
        self.button_2.setStyleSheet("background-color: #E0E0E0")
        self.button_2.setGeometry(620, 175, 50, 25)
        self.button_2.hide()

        self.combo = qtw.QComboBox(self.tab)
        self.combo.addItems(["None", "Nokia 3310", "Siemens A40", "Samsung S10"])
        self.combo.setGeometry(81, 179, 100, 20)
        self.combo.hide()

        self.combo2 = qtw.QComboBox(self.tab)
        self.combo2.addItems(["None", "True", "False"])
        self.combo2.setGeometry(200, 179, 100, 20)
        self.combo2.hide()

        self.button_1.clicked.connect(self.set_treeview_box)
        self.dataView2.clicked.connect(self.show_hidden_widgets)
        self.dataView2.clicked.connect(self.get_row)
        self.button_2.clicked.connect(self.send)

    def set_treeview_box(self):
        self.db.show_premission_table()
        # Treeview inbox model in Tab 2
        model = qtg.QStandardItemModel(0, 4)  # the 3 column of the treeview box
        self.dataView2.setModel(model)

        db = self.db.read_from_employees_table()

        model.setHorizontalHeaderLabels(  # Create the treeview box header
            db.columns
        )

        for i in range(len(db)):
            model.insertRow(i)  # make box rows

            model.setData(model.index(i, 0), db['id'].values.tolist()[i])  # insert 'First Name'
            model.setData(model.index(i, 1), db.loc[i, 'firstname'])  # insert 'First Name'
            model.setData(model.index(i, 2), db.loc[i, 'lastname'])  # insert 'Last Name'
            model.setData(model.index(i, 3), db['age'].values.tolist()[i])  # insert 'Age'
            model.setData(model.index(i, 4), db.loc[i, 'date'])  # insert 'Date'

    def get_row(self):
        row = []

        for i in self.dataView2.selectedIndexes():
            row.append(i.data())

        self.row_id = row[0]
        print(self.row_id)

    def show_hidden_widgets(self):
        self.combo.show()
        self.label_1.show()
        self.frame.show()
        self.label_2.show()
        self.combo2.show()
        self.button_2.show()

    def send(self):
        a = self.combo2.currentText()
        b = self.combo.currentText()
        if a != "None":
            print(a)
            print(b)
            print(self.row_id)
            self.db.insert_into_permissions_table(self.row_id, b, a)
            self.db.show_premission_table()
            self.combo.setCurrentText("None")
            self.combo2.setCurrentText("None")
            self.dataView2.reset()
            self.combo.hide()
            self.label_1.hide()
            self.frame.hide()
            self.label_2.hide()
            self.combo2.hide()
            self.button_2.hide()


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.tab = Tabs(self)
        self.tab2 = Tab2(self.tab.tab2)

        # Window settings
        self.HEIGHT = 800
        self.WIDTH = 600
        self.setWindowTitle("Bányász Tamás")
        self.setFixedWidth(self.HEIGHT)
        self.setFixedHeight(self.WIDTH)

        # Frame 1
        self.frame_1 = qtw.QFrame(self.tab.tab1)
        # Frame 1 settings
        self.frame_1.setFrameShape(qtw.QFrame.StyledPanel)
        self.frame_1.setGeometry(20, 20, 360, 130)
        self.frame_1.setStyleSheet("border :1px solid black; border-bottom-left-radius: 6px;"
                                   "border-top-left-radius: 6px;"                   
                                   "border-top-right-radius: 6px;")

        # Frame 2
        self.frame_2 = qtw.QFrame(self.tab.tab1)
        # Frame 2 settings
        self.frame_2.setFrameShape(qtw.QFrame.StyledPanel)
        self.frame_2.setGeometry(400, 20, 360, 130)
        self.frame_2.setStyleSheet("border :1px solid black; border-bottom-left-radius: 6px;"
                                   "border-top-left-radius: 6px;"                   
                                   "border-top-right-radius: 6px;")

        # First Name Label
        self.label_1 = qtw.QLabel("First Name ", self.tab.tab1)
        # First Name Label settings
        self.label_1.setFont(qtg.QFont('Helvetica', 16))
        self.label_1.setStyleSheet("background-color: White")
        self.label_1.move(30, 50)

        # Last Name Label
        self.label_2 = qtw.QLabel("Last Name ", self.tab.tab1)
        # Last Name Label settings
        self.label_2.setFont(qtg.QFont('Arial ', 16))
        self.label_2.setStyleSheet("background-color: White")
        self.label_2.move(30, 80)

        # Age Label
        self.label_3 = qtw.QLabel("Age ", self.tab.tab1)
        # Age Label settings
        self.label_3.setFont(qtg.QFont('Helvetica', 16))
        self.label_3.setStyleSheet("background-color: White")
        self.label_3.move(410, 50)

        # Entry boxes
        self.first_name_entry_box = self.first_name_entry_box()
        self.last_name_entry_box = self.last_name_entry_box()

        # Button
        self.button_1 = qtw.QPushButton("Ok", self.tab.tab1)
        # Button settings
        self.button_1.setStyleSheet("background-color: #E0E0E0")
        self.button_1.setGeometry(185, 120, 50, 25)

        # SpinBox
        self.spin = qtw.QSpinBox(self.tab.tab1)
        # SpinBox settings
        self.spin.setRange(1, 99)  # set the age from 1 to 99
        self.spin.setStyleSheet("background-color: #E0E0E0")
        self.spin.move(410, 90)

        # GroupBox
        self.dataGroupBox = qtw.QGroupBox("Employee", self.tab.tab1)
        # GroupBox settings
        self.dataGroupBox.setStyleSheet("title :2px solid black")
        self.dataGroupBox.setStyleSheet("border :1px solid black; border-bottom-left-radius: 6px;"
                                        "border-top-left-radius: 6px;"                   
                                        "border-top-right-radius: 6px;")
        self.dataGroupBox.setGeometry(75, 200, 600, 130)

        # TreeView
        self.dataView = qtw.QTreeView(self.tab.tab1)
        # TreeView settings
        self.dataView.setStyleSheet("border :1px solid black")
        self.dataView.setStyleSheet("background-color: #E0E0E0")
        self.dataView.setGeometry(80, 215, 590, 110)

        # Treeview inbox model
        self.model = qtg.QStandardItemModel(0, 4)  # the 3 column of the treeview box

        self.dataView.setModel(self.model)
        self.model.setHorizontalHeaderLabels(  # Create the treeview box header
            ["First Name", "Last Name", "Age", "Date"]
        )

        self.set = SetTreeViewBox(self.model)

        self.button_1.clicked.connect(self.click_ok_event)  # Button click

        self.show()

    def first_name_entry_box(self):  # Entry box of the First Name
        first_name_entry = qtw.QLineEdit(self.tab.tab1)
        first_name_entry.setStyleSheet("background-color: White;"
                                       "border :1px solid black; border-bottom-left-radius: 6px;"
                                       "border-top-left-radius: 6px;"
                                       "border-top-right-radius: 6px;"
                                       "border-bottom-right-radius: 6px;"
                                       "border-bottom-left-radius: 6px;"
                                       )
        first_name_entry.move(160, 54)

        return first_name_entry

    def last_name_entry_box(self):  # Entry box of the Last Name
        last_name_entry = qtw.QLineEdit(self.tab.tab1)
        last_name_entry.setStyleSheet("background-color: White;"
                                      "border :1px solid black; border-bottom-left-radius: 6px;"
                                      "border-top-left-radius: 6px;"                   
                                      "border-top-right-radius: 6px;"
                                      "border-bottom-right-radius: 6px;"
                                      "border-bottom-left-radius: 6px;")
        last_name_entry.move(160, 84)

        return last_name_entry

    def clear_the_values(self):
        self.first_name_entry_box.clear()
        self.last_name_entry_box.clear()
        self.spin.setValue(1)

    def click_ok_event(self):

        if self.set.datas.full_name_is_valid(self.first_name_entry_box.text(),
                                             self.last_name_entry_box.text(),
                                             self.spin.value()):

            self.set.clear_treeview_box()
            self.clear_the_values()
            self.set.insert_items_into_treeview_box()

            self.set.datas.df.to_csv('employees.csv', index=False, encoding='utf-8')  # write to csv file

            self.set.datas.database.show_employees_table()


if __name__ == "__main__":
    app = qtw.QApplication([])
    mw = MainWindow()

    app.exec_()
