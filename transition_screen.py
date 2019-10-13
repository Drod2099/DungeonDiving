import pygame


class Loading:
    def __init__(self):
        self.mFont = pygame.font.SysFont("Times New Roman", 100)
        self.mText1 = self.mFont.render("Loading", True, (255, 255, 255))
        self.mText_w = self.mText1.get_width()
        self.mLoad_width = 200
        self.mLoading = pygame.Rect(400, 300, self.mLoad_width, 25)
        self.mWidth = 1
        self.mLoad_rate = 200

    def draw(self, win):
        win.fill((0, 0, 0))
        pygame.draw.rect(win, (255, 255, 255), (400 - (self.mLoad_width/2), 300, self.mLoad_width, 25), 1)
        win.blit(self.mText1, (400 - (self.mText_w/2), 200))
        pygame.draw.rect(win, (255, 255, 255), (400 - (self.mLoad_width/2), 300, self.mWidth, 25))

    def update(self, dt):
        self.mWidth += self.mLoad_rate * dt
        if self.mWidth >= self.mLoad_width:
            return False
        return True
