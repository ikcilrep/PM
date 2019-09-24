from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.config import Config
from kivy.core.window import Window
Window.size = (400, 225) 
Config.set('graphics', 'resizable', '0')

class Menu(ScreenManager):
    pass

class PasswordManagerApp(App):
    def build(self):
        return Menu()

if __name__ == '__main__':
    PasswordManagerApp().run()
