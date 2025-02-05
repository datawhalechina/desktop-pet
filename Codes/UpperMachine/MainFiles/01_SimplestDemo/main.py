import sys

from PyQt5.QtWidgets import QApplication

from Tools.Windows.petchatbox import PetChatBox

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = PetChatBox()
    sys.exit(app.exec_())
