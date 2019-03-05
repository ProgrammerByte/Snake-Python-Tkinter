from tkinter import *
from tkinter import messagebox
from random import randint

class setupwindow():
    def __init__(window): #window is the master object of the setup window
        window.root = Tk()
        window.root.title("Setup")
        window.root.grid()

        window.finish = "N"

        labels = ["Height:", "Width:", "Speed:"]
        window.label = ["","",""]
        window.entry = ["","",""]
        
        for i in range(3):
            window.label[i] = Label(text = labels[i])
            window.label[i].grid(row = i, column = 1)
            window.entry[i] = Entry()
            window.entry[i].grid(row = i, column = 2)

        window.AImode = IntVar()
        window.ai = Checkbutton(text = "AI mode", variable = window.AImode).grid(row = 3, column = 2)

        window.startbutton = Button(text = "Start", command = lambda: setupwindow.onclick(window))
        window.startbutton.grid(row = 4, column = 2)
        window.root.mainloop()

    def onclick(window):
        setupwindow.verification(window)
        if window.verf == "Y":
            window.finish = "Y"
            window.root.destroy()
            return window

    def verification(window):
        height = window.entry[0].get()
        width = window.entry[1].get()
        speed = window.entry[2].get()

        window.verf = "N"
        if height.isdigit() and width.isdigit() and speed.isdigit():
            height = int(height)
            width = int(width)
            speed = int(speed)

            if height > 2 and height <= 24:

                if width > 2 and width <= 48:

                    if speed > 0 and speed <= 1000:
  
                        window.verf = "Y"
                        window.height = height
                        window.width = width
                        window.speed = speed
                        
                        if window.AImode.get() == 1 and width % 2 == 1:
                            window.verf = "N"
                            messagebox.showerror("Invalid", "If AI mode is on then width must be even!")

                        else:
                            window.AImode = window.AImode.get()


                            
                    else:
                        messagebox.showerror("Invalid", "Speed must be between 1 and 1000 inclusive!")
                else:
                    messagebox.showerror("Invalid", "Width must be between 3 and 48 inclusive!")
            else:
                messagebox.showerror("Invalid", "Height must be between 3 and 24 inclusive!")
        else:
            messagebox.showerror("Invalid", "All values must be integers!")


