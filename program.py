from tkinter import *
from tkinter import ttk
from time import sleep
from random import randint

def calculate_data(data, rule):
    newdata = [0]
    for i in range(1,len(data)-1):
        newdata.append(rule[int((str(data[i-1]) + str(data[i]) + str(data[i+1])), 2)])
    newdata.append(0)
    #print(newdata)
    return newdata

def blank(mode, size = 1):
    A = []
    if mode == 0:
        for i in range(int(size/2)):A.append(0)
        A.append(1)
        for i in range(size - int(size/2) - 1): A.append(0)
        return A
    elif mode == 1:
        for i in range(size): A.append(i % 2)
        return A
    elif mode == 2:
        t=[1,1,0]
        for i in range(size): A.append(t[i % 3])
        return A
    elif mode == 3:
        t=[1,0,0]
        for i in range(size): A.append(t[i % 3])
        return A
    elif mode == 4:
        for i in range(size): A.append(int(randint(0,1)))
        return A
    else: return 0

class window():
    def __init__(self, win):
        self.win = win
        self.arrSize = {"x":700, "y":300}
        self.blockSize = 2
        win.title('Elementary Cellular Automaton')
        self.city = None
        self.mainframe = Frame(self.win)
        self.mainframe.pack()

        self.f1 = Frame(self.mainframe)
        self.f1.pack(side = LEFT, padx=10, pady=5)
        self.f2 = Frame(self.mainframe)
        self.f2.pack(side = LEFT, padx=10)
        self.f3 = Frame(self.mainframe, width = 60)
        self.f3.pack(side = LEFT, padx=10)
        self.f4 = Frame(self.win)
        self.f4.pack(side = BOTTOM, pady=5)

        Label(self.f1, text = "Rule:")
        self.rules = []
        self.rule_txt = []
        for i in range(8):
            Label(self.f1, text=((3-len(str(bin(i))[2:5]))*"0") + str(bin(i))[2:5] + ": ", font="Arial").grid(row = i, column = 0)
            self.rule_txt.append(StringVar(self.win))
            self.rules.append(Entry(self.f1, font='Arial 12', textvariable = self.rule_txt[i], width = 1))
        i = 0
        for r in self.rules:
            r.grid(row = i, column = 1)
            i+=1

        self.initStates = {"Dot":0,"Switching":1,"2b-1w":2,"1b-2w":3,"Random":4}
        Label(self.f2, text = "Initial State").grid(row=0)
        self.init = StringVar(self.win)
        ttk.Combobox(self.f2, textvariable=self.init, values=list(self.initStates.keys())).grid(row = 1)

        self.preRules = {"Rule 10":"01010000","Rule 28":"00111000","Rule 30":"01111000","Rule 50":"01001100","Rule 54":"01101100","Rule 60":"00111100","Rule 90":"01011010","Rule 110":"01110110","Rule 126":"01111110","Rule 150":"01101001","Rule 182":"01101101","Rule 188":"00111101","Rule 190":"01111101","Rule 220":"00111011","Rule 222":"01111011","Rule 250":"01011111"}
        Label(self.f2, text = "Preset Rules").grid(row=2)
        self.preset_slc = StringVar(self.win)
        self.preset_slc.trace('w', self.parsePreRule)
        ttk.Combobox(self.f2, textvariable=self.preset_slc, values=list(self.preRules.keys())).grid(row = 3)

        self.f5 = Frame(self.f2)
        self.f5.grid(row=4, pady=(25, 0))
        self.sizeIn = Entry(self.f5, text=(str(self.arrSize['x']) + 'x' + str(self.arrSize['y'])), width = 15)
        self.sizeIn.grid(row = 0, column = 1)
        Button(self.f5, text="Set size", command=self.changeSize, width=8).grid(row = 0, column = 0, sticky=W, padx = 5)
        self.blockIn = Entry(self.f5, text=str(self.blockSize), width = 15)
        self.blockIn.grid(row = 1, column = 1)
        Button(self.f5, text="Set block", command=self.changeBlock, width=8).grid(row = 1, column = 0, sticky=W, padx = 5)


        Button(self.f3, text="DO IT", bg="yellow", command = self.birth).pack(fill='y')

    def changeSize(self):
        s = self.sizeIn.get().split('x')
        print(s)
        try:
            self.arrSize = {"x":int(s[0]), "y":int(s[1])}
            print("Changed canvas size!")
        except Exception as e:
            print("Error: " + str(e))

    def changeBlock(self):
        try:
            self.blockSize = int(self.blockIn.get())
            print("Changed block size")
        except Exception as e:
            print("Error: " + str(e))

    def getRule(self):
        A = []
        for i in self.rule_txt:
            A.append(i.get())
        print (A)
        return A

    def birth(self):

        try: self.city.destroy()
        except Exception as e: print(str(e) + " (No canvas)")
        self.city = Canvas(self.f4, width = self.arrSize['x'], height = self.arrSize['y'], bg="white")
        self.city.pack(side = BOTTOM)
        try:self.city.delete(ALL)
        except Exception as e: print(e)

        epoch_ = 1
        rule_ = self.getRule()
        data = blank(self.initStates[self.init.get()], int(self.arrSize['x']/self.blockSize))
        while epoch_ < int(self.arrSize['y']/self.blockSize):
            self.draw_life(epoch_, data)
            data = calculate_data(data, rule_)
            epoch_ += 1
            #print()

    def parsePreRule(self, index, value, op):
        for i in range(8):
            #print(self.preRules[self.preset_slc.get()])
            self.rule_txt[i].set(self.preRules[self.preset_slc.get()][i])

    def open(self):
        root.mainloop()

    def draw_life(self, epoch = 1, data = []):
        col = ['white', 'black']
        if epoch * 2 - 1 > int(self.arrSize['x']/self.blockSize): col = ['white', 'red']
        for i in range(int(self.arrSize['x']/self.blockSize)):
            self.city.create_rectangle(self.blockSize*i, self.blockSize*epoch, 3+self.blockSize*(i+1), 3+self.blockSize*(epoch+1), fill=col[int(data[i])], outline = "")
            #print(".", end = "")


if __name__ == "__main__":
    root = Tk()
    app = window(root)
    app.open()
