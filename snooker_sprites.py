
import pygame
from pygame.sprite import Sprite
from vector import Vector
#一些常量
# 屏幕大小的 常量
SCREEN_RECT = pygame.Rect(0, 0, 1000, 800)
WHITE = 255,255,255
BLUE = 0,0,255
BLACK = 0,0,0
RED = 255,0,0
GREEN = 0,255,0
# 刷新的帧数
FRAME_PER_SECOND = 200
#球运动时的加速度因子
ACCELERATED_SPD_FACTOR = 0

# 创建定时器常量
CREATE_TIMEIRQ_EVENT = pygame.USEREVENT
CREATE_PRINT_EVENT = pygame.USEREVENT+1

class Ball(Sprite):
    def __init__(self,screen,x,y,color,ball_id):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y,3,3)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.v = Vector(0,0)
        self.a = Vector(0,0)
        self.move_flag = False
        self.r = 50
        self.color = color
        self.id = ball_id
    
    def update_pos(self,time_between):
        if self.v.x == 0 and self.v.y==0:
            self.move_flag = False
        else:
            self.move_flag = True
            vx_last = self.v.x
            vy_last = self.v.y
            self.a = (-self.v.unit()).vector_mul_value(ACCELERATED_SPD_FACTOR)
            self.v = self.v+ self.a.vector_mul_value(time_between)
            temp_x = self.v.x
            temp_y = self.v.y
            self.v.x = round(self.v.x,4)
            self.v.y = round(self.v.y,4)
            if self.v.x**2+self.v.y**2<3 :#当速度减为0时
                self.v = Vector(0,0)
                self.a = Vector(0,0)
                self.move_flag = False
            
            self.x += round((vx_last+temp_x)*time_between/2, 4)
            self.y += round((vy_last+temp_y)*time_between/2, 4)
             
            self.rect.x = self.x
            self.rect.y = self.y
            
    def draw_ball(self):
        pygame.draw.rect(self.screen,self.color,self.rect)
        pygame.draw.circle(self.screen, self.color,(int(self.x),int(self.y)), self.r, 0)
        
class Flag():
    def __init__(self,ball_1_id,ball_2_id):
        self.ball_1_id = ball_1_id
        self.ball_2_id = ball_2_id
        self.flag = 1
    
    def neg_flag(self):
        self.flag = (self.flag+1)%2
            
        
 
        
        
        

        
