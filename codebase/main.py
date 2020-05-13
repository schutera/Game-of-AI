# Python code to implement Conway's Game Of Life 
# Contact: mark.schutera@mailbox.org and hendrik.vogt@gmail.com
import argparse 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation 

# setting up the values for the grid 
ON = 255
OFF = 0
vals = [ON, OFF] 

def randomGrid(N): 

	"""returns a grid of NxN random values"""
	return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N) 


def update(frameNum, img, grid, N):

	# copy grid since we require 8 neighbors 
	# for calculation and we go line by line 
	newGrid = grid.copy() 
	for i in range(N): 
		for j in range(N): 

			# compute 8-neghbor sum 
			# using toroidal boundary conditions - x and y wrap around 
			# so that the simulaton takes place on a toroidal surface. 
			total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
						grid[(i-1)%N, j] + grid[(i+1)%N, j] +
						grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
						grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255) 

			# apply Conway's rules 
			if grid[i, j] == ON: 
				if (total < 2) or (total > 3): 
					newGrid[i, j] = OFF 
			else: 
				if total == 3: 
					newGrid[i, j] = ON 

	# update data 
	img.set_data(newGrid) 
	grid[:] = newGrid[:] 
	return img, 


def main():

	# Command line args are in sys.argv[1], sys.argv[2] .. 
	# sys.argv[0] is the script name itself and can be ignored 
	# parse arguments 
	parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.") 

	# add arguments 
	parser.add_argument('--grid-size', dest='N', required=False) 
	parser.add_argument('--mov-file', dest='movfile', required=False) 
	parser.add_argument('--interval', dest='interval', required=False) 
	args = parser.parse_args()
	
	# set grid size 
	N = 100
	if args.N and int(args.N) > 8: 
		N = int(args.N) 
		
	# set animation update interval 
	updateInterval = 50
	if args.interval: 
		updateInterval = int(args.interval) 

	# declare grid 
	grid = np.array([]) 
	grid = randomGrid(N)

	# set up animation 
	fig, ax = plt.subplots() 
	img = ax.imshow(grid, interpolation='nearest') 
	ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ), 
								frames = 10, 
								interval=updateInterval, 
								save_count=50) 

	# # of frames? 
	# set output file 
	if args.movfile: 
		ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264']) 

	plt.show() 


if __name__ == '__main__': 
	main() 
