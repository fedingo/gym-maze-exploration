import time
import gym
import gym_maze_exploration
import gym_pigchase_topdown

env = gym.make('I-Maze-v0')

_ = env.reset()
env.render()
done = False

while True:
	action = env.read_action()
	if action != -1:
		_, reward, done, _ = env.step(action)
		print(reward)

	env.render()

	if done:
		break