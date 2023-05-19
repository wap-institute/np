import sys
import subprocess
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QFileDialog,
    QSlider,
    QMessageBox
)
from util.widget import (
    Button,
    HLayout,
    VLayout,
    Text,
    IconButton
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon

class Window(QMainWindow) : 
    def __init__(self) : 
        super().__init__()
        icon = QIcon("icons/app.png")
        self.setFixedSize(800,700)
        self.setWindowTitle("Music 0.0.1")
        self.setWindowIcon(icon)
        layout = VLayout([
            self.header(),
            self.footer()
        ])
        layout.setContentsMargins(0,0,0,0)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.player = QMediaPlayer()
        self.player.mediaStatusChanged.connect(self.mediaStatus)
        self.player.positionChanged.connect(self.playedDuration)

    def getLatestVersion(self):
        subprocess.run(['git', 'fetch'])
        subprocess.run(['git', 'reset', '--hard', 'origin/master'])

    def checkForUpdate(self):
        self.getLatestVersion()
        result = subprocess.run(['git', 'status', '-uno'], capture_output=True, text=True)
        if 'master' in result.stdout:
            reply = QMessageBox.question(self, 'Update Available', 'An update is available. Do you want to download and install it?', 
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                subprocess.run(['git', 'pull'])
                QMessageBox.information(self, 'Update', 'Update downloaded and installed successfully. Please restart the application.')
        else:
            QMessageBox.information(self, 'No Updates', 'No updates available.')


    def header(self) : 
        widget = QWidget()
        widget.setFixedHeight(500)
        widget.setStyleSheet("background-color: #FF4F00")
        self.title = Text("Choose a song !",widget,40,'Open Sans')
        self.title.move(150,150)
        btn = Button("Update",widget)
        btn.clicked.connect(self.checkForUpdate)
        return widget
    
    def footer(self) : 
        widget = QWidget()
        self.timestamp = Text("0.0",widget)
        self.timestamp.move(10,50)

        slash = Text("/",widget)
        slash.move(50,50)

        self.duration = Text("0.0",widget)
        self.duration.move(65,50)

        self.volumeIcon = IconButton("icons/volume.png",None,50,50)
        self.volumeIcon.setStyleSheet("background-color: white; border-radius: 25px;border: 1px solid #ddd")
        self.volumeIcon.clicked.connect(self.volume)

        bkIcon = IconButton("icons/bk.png",None,50,50)
        bkIcon.setStyleSheet("background-color: white; border-radius: 25px;border: 1px solid #ddd")
        bkIcon.clicked.connect(self.backward)

        self.playIcon = IconButton("icons/play.png",None,100,100)
        self.playIcon.setStyleSheet("background-color: white; border-radius: 50px;border: 1px solid #ddd")
        self.playIcon.clicked.connect(self.toggleMusic)

        fwIcon = IconButton("icons/fw.png",None,50,50)
        fwIcon.setStyleSheet("background-color: white; border-radius: 25px;border: 1px solid #ddd")
        fwIcon.clicked.connect(self.forward)

        stopIcon = IconButton("icons/stop.png",None,50,50)
        stopIcon.setStyleSheet("background-color: white; border-radius: 25px;border: 1px solid #ddd")
        stopIcon.clicked.connect(self.stop)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setGeometry(50,50,200,30)
        self.slider.sliderMoved.connect(self.onSlide)
        self.slider.sliderReleased.connect(self.sliderLeave)

        layout = HLayout([
            self.volumeIcon,
            bkIcon,
            self.playIcon,
            fwIcon,
            stopIcon
        ])
        layout.setContentsMargins(0,20,0,0)
        alignLayout = VLayout([
            self.slider
        ])
        alignLayout.addLayout(layout)
        widget.setFixedHeight(200)
        widget.setStyleSheet("background-color: #f5f5f5")
        widget.setLayout(alignLayout)
        return widget

    def upload(self) : 
        path = QFileDialog.getOpenFileName(self,"Choose a file","","Audio File (*.mp3 *.ogg *.wav)")
        if path : 
            content = QMediaContent(QUrl.fromLocalFile(path[0]))
            self.player.setMedia(content)
            self.player.play()
            if self.player.state() == QMediaPlayer.PlayingState : 
                filename = os.path.basename(path[0])
                self.playIcon.setIcon(QIcon("icons/pause.png"))
                self.title.setText(filename)

    def toggleMusic(self) : 
        if self.player.mediaStatus() == QMediaPlayer.NoMedia : 
            self.upload()
            return False
        if self.player.state() == QMediaPlayer.PlayingState : 
            self.player.pause()
            self.playIcon.setIcon(QIcon("icons/play.png"))
        elif self.player.state() == QMediaPlayer.PausedState : 
            self.player.play()
            self.playIcon.setIcon(QIcon("icons/pause.png"))
        else : 
            self.player.play()
            self.playIcon.setIcon(QIcon("icons/pause.png"))

    def stop(self) : 
        if self.player.state() == QMediaPlayer.PlayingState : 
            self.player.stop()
            self.player.setPosition(0)
            self.player.setMedia(QMediaContent())
            self.playIcon.setIcon(QIcon("icons/play.png"))

    def volume(self) : 
        if self.player.isMuted() : 
            self.player.setMuted(False)
            self.volumeIcon.setIcon(QIcon("icons/volume.png"))
        else : 
            self.player.setMuted(True)
            self.volumeIcon.setIcon(QIcon("icons/mute.png"))


    def forward(self) : 
        currentDuration = self.player.position() + 10000
        self.player.setPosition(currentDuration)
        currentSlideValue = self.slider.value()
        self.slider.setValue(currentSlideValue+10)

    def backward(self) : 
        currentDuration = max(self.player.position() - 10000,0)
        self.player.setPosition(currentDuration)
        currentSlideValue = self.slider.value()
        self.slider.setValue(currentSlideValue-10)
        
    def onSlide(self,value) : 
        self.player.setPosition(value)
        self.player.setMuted(True)

    def sliderLeave(self) : 
        self.player.setMuted(False)

    def mediaStatus(self,status) : 
        if status == QMediaPlayer.BufferedMedia : 
            duration = self.player.duration()
            minute = round(duration/60000,1)
            self.duration.setText(str(minute))
            self.slider.setMaximum(duration)

    def playedDuration(self,position) : 
        minute = round(position/60000,1)
        self.timestamp.setText(str(minute))
        self.slider.setValue(position)
        if self.player.state() == 0 : 
            self.player.setPosition(0)
            self.playIcon.setIcon(QIcon("icons/play.png"))

if __name__ == "__main__" : 
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())