import gym
import gym_game

env = gym.make('AirHockey-v0')
max_steps = 3000
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