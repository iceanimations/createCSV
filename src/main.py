'''
Created on Aug 12, 2015

@author: qurban.ali
'''
import sip
sip.setapi('QString', 2)
from site import addsitedir as asd
asd('R:/Python_Scripts/plugins')
asd('R:/Python_Scripts/plugins/utilities')
asd('R:/Pipe_Repo/Projects/TACTIC')

from PyQt4.QtGui import QApplication, QStyleFactory
import sys
import _creator as creator

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('plastique'))
    global win
    win = creator.Compositor()
    win.show()
    sys.exit(app.exec_())
