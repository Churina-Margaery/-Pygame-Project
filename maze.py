import random


def get_neighbours(mh, mw, cell, m):
    res = []
    x = cell[0]
    y = cell[1]
    if (y + 2) < mw and m[x][y+2][-1] != 1:
        res.append(m[x][y+2])
    if (x + 2) < mh and m[x+2][y][-1] != 1:
        res.append(m[x+2][y])
    if (y-2) > 0 and m[x][y-2][-1] != 1:
        res.append(m[x][y-2])
    if (x-2) > 0 and m[x-2][y][-1] != 1:
        res.append(m[x-2][y])
    return res


def remove_wall(cf, cs, m):
    x = (cf[0] - cs[0]) // 2
    y = (cf[1] - cs[1]) // 2
    m[cs[0]+x][cs[1]+y] = 0


def draw_console(m, mh, flags):
    f = open("data/map.txt", encoding="utf8", mode="w")
    f.truncate()
    lst = []
    for i in range(mh):
        if i == 0:
            t = ['##' if x else '.' for x in m[i][1:]]
            string = "@"+''.join(x for x in t).ljust(15, "#")
            lst.append(list(string))
        elif i % 2 == 0:
            t = ['##' if x else '.' for x in m[i]]
            string = ''.join(x for x in t).ljust(14, "#")
            lst.append(list(string))
        else:
            t = ['##.' if x else '.' for x in m[i][::2]]
            string = ''.join(x for x in t).ljust(14, "#")
            lst.append(list(string))
    for i in range(15 - mh):
        string = "##############"
        lst.append(list(string))
    for _ in range(flags):
        chosen = None
        i = None
        j = None
        while chosen != "#":
            i = random.choice(range(0, mh - 1))
            j = random.choice(range(0, len(m[i])))
            chosen = lst[i][j]
        lst[i][j] = "!"
    for line in lst:
        print("".join(line), file=f)
    f.close()


def maze(w0, h0, flags):
    w = 2 * w0 + 1
    h = 2 * h0 + 1
    maze = []
    stackcurr = []
    unvisitedcells = w0 * h0
    for i in range(h):
        maze.append([])
        if i % 2 == 0:
            maze[i].extend([int(x) for x in '1' * w])
        else:
            for j in range(w):
                if j % 2 == 0:
                    maze[i].append(1)
                else:
                    maze[i].append([i, j, 0])

    startcell = random.randrange(1, h, 2)
    currentcell = maze[startcell][1]
    maze[startcell][0] = 0
    currentcell[-1] = 1
    unvisitedcells -= 1
    stackcurr.append(currentcell)

    while unvisitedcells:
        neigh = get_neighbours(h, w, currentcell, maze)
        if neigh:
            randnum = random.randint(0, len(neigh)-1)
            neighbourcell = neigh[randnum]
            neighbourcell[-1] = 1
            unvisitedcells -= 1
            remove_wall(neighbourcell, currentcell, maze)
            currentcell = neighbourcell
            stackcurr.append(neighbourcell)
        else:
            stackcurr.pop()
            currentcell = stackcurr[-1]
            endcell = random.randrange(1, h, 2)
            maze[endcell][-1] = 0
    draw_console(maze, h, flags)

