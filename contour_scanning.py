# Python-ish
# steps:
# 1. generate synthetic prox sensor data that simulates the contour of the core in the box, measurements taken off-center to the side to accentuate the difference between a wood block and the rounded edge of a core
# 2. create a histogram
# 3. partition the data into two or three buckets, if the box edges differ in height to the blocks
# 4. find the section in the middle of the data array that corresponds to the first or second shortest distance from the sensor
# 5. paint the section as a no-wash zone, with customisable buffer zones on two sides
# 6. for visualisation, overlay the synth data and processed detection data

# For the synth data generation, designate a random continuous section as the wood block

import math
import random
from scipy.ndimage import gaussian_filter

#####################################################################################
# Generation routine, creates an artificial contour dataset with random (normal) noise added in
# returns a list of floats
def generate_synthetic_data(data_len=1000, block_max_len=50, block_height=50):
  DATA_LEN = data_len # mimics millimeters
  AVERAGE = 10 
  VARIANCE = 1 
  RNG = random
  added_block = False
  BLOCK_MAX_LEN = block_max_len # in mm
  BLOCK_HEIGHT = block_height
  CORE_HEIGHT  = BLOCK_HEIGHT * (RNG.random() + 0.2) * 0.7
  SYNTH_DATA = [CORE_HEIGHT for i in range(DATA_LEN)]
  NOISY_DATA = SYNTH_DATA.copy()
  print("Core height is", CORE_HEIGHT)
  x = 0

  # Generate the contour data without noise
  while not added_block:
    chances = 0.1 / (data_len - block_max_len)
    while x < DATA_LEN:
      # toss a coin and if successful, add the block
      if not added_block and RNG.random() < chances:
        selected_block_len = math.floor(((RNG.random()+0.6)*0.625)*BLOCK_MAX_LEN)
        print("Adding block at", x, "to", x+selected_block_len)
        for i in range(selected_block_len):
          SYNTH_DATA[x+i] = BLOCK_HEIGHT
          if x+i >= DATA_LEN:
            break
        added_block = True
        break
    # else keep moving
      x += 1
    # if still not added, repeat
    x = 0
  
  # Add noise to the data
  for x in range(DATA_LEN):
    NOISY_DATA[x] = SYNTH_DATA[x] + (RNG.random() - 0.5) * CORE_HEIGHT * 0.2
  
  return NOISY_DATA, SYNTH_DATA, BLOCK_HEIGHT, CORE_HEIGHT

#####################################################################################
# Detection routine, finds one (the first) wooden block based on its height difference from its surroundings
def detect_obstacle(data=[]):

  DATA = data.copy() # Create a copy to be modified by this routine
  x = 0 # the position of the cnc head in mm, might need additional offsets for tools
  #def step():
  #  x += 1
  
  # Runs through the data and groups the data into two or three buckets:
  # Low, (middle,) high; returns
  def partition_data():
    # aka, a histogram into buckets
    # PLACEHOLDER 
    low  = math.inf
    high = -math.inf
    for i in range(len(DATA)):
      if DATA[i] > high:
        high = DATA[i]
      if DATA[i] < low:
        low  = DATA[i]
    return low, high
  
  low, high = partition_data()
  block_start = 0
  block_end = 0

  # Possibly pre-process the data to remove noise?
  def remove_noise(input, sigma=3):
    #  # do something: Gaussian smoothing? average of neighbours?
    return gaussian_filter(input, sigma)
  
  data_noise_removed = remove_noise(DATA)

  # A simple solution to finding the wood block edges from noisy data
  threshold = (high + low) / 2

  elev = data_noise_removed[x]
  # Step forwards until something high is found
  while elev < threshold:
    x += 1 # step()
    elev = data_noise_removed[x]
  
  # Mark the starting edge
  block_start = x
  x += 1 # step()
  elev = data_noise_removed[x]

  # Find the ending edge and mark that
  while elev >= threshold:
    x += 1 # step()
    elev = data_noise_removed[x]
  
  # Mark the ending edge
  block_end = x

  print("Detected block at (", block_start, ",", block_end, ").")
  # Return the coordinates as a tuple?
  return (block_start, block_end)
#####################################################################################


# Does this need Bayesian inference? Might make it much more reliable but needs some reading. Needs to deal with data noise

def step():

  return 0