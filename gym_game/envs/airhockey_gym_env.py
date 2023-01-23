import gym
import numpy as np
from gym import spaces
import pygame
from pygame.locals import *

window_size = [500,700]
max_paddle_speed = 10
max_time_steps = 10000
paddle_radius = 20
puck_radius = 20
mass_puck = 1 # measured in grams i guess
mass_paddle = 2


class Goal(object):
    def __init__(self,x,y,w=100,h=5):
        self.x=x
        self.y=y
        self.w=w
        self.h=h

        self.centre_x=self.x+self.w/2
        self.centre_y=self.y+self.h/2

leftGoal=Goal(200,5)
rightGoal=Goal(200,695)
max_puck_speed = 10

class AirHockeyEnv(gym.Env):
    metadata = {'render.modes': ['human', "rgb_array"], "render_fps": 100}
    def __init__(self, render_mode=None):
        self.action_space = spaces.Box(low=np.array([-1]), high=np.array([1]))
        self.time_step=0
        self.observation_space = spaces.Dict(
            {
                "puck":spaces.Box(low=np.array([0,0, -max_puck_speed, -max_puck_speed]), high=np.array([500,700, max_puck_speed, max_puck_speed])), # 4D vector: x,y,dx,dy
                "paddle2":spaces.Box(low=np.array([0,350, -max_paddle_speed, -max_paddle_speed]), high=np.array([500,700, max_paddle_speed,max_paddle_speed])) # paddle 2 is restricted to the bottom of the table
            }
        )
        self.action_space = spaces.Box(low=np.array([-max_paddle_speed, -max_paddle_speed]), high=np.array([max_paddle_speed, max_paddle_speed])) # 2D vector: dx,dy

        assert render_mode is None or render_mode in self.metadata["render.modes"]
        self.render_mode = render_mode
    # def collide(self,paddle_num): # 1 for paddle 1 and 2 for paddle 2
    #     paddle_loc = list([self._paddle1_location, self._paddle2_location])[paddle_num-1]
    #     paddle_vel = list([self._paddle1_velocity, self._paddle2_velocity])[paddle_num-1]
    #     if(((paddle_loc[0]-self._puck_location[0])**2+(paddle_loc[1]-self._puck_location[1])**2)**0.5<2*paddle_radius):
    #         dist_off = 2*paddle_radius-(((paddle_loc[0]-self._puck_location[0])**2+(paddle_loc[1]-self._puck_location[1])**2)**0.5)
    #         vec = (paddle_loc[0]-self._puck_location[0], paddle_loc[1]-self._puck_location[1])
    #         mag_vec = ((vec[0]**2)+(vec[1]**2))**0.5
    #         if mag_vec!=0:
    #             scaled_vec = ((dist_off/mag_vec)*vec[0], (dist_off/mag_vec)*vec[1])
    #         else:
    #             scaled_vec=(0,0)
    #         self._puck_location[0] -= scaled_vec[0]
    #         self._puck_location[1] -= scaled_vec[1]
    #     if (((paddle_loc[0]-self._puck_location[0])**2+(paddle_loc[1]-self._puck_location[1])**2)**0.5==2*paddle_radius):
    #         self._puck_velocity[0]=-1*self._puck_velocity[0]+paddle_vel[0]
    #         self._puck_velocity[1]=-1*self._puck_velocity[1]+paddle_vel[1]
    def collide_eric(self, paddle_num):
        paddle_loc = list([self._paddle1_location, self._paddle2_location])[paddle_num-1]
        paddle_vel = list([self._paddle1_velocity, self._paddle2_velocity])[paddle_num-1]
        # paddle 1 puck 2
        if(((paddle_loc[0]-self._puck_location[0])**2+(paddle_loc[1]-self._puck_location[1])**2)**0.5<puck_radius+paddle_radius):
            dist_off = 2*paddle_radius-(((paddle_loc[0]-self._puck_location[0])**2+(paddle_loc[1]-self._puck_location[1])**2)**0.5)
            vec = (paddle_loc[0]-self._puck_location[0], paddle_loc[1]-self._puck_location[1])
            mag_vec = ((vec[0]**2)+(vec[1]**2))**0.5
            if mag_vec!=0:
                scaled_vec = ((dist_off/mag_vec)*vec[0], (dist_off/mag_vec)*vec[1])
            else:
                scaled_vec=(0,0)
            d = ((paddle_loc[0]-self._puck_location[0])**2+(paddle_loc[1]-self._puck_location[1])**2)**0.5
            nx = (self._puck_location[0]-paddle_loc[0])/d
            ny = (self._puck_location[1]-paddle_loc[1])/d
            p = 2*(paddle_vel[0]*nx+paddle_vel[1]*ny-self._puck_velocity[0]*nx-self._puck_velocity[1]*ny)/(mass_puck+mass_paddle)
            self._puck_velocity[0] += p*mass_puck*nx
            self._puck_velocity[1] += p*mass_puck*ny
            # update location after updating new direction so it doesn't end up just sticking to the paddle
            self._puck_location[0] -= scaled_vec[0]
            self._puck_location[1] -= scaled_vec[1]
            self._puck_location += self._puck_velocity
        if(((paddle_loc[0]-self._puck_location[0])**2+(paddle_loc[1]-self._puck_location[1])**2)**0.5<=puck_radius+paddle_radius):
            d = ((paddle_loc[0]-self._puck_location[0])**2+(paddle_loc[1]-self._puck_location[1])**2)**0.5
            nx = (self._puck_location[0]-paddle_loc[0])/d
            ny = (self._puck_location[1]-paddle_loc[1])/d
            p = 2*(paddle_vel[0]*nx+paddle_vel[1]*ny -self._puck_velocity[0]*nx-self._puck_velocity[1]*ny)/(mass_puck+mass_paddle)
            self._puck_velocity[0] += p*mass_puck*nx
            self._puck_velocity[1] += p*mass_puck*ny
            # print(p)

    def collide_physical(self,paddle_num): # collision code assuming fully elastic collisions and no external forces
        paddle_loc = list([self._paddle1_location, self._paddle2_location])[paddle_num-1]
        paddle_vel = list([self._paddle1_velocity, self._paddle2_velocity])[paddle_num-1]
        # m1v1x0 + m2v2x0 = m1v1xf + m2v2xf
        if(((paddle_loc[0]-self._puck_location[0])**2+(paddle_loc[1]-self._puck_location[1])**2)**0.5<puck_radius+paddle_radius):
            dist_off = 2*paddle_radius-(((paddle_loc[0]-self._puck_location[0])**2+(paddle_loc[1]-self._puck_location[1])**2)**0.5)
            vec = (paddle_loc[0]-self._puck_location[0], paddle_loc[1]-self._puck_location[1])
            mag_vec = ((vec[0]**2)+(vec[1]**2))**0.5
            if mag_vec!=0:
                scaled_vec = ((dist_off/mag_vec)*vec[0], (dist_off/mag_vec)*vec[1])
            else:
                scaled_vec=(0,0)
            self._puck_location[0] -= scaled_vec[0]
            self._puck_location[1] -= scaled_vec[1]
        if(((paddle_loc[0]-self._puck_location[0])**2+(paddle_loc[1]-self._puck_location[1])**2)**0.5==puck_radius+paddle_radius):
            M_x0 = paddle_vel[0]*mass_paddle+self._puck_velocity[0]*mass_puck #initial momentum in x
            M_y0 = paddle_vel[1]*mass_paddle+self._puck_velocity[1]*mass_puck #initial momentum in y
            self._puck_velocity[0] = M_x0/mass_puck # assuming paddle_velocity is zero
            self._puck_velocity[1] = M_y0/mass_puck
            #friction
            if self._puck_velocity[0]>0: self._puck_velocity[0]-=1 
            else: self._puck_velocity[0]+=1
            if self._puck_velocity[1]>0: self._puck_velocity[1]-=1 
            else: self._puck_velocity[1]+=1


    def _get_obs(self):
        return {
            "puck":np.concatenate([self._puck_location, self._puck_velocity]),
            "paddle2":np.concatenate([self._paddle2_location, self._paddle2_velocity])
        }
    def step(self, action):
        self._puck_location += self._puck_velocity
        self._paddle1_location[0] = max(0, min(self._paddle1_location[0], 500))
        self._paddle1_location[1] = max(0, min(self._paddle1_location[1], 350))
        self._paddle1_location+=self._paddle1_velocity


        self._paddle2_velocity=action
        self._paddle2_location += self._paddle2_velocity
        self._paddle2_location[0] = max(0, min(self._paddle2_location[0], 500))
        self._paddle2_location[1] = max(350, min(self._paddle2_location[1], 700))

        # last_loc = self._paddle2_location
        # self._paddle2_location = np.asarray(pygame.mouse.get_pos())

        # if self._paddle2_location[1]<350:
        #     self._paddle2_location[1]=350
        # self._paddle2_velocity = np.array([self._paddle2_location[0]-last_loc[0], self._paddle2_location[1]-last_loc[1]])
        lLim = 50
        uLim = 370
        rLim = 450
        # Paddle1 Heuristic Code
        if self._puck_location[0] < self._paddle1_location[0]:
                if self._puck_location[0] < lLim:
                    self._paddle1_velocity[0]=1
                else:
                    self._paddle1_velocity[0]=-2
        if self._puck_location[0] > self._paddle1_location[0]:
            if  self._puck_location[0] > rLim:
                self._paddle1_velocity[0]=-1
            else:
                self._paddle1_velocity[0]=2
        if self._puck_location[1] < self._paddle1_location[1]:
            if self._puck_location[1] < uLim:
                self._paddle1_velocity[1]=1
            else:
                self._paddle1_velocity[1]=-6
        if self._puck_location[1] > self._paddle1_location[1]:
            if self._puck_location[1]<=360:
                self._paddle1_velocity[1]=6
            else:
                if self._paddle1_location[1]>200:
                    self._paddle1_velocity[1]=-2
                else:
                    self._paddle1_velocity[1]=0
        observation = self._get_obs()
        # if paddle 1 hits puck
        # self.collide(1)
        # self.collide(2)

        # self.collide_physical(1)
        # self.collide_physical(2)
        
        self.collide_eric(1)
        self.collide_eric(2)

        # update puck based on walls
        if self._puck_location[0]<=0+10:
            self._puck_location[0]=1+10
            self._puck_velocity[0]*=-1
        elif self._puck_location[0]>=500-10:
            self._puck_location[0] =499-10
            self._puck_velocity[0]*=-1
        if self._puck_location[1]<=0+10:
            self._puck_location[1]=1+10
            self._puck_velocity[1]*=-1
        elif self._puck_location[1]>=700-10:
            self._puck_location[1]=699-10
            self._puck_velocity[1]*=-1

        # limit puck speed
        self._puck_velocity = np.clip(self._puck_velocity, -max_puck_speed, max_puck_speed)
        
        # Check if Goal Scored -> reset, game over
        self.time_step+=1
        done=False
        if (abs(leftGoal.centre_y-self._puck_location[1])<=10 and abs(leftGoal.centre_x-self._puck_location[0])<=50):
            # print("Goal Scored upper", self._puck_location)
            done=True
            reward = 4
        elif (abs(rightGoal.centre_y-self._puck_location[1])<=10 and abs(rightGoal.centre_x-self._puck_location[0])<=50):
        # elif (abs(rightGoal.centre_y-self._paddle2_location[1])<=10 and abs(rightGoal.centre_x-self._paddle2_location[0])<=50):
            # print("Goal Scored lower", self._puck_location)
            done=True
            reward = -4
        else:  
            reward = 0
        if self.time_step>max_time_steps and not done:
            done=True
            reward = -2
        info = {}
        if self.render_mode =="human":
            self.render()
        return observation, reward, done, info

    def reset(self):
        # return initial observation
        self._puck_location = np.array([250,350], dtype = float)
        self._puck_velocity = np.array([0,0], dtype = float)
        self._paddle1_location = np.array([250,150], dtype = float)
        self._paddle2_location = np.array([250,550], dtype = float)
        self._paddle2_velocity = np.array([0,0], dtype = float)
        self._paddle1_velocity = np.array([0,0], dtype = float)
        observation = self._get_obs()
        return observation

    def render(self, mode='human'):
        pygame.init()
        pygame.display.init()
        self.window = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        canvas = pygame.Surface(window_size)
        canvas.fill((0,0,0))
        pygame.draw.rect(canvas, (255,255,255), (leftGoal.x,leftGoal.y,leftGoal.w,leftGoal.h))
        pygame.draw.rect(canvas, (255,255,255), (rightGoal.x,rightGoal.y,rightGoal.w,rightGoal.h))
        pygame.draw.circle(canvas, (255,255,255), (int(self._puck_location[0]),int(self._puck_location[1])), puck_radius)
        pygame.draw.circle(canvas, (255,0,0), (int(self._paddle1_location[0]),int(self._paddle1_location[1])), paddle_radius)
        pygame.draw.circle(canvas, (0,255,255), (int(self._paddle2_location[0]),int(self._paddle2_location[1])), paddle_radius)
        self.window.blit(canvas, (0,0))
        pygame.display.flip()
        self.clock.tick(self.metadata["render_fps"])

    def close(self):
        pygame.display.quit()
        pygame.quit()

    def seed(self, seed=None):
        pass
