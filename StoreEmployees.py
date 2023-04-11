import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import pandas as pd
from abc import abstractmethod


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


class NameValid(MessageBox):

    def first_name_is_valid(self, first_name):
        if not first_name.isalpha():
            self.incorrect_first_name(first_name)
        return first_name.isalpha()

    def last_name_is_valid(self, last_name):
        if not last_name.isalpha():
            self.incorrect_last_name(last_name)
        return last_name.isalpha()

    @abstractmethod
    def full_name_is_valid(self, first_name, last_name, age):
        return self.first_name_is_valid(first_name) and self.last_name_is_valid(last_name)


class GetEmployeesData(NameValid):
    def __init__(self):
        super().__init__()
        self.df = pd.DataFrame(columns=["First Name", "Last Name", "Age"])  # DataFrame to store employee datas

    def set_datas(self, firstname, lastname, age):  # add new employee datas to DataFrame
        self.df.loc[len(self.df.index)] = [firstname, lastname, age]

    def full_name_is_valid(self, first_name, last_name, age):
        if super().full_name_is_valid(first_name, last_name, age):
            self.set_datas(first_name, last_name, age)


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        # Window settings
        self.HEIGHT = 800
        self.WIDTH = 600
        self.setWindowTitle("Bányász Tamás")
        self.setFixedWidth(self.HEIGHT)
        self.setFixedHeight(self.WIDTH)

        # Frame 1
        self.frame_1 = qtw.QFrame(self)
        # Frame 1 settings
        self.frame_1.setFrameShape(qtw.QFrame.StyledPanel)
        self.frame_1.setGeometry(20, 20, 360, 130)
        self.frame_1.setStyleSheet("border :1px solid black")

        # Frame 2
        self.frame_2 = qtw.QFrame(self)
        # Frame 2 settings
        self.frame_2.setFrameShape(qtw.QFrame.StyledPanel)
        self.frame_2.setGeometry(400, 20, 360, 130)
        self.frame_2.setStyleSheet("border :1px solid black")

        # First Name Label
        self.label_1 = qtw.QLabel("First Name ", self)
        # First Name Label settings
        self.label_1.setFont(qtg.QFont('Helvetica', 16))
        self.label_1.setStyleSheet("background-color: White")
        self.label_1.move(30, 50)

        # Last Name Label
        self.label_2 = qtw.QLabel("Last Name ", self)
        # Last Name Label settings
        self.label_2.setFont(qtg.QFont('Arial ', 16))
        self.label_2.setStyleSheet("background-color: White")
        self.label_2.move(30, 80)

        # Age Label
        self.label_3 = qtw.QLabel("Age ", self)
        # Age Label settings
        self.label_3.setFont(qtg.QFont('Helvetica', 16))
        self.label_3.setStyleSheet("background-color: White")
        self.label_3.move(410, 50)

        # Entry boxes
        self.first_name_entry_box = self.first_name_entry_box()
        self.last_name_entry_box = self.last_name_entry_box()

        # Button
        self.button_1 = qtw.QPushButton("Ok", self)
        # Button settings
        self.button_1.setStyleSheet("background-color: #E0E0E0")
        self.button_1.setGeometry(200, 110, 50, 30)

        # SpinBox
        self.spin = qtw.QSpinBox(self)
        # SpinBox settings
        self.spin.setRange(1, 99)  # set the age from 1 to 99
        self.spin.setStyleSheet("background-color: #E0E0E0")
        self.spin.move(410, 90)

        # GroupBox
        self.dataGroupBox = qtw.QGroupBox("Employee", self)
        # GroupBox settings
        self.dataGroupBox.setStyleSheet("title :2px solid black")
        self.dataGroupBox.setStyleSheet("border :2px solid black")
        self.dataGroupBox.setGeometry(50, 200, 600, 130)

        # TreeView
        self.dataView = qtw.QTreeView(self)
        # TreeView settings
        self.dataView.setStyleSheet("border :1px solid black")
        self.dataView.setStyleSheet("background-color: #E0E0E0")
        self.dataView.setGeometry(55, 215, 590, 110)

        # Treeview inbox model
        self.model = qtg.QStandardItemModel(0, 3)  # the 3 column of the treeview box

        self.dataView.setModel(self.model)
        self.model.setHorizontalHeaderLabels(  # Create the treeview box header
            ["First Name", "Last Name", "Age"]
        )


        self.datas = GetEmployeesData()

        self.button_1.clicked.connect(self.click_ok_event)  # Button click

        self.show()

    def first_name_entry_box(self):  # Entry box of the First Name
        first_name_entry = qtw.QLineEdit(self)
        first_name_entry.setStyleSheet("background-color: White")
        first_name_entry.move(160, 54)

        return first_name_entry

    def last_name_entry_box(self):  # Entry box of the Last Name
        last_name_entry = qtw.QLineEdit(self)
        last_name_entry.setStyleSheet("background-color: White")
        last_name_entry.move(160, 84)

        return last_name_entry

    def clear_treeview_box(self):  # clear the treeview box for the new datas
        for i in range(len(self.datas.df)):
            self.model.removeRows(i, len(self.datas.df))

    def clear_the_values(self):
        self.first_name_entry_box.clear()
        self.last_name_entry_box.clear()
        self.spin.setValue(1)

    def insert_items_into_treeview_box(self):

        ages = self.datas.df['Age'].values.tolist()  # store 'Age' values in classic list because the type of the DataFrame column is 'numpy.integer' and it couldnt display
        print(self.datas.df['First Name'])
        for i in range(len(self.datas.df)):
            self.model.insertRow(i)  # make box rows

            self.model.setData(self.model.index(i, 0), self.datas.df.loc[i, "First Name"])  # insert 'First Name'
            self.model.setData(self.model.index(i, 1), self.datas.df.loc[i, "Last Name"])     # insert 'Last Name'
            self.model.setData(self.model.index(i, 2), ages[i])  # insert 'Age' (from the list)

    def click_ok_event(self):

        self.clear_treeview_box()

        self.datas.full_name_is_valid(self.first_name_entry_box.text(),
                                      self.last_name_entry_box.text(),
                                      self.spin.value())

        self.clear_the_values()

        self.insert_items_into_treeview_box()


if __name__ == "__main__":
    app = qtw.QApplication([])

    mw = MainWindow()
    app.exec_()
