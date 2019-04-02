from gym.envs.registration import register
import numpy as np
 
register(id='MazeExploration7x7-v0', 
    entry_point='gym_maze_exploration.envs:MazeEnv'
)

matrix = np.array([ [1,1,1,1,1],
                    [1,2,0,0,1],
                    [1,0,1,1,1],
                    [1,0,0,0,1],
                    [1,0,1,1,1],
                    [1,0,0,3,1],
                    [1,1,1,1,1]])

register(id='MazeExploration7x7FixedMap-v0', 
    entry_point='gym_maze_exploration.envs:MazeEnv', 
    kwargs = {'fix_map' : True,
              'source'  : matrix}
)

register(id='MazeExploration12x12FixedMap-v0', 
    entry_point='gym_maze_exploration.envs:MazeEnv', 
    kwargs = {'fix_map'  : True, 
    		  'width'    : 12,
    		  'height'   : 12,
    		  'max_steps': 500,
              'final_reward': 50,
    		  }
)