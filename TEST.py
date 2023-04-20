from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import sys


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        # Set up initial data
        data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.load_data(data)

    def load_data(self, data):
        self.table.clearContents()
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data[0]))
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                if j == 0:
                    item.setFlags(item.flags() & ~Qt.ItemIsSelectable)  # Disable selection for first column
                self.table.setItem(i, j, item)


if __name__ == "__main__":
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
