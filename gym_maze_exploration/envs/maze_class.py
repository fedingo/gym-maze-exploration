import numpy as np

source = np.array([\
	[1,1,1,1,1],
	[1,2,0,0,1],
	[1,0,0,0,1],
	[1,0,0,0,1],
	[1,0,0,0,1],
	[1,0,0,3,1],
	[1,1,1,1,1]
])

# Codebook:
# 0: empty cell
# 1: wall cell
# 2: player cell
# 3: target cell



class maze_class:

	def __init__(self, source):

		self.shape = source.shape
		self.source = source
		self.reset()
		self.indicator = False

	def reset(self):	
		self.internal_state = np.zeros(self.shape)

		self.internal_state[:,:] = (self.source == 1).astype(int)

		self.position = np.concatenate(np.where(self.source == 2))
		self.target_position = np.concatenate(np.where(self.source == 3))
		self.indicator = False

		if 4 in self.source:
			self.indicator = True
			self.target_position = []
			for i in range(3,7):
				x = np.concatenate(np.where(self.source == i))
				if len(x) != 0:
					self.target_position.append(x)

			self.target_position = np.array(self.target_position)

	def step(self, action):
		# actions possible are 4 (the 4 directions)

		# [North, South, East, West]
		# Returns True only if there was an actual move

		shift = None

		if action == 0:
			shift = [-1, 0]
		elif action == 1:
			shift = [1, 0]
		elif action == 2:
			shift = [0, 1]
		elif action == 3:
			shift = [0, -1]

		target = tuple(self.position + shift)
		if self.internal_state[target] == 0:
			#only move if the cell is free
			self.position = self.position + shift

			return True

		return False

	def is_target_reached(self):
		# Boolean function to evaluate if the target has been reached
		return np.array([(self.position == x).all() for x in self.target_position[0:2]]).any()

	def __get_view(self):
		view = np.zeros(self.shape)
		view += self.internal_state

		view[tuple(self.position)] += 2
		view[self.target_position] += 3

		view[view == 5] = 2 #if player reached the final cell
		return view

	def get_observation(self, radius = 1, internal_view = None):

		view = np.ones([radius*2+1]*2)

		width = self.shape[0]
		height = self.shape[1]
		target_coords = np.array([[0,width],[0,height]])

		x_min = self.position[0]-radius
		if x_min < 0:
			target_coords[0,0] = -x_min
			x_min = 0

		x_max = self.position[0] + radius + 1
		if x_max >= width:
			target_coords[0,1] = -(x_max - width + 1)
			x_max = width - 1

		y_min = self.position[1]-radius
		if y_min < 0:
			target_coords[1,0] = -y_min
			y_min = 0

		y_max = self.position[1]+radius + 1
		if y_max >= height:
			target_coords[1,1] = -(y_max - height + 1)
			y_max = height - 1

		if internal_view is None:
			internal_view = self.__get_view()

		observation = internal_view[x_min:x_max,
									y_min:y_max]

		view[target_coords[0,0]:target_coords[0,1],
			 target_coords[1,0]:target_coords[1,1]] = observation

		goal = np.array(view == 3, dtype=np.int32)

		result= np.array([view, goal])

		if self.indicator:
			tmp = [view]
			for i in range(3,7):
				tmp.append(np.array(view == i, dtype=np.int32))
			result = np.array(tmp)

		result[result != 1] = 0
		return result

	def print(self):

		view = self.__get_view()
		print(view)

	def get_view_to_render(self):
		view = self.__get_view()

		return view

		

if __name__ == "__main__":

	from maze_generator import generate_maze

	source = generate_maze()
	obj = maze_class(source)
	obj.render()

	for i in range(100):
		obj.step(np.random.randint(4))
		obj.render()
