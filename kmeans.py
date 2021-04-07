import PIL
import sys
from PIL import Image
import io
import urllib.request
import random

num = 0
means = []

def get_distinct(pix):
    count = 0
    all_pix = set()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            count += 1
            pixels = pix[x,y]
            all_pix.add(pixels)
    return count, len(all_pix), all_pix

def most_common(all_pix, pix):
    pixels = {}
    for val in all_pix:
        pixels[val] = 0
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pixel = pix[x, y]
            pixels[pixel] = pixels[pixel] + 1
    common = (0, 0, 0)
    max = 0
    for value in pixels:
        if pixels[value] > max:
            common = value
            max = pixels[value]
    return common, max

def kmeans(pix):
    groups = []
    indexes = []
    new_indexes = []
    same = False

    for i in range(num):
        groups.append([])
        indexes.append([])
        new_indexes.append([])
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pixel = pix[x, y]
            i = distances(pixel)
            groups[i].append(pixel)
            indexes[i].append([x, y])
    gen_new_means(groups)

    while(same == False):
        groups = []
        new_indexes = []
        for i in range(num):
            groups.append([])
            new_indexes.append([])
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                pixel = pix[x,y]
                i = distances(pixel)
                groups[i].append(pixel)
                new_indexes[i].append([x,y])
        print(means)
        if(new_indexes != indexes):
            gen_new_means(groups)
            indexes = new_indexes
        else:
            return means

def gen_new_means(groups):
    count = 0
    for i in groups:
        sum_red = 0
        sum_green = 0
        sum_blue = 0
        for element in i:
            sum_red += element[0]
            sum_green += element[1]
            sum_blue += element[2]
        new_mean = [(sum_red/len(i)), (sum_green/len(i)), (sum_blue/len(i))]
        means[count] = new_mean
        count+=1

def distances(pixel):
    index = 0
    min_diff = 255*3
    for i in range(num):
        mean = means[i]
        diff = ((pixel[0] - mean[0])**2 + (pixel[1] - mean[1])**2 + (pixel[2] - mean[2])**2) ** 0.5
        if diff < min_diff:
            min_diff = diff
            index = i
    return index

def convert(pix):
    groups = []
    for i in range(num):
        groups.append(0)
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pixel = pix[x, y]
            i = distances(pixel)
            mean = means[i]
            groups[i] = groups[i] + 1
            pix[x,y] = (int(mean[0]), int(mean[1]), int(mean[2]))
    return groups

def gen_random():
    for i in range(num):
        means.append([random.randint(0,256), random.randint(0,256), random.randint(0,256)])

def adjacents(img, pix, x, y):
    queue = set()
    pixel = pix[x,y]
    if(x+1 < img.size[0]):
        if pix[x + 1, y] == pixel:
            queue.add(str(x+1) + " " + str(y))
    if (x -1 >= 0):
        if pix[x - 1, y] == pixel:
            queue.add(str(x-1) + " " + str(y))
    if (y + 1 < img.size[1]):
        if pix[x, y + 1] == pixel:
            queue.add(str(x) + " " + str(y+1))
    if (y - 1 >= 0):
        if pix[x, y - 1] == pixel:
            queue.add(str(x) + " " + str(y-1))
    if (x+1 < img.size[0] and y+1 < img.size[1]):
        if pix[x + 1, y + 1] == pixel:
            queue.add(str(x+1) + " " + str(y+1))
    if (x + 1 < img.size[0] and y -1 >= 0):
        if pix[x + 1, y - 1] == pixel:
            queue.add(str(x+1) + " " + str(y-1))
    if (x - 1 >= 0 and y + 1 < img.size[1]):
        if pix[x - 1, y + 1] == pixel:
            queue.add(str(x-1) + " " + str(y+1))
    if (x - 1 >=0 and y -1 >= 0):
        if pix[x - 1, y - 1] == pixel:
            queue.add(str(x-1) + " " + str(y-1))

    return queue

def region_counts(img, pix):
    visited = set()
    queue = set()
    regions = []

    all_pix = set()
    for i in range(num):
        regions.append(0)

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            coor = str(x) + " " + str(y)
            all_pix.add(coor)

    while len(all_pix) > 0:
        element = all_pix.pop()
        element = element.split(" ")
        pixel = pix[int(element[0]), int(element[1])]
        index = 0
        temp = [pixel[0], pixel[1], pixel[2]]
        for i in range(num):
            curr_mean = means[i]
            mean_temp = [int(curr_mean[0]), int(curr_mean[1]), int(curr_mean[2])]
            if mean_temp == temp:
                index = i
                break
        regions[index] = regions[index] + 1

        adjacent = adjacents(img, pix, int(element[0]), int(element[1]))
        for value in adjacent:
            if value in all_pix:
                queue.add(value)
                all_pix.remove(value)
        while len(queue) > 0:
            coordinates = queue.pop()
            coordinates = coordinates.split(" ")
            adjacent = adjacents(img, pix, int(coordinates[0]), int(coordinates[1]))
            for element in adjacent:
                if element in all_pix:
                    queue.add(element)
                    all_pix.remove(element)

    return regions


input = list(sys.argv)
input = input[1:]

num = int(input[0])
picture = input[1]

if picture[0:4] == 'http':
    URL = picture
    f = io.BytesIO(urllib.request.urlopen(URL).read())
    img = Image.open(f)

else:
    img = Image.open(picture)
#img.show()

pix = img.load()

gen_random()
distinct = get_distinct(pix)
most_common = most_common(distinct[2], pix)

print("Size: " + str(img.size))
print("Pixels: " + str(distinct[0]))
print("Distinct pixel count: " + str(distinct[1]))
print("Most common pixel: " + str(most_common[0]) + " => " + str(most_common[1]))

kmeans(pix)
groups = convert(pix)

print("Final means:")

for i in range(num):
    print(str(i + 1) + ":" + str(means[i]) + " => " + str(groups[i]))

regions = region_counts(img,pix)
print("Distinct Regions: " + str(regions))
img.show()
#img.save("kmeans/2020syadlapa.png", "PNG")

