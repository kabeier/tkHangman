from tkinter import Tk
from tkinter.ttk import Frame, Button
import tkinter as tk
from PIL import Image, ImageTk
import string
import random
import csv


class Hangman(Frame):
    def __init__(self,root):
        super().__init__()
        self.root=root
        self.guessnumber = 0
        self.wrongguess = 0
        self.goal_word = ''
        self.display_word = ''
        self.win=False
        self.lose=False
        self.category='fandb'
        self.goal_word_nospc=''
        self.keybuttons = []
        self.catstring=''
        self.catbuts=[]
        self.initUI()
        self.catdisbut=tk.Button(self)

    def initUI(self):
        alphabet=[]
        def make_word():
            wordbankfb = []
            wordbankan = []
            wordbankr = []
            wordbankc = []
            with open('fandb.csv') as csvfile:
                word_reader = csv.reader(csvfile, delimiter=',')
                for row in word_reader:                          
                        wordbankfb.append(row[0])

            with open('animals.csv') as csvfile:
                word_reader = csv.reader(csvfile, delimiter=',')
                for row in word_reader:
                    wordbankan.append(row[0])
        
            with open('random.csv') as csvfile:
                word_reader = csv.reader(csvfile, delimiter=',')
                for row in word_reader:
                    wordbankr.append(row[0])
        
            with open('clothes.csv') as csvfile:
                word_reader = csv.reader(csvfile, delimiter=',')
                for row in word_reader:
                    wordbankc.append(row[0])
 
            if(self.category == "fandb"):
                wordbank = wordbankfb
                self.catstring = "Food & Bev"
            if(self.category == "animals"):
                wordbank=wordbankan
                self.catstring = "Animals"
            if(self.category == "random"):
                wordbank = wordbankr
                self.catstring = "Random"
            if(self.category == "clothes"):
                wordbank = wordbankc
                self.catstring = "Clothes"

            gw = random.sample(wordbank, 1)[0]
            print(gw)
            self.goal_word_nospc=gw
            gws=''
            for letter in gw:
                gws += letter+" "
            self.goal_word=gws
           
        def make_word_board(self):
            make_word()
            word=''
            for letters in self.goal_word.split():
                word += "_ "
            self.display_word = word

        def make_letters():
            for letter in string.ascii_lowercase[:26]:
                alphabet.append(letter)

        def make_letter_buttons(self):
            make_letters()
            row_position = 2
            col_position = 1
            for letter in alphabet:
                if(col_position > 7):
                    col_position=1
                    row_position+=1
                lb = tk.Button(self, text=letter.capitalize(), bg="darkgrey", fg="black",font='Helvetica 18 bold', width=2, height=2, command=lambda j=letter: [press(self,j)])
                lb.grid(row=row_position, column=col_position)
                col_position+=1
                self.keybuttons.append(lb)

        def guess_letter(self, letter):
            dp_word = []
            test_array = self.goal_word.split()
            display_array = self.display_word.split()
            for i in range(len(test_array)):
                if test_array[i] == letter:
                    display_array[i] = letter
                dp_word.append(display_array[i])
            self.display_word = ' '.join(dp_word)
            self.display_word = self.display_word.strip()

        def press(self, letter):           
            compstr=self.display_word        
            guess_letter(self, letter)
            self.guessnumber+=1
            letterindex = 27

            for i in range(len(string.ascii_lowercase[:26])):
                if string.ascii_lowercase[i] == letter:
                    letterindex = i

            self.keybuttons[letterindex].configure(
                command=lambda: [], fg='lightgrey')
            
            if(compstr.strip()==self.display_word):
                self.wrongguess+=1
                imgfile = f"{self.wrongguess}.gif"
                image = ImageTk.PhotoImage(file=imgfile)
                hangman.config(image=image, bg="black")
                hangman.image = image
            
            ansb.delete("1.0", tk.END)
            ansb.insert(tk.END, self.display_word)
            ansb.tag_configure("center", justify='center')
            ansb.tag_add("center", "1.0", "end")
            win_or_lose()
            
        def win_or_lose():
            if self.wrongguess>=7:
                self.lose=True
            if self.display_word.strip()==self.goal_word.strip():
                self.win=True
            if self.win:
                for btn in self.keybuttons:
                    btn.grid_forget()
                self.catdisbut.grid_forget()
                win = tk.Text(self, height=2, width=15, fg="black",
                            bg="darkgrey", font='Helvetica 40 bold')
                win.insert(tk.END, f"You Win! \n In {self.guessnumber} tries")
                win.tag_configure("center", justify='center')
                win.tag_add("center", "1.0", "end")
                win.grid(row=2, column=1, columnspan=4, rowspan=3)
                quit = tk.Button(self, text="QUIT", fg="black", bg="red", font='Helvetica 18 bold', command=lambda: [self.master.destroy()], width=4, height=2)
                quit.grid(row=5, column=1, columnspan=2)
                newgame = tk.Button(self, text="New \n Game", fg="black", bg="green", font='Helvetica 14 bold', command=lambda: [
                                    new_game(self)], width=5, height=2)
                newgame.grid(row=5, column=3, columnspan=2)

            if self.lose:
                for btn in self.keybuttons:
                    btn.grid_forget()
                self.catdisbut.grid_forget()
                lose = tk.Text(self, height=2, width=15, fg="black",
                                  bg="darkgrey", font='Helvetica 40 bold')
                lose.insert(tk.END, "You're a Loser!\n it was "+self.goal_word_nospc.title())
                lose.tag_configure("center", justify='center')
                lose.tag_add("center", "1.0", "end")
                lose.grid(row=2, column=1, columnspan=4, rowspan=3)
                quit = tk.Button(self, text="QUIT", fg="black", bg="red", font='Helvetica 18 bold', command=lambda: [
                                 self.master.destroy()], width=4, height=2)
                quit.grid(row=5, column=1, columnspan=2)
                newgame = tk.Button(self, text="New \n Game", fg="black", bg="green", font='Helvetica 14 bold', command=lambda: [
                    new_game(self)], width=5, height=2)
                newgame.grid(row=5, column=3, columnspan=2)

        def new_game(self):
            refresh(self.root)

        def get_category(self):
            cat = tk.Text(self, height=1, width=15, fg="black",
                           bg="darkgrey", font='Helvetica 25 bold')
            cat.insert(tk.END, "Pick a Category")
            cat.tag_configure("center", justify='center')
            cat.tag_add("center", "1.0", "end")
            cat.grid(row=2, column=1, columnspan=7)
            self.catbuts.append(cat)

            catbut1 = tk.Button(self, command=lambda: [set_cat('animals'), kill_cat()])
            image = ImageTk.PhotoImage(file="animals.gif")
            catbut1.image = ImageTk.PhotoImage(file="animals.gif")
            catbut1.config(image=image, bg="black")
            catbut1.image = image
            catbut1.grid(row=3, column=1)
            self.catbuts.append(catbut1)

            catbut2 = tk.Button(self, command=lambda: [set_cat('fandb'), kill_cat()])
            image = ImageTk.PhotoImage(file="fandb.gif")
            catbut2.image = ImageTk.PhotoImage(file="fandb.gif")
            catbut2.config(image=image, bg="black")
            catbut2.image = image
            catbut2.grid(row=3, column=4)
            self.catbuts.append(catbut2)

            catbut3 = tk.Button(self, command=lambda:[set_cat("random"), kill_cat()])
            image = ImageTk.PhotoImage(file="random.gif")
            catbut3.image = ImageTk.PhotoImage(file="random.gif")
            catbut3.config(image=image, bg="black")
            catbut3.image = image
            catbut3.grid(row=4, column=4 )
            self.catbuts.append(catbut3)

            catbut4 = tk.Button(self, command=lambda: [set_cat('clothes'), kill_cat()])
            image = ImageTk.PhotoImage(file="clothes.gif")
            catbut4.image = ImageTk.PhotoImage(file="clothes.gif")
            catbut4.config(image=image, bg="black")
            catbut4.image = image
            catbut4.grid(row=4, column=1)
            self.catbuts.append(catbut4)
            self.pack()

        def kill_cat():
            make_word_board(self)
            for buts in self.catbuts:
                buts.grid_forget()
            catdisbut = tk.Text(self, height=2, width=12, fg="black",
                                    bg="darkgrey", font='Helvetica 8 bold')
            catdisbut.insert(
                tk.END, f"Category:\n {self.catstring}")
            catdisbut.tag_configure("center", justify='center')
            catdisbut.tag_add("center", "1.0", "end")
            catdisbut.grid(row=5, column=6, columnspan=2, rowspan=2)
            self.catdisbut = catdisbut
            make_letter_buttons(self)

        def set_cat(s):
            self.category=s
            
        
        #body Starts here

        self.master.title("Hang Man v1.1.2")
        get_category(self)
        ansb = tk.Text(self, height=1, width=25, fg="black",
                        bg="darkgrey", font='Helvetica 22 bold')
        ansb.insert(tk.END, self.display_word.strip())
        ansb.tag_configure("center", justify='center')
        ansb.tag_add("center", "1.0", "end")
        ansb.grid(row=1, column=1, columnspan=10)

        hangman = tk.Button(self)
        imgfile = f"{self.wrongguess}.gif"
        image = ImageTk.PhotoImage(file=imgfile)
        hangman.config(image=image, bg="black")
        hangman.image = image
        hangman.grid(row=2, column=10, rowspan=4)
        self.pack()

def main(): 
    root= Tk()
    root.configure(background="black")
    app = Hangman(root)
    root.mainloop()

def refresh(root):
    root.destroy()
    main()
    

if __name__ == '__main__':
    main()

    
