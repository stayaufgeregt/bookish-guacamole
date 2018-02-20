import sys
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(500,500)
    w.move(300, 300)
    w.setWindowTitle('Projet Anglais avec le point bonus')
    w.show()
    
    sys.exit(app.exec_())