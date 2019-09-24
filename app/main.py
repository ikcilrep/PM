from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config
Config.set('graphics', 'resizable', '0') #0 being off 1 being on as in true/false
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '200')
class Menu(Widget):
    pass

class PasswordManagerApp(App):
    def build(self):
        return Menu()

if __name__ == '__main__':
    PasswordManagerApp().run()
