'''
Copyright (C) 2018 Palash Parmar - All Rights Reserved

You may use, and modify this code under the
terms of the generating data for research purpose.

Redistribution of this software is not allowed without
prior notice.
'''


import cv2
import sys
import csv
import os
import pickle
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import  QTimer, QCoreApplication, QUrl, QDateTime
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QVBoxLayout, QInputDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon

n = ''

class videoViewer(QDialog):
    def __init__(self):
        super(videoViewer,self).__init__()

        loadUi('..\gui\viewer.ui',self)
        self.setWindowTitle('Recorded Videos')
        self.setWindowIcon(QIcon('..\resources\icon.png'))
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget(self)
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.videoWidget.setLayout(layout)

        self.userPath = os.path.join(os.getcwd(),'..\data')
        userList = [o for o in os.listdir(self.userPath) if os.path.isdir(os.path.join(self.userPath,o))]
        self.list1.addItems(userList)
        self.list1.itemClicked.connect(self.loadFile)
        self.playButton.clicked.connect(self.play)
        self.pauseButton.clicked.connect(self.pause)
        self.stopButton.clicked.connect(self.stop)
        self.exitButton.clicked.connect(self.exit)
        self.playButton.setEnabled(False)
        self.pauseButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.understanding1.setText('-')
        self.understanding2.setText('-')
        self.data = pickle.load(open('..\data\data.pkl','rb'))
        self.mediaPlayer.mediaStatusChanged.connect(self.mediaStatusfn)

    def mediaStatusfn(self):
        if self.mediaPlayer.position()==self.mediaPlayer.duration():
            self.mediaPlayer.stop()




    def updateFrame(self):

        currentFrame = round(self.mediaPlayer.position()*30/1000)
        totalFrame = round(self.mediaPlayer.duration()*30/1000)
        if currentFrame>totalFrame:
            self.timer.stop()
            self.mediaPlayer.stop()
        else:
            if self.understandingData[self.i][0]<currentFrame and self.i<len(self.understandingData)-1:
                self.i += 1
                self.understanding1.setText(str(self.understandingData[self.i][1]))
                self.understanding2.setText(str(self.understandingData[self.i][1]))


    def play(self):
        self.mediaPlayer.play()
        self.pauseButton.setEnabled(True)
        self.playButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.timer.start(30)


    def pause(self):
        self.mediaPlayer.pause()
        self.playButton.setEnabled(True)
        self.pauseButton.setEnabled(False)
        self.timer.stop()

    def stop(self):
        self.mediaPlayer.stop()
        self.playButton.setEnabled(True)
        self.pauseButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.timer.stop()

    def exit(self):
        self.close()

    def loadFile(self, item):
        self.filePath = os.path.join(self.userPath,item.text())
        fileList = [o for o in os.listdir(self.filePath) if not os.path.isdir(os.path.join(self.filePath,o))]
        self.list2.clear()
        self.list2.addItems(fileList)
        self.list2.itemClicked.connect(self.playFile)

    def playFile(self, item):
        if (os.path.splitext(item.text())[-1].lower()=='.avi'):
            self.fileLabel.setText(item.text())
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.join(self.filePath,item.text()))))
            for file, understanding in self.data.items():
                if os.path.basename(file)==item.text():
                    self.understandingData = understanding
                    break
            self.playButton.setEnabled(True)
            self.pauseButton.setEnabled(False)
            self.stopButton.setEnabled(False)
            self.i = 0




