from setuptools import setup

setup(name='gym_maze_exploration',
      version='0.1',
      url="https://github.com/fedingo/gym-maze-exploration",
      author="Federico Rossetto",
      license="MIT",
      packages=["gym_maze_exploration", "gym_maze_exploration.envs"],
      install_requires=['gym', 'numpy', 'pygame']
)