from pico2d import load_image


class Cloud:
    def __init__(self):
        self.image = load_image('cloud.PNG')
        self.w = self.image.w
        self.h = self.image.h
    def draw(self):
        self.image.draw(self.w*1.5//2,300,self.w*1.5,self.h*1.5)

    def update(self):
        pass
