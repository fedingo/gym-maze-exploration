import gym
from gym.utils import seeding
from gym import spaces

import time
import numpy as np
from gym_maze_exploration.envs.maze_class import *
from gym_maze_exploration.envs.maze_generator import *
from gym_maze_exploration.envs.renderer import *

class MazeEnv(gym.Env):

	metadata = {"render.modes": ["human"],}
	ACTION = ["N", "S", "E", "W"]

	def __init__(self, fix_map = False, width = 7, height = 7, radius = 2,
				 max_steps = 200, final_reward = 10, source = None):
		
		self.width = width
		self.height = height
		self.fix_map = fix_map
		self.radius = radius
		self.max_steps = max_steps
		self.final_reward = final_reward

		if source is not None:
			self.source = source
			self.width, self.height = self.source.shape
		else:
			self.source = generate_maze(mx=self.width, my=self.height)

		self.seed()
		self.reset()

	def seed(self, seed=None):
		self.np_random, seed = seeding.np_random(seed)
		return [seed]

	def step(self, action):
		# Assertion to check Action is valid
		assert self.action_space.contains(action)

		self.steps += 1
		successful = self.game.step(action)
		state = self.game.get_observation(radius = self.radius)
		reward = -0.1
		if not successful:
			reward = -1

		done = self.game.is_target_reached()
		if done:
			reward = self.final_reward

		done = done or self.steps >= self.max_steps
		add_info = {"steps" : self.steps}

		return state, reward, done, add_info 

	def reset(self):

		if not self.fix_map:
			self.source = generate_maze(mx = self.width, my = self.height)
		
		self.game = maze_class(self.source)
		self.game.reset()
		self.steps = 0

		l = self.radius*2+1
		self.obs_shape = [2,l,l]
		self.action_space = spaces.Discrete(4)
		self.observation_space = spaces.Box(low=0, high=1, shape=self.obs_shape, dtype=np.int)

		return self.game.get_observation(radius = self.radius)

	def render(self, mode='human', close=False):

		render(self.game.internal_state)

		draw_player(self.game.position)
		draw_target(self.game.target_position)

		time.sleep(0.05)
		if close:
			pygame.quit()


if __name__ == "__main__":
	import time

	env = MazeEnv()
	_ = env.reset()

	for _ in range(0,100):
		state, reward, done, _ = env.step(env.action_space.sample())
		env.render()

		print(state)

		if done:
			env.reset()