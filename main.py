import sys
from PyQt5.QtWidgets import QApplication
from Application import Application

# Start the app
app = QApplication(sys.argv)
window = Application()

sys.exit(app.exec_())

