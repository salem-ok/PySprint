import numpy as np
from PIL import Image

for i in range(0, 16):
    im = Image.open('Assets/BlueCarDrone{}.png'.format(i))
    data = np.array(im)

    r1, g1, b1 = 34, 68, 204 # Original value
    r2, g2, b2 = 34, 136, 208 # Value that we want to replace it with

    red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
    mask = (red == r1) & (green == g1) & (blue == b1)
    data[:,:,:3][mask] = [r2, g2, b2]

    im = Image.fromarray(data)
    im.save('Assets/BlueCarDrone{}.png'.format(i))