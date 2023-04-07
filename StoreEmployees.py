import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.HEIGHT = 800
        self.WIDTH = 600
        self.setWindowTitle("Bányász Tamás")
        self.setFixedWidth(self.HEIGHT)
        self.setFixedHeight(self.WIDTH)

        # Frames
        self.frame_1 = qtw.QFrame(self)
        self.frame_1.setFrameShape(qtw.QFrame.StyledPanel)
        self.frame_1.setGeometry(20, 20, 360, 130)
        self.frame_1.setStyleSheet("border :1px solid black")

        self.frame_2 = qtw.QFrame(self)
        self.frame_2.setFrameShape(qtw.QFrame.StyledPanel)
        self.frame_2.setGeometry(400, 20, 360, 130)
        self.frame_2.setStyleSheet("border :1px solid black")

        # First Name Label
        self.label_1 = qtw.QLabel("First Name ", self)
        self.label_1.setFont(qtg.QFont('Helvetica', 16))
        self.label_1.setStyleSheet("background-color: White")
        self.label_1.move(30, 50)

        self.label_2 = qtw.QLabel("Last Name ", self)
        self.label_2.setFont(qtg.QFont('Arial ', 16))
        self.label_2.setStyleSheet("background-color: White")
        self.label_2.move(30, 80)

        # Last Name Label
        self.label_3 = qtw.QLabel("Age ", self)
        self.label_3.setFont(qtg.QFont('Helvetica', 16))
        self.label_3.setStyleSheet("background-color: White")
        self.label_3.move(410, 50)

        # Entry boxes
        self.entry_1 = qtw.QLineEdit(self)
        self.entry_1.setStyleSheet("background-color: White")
        self.entry_1.move(160, 54)

        self.entry_2 = qtw.QLineEdit(self)
        self.entry_2.setStyleSheet("background-color: White")
        self.entry_2.move(160, 84)

        # Button
        self.button_1 = qtw.QPushButton("Ok", self)
        self.button_1.setStyleSheet("background-color: #E0E0E0")
        self.button_1.setGeometry(200, 110, 50, 30)

        # SpinBox
        self.spin = qtw.QSpinBox(self)
        self.spin.setRange(1, 99)
        self.spin.setStyleSheet("background-color: #E0E0E0")
        self.spin.move(410, 90)

        # GroupBox
        self.dataGroupBox = qtw.QGroupBox("Employee", self)
        self.dataGroupBox.setStyleSheet("title :2px solid black")
        self.dataGroupBox.setStyleSheet("border :2px solid black")
        self.dataGroupBox.setGeometry(50, 200, 600, 130)

        # TreeView
        self.dataView = qtw.QTreeView(self)
        self.dataView.setStyleSheet("border :1px solid black")
        self.dataView.setStyleSheet("background-color: #E0E0E0")
        self.dataView.setGeometry(55, 215, 590, 110)

        self.model = qtg.QStandardItemModel(0, 3)
        self.dataView.setModel(self.model)
        self.model.setHorizontalHeaderLabels(
            ["First Name", "Last Name", "Age"]
        )
        self.model.insertRow(0)
        self.model.setData(self.model.index(0, 0), "Hehe")
        self.model.setData(self.model.index(0, 1), "Haha")
        self.model.setData(self.model.index(0, 2), 99)

        self.button_1.clicked.connect(self.click)

        self.show()

    def click(self):
        print(self.entry_1.text())
        self.entry_1.clear()
        print(self.spin.value())
        self.spin.setValue(1)

if __name__ == "__main__":
    app = qtw.QApplication([])

    mw = MainWindow()
    app.exec_()


