import gym
import sys
import gym_game
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy

env = gym.make('AirHockey-v0')
env._max_episode_steps = 10000
def train_model(env):
    env = DummyVecEnv([lambda: env])
    model = PPO('MultiInputPolicy', env, verbose=1)
    model.learn(total_timesteps=100000)
    model.save("/home/ericwfeng/AirhockeyAI/Training/Saved Models/PPOMIP_100000_1_23_23")
    return model
def run_model():
    max_steps = 10000
    episodes = 10
    for episode in range(1, episodes+1):
        state = env.reset()
        done = False
        score =0
        step = 0
        while step<max_steps and not done:
            env.render()
            if step%10==0:
                action = env.action_space.sample()
            n_state, reward, done, info  = env.step(action)
            score+=reward
            step+=1
        print('Episode:{} Score:{}'.format(episode, score))
    env.close()

# model = train_model(env)
# print("done training")

# print("result:",evaluate_policy(model, env, n_eval_episodes = 10, render=True))
model = PPO.load("/home/ericwfeng/AirhockeyAI/Training/Saved Models/PPOMIP_100000_1_23_23", env=env)
run_model()