class task1(QDialog):
    def __init__(self, nam):
        super(task1,self).__init__()
        loadUi('..\gui\task.ui',self)
        self.setWindowTitle('Activity Recorder')
        self.setWindowIcon(QIcon('..\resources\icon.png'))
        self.image = None
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget(self)
        self.recording = False
        self.start_webcam.clicked.connect(self.startWebcam)
        self.stop_webcam.clicked.connect(self.stopWebcam)
        self.exit.clicked.connect(self.exitClicked)
        self.playStatus = 'Pause'

        self.nameLabel.setText(nam)
        self.name = nam
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.widget.setLayout(layout)
        self.cwd = os.getcwd()
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.cwd+"..\lecture_videos\lecture.mp4")))
        self.webcamEnabled = 0
        self.frame = 0
        self.markerArr = []
        self.c0.stateChanged.connect(lambda: self.checkClick(0,self.c0))
        self.c1.stateChanged.connect(lambda: self.checkClick(1,self.c1))
        self.c2.stateChanged.connect(lambda: self.checkClick(2,self.c2))
        self.c3.stateChanged.connect(lambda: self.checkClick(3,self.c3))
        self.c4.stateChanged.connect(lambda: self.checkClick(4,self.c4))
        self.c5.stateChanged.connect(lambda: self.checkClick(5,self.c5))
        self.c6.stateChanged.connect(lambda: self.checkClick(6,self.c6))
        self.c7.stateChanged.connect(lambda: self.checkClick(7,self.c7))
        self.c8.stateChanged.connect(lambda: self.checkClick(8,self.c8))
        self.c9.stateChanged.connect(lambda: self.checkClick(9,self.c9))
        self.capture = None
        self.out = None

        self.recordedVideo.clicked.connect(self.videoViewerLaunch)

    def videoViewerLaunch(self):
        num,  ok = QInputDialog.getText(self, "Verify yourself","Enter Password")
        if ok and num=='a':
            viewWindow = videoViewer()
            viewWindow.show()
            viewWindow.exec_()
        elif ok and num!='a':
            QMessageBox.critical(self, 'Error', "wrong password..", QMessageBox.Ok)



    def checkClick(self,n,checkItem):
        if checkItem.isChecked():
            self.markerArr.append([self.frame,n])

    def exitClicked(self):
        result = QMessageBox.question(self, 'Message', "Are you sure?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.Yes:
            if self.capture != None:
                self.capture.release()
                self.timer.stop()
            self.mediaPlayer.stop()
            if self.out != None:
                self.out.release()
            self.close()


    def startWebcam(self):
        self.exit.setEnabled = False
        if self.webcamEnabled == 0:
            self.savedir = self.cwd+"..\data\\"+self.name
            if not os.path.exists(self.savedir):
                os.mkdir(self.savedir)
            self.fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
            self.outputFile = self.savedir+"\\"+str(QDateTime.currentMSecsSinceEpoch())+".avi"
            self.out = cv2.VideoWriter(self.outputFile, self.fourcc, 30.0, (640,480))
            self.capture = cv2.VideoCapture(0)
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,640)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
            self.webcamEnabled = 1
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.updateFrame)



        self.start_webcam.setText(self.playStatus)
        if self.playStatus=='Play':
            self.playStatus = 'Pause'
            self.mediaPlayer.pause()
            self.timer.stop()
            self.recording = False
        else:
            self.playStatus = 'Play'
            self.mediaPlayer.play()
            self.timer.start(5)
            self.recording = True
        self.stop_webcam.setEnabled(True)





    def updateFrame(self):
        ret, image = self.capture.read()

        if ret==True:
            image = cv2.flip(image,1)

            if self.recording == True:
                self.out.write(image)
                self.frame += 1
        else:
            self.stopWebcam()
            QMessageBox.critical(self, 'Error', "Error opening webcam", QMessageBox.Ok)

    def saveCSV(self):
        try:
            data = pickle.load(open('..\data\data.pkl','rb'))
        except FileNotFoundError:
            data = {}

        data[self.outputFile] = self.markerArr

        pickle.dump(data,open('..\data\data.pkl','wb'))






    def stopWebcam(self):
        self.webcamEnabled = 0
        self.timer.stop()
        self.saveCSV()
        self.capture.release()
        self.start_webcam.setText('Play')
        self.playStatus = 'Pause'
        self.stop_webcam.setEnabled(False)
        self.mediaPlayer.stop()
        self.recording = False
        self.out.release()
        self.exit.setEnabled = True


class login(QDialog):
    def __init__(self):
        super(login,self).__init__()
        loadUi('login.ui',self)
        self.okButton.clicked.connect(self.login)
        self.exitButton.clicked.connect(QCoreApplication.instance().quit)

    def login(self):
        global n
        n = self.nameText.text()
        self.accept()





app = QApplication(sys.argv)
loginWindow = login()
loginWindow.setWindowTitle('Activity Recorder')
loginWindow.setWindowIcon(QIcon('..\resources\icon.png'))
loginWindow.show()

if loginWindow.exec_() == QDialog.Accepted:
    window = task1(n)
    window.show()
    sys.exit(app.exec_())
