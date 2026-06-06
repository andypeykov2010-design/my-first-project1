from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from audio_manager import AudioManager


class GameMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shooter – Меню")
        self.setGeometry(200, 200, 600, 550)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #0d1117;
            }
        """)
        
        title = QLabel("ИЗБЕРИ РЕЖИМ")
        title.setStyleSheet("""
            QLabel {
                color: #00d9ff;
                font-size: 36px;
                font-weight: bold;
                padding: 20px;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        
        btn_training = QPushButton("🎯 ТРЕНИРОВКА")
        btn_training.setStyleSheet("""
            QPushButton {
                background-color: #161b22;
                color: #f0f6fc;
                border: 3px solid #28a745;
                border-radius: 12px;
                padding: 12px;
                font-size: 20px;
                font-weight: bold;
                min-width: 350px;
                min-height: 60px;
            }
            QPushButton:hover {
                background-color: #28a745;
                color: white;
            }
        """)
        btn_training.clicked.connect(lambda: self.start_game("training"))
        
        btn_level1 = QPushButton("⭐ НИВО 1")
        btn_level1.setStyleSheet("""
            QPushButton {
                background-color: #161b22;
                color: #f0f6fc;
                border: 3px solid #ffc107;
                border-radius: 12px;
                padding: 12px;
                font-size: 20px;
                font-weight: bold;
                min-width: 350px;
                min-height: 60px;
            }
            QPushButton:hover {
                background-color: #ffc107;
                color: black;
            }
        """)
        btn_level1.clicked.connect(lambda: self.start_game("level1"))
        
        btn_level2 = QPushButton("🔥 НИВО 2")
        btn_level2.setStyleSheet("""
            QPushButton {
                background-color: #161b22;
                color: #f0f6fc;
                border: 3px solid #dc3545;
                border-radius: 12px;
                padding: 12px;
                font-size: 20px;
                font-weight: bold;
                min-width: 350px;
                min-height: 60px;
            }
            QPushButton:hover {
                background-color: #dc3545;
                color: white;
            }
        """)
        btn_level2.clicked.connect(lambda: self.start_game("level2"))
        
        btn_back = QPushButton("⬅ НАЗАД")
        btn_back.setStyleSheet("""
            QPushButton {
                background-color: #161b22;
                color: #f0f6fc;
                border: 2px solid #1f6feb;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                min-width: 200px;
                min-height: 45px;
            }
            QPushButton:hover {
                background-color: #1f6feb;
            }
        """)
        btn_back.clicked.connect(self.go_back)

        self.audio = AudioManager()
        self.btn_music = QPushButton("🔊 МУЗИКА: ВКЛ")
        self.btn_music.setStyleSheet("""
            QPushButton {
                background-color: #161b22;
                color: #f0f6fc;
                border: 2px solid #6f42c1;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                min-width: 200px;
                min-height: 45px;
            }
            QPushButton:hover {
                background-color: #6f42c1;
            }
        """)
        self.btn_music.clicked.connect(self.toggle_music)
    
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(50, 40, 50, 40)
        
        layout.addWidget(title)
        layout.addSpacing(40)
        layout.addWidget(btn_training)
        layout.addSpacing(25)
        layout.addWidget(btn_level1)
        layout.addSpacing(25)
        layout.addWidget(btn_level2)
        layout.addSpacing(40)
        layout.addWidget(self.btn_music)
        layout.addSpacing(15)
        layout.addWidget(btn_back)
       

        
        self.setLayout(layout)

    def toggle_music(self):
        is_on = self.audio.toggle_music()
        self.btn_music.setText("🔊 МУЗИКА: ВКЛ" if is_on else "🔇 МУЗИКА: ИЗКЛ")


    def start_game(self, mode):
        from shooter import start_game
        self.close() 
        start_game(mode)
        
    def go_back(self):
        from start_screen import StartScreen
        self.start_screen = StartScreen()
        self.start_screen.show()
        self.close()