import sys
from PySide2.QtUiTools import QUiLoader #allows us to import .ui files
from PySide2.QtWidgets import QApplication, QLineEdit, QListWidget, QPushButton, QFileDialog, QAction, QSlider
from PySide2.QtCore import QFile, QObject, QUrl
from PySide2.QtMultimedia import QMediaPlayer

class MainWindow(QObject):

    #class constructor
    def __init__(self, ui_file, parent=None):

        #reference to our music player
        self.music_player = QMediaPlayer()
        self.music_player.setVolume(100)
        self.music_player.positionChanged.connect(self.position_changed)
        self.music_player.durationChanged.connect(self.duration_changed)
        #call parent QObject constructor
        super(MainWindow, self).__init__(parent)

        #load the UI file into Python
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        
        #always remember to close files
        ui_file.close()

        #add event listeners
        open_action = self.window.findChild(QAction, 'action_open')
        open_action.triggered.connect(self.open_action_triggered)

        quit_action = self.window.findChild(QAction, 'action_quit')
        quit_action.triggered.connect(self.quit_action_triggered)

        play_button = self.window.findChild(QPushButton, 'play_button')
        play_button.clicked.connect(self.play_button_clicked)

        pause_button = self.window.findChild(QPushButton, 'pause_button')
        pause_button.clicked.connect(self.pause_button_clicked)

        toggle_forward = self.window.findChild(QPushButton, 'toggle_forward')
        toggle_forward.clicked.connect(self.toggle_forward_function)

        self.progress_bar = self.window.findChild(QSlider, 'progress_bar')
        self.progress_bar.sliderMoved.connect(self.set_position)

        # toggle_back = self.window.findChild(QPushButton, 'toggle_back')
        # toggle_back.clicked.connect(self.toggle_back_function)

        self.song_library = self.window.findChild(QListWidget, 'song_library')

       	
       	#self.song_library.addItem(1, "videogame.mp3")

        self.volume_slider = self.window.findChild(QSlider, 'volume_slider')
        self.volume_slider.valueChanged.connect(self.volume_control)

        self.volume_slider.setMinimum(1)
        self.volume_slider.setMaximum(90)
        self.volume_slider.setValue(25)
        self.volume_slider.setTickInterval(10)
        self.volume_slider.setTickPosition(QSlider.TicksBelow)

        #show window to user
        self.window.show()

    def open_action_triggered(self):
        file_name = QFileDialog.getOpenFileName(self.window)
        self.music_player.setMedia(QUrl.fromLocalFile(file_name[0]))

    def position_changed(self, position):
    	self.progress_bar.setValue(position)

    def duration_changed(self, duration):
    	self.progress_bar.setRange(0, duration)

    def set_position(self, position):
    	self.music_player.setPosition(position)

    def quit_action_triggered(self):
        self.window.close()

    def toggle_forward_function(self):
    	pass

    def toggle_back_function(self):	
        pass

    def play_button_clicked(self):
        self.music_player.play()

    def pause_button_clicked(self):
        self.music_player.pause()

    def volume_control(self):
        vol_level = int(self.volume_slider.value())
        self.music_player.setVolume(vol_level)

    # def toggle_forward_function(self):
    #     self.music_player.positionChanged(150)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow('MainWindow.ui')
    sys.exit(app.exec_())