from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt

class StartScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shooter Game")
        self.setGeometry(200, 200, 600, 500)  
        
        self.setStyleSheet("""
            QWidget {
                background-color: #0d1117;
            }
        """)
        
        title = QLabel("🎯 SHOOTER GAME 🎯")
        title.setStyleSheet("""
            QLabel {
                color: #00d9ff;
                font-size: 48px;
                font-weight: bold;
                padding: 20px;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        
        start_button = QPushButton("▶ СТАРТ")
        start_button.setStyleSheet("""
            QPushButton {
                background-color: #161b22;
                color: #f0f6fc;
                border: 3px solid #00d9ff;
                border-radius: 15px;
                padding: 15px;
                font-size: 24px;
                font-weight: bold;
                min-width: 300px;
                min-height: 70px;
            }
            QPushButton:hover {
                background-color: #1f6feb;
                border-color: #00d9ff;
            }
            QPushButton:pressed {
                background-color: #0d4a9f;
            }
        """)
        start_button.clicked.connect(self.open_menu)
        
        exit_button = QPushButton("❌ ИЗХОД")
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #161b22;
                color: #f0f6fc;
                border: 3px solid #dc3545;
                border-radius: 15px;
                padding: 10px;
                font-size: 18px;
                font-weight: bold;
                min-width: 250px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #dc3545;
                border-color: #ff4444;
            }
            QPushButton:pressed {
                background-color: #a02a2a;
            }
        """)
        exit_button.clicked.connect(self.close)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50) 
        
        layout.addWidget(title)
        layout.addSpacing(50)  
        layout.addWidget(start_button)
        layout.addSpacing(30) 
        layout.addWidget(exit_button)
        
        self.setLayout(layout)

    def open_menu(self):
        from game_menu import GameMenu
        self.menu = GameMenu()
        self.menu.show()
        self.close()