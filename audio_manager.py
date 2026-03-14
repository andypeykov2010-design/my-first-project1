import pygame.mixer

class AudioManager:
    """Singleton за управление на музиката и звуковите ефекти."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        pygame.mixer.init()
        self.music_on = True
        self.music_file = "audio/background_battle_music.wav" # промени тук за твоето музикално парче

        self.shoot_sound = None
        try:
            self.shoot_sound = pygame.mixer.Sound("audio/attack.wav") # промени звук при удар
            self.shoot_sound.set_volume(0.5)
        except Exception as e:
            print(f"⚠️ Няма attack.wav: {e}")

        self._initialized = True
        self.start_music()

    def start_music(self):
        if not self.music_on:
            return
        try:
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)  # безкраен цикъл
        except Exception as e:
            print(f"⚠️ Няма музика: {e}")

    def toggle_music(self):
        """Включва / изключва музиката. Връща новото състояние (True = включена)."""
        self.music_on = not self.music_on
        if self.music_on:
            self.start_music()
        else:
            pygame.mixer.music.stop()
        return self.music_on

    def play_shoot(self):
        """Пуска звука при изстрел."""
        if self.shoot_sound and self.music_on:
            self.shoot_sound.play()