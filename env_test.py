import time
import gym
import gym_maze_exploration

env = gym.make('Maze-Exploration-v0')

_ = env.reset()

for _ in range(200):
	_, _, done, _ = env.step(env.action_space.sample())
	env.render()

	if done:
		_ = env.reset()