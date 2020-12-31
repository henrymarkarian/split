from PIL import Image
import numpy as np

h, w = 512, 512 #initializes height and width, coordinates are [Y, X]
data = np.zeros((h, w, 3), dtype=np.uint8) #blacks out the background
images = [] #initializes a list of gif frames

def start():
    startwall = np.random.binomial(1, 0.5) #randomly chooses wall to start from
    if(startwall == 0): #starts at left
        position = [np.random.randint(0, 512), 0] #chooses a point on the left wall
    else: #starts at bottom
        position = [0, np.random.randint(0, 512)] #chooses a point on the bottom wall
    data[position[0], position[1]] = [255, 255, 255] #paints that point white
    return position, startwall

def creep(startwall, position, lastline, bias):
    if(startwall == 0): #starts at left
        if(position[0] == 0): #adds a lower limit
            newposition = [position[0] + np.random.binomial(1, 0.5), position[1] + 1] #uses binomial dist to determine direction to creep in
        elif(position[0] == 511): #adds an upper limit
            newposition = [position[0] + np.random.binomial(1, 0.5) - 1, position[1] + 1] #uses binomial dist to determine direction to creep in
        else: #normal function
            newposition = [position[0] + np.random.binomial(2, bias) - 1, position[1] + 1] #uses binomial dist to determine direction to creep in
    else: #starts at bottom
        if(position[1] == 0):
            newposition = [position[0] + 1, position[1] + np.random.binomial(1, 0.5)]
        elif(position[1] == 511):
            newposition = [position[0] + 1, position[1] + np.random.binomial(1, 0.5) - 1]
        else:
            newposition = [position[0] + 1, position[1] + np.random.binomial(2, bias) - 1]
    data[position[0], position[1]] = [255, 255, 255] #paints the position pixel white
    lastline.append(newposition) #adds the position to the lastline list
    return newposition, lastline

def split(data, lastline, startwall):
    offset = 1
    if(startwall == 0): #splits vertically
        for spread in range(1, 15): #iterates through the number of spreads
            for x in range(512): #iterates through the direction parallel to the vine
                for y in range(0, 511, 1): #iterates through the direction perpendicular to the vine, starting at 511
                    if(y <= lastline[x][0] - offset): #checks if the iterated pixel is above or equal to the given vine
                        try:
                            data[y, x] = data[y + offset, x] #shifts every pixel away from the vine
                            if(spread != 1): #prevents the function from deleting any part of the original vine
                                data[y + offset, x] = [0, 0, 0] #deletes the past vine
                        except:
                            continue
                for y in range(511, -1, -1): #iterates through the direction perpendicular to the vine, starting at 0
                    if(y >= lastline[x][0] + offset): #checks if the iterated pixel is below or equal to the given vine
                        try:
                            data[y, x] = data[y - offset, x]
                            data[y - offset, x] = [0, 0, 0]
                        except:
                            continue
            img = Image.fromarray(data, 'RGB')
            images.append(img)
    else:
        for spread in range(1, 15):
            for y in range(512):
                for x in range(0, 511, 1):
                    if(x <= lastline[y][1] - offset):
                        try:
                            data[y, x] = data[y, x + offset]
                            if(spread != 1):
                                data[y, x + offset] = [0, 0, 0]
                        except:
                            continue
                for x in range(511, -1, -1):
                    if(x >= lastline[y][1] + offset):
                        try:
                            data[y, x] = data[y, x - offset]
                            data[y, x - offset] = [0, 0, 0]
                        except:
                            continue
            img = Image.fromarray(data, 'RGB')
            images.append(img)

for i in range(50):
    position, startwall = start() #generates a seed
    lastline = [position] #starts off the "lastline" variable with the seed
    #position, startwall = [300, 0], 0 #adds in a custom seed
    bias = np.random.randint(3, 8) / 10 #creates a bias to skew the vines, can be changed to make straighter or less straight vines
    print(bias, i)
    while(position[0] > -1 and position[0] < 512 and position[1] > -1 and position[1] < 512): #bounds the generation to the box size
        position, lastline = creep(startwall, position, lastline, bias) #creeps from seed
    img = Image.fromarray(data, 'RGB')
    images.append(img)
    print("frame", i, 0, "complete")
    split(data, lastline, startwall)

images[0].save('split.gif', save_all=True, append_images=images[1:], optimize=False, duration=40, loop=0)
