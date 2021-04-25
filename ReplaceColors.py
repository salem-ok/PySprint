import numpy as np
from PIL import Image

red_color = (238, 0, 34)
blue_color = (68, 102, 238)
yellow_color = (238, 238, 102)
green_color = (34, 170, 102)
green_secondary_color = (170, 204, 102)
blue_secondary_color = (170, 204, 238)
red_secondary_color = (170, 0, 0)
yellow_secondary_color = (170, 170, 0)

#BLUE CARS

im = Image.open('Assets/SuperSprintRacePodiumFirstCarGreenDrone.png')
data = np.array(im)

r1, g1, b1 = 170, 204, 102 # Original value
r2, g2, b2 = 170, 204, 238 # Value that we want to replace it with

red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
mask = (red == r1) & (green == g1) & (blue == b1)
data[:,:,:3][mask] = [r2, g2, b2]

im = Image.fromarray(data)
im.save('Assets/SuperSprintRacePodiumFirstCarBlueCarDrone.png')

im = Image.open('Assets/SuperSprintRacePodiumFirstCarBlueCarDrone.png')
data = np.array(im)

r1, g1, b1 = 136, 136, 136 # Original value
r2, g2, b2 = 68, 102, 238 # Value that we want to replace it with

red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
mask = (red == r1) & (green == g1) & (blue == b1)
data[:,:,:3][mask] = [r2, g2, b2]

im = Image.fromarray(data)
im.save('Assets/SuperSprintRacePodiumFirstCarBlueCar.png')

#RED CARS
im = Image.open('Assets/SuperSprintRacePodiumFirstCarGreenDrone.png')
data = np.array(im)

r1, g1, b1 = 170, 204, 102 # Original value
r2, g2, b2 = 170, 0, 0 # Value that we want to replace it with

red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
mask = (red == r1) & (green == g1) & (blue == b1)
data[:,:,:3][mask] = [r2, g2, b2]

im = Image.fromarray(data)
im.save('Assets/SuperSprintRacePodiumFirstCarRedCarDrone.png')

im = Image.open('Assets/SuperSprintRacePodiumFirstCarRedCarDrone.png')
data = np.array(im)

r1, g1, b1 = 136, 136, 136 # Original value
r2, g2, b2 = 238, 0, 34 # Value that we want to replace it with

red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
mask = (red == r1) & (green == g1) & (blue == b1)
data[:,:,:3][mask] = [r2, g2, b2]

im = Image.fromarray(data)
im.save('Assets/SuperSprintRacePodiumFirstCarRedCar.png')


#YELLOW CARS
im = Image.open('Assets/SuperSprintRacePodiumFirstCarGreenDrone.png')
data = np.array(im)

r1, g1, b1 = 170, 204, 102 # Original value
r2, g2, b2 = 170, 170, 0 # Value that we want to replace it with

red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
mask = (red == r1) & (green == g1) & (blue == b1)
data[:,:,:3][mask] = [r2, g2, b2]

im = Image.fromarray(data)
im.save('Assets/SuperSprintRacePodiumFirstCarYellowCarDrone.png')

im = Image.open('Assets/SuperSprintRacePodiumFirstCarYellowCarDrone.png')
data = np.array(im)

r1, g1, b1 = 136, 136, 136 # Original value
r2, g2, b2 = 238, 238, 102 # Value that we want to replace it with

red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
mask = (red == r1) & (green == g1) & (blue == b1)
data[:,:,:3][mask] = [r2, g2, b2]

im = Image.fromarray(data)
im.save('Assets/SuperSprintRacePodiumFirstCarYellowCar.png')