
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time,sys,math
import threading
from snooker_sprites import *
from vector import Vector

class Snooker():
    
    def start_game(self):
        
        # print("游戏开始")
        while True:
            self.screen.fill(GREEN) # 填充屏幕
            # 1.设置刷新帧率
            self.colck.tick(FRAME_PER_SECOND)

            # MY:设置定时器，跟踪玩家的进程
            self.__timer()
            
            

            # 2.事件监听
            self.__event_handle()

            # 3.碰撞检测
            #self.__check_collide()

            # 4.更新/绘制精灵组
            self.__update_sprites()

            # 5.更新显示
            pygame.display.flip()
            
            
    def __init__(self):
        

        
        self.screen = pygame.display.set_mode((1000,800))

        # 2. 创建游戏时钟
        self.colck = pygame.time.Clock()

        # 3. 调用私有方法，完成精灵和精灵组的创建
        self.__create_sprites()

        # MY:设置时间变量 跟踪玩家进程
        self.start_time = time.time()
        
        self.timestart = True
        
        
        self.flag = [[1 for i in range(20)]for i in range(20)]
        self.last_time = time.time()
    
    def __time_irq(self):
        
        while True:
       
            time_between = time.time()-self.last_time
            self.last_time = time.time()
        
            self.__check_collide()      
            for ball in self.balls_group:
                ball.update_pos(time_between)
            
            while time.time()-self.last_time<=0.002:
                pass
        
            print(time_between)
    
    def __create_sprites(self):
        """创建精灵"""
        self.balls_group = pygame.sprite.Group()
        self.moving_balls_group = pygame.sprite.Group()
        
    def __manage_moving_balls(self):
        for ball in self.balls_group:
            if ball.move_flag == True:
                self.moving_balls_group.add(ball)
            if ball.move_flag == False:
                self.moving_balls_group.remove(ball)
            
        
    def __event_handle(self):
        """事件监听[玩家事件，游戏事件]"""
       

        # 游戏事件列表
        for event in pygame.event.get():
            # 判断是否退出
            if event.type == pygame.QUIT:
                game.__game_over()

            elif event.type == CREATE_TIMEIRQ_EVENT:
                
                time_between = time.time()-self.last_time
                self.last_time = time.time()
                tt = time.time()
                
                self.__check_collide()
                
                for ball in self.balls_group:
                    ball.update_pos(time_between)
                
                #print(time.time()-tt)
                #print(time_between)
            elif event.type == CREATE_PRINT_EVENT:
                pass
                #print(self.moving_balls_group)
                
               # for ball in self.balls_group:
                   # print(ball.v.x,ball.a.x,ball.x)

    def __check_collide(self):
        '''碰撞检测'''
        self.__manage_moving_balls()
        for ball in self.moving_balls_group:
            
                
            if ball.x-ball.r<=0:ball.v.x = abs(ball.v.x)    
            if ball.x+ball.r>=1000:ball.v.x = -abs(ball.v.x)
            if ball.y-ball.r<=0:ball.v.y = abs(ball.v.y)
            if ball.y+ball.r>=800:ball.v.y = -abs(ball.v.y)
        
            for every_ball in self.balls_group:
                
                if every_ball == ball:
                    continue
                
                distance = math.sqrt((every_ball.x-ball.x)**2 + (every_ball.y-ball.y)**2)
                if distance > ball.r*2:
                    
                    self.flag[every_ball.id][ball.id] = 1
                    self.flag[ball.id][every_ball.id] = 1
                #if distance<= ball.r*2:
                    #print(distance)
                    #print(every_ball.id,ball.id,self.flag[every_ball.id][ball.id],self.flag[ball.id][every_ball.id])
                if  distance <= ball.r*2 and (self.flag[every_ball.id][ball.id] or self.flag[ball.id][every_ball.id]):
                    
                    v1_x = every_ball.v.x
                    v1_y = every_ball.v.y
                    v2_x = ball.v.x
                    v2_y = ball.v.y
                    #print(v2_x,v1_x)
                    alpha = math.atan2(every_ball.y-ball.y,every_ball.x-ball.x)#两球与x轴夹角
                    #计算切向与法向速度
                    v1_n = v1_x*math.cos(alpha) + v1_y*math.sin(alpha)
                    v1_t = -v1_x*math.sin(alpha) + v1_y*math.cos(alpha)
                    v2_n = v2_x*math.cos(alpha) + v2_y*math.sin(alpha)
                    v2_t = -v2_x*math.sin(alpha) + v2_y*math.cos(alpha)
                    #交换法相速度
                    temp = v1_n
                    v1_n = v2_n
                    v2_n = temp
                    every_ball.v.x = round(v1_n*math.cos(alpha) - v1_t*math.sin(alpha),4)
                    every_ball.v.y = round(v1_n*math.sin(alpha) + v1_t*math.cos(alpha),4)
                    
                    ball.v.x       = round(v2_n*math.cos(alpha) - v2_t*math.sin(alpha), 4)
                    ball.v.y       = round(v2_n*math.sin(alpha) + v2_t*math.cos(alpha), 4)
                    
                    self.flag[every_ball.id][ball.id] = 0
                    self.flag[ball.id][every_ball.id] = 0
                    '''
                    if every_ball.color == RED:
                        every_ball.color = BLACK
                        
                    else:
                        every_ball.color = RED
                        
                    if ball.color == RED:
                        
                        ball.color = BLACK
                    else:
                        
                        ball.color = RED
                    #print('球号：', ball.id, '速度：', ball.v.x,'球号：',every_ball.id,'速度：',every_ball.v.x)
                    '''
                
        
                
    def __update_sprites(self):
        '''更新球位置'''
        for ball in self.balls_group:
            ball.draw_ball()
    
    
        
    
    def __timer(self):
        if self.timestart:
            
            new_ball = Ball(self.screen,800,500,WHITE,0)
            new_ball.v = Vector(0,0)
            self.balls_group.add(new_ball)
            
            new_ball = Ball(self.screen,200,500,BLUE,1)
            new_ball.v = Vector(100,0)
            self.balls_group.add(new_ball)
            
            new_ball = Ball(self.screen,500,500,BLACK,6)
            new_ball.v = Vector(0,0)
            self.balls_group.add(new_ball)
            
            new_ball = Ball(self.screen,100,300,WHITE,2)
            new_ball.v = Vector(100,0)
            self.balls_group.add(new_ball)
            
            new_ball = Ball(self.screen,200,300,BLACK,3)
            new_ball.v = Vector(120,0)
            self.balls_group.add(new_ball)
            
            new_ball = Ball(self.screen,300,300,RED,4)
            new_ball.v = Vector(0,0)
            self.balls_group.add(new_ball)
            
            new_ball = Ball(self.screen,400,300,RED,5)
            new_ball.v = Vector(100,0)
            self.balls_group.add(new_ball)
            
            
            '''
            new_ball = Ball(self.screen,600,500,RED,7)
            new_ball.v = Vector(440,0)
            self.balls_group.add(new_ball)
            
            new_ball = Ball(self.screen,700,600,RED,8)
            new_ball.v = Vector(220,0)
            self.balls_group.add(new_ball)
            
            new_ball = Ball(self.screen,100,600,BLACK,9)
            new_ball.v = Vector(20,0)
            self.balls_group.add(new_ball)
            
            new_ball = Ball(self.screen,200,700,RED,10)
            new_ball.v = Vector(0,0)
            self.balls_group.add(new_ball)
            
            new_ball = Ball(self.screen,300,700,BLACK,11)
            new_ball.v = Vector(0,0)
            self.balls_group.add(new_ball)
            
            new_ball = Ball(self.screen,400,700,RED,12)
            new_ball.v = Vector(0,0)
            self.balls_group.add(new_ball)
            
            new_ball = Ball(self.screen,500,700,BLUE,13)
            new_ball.v = Vector(0,0)
            self.balls_group.add(new_ball)
            
            new_ball = Ball(self.screen,300,600,BLUE,14)
            new_ball.v = Vector(330,0)
            self.balls_group.add(new_ball)
            
            new_ball = Ball(self.screen,800,600,RED,15)
            new_ball.v = Vector(0,0)
            self.balls_group.add(new_ball)
            '''
            pygame.time.set_timer(CREATE_TIMEIRQ_EVENT, 5)
            pygame.time.set_timer(CREATE_PRINT_EVENT, 500)
            
            #t1 = threading.Thread(target=self.__time_irq)
            #t1.start()
            #t1.join()
            
            self.timestart = False
    
    @staticmethod
    def __game_over():
        #t1.join()
        print("游戏结束")
        pygame.quit()
        sys.exit()
            
    
    
if __name__ == '__main__':
    
    
    
    game = Snooker()
    # 启动游戏循环
    game.start_game()
           
