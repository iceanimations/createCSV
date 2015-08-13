'''
Created on Aug 12, 2015

@author: qurban.ali
'''
import sip
sip.setapi('QString', 2)
from site import addsitedir as asd
from PyQt4.QtGui import QApplication
import sys
import _creator as creator

asd('R:/Python_Scripts/plugins')



app = QApplication(sys.argv)
win = creator.Compositor()
win.show()
sys.exit(app.exec_())