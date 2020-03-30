from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import *
import sys
import pafy
import humanize

import os
import os.path
import urllib.request
from PyQt5.uic import loadUiType

ui, _ = loadUiType('main.ui')


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.init_ui()
        self.handle_buttons()

    def init_ui(self):
        self.tabWidget.tabBar().setVisible(False)
        self.move_box_1()

    def handle_buttons(self):
        self.pushButton.clicked.connect(self.download)
        self.pushButton_2.clicked.connect(self.handle_browse)
        self.pushButton_5.clicked.connect(self.get_video_data)
        self.pushButton_4.clicked.connect(self.download_video)
        self.pushButton_3.clicked.connect(self.save_browse)
        self.pushButton_7.clicked.connect(self.playlist_download)
        self.pushButton_6.clicked.connect(self.playlist_save_browse)
        self.pushButton_8.clicked.connect(self.open_home)
        self.pushButton_11.clicked.connect(self.open_download)
        self.pushButton_10.clicked.connect(self.open_youtube)
        self.pushButton_9.clicked.connect(self.open_settings)
        self.pushButton_12.clicked.connect(self.apply_dark_orange_style)
        self.pushButton_13.clicked.connect(self.apply_dark_style)
        self.pushButton_14.clicked.connect(self.apply_dark_gray_style)
        self.pushButton_15.clicked.connect(self.apply_dark_blue_style)

    def handle_progress(self, block_num, block_size, total_size):
        # calculate the progress
        read_data = block_num * block_size
        QApplication.processEvents()

        if total_size > 0:
            download_percentage = read_data * 100 / total_size
            self.progressBar.setValue(download_percentage)

    def handle_browse(self):
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        self.lineEdit_2.setText(str(save_location[0]))

    def download(self):
        download_url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()

        if download_url == '' or save_location == '':
            QMessageBox.warning(self, "Data error", "Please provide a valid URL or storage location")
        else:
            try:
                urllib.request.urlretrieve(download_url, save_location, self.handle_progress)
            except Exception:
                QMessageBox.warning(self, "Data error", "Please provide a valid URL or storage location")
                return

        QMessageBox.information(self, "Download Completed", "The download completed successfully")
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.progressBar.setValue(0)

    # download single video from youtube

    def get_video_data(self):
        video_url = self.lineEdit_3.text()
        if video_url == '':
            QMessageBox.information(self, "Data error", "Please provide a valid video URL")
        else:
            video = pafy.new(video_url)
            print(video.title)
            print(video.duration)

            video_streams = video.streams
            for stream in video_streams:
                size = humanize.naturalsize(stream.get_filesize())
                data = '{} {} {} {}'.format(stream.mediatype, stream.extension, stream.quality, size)
                self.comboBox.addItem(data)

    def download_video(self):
        video_url = self.lineEdit_3.text()
        save_location = self.lineEdit_4.text()

        if video_url == '' or save_location == '':
            QMessageBox.warning(self, "Data error", "Please provide a valid URL or storage location")
        else:
            try:
                video = pafy.new(video_url)
                video_stream = video.streams
                video_quality = self.comboBox.currentIndex()
                download = video_stream[video_quality].download(filepath=save_location, callback=self.video_progress)

            except Exception:
                QMessageBox.warning(self, "Data error", "Please provide a valid URL or storage location")
                return

    def video_progress(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            download_percentage = read_data * 100 / total
            self.progressBar_2.setValue(download_percentage)
            remaining_time = round(time/60, 2)

            self.label_5.setText(str('{} minutes remaining'.format(remaining_time)))
            QApplication.processEvents()

    def save_browse(self):
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        self.lineEdit_4.setText(str(save_location[0]))

    # playlist download section
    def playlist_download(self):
        playlist_url = self.lineEdit_5.text()
        save_location = self.lineEdit_6.text()

        if playlist_url == '' or save_location == '':
            QMessageBox.warning(self, "Data error", "Please provide a valid URL or storage location!!!")
        else:
            # try:
            playlist = pafy.get_playlist(playlist_url)

            playlist_videos = playlist['items']
            print(len(playlist_videos))
            self.label_6.setText(str(len(playlist_videos)))

            os.chdir(save_location)
            if os.path.exists(str(playlist['title'])):
                os.chdir(str(playlist['title']))

            else:
                os.mkdir(str(playlist['title']))
                os.chdir(str(playlist['title']))

            current_video_in_download = 1
            quality = self.comboBox_2.currentIndex()
            QApplication.processEvents()

            for video in playlist_videos:
                current_video = video['pafy']
                current_video_stream = current_video.videostreams
                print(current_video_stream)
                self.label_7.setText(str(current_video_in_download))
                download = current_video_stream[quality].download(callback=self.playlist_progress)
                QApplication.processEvents()

                current_video_in_download += 1

            # except Exception:
            #     QMessageBox.warning(self, "Data error", "Please provide a valid URL or storage location")
            #     return

    def playlist_progress(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            download_percentage = read_data * 100 / total
            self.progressBar_3.setValue(download_percentage)
            remaining_time = round(time / 60, 2)

            self.label_8.setText(str('{} minutes remaining'.format(remaining_time)))
            QApplication.processEvents()

    def playlist_save_browse(self):
        save_location = QFileDialog.getExistingDirectory(self, "Select existing directory")
        self.lineEdit_6.setText(str(save_location[0]))

    # UI changed methods
    def open_home(self):
        self.tabWidget.setCurrentIndex(0)

    def open_download(self):
        self.tabWidget.setCurrentIndex(2)

    def open_youtube(self):
        self.tabWidget.setCurrentIndex(1)

    def open_settings(self):
        self.tabWidget.setCurrentIndex(3)

    # App themes
    def apply_dark_orange_style(self):
        style = open("themes/qdarkorange.css",'r')
        style = style.read()
        self.setStyleSheet(style)

    def apply_dark_style(self):
        style = open("themes/qdark.css", 'r')
        style = style.read()
        self.setStyleSheet(style)

    def apply_dark_gray_style(self):
        style = open("themes/qdarkgray.css", 'r')
        style = style.read()
        self.setStyleSheet(style)

    def apply_dark_blue_style(self):
        style = open("themes/qwhite.css", 'r')
        style = style.read()
        self.setStyleSheet(style)

    # App Animations

    def move_box_1(self):
        box_animation = QPropertyAnimation(self.groupBox, b"geometry")
        box_animation.setDuration(1000)
        box_animation.setStartValue(QRect(0, 0, 0, 0))
        box_animation.setStartValue(QRect(20, 20, 261, 151))
        box_animation.start()
        self.box_animation = box_animation


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
