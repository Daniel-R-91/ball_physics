import pygame
from random import randint
import time

class SmallBall:
    def __init__(self, x, y, velocity_x, velocity_y, gravity):
        self.image = pygame.image.load("images/small_ball.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)

        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.gravity = gravity

    def update(self, box_rect):

        self.friction = 0.3

        self.velocity_y += self.gravity

        self.pos_x -= self.velocity_x
        self.pos_y += self.velocity_y

        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

        if self.rect.bottom >= box_rect.bottom:
            self.rect.bottom = box_rect.bottom
            self.pos_y = self.rect.y

            if abs(self.velocity_y) < 1:
                self.velocity_y = 0
                self.gravity = 0
            else:
                self.velocity_y *= -0.8

            if abs(self.velocity_x) > 0:
                if self.velocity_x > 0:
                    self.velocity_x -= self.friction
                    if self.velocity_x < 0:
                        self.velocity_x = 0
                else:
                    self.velocity_x += self.friction
                    if self.velocity_x > 0:
                        self.velocity_x = 0

        if self.rect.top <= box_rect.top:
            self.rect.top = box_rect.top
            self.pos_y = self.rect.y
            self.velocity_y *= -0.8

        if self.rect.left <= box_rect.left:
            self.rect.left = box_rect.left
            self.pos_x = self.rect.x
            self.velocity_x *= -1

        if self.rect.right >= box_rect.right:
            self.rect.right = box_rect.right
            self.pos_x = self.rect.x
            self.velocity_x *= -1

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Game:
    def __init__(self, ball_speed):
        pygame.init()
        self.ball_speed = ball_speed
        self.small_balls = []

        self.screen_height = 900
        self.screen_width = 1200
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        icon = pygame.image.load("images/big_ball.png").convert_alpha()
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Ball Physics")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 50)

        self.background = pygame.image.load("images/background.png").convert()
        self.background_rect = self.background.get_rect(center = (self.screen_width / 2 , self.screen_height / 2))
        self.box_rect = pygame.Rect(335, 150, 550, 550)

        self.big_ball = pygame.image.load("images/big_ball.png").convert_alpha()
        self.big_ball_rect = self.big_ball.get_rect(center = (360 , self.screen_height / 2 ))

        self.game_active = False
        self.running = True
        self.big_ball_visible = True
        self.small_ball_visible = False

        self.start_time = pygame.time.get_ticks()
        self.delay_ms = 3000

        if self.ball_speed == 1:
            self.gravity = 0.2
            self.velocity_x = 1
            self.velocity_y = 0

        if self.ball_speed == 2:
            self.gravity = 0.2
            self.velocity_x = 5
            self.velocity_y = 0

        if self.ball_speed == 3:
            self.gravity = 0.3
            self.velocity_x = 15
            self.velocity_y = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def movement(self):
        current_time = pygame.time.get_ticks()

        if self.game_active and current_time - self.start_time >= self.delay_ms:
            if self.big_ball_rect.x < 837:
                if self.ball_speed == 1:
                    self.big_ball_rect.x += 1

                if self.ball_speed == 2:
                    self.big_ball_rect.x += 5

                if self.ball_speed == 3:
                    self.big_ball_rect.x += 15

            else:
                self.big_ball_visible = False
                self.small_ball_visible = True

                if not self.small_balls:
                    if self.ball_speed == 1:
                        count = 1
                    elif self.ball_speed == 2:
                        count = 4
                    else:
                        count = 10

                    for _ in range(count):
                        ball = SmallBall(
                            875,
                            self.screen_height // 2,
                            velocity_x=randint(3, 8),
                            velocity_y=randint(-10, -5),
                            gravity=self.gravity
                        )
                        self.small_balls.append(ball)

        if self.game_active and self.small_ball_visible:
            for ball in self.small_balls:
                ball.update(self.box_rect)

    def draw(self):
        if self.game_active:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, self.background_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), self.box_rect, 3)

            if self.game_active:
                current_time = pygame.time.get_ticks()
                if current_time - self.start_time >= self.delay_ms and self.big_ball_visible:
                    self.screen.blit(self.big_ball, self.big_ball_rect)

                if self.small_ball_visible:
                    for ball in self.small_balls:
                        ball.draw(self.screen)

        if not self.game_active:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, self.background_rect)

    def run(self):
        while self.running:
            self.draw()
            self.movement()
            self.handle_events()
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    def get_ball_speed():
        while True:
            try:
                speed = int(input("Enter ball speed (1 for slow, 2 for medium and 3 for fast): "))
                if 1 <= speed <= 3:
                    return speed
                else:
                    print("Please enter a number between 1 and 3.")
            except ValueError:
                print("That is not a valid number, please enter 1, 2 or 3.")


    speed = get_ball_speed()
    game = Game(speed)
    game.game_active = True

    game.run()
