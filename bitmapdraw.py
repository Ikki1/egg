import numpy as np
from tkinter import *
from itertools import product, chain

size = 300  # 画面のサイズ

cubesize = 30

points = np.zeros((cubesize,cubesize))

shapes = {
    'circles': [],
    'lines': [],
    'texts': [],
    'rectangle': []
}

root = Tk()

#def reform(x):
#    return size * (x / cubesize - 1 / 2) + fullsize / 2


def initializeDraw():
    # キャンパス
    global window, length, node_pos
    window = Canvas(root, width=size, height=size, bg='White')
    window.pack()
    length = size / cubesize

    for j,i in product(range(cubesize), range(cubesize)):
        shapes['rectangle'].append(
            window.create_rectangle(i*length, j*length, (i+1)*length, (j+1)*length, fill='White', outline='', tags='rectangle'))


initializeDraw()

def draw(event):
    x = event.x
    y = event.y
    # nodeの更新
    if points[int(x // length)][int(y // length)] == 0:
        points[int(x // length)][int(y // length)] = 1
        window.itemconfigure(int((x) // length + (y) // length * cubesize)+1, fill = 'Blue')

def fix(event):
    x = event.x
    y = event.y
    # nodeの更新
    if points[int(x // length)][int(y // length)] == 1:
        points[int(x // length)][int(y // length)] = 0
        window.itemconfigure(int((x) // length + (y) // length * cubesize)+1, fill = 'White')

def edit():
    window.tag_bind('rectangle', '<Button1-Motion>', draw)
    window.tag_bind('rectangle', '<Button2-Motion>', fix)

def save():
    np.savetxt("new_picture.csv", points.T, delimiter=",")

def button_command():
    global val
    val = IntVar()
    val.set(0)
    edit()

    r0 = Radiobutton(text='draw', variable=val, value=1, command=edit)
    r0.pack()
    r1 = Radiobutton(text='save', variable=val, value=2, command=save)
    r1.pack()

button_command()

root.mainloop()
