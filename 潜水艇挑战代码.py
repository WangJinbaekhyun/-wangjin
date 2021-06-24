# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 23:02:46 2021

@author: 15065901137
"""

import pygame, sys, random, pygame.freetype

pygame.init()
size=width,height=800,600
screen = pygame.display.set_mode(size)
background = pygame.image.load("background.jpg")
pygame.display.set_caption("潜水艇挑战")
icon=pygame.image.load("hx.png")
pygame.display.set_icon(icon)
f1 = pygame.freetype.Font("C://Windows//Fonts//msyh.ttc",16)
BLACK = 0,0,0

class Submarine(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect().move(300,200)

class Stone(pygame.sprite.Sprite):              #派生stone子类继承pygame.sprite.Sprite精灵类，重写构造方法及update()方法
    def __init__(self, image_path, x, speed, upwards = True):
        #super()一下父类的构造方法，保证父类的__init__代码能够被正常运行
        super().__init__()
        self.image = pygame.image.load(image_path)
        if upwards: #朝上正向石头
            self.rect = self.image.get_rect().move(720, 600-x*350)
        else:       #朝下倒向石头
            self.rect = self.image.get_rect().move(720, 600-x*350-150-350)
        self.speed = speed
        
    def update(self):
        if self.rect.right < 0:
            self.kill()
        self.rect = self.rect.move(-self.speed,0)
        
def main():
    submarine = Submarine("submarine.png")
    stop = 0
    up = False
    down = False
    fps = 50
    flock = pygame.time.Clock()
    x = random.random()
    speed = 2
    stone = Stone("stone.png", x, speed, True)
    stone1 = Stone("stone1.png", x, speed, False)
    stones = pygame.sprite.Group(stone,stone1)
    s = speed
    score = 0
    score_stones = []
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:  #可加速可减速
                if event.key == pygame.K_UP:
                    for stone in stones.sprites():
                         s = stone.speed + 1
                         stone.speed = s
                elif event.key == pygame.K_DOWN:
                    for stone in stones.sprites():
                        if stone.speed > 0:
                           s = stone.speed - 1
                           stone.speed = s
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    up = True
                    down = False
                elif event.button == 3:
                    down = True
                    up = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    up = False
                elif event.button == 3:
                    down = False
        if pygame.display.get_active() and up and not stop:
            submarine.rect = submarine.rect.move(0,-5)
        if pygame.display.get_active() and down and not stop:    
            submarine.rect = submarine.rect.move(0,5)
          
        #障碍物更新
        if stones.sprites()[-2].rect.right < 550: 
            speed = s
            x = random.random()
            stone = Stone("stone.png", x, speed, True)
            stone1 = Stone("stone1.png", x, speed, False)
            stones.add(stone,stone1)
        if  pygame.display.get_active():
            stones.update()
                
         #判断碰撞，结束游戏
        if pygame.sprite.spritecollideany(submarine,stones) or submarine.rect.top <= 0 or submarine.rect.bottom >= 600:
            stop = 1
            for stone in stones.sprites():
                stone.speed = 0
            gameover = pygame.image.load("gameover.png")
            gameoverrect = gameover.get_rect().move(200,95)
            
         #记分
        for stone in stones:
            if stone.rect.right < submarine.rect.left and not stone in score_stones:
                score_stones.append(stone)
                score = score + 0.5

    
        screen.blit(background,(0,0))
        screen.blit(submarine.image,submarine.rect)
        stones.draw(screen)
        if stop:       #显示游戏结束界面，可选择再来一局
            screen.blit(gameover,gameoverrect)
            f1surf,f1rect = f1.render("分数:"+str(int(score)),fgcolor = BLACK,size = 16)
            screen.blit(f1surf,(370,210))
            if pygame.key.get_pressed()[pygame.K_a]:
                main()
            elif pygame.key.get_pressed()[pygame.K_b]:
                pygame.quit()
                sys.exit()
            
        pygame.display.update()
        flock.tick(fps)
    
if __name__ == '__main__':
     main()
     
     