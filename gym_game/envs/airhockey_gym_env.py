import gym
import numpy as np
from gym import spaces
import pygame
from pygame.locals import *

window_size = [500,700]
max_paddle_speed = 10
paddle_radius = 20

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
        self.observation_space = spaces.Dict(
            {
                "puck":spaces.Box(low=np.array([0,0, -max_puck_speed, -max_puck_speed]), high=np.array([500,700, max_puck_speed, max_puck_speed])), # 4D vector: x,y,dx,dy
                "paddle1":spaces.Box(low=np.array([0,0, -max_paddle_speed, -max_paddle_speed]), high=np.array([500,350, max_paddle_speed,max_paddle_speed])) # paddle 1 is restricted to the left side of the table
            }
        )
        self.action_space = spaces.Box(low=np.array([-max_paddle_speed, -max_paddle_speed]), high=np.array([max_paddle_speed, max_paddle_speed])) # 2D vector: dx,dy

        assert render_mode is None or render_mode in self.metadata["render.modes"]
        self.render_mode = render_mode
    def _get_obs(self):
        return {
            "puck":np.concatenate([self._puck_location, self._puck_velocity]),
            "paddle1":np.concatenate([self._paddle1_location, self._paddle1_velocity])
        }
    def step(self, action):
        self._puck_location += self._puck_velocity
        self._paddle1_location += self._paddle1_velocity
        last_loc = self._paddle2_location
        self._paddle2_location = np.asarray(pygame.mouse.get_pos())
        if self._paddle2_location[1]<350:
            self._paddle2_location[1]=350
        self._paddle2_velocity = np.array([self._paddle2_location[0]-last_loc[0], self._paddle2_location[1]-last_loc[1]])
        observation = self._get_obs()

        # Collision Code

        if(((self._paddle1_location[0]-self._puck_location[0])**2+(self._paddle1_location[1]-self._puck_location[1])**2)**0.5<2*paddle_radius):
            dist_off = 2*paddle_radius-(((self._paddle1_location[0]-self._puck_location[0])**2+(self._paddle1_location[1]-self._puck_location[1])**2)**0.5)
            vec = (self._paddle1_location[0]-self._puck_location[0], self._paddle1_location[1]-self._puck_location[1])
            mag_vec = ((vec[0]**2)+(vec[1]**2))**0.5
            if mag_vec!=0:
                scaled_vec = ((dist_off/mag_vec)*vec[0], (dist_off/mag_vec)*vec[1])
            else:
                scaled_vec=(0,0)
            self._puck_location[0] -= scaled_vec[0]
            self._puck_location[1] -= scaled_vec[1]
        if(((self._paddle2_location[0]-self._puck_location[0])**2+(self._paddle2_location[1]-self._puck_location[1])**2)**0.5<2*paddle_radius):
            dist_off = 2*paddle_radius-(((self._paddle2_location[0]-self._puck_location[0])**2+(self._paddle2_location[1]-self._puck_location[1])**2)**0.5)
            vec = (self._paddle2_location[0]-self._puck_location[0], self._paddle2_location[1]-self._puck_location[1])
            mag_vec = ((vec[0]**2)+(vec[1]**2))**0.5
            if mag_vec!=0:
                scaled_vec = ((dist_off/mag_vec)*vec[0], (dist_off/mag_vec)*vec[1])
            else:
                scaled_vec=(0,0)
            self._puck_location[0] -= scaled_vec[0]
            self._puck_location[1] -= scaled_vec[1]
        if (((self._paddle1_location[0]-self._puck_location[0])**2+(self._paddle1_location[1]-self._puck_location[1])**2)**0.5==2*paddle_radius):
            self._puck_velocity[0]=-1*self._puck_velocity[0]+self._paddle1_velocity[0]
            self._puck_velocity[1]=-1*self._puck_velocity[1]+self._paddle1_velocity[1]

        if (((self._paddle2_location[0]-self._puck_location[0])**2+(self._paddle2_location[1]-self._puck_location[1])**2)**0.5==2*paddle_radius):
            self._puck_velocity[0]=-1*self._puck_velocity[0]+self._paddle2_velocity[0]
            self._puck_velocity[1]=-1*self._puck_velocity[1]+self._paddle2_velocity[1]
        

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
        done=False
        if (abs(leftGoal.centre_y-self._puck_location[1])<=10 and abs(leftGoal.centre_x-self._puck_location[0])<=50):
            print("Goal Scored upper", self._puck_location)
            done=True
            reward = -1
        elif (abs(rightGoal.centre_y-self._puck_location[1])<=10 and abs(rightGoal.centre_x-self._puck_location[0])<=50):
        # elif (abs(rightGoal.centre_y-self._paddle2_location[1])<=10 and abs(rightGoal.centre_x-self._paddle2_location[0])<=50):
            print("Goal Scored lower", self._puck_location)
            done=True
            reward = 1
        else:  
            reward = 0
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
        pygame.draw.circle(canvas, (255,255,255), (int(self._puck_location[0]),int(self._puck_location[1])), paddle_radius)
        pygame.draw.circle(canvas, (255,0,0), (int(self._paddle1_location[0]),int(self._paddle1_location[1])), paddle_radius)
        pygame.draw.circle(canvas, (0,0,255), (int(self._paddle2_location[0]),int(self._paddle2_location[1])), paddle_radius)
        self.window.blit(canvas, (0,0))
        pygame.display.flip()
        self.clock.tick(self.metadata["render_fps"])

    def close(self):
        pygame.display.quit()
        pygame.quit()

    def seed(self, seed=None):
        pass
