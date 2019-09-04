import gym
from gym.utils import seeding
from gym import spaces

from gym_maze_exploration.envs.maze_class import *
from gym_maze_exploration.envs.renderer import *

matrix = np.array([ [1,1,1,1,1],
                    [1,5,2,0,1],
                    [1,1,0,1,1],
                    [1,3,0,4,1],
                    [1,1,1,1,1]])

DIR_DICT = {1: [0, -1],
            2: [+1, 0],
            3: [0, +1],
            0: [-1, 0]}

class IMazeFPEnv(gym.Env):
    metadata = {"render.modes": ["human"], }
    ACTION = ["F", "B", "L", "R"]

    __CONVERTER = {0:0, 2:1, 1:2, 3:3} # Convert direction to action for Maze_class

    def __init__(self, radius=1, max_steps=50, final_reward=2, switch=False):

        self.radius = radius
        self.max_steps = max_steps
        self.final_reward = final_reward
        self.switch = switch

        self.start = matrix[0:2]
        self.mid   = matrix[2]
        self.end   = matrix[3:]

        self.player_direction = 1

        self.indicator = "yellow"

        self.seed()
        self.reset()

    def create_maze(self, length, switch=False):

        if np.random.rand() < 0.5:
            self.start[1, 1] = 5
            self.indicator = "yellow"
            # blue -1, red +1
        else:
            self.start[1, 1] = 6
            self.indicator = "green"
            # blue +1, red -1

        if switch:
            self.end = np.flip(self.end, axis=1)

        maze = np.concatenate([self.start, np.tile(self.mid, [length, 1]), self.end])
        return maze

    # function that cuts the observation to get a First Person View model
    def cut_observation(self, obs):

        sight = self.radius + 1
        straight = np.array(DIR_DICT[self.player_direction])
        right = np.array(DIR_DICT[(self.player_direction + 1) % 4])
        left = np.array(DIR_DICT[(self.player_direction - 1) % 4])

        center = [self.radius//2 + 1, self.radius//2 + 1]

        x = []
        for j in range(sight):
            for i in range(j, sight):

                coords = (range(5),) + tuple(((i) * straight + j * right + center) % np.array(obs.shape[1:]))
                x.append(obs[coords])
                if j != 0:
                    coords = (range(5),) + tuple(((i) * straight + j * left + center) % np.array(obs.shape[1:]))
                    x.append(obs[coords])

        x = np.squeeze(x)
        return np.array(x)

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        # Assertion to check Action is valid
        assert self.action_space.contains(action)

        self.steps += 1
        if action > 1:
            self.player_direction += 2*action - 5 # -1 for L, +1 for R
            self.player_direction %= 4
            successful = True
        else:
            if action == 0:
                action = self.__CONVERTER[self.player_direction]
            else:
                action = self.__CONVERTER[(self.player_direction+2)%4]
            successful = self.game.step(action)

        tmp_state = self.game.get_observation(radius=self.radius, internal_view=self.source)

        tmp_state = self.cut_observation(tmp_state)

        reward = -0.04  # Maybe change the default reward, weighting more the move than the rotation
        if action == 2 or action == 3:
            reward = -0.08

        if not successful:
            reward = -0.5

        done = self.game.is_target_reached()
        if done:
            final = self.source[tuple(self.game.position)]
            if ((final == 3 and self.indicator == "yellow") or
                (final == 4 and self.indicator == "green")):
                reward = self.final_reward
            else:
                reward = -self.final_reward/2

        done = done or self.steps >= self.max_steps
        add_info = {"steps": self.steps}

        return tmp_state, reward, done, add_info

    def reset(self, training=True):

        reset_screen()

        length = 4 + np.random.randint(4)  # 4-7
        if not training:
            length = 3 + np.random.randint(38)  # 3-40

        self.source = self.create_maze(length, switch=self.switch)

        self.game = maze_class(self.source)
        self.game.reset()
        self.steps = 0

        side = self.radius * 2 + 1
        self.obs_shape = [5, side, side]
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=1, shape=self.obs_shape, dtype=np.int)

        tmp_state = self.game.get_observation(radius=self.radius, internal_view=self.source)
        tmp_state = self.cut_observation(tmp_state)
        return tmp_state

    def render(self, mode='human', close=False):

        render(self.game.internal_state)

        # indicator
        draw_target(np.where(self.source == 6), "green")
        draw_target(np.where(self.source == 5), "yellow")

        # red target
        draw_target(np.where(self.source == 3), "red")

        # blue target
        draw_target(np.where(self.source == 4), "blue")

        draw_player_with_dir(self.game.position, self.player_direction)

        time.sleep(0.5)
        if close:
            pygame.quit()

    def read_action(self):
        return get_action()


if __name__ == "__main__":
    import time

    env = IMazeFPEnv()
    _ = env.reset()

    for _ in range(0, 50):

        state, reward, done, _ = env.step(env.action_space.sample())
        env.render()

        if done:
            env.reset()
