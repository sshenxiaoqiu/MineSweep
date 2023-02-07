import tkinter as tk
import random
import tkinter.messagebox

MAXSIZE = 10    #棋盘长宽
SIMPEE = 10      #难度权重

root = tk.Tk()
root.title('扫雷')
root.geometry('310x310')

imgs = {i: tk.PhotoImage(file='./images/{}.jpg'.format(i)) for i in range(12)}
ssxx = set()
direct = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

class Block(tk.Button):
    def __init__(self, master, true_state, x, y):
        self.state = 9
        self.true_state = true_state
        self.img = imgs[self.state]
        self.x = x
        self.y = y
        self.master = master
        super().__init__(master=master, image=self.img)
        self.bind("<ButtonPress-1>", self.ImgChangeLeft)
        self.bind("<ButtonPress-3>", self.ImgChangeRight)

    def ImgChangeLeft(self, *args):
        if self.state == self.true_state:
            return
        if self.state == 9:
            if self.true_state == 11:
                for i in game.Btn_block:
                    i.ImgShow()
                tkinter.messagebox.askokcancel(title='扫雷', message='你输了!')
            else:
                self.state = self.true_state
                self.config(image=imgs[self.true_state])
                check_pose(self.x, self.y)
                show()
        if cw():
            tkinter.messagebox.askokcancel(title='扫雷', message='你赢了!')

    def ImgChangeRight(self, *args):
        if self.state == self.true_state:
            return
        if self.state == 9:
            self.state = 10
            game.Btn_state[self.x][self.y] = 10
            self.config(image=imgs[self.state])
        elif self.state == 10:
            self.state = 9
            game.Btn_state[self.x][self.y] = 10
            self.config(image=imgs[self.state])
        if cw():
            tkinter.messagebox.askokcancel(title='扫雷', message='你赢了!')

    def ImgShow(self, *args):
        self.state = self.true_state
        self.config(image=imgs[self.state])

class GM(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.Btn_block = None
        self.Btn_state = None
        self.creat_main()

    def creat_main(self):
        self.creat_Lei()
        self.Btn_block = list()
        for i in range(MAXSIZE):
            for j in range(MAXSIZE):
                block = Block(self.master, self.Btn_state[i][j], i, j)
                block.grid(column=i, row=j)
                self.Btn_block.append(block)

    def creat_Lei(self):
        self.Btn_state = [[0 if random.randint(0, SIMPEE-1) > 0 else 11 for i in range(MAXSIZE)] for j in range(MAXSIZE)]
        for i in range(MAXSIZE):
            for j in range(MAXSIZE):
                if self.Btn_state[i][j] == 11:
                    for k in direct:
                        dx = i + k[0]
                        dy = j + k[1]
                        if dx < 0 or dy < 0 or dx > MAXSIZE-1 or dy > MAXSIZE-1:
                            continue
                        if self.Btn_state[dx][dy] != 11:
                            self.Btn_state[dx][dy] += 1

def show():
    global ssxx
    y = list(ssxx)
    for i in y:
        game.Btn_block[i[0]*MAXSIZE + i[1]].ImgShow()
    ssxx = set()

def check_pose(x, y):
    ssxx.add((x, y))
    if game.Btn_state[x][y] != 0:
        return
    for k in direct:
        dx = x + k[0]
        dy = y + k[1]
        if dx<0 or dy<0 or dy>MAXSIZE-1 or dx>MAXSIZE-1:
            continue
        if game.Btn_state[dx][dy] == 10 or game.Btn_state[dx][dy] == 11:
            continue
        if (dx, dy) in ssxx:
            continue
        elif game.Btn_state[dx][dy] == 0:
            check_pose(dx, dy)
        ssxx.add((dx, dy))

def cw():
    for i in game.Btn_block:
        if i.true_state == 11 and i.state != 10:
            return False
    return True

game = GM(root)
game.mainloop()