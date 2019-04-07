import numpy as np
from matplotlib import pyplot as plt

n = 3000

def read_file(file_path, n):
    '''

    :param file_path: file to be parsed
    :param n: number of iterations were made during pict generation
    :return: list of parsed data
    '''

    f = list(map(float, open(file_path, 'r').read().split('\n')))

    buffer = [[]]
    counter = 0

    for x in f:
        if x < n:
            buffer[counter].insert(0, x)
            buffer.append([])
            counter += 1
        else:
            buffer[counter].append(x)

    value = 0
    for x in range(len(buffer)):
        if len(buffer[x]) != 0:
            if len(buffer[x]) != 1:
                buffer[x] = buffer[x][:2]
                value = buffer[x][1]
            else:
                buffer[x] = buffer[x] + [value]
        else:
            buffer.pop(x)
    return list(zip(*buffer))


axes = plt.gca()

plt.ylabel('Fitness function value ((original_im - new_im)^2).sum')
plt.xlabel('Generation')
plt.title("Tested photo FF convergence")

plt.axis([-100, 3000, 200000, 4000000000])
plt.plot(*read_file("logs\\pic3-ozhogin.txt", 3000), 'ro', label="pic.3 - colour")
plt.plot(*read_file("logs\\pic3-ozhoginBW.txt", 3000), 'go', label="pic.3 - bw")
plt.plot(*read_file("logs\\pic1-cat.txt", 3000), 'yo', label="pic.1 - cat")
plt.plot(*read_file("logs\\pic2-barash.txt", 3000), 'mo', label="pic.2 - cartoon")

plt.legend()

plt.show()
