'''
Created on Aug 12, 2015

@author: qurban.ali
'''
from site import addsitedir as asd
asd(r'R:\Pipe_Repo\Users\Qurban\utilities')
from PyQt4 import uic
from PyQt4.QtGui import QMessageBox, QFileDialog, qApp
import os.path as osp
import msgBox
import iutil
reload(iutil)
import os
import re
import cui
reload(cui)
import shutil
import csv
import appUsageApp

title = 'Create CSV'

homeDir = osp.join(osp.expanduser('~'), 'create_csv')
if not osp.exists(homeDir):
    os.mkdir(homeDir)

rootPath = iutil.dirname(__file__, depth=2)
uiPath = osp.join(rootPath, 'ui')
iconPath = osp.join(rootPath, 'icons')

Form, Base = uic.loadUiType(osp.join(uiPath, 'main.ui'))
class Compositor(Form, Base):
    '''
    Takes input from the user to create comp and collage
    '''
    def __init__(self, parent=None, data=None):
        super(Compositor, self).__init__(parent)
        self.setupUi(self)
        
        self.setWindowTitle(title)
        self.seqBox = cui.MultiSelectComboBox(self, '--Select Sequences--')
        self.pathLayout.addWidget(self.seqBox)
        
        self.lastPath = ''
        
        self.startButton.clicked.connect(self.start)
        self.browseButton.clicked.connect(self.setPath)
        self.epPathBox.textChanged.connect(self.populateShots)
        self.browseButton2.clicked.connect(self.setCSVPath)
        
        self.progressBar.hide()
        
        appUsageApp.updateDatabase('createCSV')
        
    def setCSVPath(self):
        filename = QFileDialog.getSaveFileName(self, title, self.lastPath, '*.csv')
        if filename:
            self.lastPath = osp.dirname(filename)
            self.csvPathBox.setText(filename)
        
    def getStartEnd(self, seqPath, shot):
        path = osp.join(seqPath, shot, 'animatic')
        files = os.listdir(path)
        if files:
            rng = self.getRange(files)
            if rng:
                return min(rng), max(rng)
        return 0, 0
    
    def getRange(self, files):
        rng = []
        for phile in files:
            try:
                rng.append(int(phile.split('.')[-2]))
            except:
                pass
        return rng
        
    def start(self):
        try:
            for directory in os.listdir(homeDir):
                path = osp.join(homeDir, directory)
                if osp.isdir(path):
                    shutil.rmtree(path)
        except Exception as ex:
            self.showMessage(msg=str(ex),
                             icon=QMessageBox.Critical)
            return
        try:
            seqPath = self.getEpPath()
            if seqPath:
                sequences = self.seqBox.getSelectedItems()
                if not sequences:
                    sequences = self.seqBox.getItems()
                csvfile = self.getCSVPath()
                if csvfile:
                    with open(csvfile, 'wb') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(['Sequence', 'Shot', 'In', 'Out', 'Frames', 'Seconds', 'TEAM'])
                        self.progressBar.show()
                        length = len(sequences)
                        for i, seq in enumerate(sequences):
                            self.setStatus('Creating %s (%s of %s)'%(seq, i+1, length))
                            shotsPath = osp.join(seqPath, seq, 'SHOTS')
                            #writer.writerow([seq] + [''] * 6)
                            shots = os.listdir(shotsPath)
                            self.progressBar.setMaximum(len(shots))
                            for j, shot in enumerate(shots):
                                if re.match('SQ\d+_SH\d+', shot):
                                    rng = self.getStartEnd(shotsPath, shot)
                                    frames = rng[1] - rng[0]
                                    seconds = frames/25.0
                                    writer.writerow([seq, shot, rng[0], rng[1], frames, seconds, ''])
                                    self.progressBar.setValue(j+1)
        except Exception as ex:
            self.showMessage(msg=str(ex), icon=QMessageBox.Critical)
        finally:
            self.progressBar.setMaximum(0)
            self.progressBar.setValue(0)
            self.progressBar.hide()
            self.setStatus('')
            
                        
    def getCSVPath(self):
        path = self.csvPathBox.text()
        if (not path or not osp.exists(osp.dirname(path))):
            self.showMessage(msg='The system could not find the path specified\n%s'%path,
                             icon=QMessageBox.Information)
            path = ''
        return path
        
    def setStatus(self, msg):
        self.statusLabel.setText(msg)
        qApp.processEvents()
    
    def setPath(self):
        filename = QFileDialog.getExistingDirectory(self, title, self.lastPath,
                                                    QFileDialog.ShowDirsOnly)
        if filename:
            self.lastPath = filename
            self.epPathBox.setText(filename)

    def showMessage(self, **kwargs):
        return cui.showMessage(self, title=title, **kwargs)
            
    def getEpPath(self, msg=True):
        path = self.epPathBox.text()
        if (not path or not osp.exists(path)) and msg:
            self.showMessage(msg='The system could not find the path specified\n%s'%path,
                             icon=QMessageBox.Information)
            path = ''
        return path
    
    def populateShots(self):
        path = self.getEpPath(msg=False)
        if path:
            sequences = [seq for seq in os.listdir(path) if re.match('SQ\d+', seq)]
            self.seqBox.addItems(sequences)
    
    def closeEvent(self, event):
        self.deleteLater()
        event.accept()