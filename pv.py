import numpy as np
from tkinter import *
import time
import sympy as sp
from itertools import product, chain

fullsize = 630  # 余白込みの画面のサイズ 630,1000
size = 300  # 画面のサイズ

ep = 0.01

dim = 3

cubesize = 30

file = 'sample02'

pvX = np.genfromtxt(file + '/x.csv', delimiter=",").astype(np.int64)
pvY = np.genfromtxt(file + '/y.csv', delimiter=",").astype(np.int64)
pvZ = np.genfromtxt(file + '/z.csv', delimiter=",").astype(np.int64)

points = np.ones((cubesize,cubesize,cubesize))

for i in range(cubesize):
    points[i,:,:] = points[i,:,:]*pvX
    points[:,i,:] = points[:,i,:]*pvY
    points[:,:,i] = points[:,:,i]*pvZ

N = points.sum().astype(np.int64)

shapes = {
    'circles': [],
    'lines': [],
    'texts': []
}

root = Tk()


def colors(r, g, b):
    c = '#' + ('%x' % int(r)).zfill(2) + ('%x' % int(g)).zfill(2) + ('%x' % int(b)).zfill(2)
    return c


color_num = 8


def colormap(i):
    maxcolor = np.array([255, 255, 255])
    mincolor = np.array([50, 50, 100])
    colorlist = np.array([np.linspace(maxcolor[i], mincolor[i], color_num, endpoint=True) for i in range(3)]).T
    return colors(colorlist[i][0], colorlist[i][1], colorlist[i][2])


def depth_to_color(z):
    num = int(z / (fullsize / color_num))
    if num <= 0:
        num = 0
    elif num >= color_num:
        num = color_num - 1
    return colormap(num)


def reform(x):
    return size * (x / cubesize - 1 / 2) + fullsize / 2


def initializeDraw():
    # キャンパス
    global window, radius, node_pos
    window = Canvas(root, width=fullsize, height=fullsize, bg='White')
    window.pack()
    back = window.create_rectangle(0, 0, fullsize, fullsize, fill='black', outline='', tags='back')
    radius = 5

    node_pos = np.empty((0, 3))

    for x, y, z in product(range(cubesize), range(cubesize), range(cubesize)):
        if points[x, y, z] == 1:
            node_pos = np.r_[node_pos, np.array([[reform(x), reform(y), reform(z)]])]

    for i in range(N):
        shapes['circles'].append(
            window.create_oval(node_pos[i][0] - radius, node_pos[i][1] - radius, node_pos[i][0] + radius,
                               node_pos[i][1] + radius,
                               fill=depth_to_color(node_pos[i][2]), outline='', tags='node_pos'))


initializeDraw()

# 移動
def update_node(x, y, nodeID):
    # circle,text,lineの更新(描画の更新)
    window.coords(shapes['circles'][nodeID], x - radius, y - radius, x + radius, y + radius)
    window.itemconfigure(shapes['circles'][nodeID], fill = depth_to_color(node_pos[nodeID][2]))

def rotation_3D():
    global node_pos
    node_pos -= (sum(node_pos) / N - np.ones(dim) * fullsize / 2)
    while dim == 3 and val.get() == 2:
        theta = 3 * np.pi / 360
        node_pos = (np.array([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0],[- np.sin(theta), 0, np.cos(theta)]]).dot((node_pos - fullsize / 2).T)).T + fullsize / 2
        for i in range(N):
            update_node(node_pos[i][0], node_pos[i][1], i)

        time.sleep(0.01)

        window.pack()
        window.update()


def click_rotation(event):
    if dim == 3 and val.get() == 3:
        global x0, y0, nall
        x0 = event.x
        y0 = event.y
        nall = np.zeros((N, dim))
        for i in range(N):
            nall[i] = [node_pos[i][w] for w in range(dim)]

def move_rotation(event):
    global node_pos
    if dim == 3 and val.get() == 3:
        x = event.x
        y = event.y
        theta = - 2 * (x - x0) * np.pi / fullsize
        phi = 2 * (y - y0) * np.pi / fullsize
        rotation_theta = np.array([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [- np.sin(theta), 0, np.cos(theta)]])
        rotation_phi = np.array([[1, 0, 0], [0, np.cos(phi), - np.sin(phi)], [0, np.sin(phi), np.cos(phi)]])
        node_pos = ((rotation_phi.dot(rotation_theta)).dot((nall - fullsize / 2).T)).T + fullsize / 2

        for i in range(N):
            update_node(node_pos[i][0], node_pos[i][1], i)


def rotation_free():
    # バインディング
    window.tag_bind(ALL, '<1>', click_rotation)
    window.tag_bind(ALL, '<Button1-Motion>', move_rotation)


def button_command():
    global val
    val = IntVar()
    val.set(2)

    r2 = Radiobutton(text='3D View', variable=val, value=2, command=rotation_3D)
    r2.pack()
    r3 = Radiobutton(text='3D Drag', variable=val, value=3, command=rotation_free)
    r3.pack()


button_command()

root.mainloop()