from pico2d import load_image

class Menu:
    def __init__(self):
        self.image = load_image('menu.png')

    def draw(self):
        self.image.draw(500, 250)

    def update(self):
        pass