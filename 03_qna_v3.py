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

        self.question = self.generate_quote_answers()
        self.quote = self.question[0]

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
        answers = self.question[2]
        # the list and makes the button
        option_button_list = [
            [0, 0, answers[0]],
            [0, 1, answers[1]],
            [1, 0, answers[2]],
            [1, 1, self.question[1]]
        ]

        for item in range(0, 4):
            self.option_button = Button(self.options_frame,
                                        width=16, height=3,
                                        bg="#FFF2CC", text=option_button_list[item][2],
                                        font=("Arial", 11),
                                        wraplength=140,
                                        highlightbackground="#C9BFA1",
                                        highlightthickness=1)
            self.option_button.grid(row=option_button_list[item - 1][0],
                                    column=option_button_list[item - 1][1],
                                    padx=5, pady=5)

    def generate_quote_answers(self):
        file = open("movie_quotes.csv", "r")
        movie_quotes = list(csv.reader(file, delimiter=","))
        file.close()

        # remove the first row (header values
        movie_quotes.pop(0)

        # get a random row to get the question and correct answer from
        correct_info = random.choice(movie_quotes)

        question = correct_info[0]
        self.answer = correct_info[1]
        answers = []
        # make a new list to put all the quotes in
        all_movies = []
        for item in movie_quotes:
            all_movies.append(item[1])

        # pick three random answers
        for i in range(0, 3):
            while True:
                rand_movie = random.choice(all_movies)
                print(rand_movie)
                # check if answer is the same as correct
                if rand_movie != self.answer and rand_movie not in answers:
                    answers.append(rand_movie)
                    break

        return [question, self.answer, answers]


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    Menu()
    root.mainloop()

