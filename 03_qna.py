from tkinter import *
import csv
import random

class Menu:

    def __init__(self):
        # common format for all buttons
        # Arial size 14 bold with white text
        button_font = ("Arial", "12")
        button_fg = "#000000"

        # Set up GUI Frame
        self.chose_rounds_frame = Frame(padx=10, pady=10)
        self.chose_rounds_frame.grid()

        self.menu_heading = Label(self.chose_rounds_frame,
                                  text="Questions and Answers",
                                  font=("Arial", "18", "bold"))
        self.menu_heading.grid(row=0)

        self.quote = self.generate_quote()

        self.quote_label = Label(self.chose_rounds_frame,
                                 text='Quote:\n"{}"'.format(self.quote),
                                 justify="left", wraplength=290, width=31,
                                 font=("Arial", "12"),
                                 bg="#D5E8D4", pady=5, padx=10,
                                 highlightbackground="#77a674",
                                 highlightthickness=1)
        self.quote_label.grid(row=1, column=0)

        self.options_frame = Frame(self.chose_rounds_frame)
        self.options_frame.grid(row=2)

        # A list of buttons to make a for loop that calls
        # the list and makes the button
        option_button_list = [
            [0, 0, "The Lord of the Rings: The Fellowship of the Ring (2001)"],
            [0, 1, "Up (2009)"],
            [1, 0, "Option 3"],
            [1, 1, "Option 4"]
        ]

        for item in range(0, 4):
            self.option_button = Button(self.options_frame,
                                        width=16, height=3,
                                        bg="#FFF2CC", text=option_button_list[item][2],
                                        font=("Arial", 11),
                                        wraplength=160,
                                        highlightbackground="#C9BFA1",
                                        highlightthickness=1)
            self.option_button.grid(row=option_button_list[item - 1][0],
                                    column=option_button_list[item - 1][1],
                                    padx=5, pady=5)

    def generate_quote(self):
        file = open("movie_quotes.csv", "r")
        movie_quotes = list(csv.reader(file, delimiter=","))
        file.close()

        # remove the first row (header values
        movie_quotes.pop(0)

        # get the first 50 rows ( used to develop colour
        # buttons for play GUI
        print(movie_quotes[:50])

        print("Length: {}".format(len(movie_quotes)))

        # make a new list to put all the quotes in
        all_quotes = []
        for item in movie_quotes:
            all_quotes.append(item[0])

        # pick a random quote
        rand_quote = random.choice(all_quotes)
        print(rand_quote)

        return rand_quote


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    Menu()
    root.mainloop()