class gamewindow():
    #"s" is the shorthand of "self"
    def __init__(s, setup):
        s.width = setup.width
        s.height = setup.height
        s.speed = setup.speed
        s.AImode = setup.AImode
        s.score = 0

        s.buffer = float(1 / s.speed)
        s.buffer = int(s.buffer * 1000)

        s.combinationsi = [1, -1, 0, 0]
        s.combinationsx = [0, 0, 1, -1]

        s.currenti = s.combinationsi[2]
        s.currentx = s.combinationsx[2]

        s.eaten = "N"
        s.cont = "Y"
        
        s.root = Tk()
        s.root.title("Snake")
        
        s.root.bind("a", lambda event="a", index=3: gamewindow.keypress(event, s, index))
        s.root.bind("w", lambda event="w", index=1: gamewindow.keypress(event, s, index))
        s.root.bind("s", lambda event="s", index=0: gamewindow.keypress(event, s, index))
        s.root.bind("d", lambda event="d", index=2: gamewindow.keypress(event, s, index))
        
        s.root.grid()

        s.scorelabel = Label(text = "Score: 0", font = "Calibri 20 bold")
        s.scorelabel.grid()
        
        s.frame = Frame()
        s.maingrid = list()
        for i in range(s.height):
            s.maingrid.append([])
            for x in range(s.width):
                s.maingrid[i].append("")
                s.maingrid[i][x] = Label(s.frame, bg = "Black", height = 2, width = 4)
                s.maingrid[i][x].grid(row = i, column = x)
                s.maingrid[i][x].tail = "False"
                s.maingrid[i][x].head = "False"

        s.frame.grid(row = 2)
        
        s.midpoint = int(s.height / 2)
        s.maingrid[s.midpoint][0].configure(bg = "Green")
        s.maingrid[s.midpoint][0].tail = "True"         #Where the tail starts
        s.maingrid[s.midpoint][1].configure(bg = "Green")
        s.maingrid[s.midpoint][1].head = "True"         #Where the head starts

        s.maingrid[s.midpoint][0].directioni = s.currenti
        s.maingrid[s.midpoint][0].directionx = s.currentx #Flags which determine which direction the head and tail must move
        s.maingrid[s.midpoint][1].directioni = s.currenti
        s.maingrid[s.midpoint][1].directionx = s.currentx

        gamewindow.generatefood(s)
            
        gamewindow.RefreshScreen(s)

        if s.AImode == 1 and s.width % 2 == 0:
            s.nearbottom = s.height - 2
            s.farright = s.width - 1
            s.farleft = 0
            s.top = 0
            s.bottom = s.height - 1
            gamewindow.AI(s)

        s.root.mainloop()

    def AI(s):
        event = "placeholder"
        index = 0
        gamewindow.keypress(event, s, index) #Starts the snake moving downwards
        s.direction = "Down" #keep track of what direction the AI is travelling
        s.temp = "N"

        def AIloop(s):
            for x in range(s.width):
                for i in range(s.height):
                    if i == s.bottom and s.maingrid[i][x].head == "True" and s.temp == "N": #This part of the AI must only be executed once
                        s.temp = "Y"
                        index = 2
                        gamewindow.keypress(event, s, index)

                    elif s.temp == "Y": #Main loop section
                        if (i == s.bottom and x == s.farright and s.maingrid[i][x].head == "True") or (i == s.nearbottom and s.direction == "Left" and s.maingrid[i][x].head == "True"):
                            index = 1
                            s.direction = "Up"
                            gamewindow.keypress(event, s, index)

                        elif (i == s.top and s.direction == "Up" and s.maingrid[i][x].head == "True") or (i == s.nearbottom and x != 0 and s.direction == "Down" and s.maingrid[i][x].head == "True"):
                            index = 3
                            s.direction = "Left"
                            gamewindow.keypress(event, s, index)

                        elif i == s.top and s.direction == "Left" and s.maingrid[i][x].head == "True":
                            index = 0
                            s.direction = "Down"
                            gamewindow.keypress(event, s, index)

                        elif i == s.bottom and x == s.farleft and s.maingrid[i][x].head == "True":
                            index = 2
                            s.direction = "Right"
                            gamewindow.keypress(event, s, index)

            
            s.root.after(s.buffer, AIloop, s)
            
        AIloop(s)
    
    def keypress(event, s, index):
        nexti = s.combinationsi[index]
        nextx = s.combinationsx[index]
        
        headfound = "N"

        if s.refresh == "Y":
            for a in range(s.height):
                for b in range(s.width):
                    if s.maingrid[a][b].head == "True" and headfound == "N":
                        headfound = "Y"
                        previousi = s.maingrid[a][b].directioni
                        previousx = s.maingrid[a][b].directionx
                        
                        if nexti == 0 or previousi == 0:
                            if nextx == 0 or previousx == 0:
                                s.maingrid[a][b].directioni = nexti
                                s.maingrid[a][b].directionx = nextx
                                s.refresh = "N"

    def generatefood(s):
        acceptableindexesi = list()
        acceptableindexesx = list()
        
        for i in range(s.height):
            for x in range(s.width):
                if s.maingrid[i][x]["bg"] == "Black":
                    acceptableindexesi.append(i)
                    acceptableindexesx.append(x)

        if len(acceptableindexesi) != 0:
            index = randint(0, len(acceptableindexesi) - 1)
            ivalue = acceptableindexesi[index]
            xvalue = acceptableindexesx[index]

            s.maingrid[ivalue][xvalue].configure(bg = "Red")
                    
        
    def RefreshScreen(s):
        s.refresh = "Y"
        headfound = "N"
        tailfound = "N"

        if s.cont == "Y":
            for a in range(s.height):
                for b in range(s.width):
                    
                    if s.maingrid[a][b].head == "True" and headfound == "N":
                        headfound = "Y"
                        s.maingrid[a][b].head = "False"
                        avalue = a + s.maingrid[a][b].directioni
                        bvalue = b + s.maingrid[a][b].directionx
                        
                        if avalue >= 0 and avalue < s.height and bvalue >= 0 and bvalue < s.width:
                            if s.maingrid[avalue][bvalue]["bg"] != "Green":

                                if s.maingrid[avalue][bvalue]["bg"] == "Red":
                                    s.eaten = "Y"
                                    gamewindow.generatefood(s)

                                    s.score += 1
                                    s.scorelabel.configure(text = "Score: {}".format(s.score))
                                
                                s.maingrid[avalue][bvalue].head = "True"
                                s.maingrid[avalue][bvalue].configure(bg = "Green")

                                s.maingrid[avalue][bvalue].directioni = s.maingrid[a][b].directioni
                                s.maingrid[avalue][bvalue].directionx = s.maingrid[a][b].directionx

                            else:
                                messagebox.showinfo("GAME OVER", "You have lost!")
                                s.cont = "N"
                                s.root.destroy()
                        else:
                            messagebox.showinfo("GAME OVER", "You have lost!")
                            s.cont = "N"
                            s.root.destroy()


                    elif s.eaten == "N": 
                        if s.maingrid[a][b].tail == "True" and tailfound == "N":
                            tailfound = "Y"
                            s.maingrid[a][b].tail = "False"
                            if s.cont == "Y":
                                s.maingrid[a][b].configure(bg = "Black")
                                
                                avalue = a + s.maingrid[a][b].directioni
                                bvalue = b + s.maingrid[a][b].directionx

                                s.maingrid[avalue][bvalue].tail = "True"

                    elif tailfound == "N":
                        tailfound = "Y"
                        s.eaten = "N"

        s.root.after(s.buffer, gamewindow.RefreshScreen, s)


if __name__ == "__main__":
    setup = setupwindow()
    if setup.finish == "Y":
        game = gamewindow(setup)
        quit()
