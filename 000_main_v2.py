from tkinter import *
from functools import partial
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
                                  text="Movie Quote Quiz",
                                  font=("Arial", "18", "bold"))
        self.menu_heading.grid(row=0)

        instructions = "Welcome to the Movie Quote Quiz! In this quiz " \
                       "a quote from a movie will appear and 4 different " \
                       "movies will appear below. You will have to guess which " \
                       "movie you think the quote comes from. Your stats will " \
                       "appear when you hit the 'statistics' button while in game.\n\n" \
                       "Please enter the amount of rounds in bar below or leave blank " \
                       "for infinite mode!"
        self.menu_instructions = Label(self.chose_rounds_frame,
                                       text=instructions,
                                       wraplength=220, width=35,
                                       justify="left",
                                       pady=10, bg="#DAE8FC",
                                       highlightbackground="#728fb8",
                                       highlightthickness=1)
        self.menu_instructions.grid(row=1)

        self.error_label = Label(self.chose_rounds_frame,
                                 text="Leave blank for infinite mode",
                                 fg="#00b816", padx=10, pady=10,
                                 font=("Arial", "12", "bold"),
                                 wraplength=235)
        self.error_label.grid(row=2)

        self.entry_button_frame = Frame(self.chose_rounds_frame)
        self.entry_button_frame.grid(row=3)

        self.rounds_entry = Entry(self.entry_button_frame, width=10,
                                  font=("Arial", 18))
        self.rounds_entry.grid(row=0, column=0)

        self.start_button = Button(self.entry_button_frame,
                                   text="Start",
                                   font=button_font, width=10,
                                   bg="#8af29b",
                                   fg=button_fg,
                                   activebackground="#6bcf7d",
                                   command=lambda: self.check_rounds())
        self.start_button.grid(row=0, column=1,
                               padx=5, pady=5)

    def check_rounds(self):
        has_error = "no"
        error = "Please enter a number above 0"

        response = self.rounds_entry.get()

        if response == "":
            self.error_label.config(text="Leave blank for infinite mode",
                                    fg="#00b816")
            self.to_play("infinite")
            return

        # check that user has entered a valid number...
        try:
            response = int(response)

            if response <= 0:
                has_error = "yes"

        except ValueError:
            has_error = "yes"

        # give response if there is error or not
        if has_error == "yes":
            self.error_label.config(text=error,
                                    fg="#b30000")
        else:
            self.error_label.config(text="Leave blank for infinite mode".format(response),
                                    fg="#00b816")
            self.to_play(response)

    def to_play(self, num_rounds):
        Play(num_rounds)

        # hide Menu
        root.withdraw()


class Play:

    def __init__(self, how_many):
        self.play_box = Toplevel()

        # set number of rounds
        self.num_rounds = how_many
        self.rounds_played = 1

        # set number of correct an incorrect
        self.num_correct = 0
        self.num_incorrect = 0

        # list of questions and answers for the statistics window
        # will be updated every question
        self.statistics = []

        # if users press cross at tip, closes help and
        # 'refuses' help button
        self.play_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_play))

        self.in_quiz_frame = Frame(self.play_box, padx=10, pady=10)
        self.in_quiz_frame.grid()

        rounds_heading = "Round {} of {}".format(self.rounds_played, self.num_rounds)
        self.choose_heading = Label(self.in_quiz_frame,
                                    text=rounds_heading,
                                    font=("Arial", "16", "bold"))
        self.choose_heading.grid(row=0)

        self.question = self.generate_quote_answers()
        self.quote = self.question[0]

        self.quote_label = Label(self.in_quiz_frame,
                                 text='Quote:\n"{}"'.format(self.quote),
                                 justify="left", wraplength=290, width=31,
                                 font=("Arial", "12"),
                                 bg="#D5E8D4", pady=5, padx=10,
                                 highlightbackground="#77a674",
                                 highlightthickness=1)
        self.quote_label.grid(row=1, column=0)

        self.options_frame = Frame(self.in_quiz_frame)
        self.options_frame.grid(row=2)

        # A list of buttons to make a for loop that calls
        answers = self.question[2]

        # randomise a list of 4 positions to make the answers randomise positions'
        self.position_list = [0, 1, 2, 3]
        random.shuffle(self.position_list)

        # the list and makes the button
        option_button_list = [
            [0, 0, answers[0]],
            [0, 1, answers[1]],
            [1, 0, answers[2]],
            [1, 1, self.question[1]]
        ]

        # list to hold references for answer buttons
        # So I can easily config it later
        self.answer_button_ref = []

        for item in range(0, 4):
            self.option_button = Button(self.options_frame,
                                        width=15, height=3,
                                        bg="#FFF2CC", text=option_button_list[self.position_list[item]][2],
                                        font=("Arial", 11), padx=5,
                                        wraplength=150, activebackground="#FFF2CC",
                                        highlightbackground="#C9BFA1",
                                        highlightthickness=1,
                                        command=lambda i=self.position_list[item]: self.check_answer(
                                            option_button_list[i][2]))
            self.option_button.grid(row=option_button_list[self.position_list[item - 1]][0],
                                    column=option_button_list[self.position_list[item - 1]][1],
                                    padx=5, pady=5)
            # add buttons to answer list
            self.answer_button_ref.append(self.option_button)

        # recycling from colour game the control buttons stay the same
        self.control_frame = Frame(self.in_quiz_frame)
        self.control_frame.grid(row=7)

        # a list to make my control buttons at the bottom vary
        control_buttons = [
            ["#99CCFF", "Help", "get help"],
            ["#FFB366", "Statistics", "get stats"],
            ["#808080", "Start Over", "start over"]
        ]

        # list to hold  references for control buttons
        # con easily be configured when the game
        self.control_button_ref = []

        for item in range(0, 3):
            self.make_control_button = Button(self.control_frame,
                                              bg=control_buttons[item][0],
                                              text=control_buttons[item][1],
                                              width=9, font=("Arial", 12, "bold"))
            self.make_control_button.grid(row=0, column=item, padx=5, pady=5)

            # add buttons to control list
            self.control_button_ref.append(self.make_control_button)

        # make help button have a command
        self.to_help_btn = self.control_button_ref[0]
        self.to_help_btn.config(command=lambda: self.to_help())

        # get stats button and disable it
        self.to_stats_btn = self.control_button_ref[1]
        self.to_stats_btn.config(state=DISABLED,
                                 command=lambda: self.to_stats(self.statistics))

        # get start over button
        self.restart_btn = self.control_button_ref[2]
        self.restart_btn.config(text="Restart", command=lambda: self.close_play())

        # frame for the next round button and the temporary statistics
        self.temp_state_frame = Frame(self.in_quiz_frame)
        self.temp_state_frame.grid(row=6, padx=10, pady=10)

        self.next_round_button = Button(self.temp_state_frame,
                                        text="Next Round",
                                        font=("Arial", "12"), width=10,
                                        bg="#e88cff", state=DISABLED,
                                        command=lambda: self.next_round())
        self.next_round_button.grid(row=0, column=0,  padx=5)

        self.stats_label = Label(self.temp_state_frame,
                                 text="Correct:  {}   Incorrect:  {}".format(self.num_correct, self.num_incorrect),
                                 justify="left",
                                 font=("Arial", "12"),
                                 bg="#ffe380", pady=5, padx=5,
                                 highlightbackground="#e3c96f",
                                 highlightthickness=1)
        self.stats_label.grid(row=0, column=1, padx=5)

    def close_play(self):
        # reshow menu
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

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
                # check if answer is the same as correct
                if rand_movie != self.answer and rand_movie not in answers:
                    answers.append(rand_movie)
                    break

        return [question, self.answer, answers]

    def next_round(self):

        # change heading
        self.choose_heading.config(text="Round {} of {}".format(self.rounds_played, self.num_rounds))

        # get new quote and answers
        self.question = self.generate_quote_answers()
        self.quote = self.question[0]

        # update quotes
        self.quote_label.config(text='Quote:\n"{}"'.format(self.quote))

        # A list of buttons to make a for loop that calls
        answers = self.question[2]
        # the list and makes the button
        option_button_list = [
            [0, 0, answers[0]],
            [0, 1, answers[1]],
            [1, 0, answers[2]],
            [1, 1, self.question[1]]
        ]

        # shuffle positions
        random.shuffle(self.position_list)

        # change and enable buttons
        option_config_count = 0
        for item in self.answer_button_ref:
            item.config(text=option_button_list[self.position_list[option_config_count]][2],
                        command=lambda i=self.position_list[option_config_count]: self.check_answer(
                            option_button_list[i][2]),
                        state=NORMAL, bg="#FFF2CC")
            option_config_count += 1

        # disable next round button
        self.next_round_button.config(state=DISABLED)

    def check_answer(self, user_answer):

        print(user_answer)
        if user_answer == self.answer:
            self.num_correct += 1
        else:
            self.num_incorrect += 1

        # enable stats button as a question has been answered
        self.to_stats_btn.config(state=NORMAL)

        # check if answer is correct or not
        if self.num_correct >= self.num_incorrect:
            self.stats_label.config(bg="#98eda6",
                                    highlightbackground="#1ced3f")
        else:
            self.stats_label.config(bg="#ed9898",
                                    highlightbackground="#eb6060")

        # update mini stats
        self.stats_label.config(text="Correct:  {}   Incorrect:  {}".format(self.num_correct, self.num_incorrect))

        # disable options and enable next round button
        for item in self.answer_button_ref:
            item.config(state=DISABLED)
            # change the colours of the correct and incorrect answers
            if item.cget("text") == self.answer:
                item.config(bg="#97f98f")
            elif item.cget("text") == user_answer and item.cget("text") != self.answer:
                item.config(bg="#f8b8b8")

        # continue uf there are still more rounds
        if self.num_rounds == "infinite":
            self.next_round_button.config(state=NORMAL)
            self.rounds_played += 1
        elif self.rounds_played < self.num_rounds:
            self.next_round_button.config(state=NORMAL)
            self.rounds_played += 1
        else:
            self.restart_btn.config(bg="#B3FF66", text="Play Again")

        # update statistics list so the stats includes the question just answered
        # and add item to the top of the list so that the most recent is shown at
        # the top
        current_stat = [self.quote, user_answer, self.answer]
        self.statistics.insert(0, current_stat)

    def to_help(self):
        DisplayHelp(self)

    def to_stats(self, statistics):
        DisplayStats(self, statistics)


class DisplayStats:
    def __init__(self, partner, statistics):
        self.stats_box = Toplevel()

        # number of correct and incorrect variables
        self.num_correct = 0
        self.num_incorrect = 0

        # disable the statistics button when stats is open
        partner.to_stats_btn.config(state=DISABLED)

        # make sure the window will close when 'x' at top left is clicked
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))

        # create the statistics heading
        heading_label = Label(self.stats_box, text="Statistics", font=("Arial", 16, "bold"))
        heading_label.pack(pady=10)

        # frame for the statistics
        self.stats_table_frame = Frame(self.stats_box, width=300, height=200)
        self.stats_table_frame.pack()

        # a canvas which CHATGPT showed me how to use to get the scroll feature
        self.stats_table = Canvas(self.stats_table_frame, width=490, height=300)
        self.scrollbar = Scrollbar(self.stats_table_frame, orient="vertical", command=self.stats_table.yview)
        self.table_inner_frame = Frame(self.stats_table, padx=20, pady=20)

        # set the region that scrolls down to the whole window
        self.table_inner_frame.bind(
            "<Configure>",
            lambda e: self.stats_table.configure(scrollregion=self.stats_table.bbox("all"))
        )

        # the next few lines is Chat GPT, here it is creating a window that goes
        # in the frame, and it can hold 1 tkinter widget
        self.stats_table.create_window((0, 0), window=self.table_inner_frame, anchor="nw")

        # here Chat creates a scroll bar on hte left in the window
        self.stats_table.configure(yscrollcommand=self.scrollbar.set)

        # here Chat binds mouse scrolling using a function called _on_mousewheel
        self.stats_table.bind_all("<MouseWheel>", self._on_mousewheel)

        # here this puts the scrollbar on the right and the table with stats on the left
        self.stats_table.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y", padx=10, pady=10)

        # headings for the columns
        question_label_heading = Label(self.table_inner_frame, text="Question",
                                       padx=10, pady=2, width=25, height=3, justify="left",
                                       wraplength=170, bg="#A0A0A0")
        question_label_heading.grid(row=0, column=0, sticky="ew")

        user_answer_label_heading = Label(self.table_inner_frame, text="Your Answer",
                                          padx=10, pady=2, width=15, height=3, justify="left",
                                          wraplength=100, bg="#A0A0A0")
        user_answer_label_heading.grid(row=0, column=1, sticky="ew")

        answer_label_heading = Label(self.table_inner_frame, text="Answer",
                                     padx=10, pady=2, width=15, height=3, justify="left",
                                     wraplength=100, bg="#A0A0A0")
        answer_label_heading.grid(row=0, column=2, sticky="ew")

        # loop that creates the items that goes in the table
        # variable to change the row each loop
        self.list_row = 1
        for i in list(statistics):
            question_label = Label(self.table_inner_frame, text=i[0],
                                   padx=10, pady=5, width=25, height=3,
                                   wraplength=170)
            question_label.grid(row=self.list_row, column=0, sticky="ew")

            user_answer_label = Label(self.table_inner_frame, text=i[1],
                                      padx=10, pady=5, width=15, height=3,
                                      wraplength=100)
            user_answer_label.grid(row=self.list_row, column=1, sticky="ew")

            answer_label = Label(self.table_inner_frame, text=i[2],
                                 padx=10, pady=5, width=15, height=3,
                                 wraplength=100)
            answer_label.grid(row=self.list_row, column=2, sticky="ew")

            # add 1 to num of rows
            self.list_row += 1

            # checks if answer was incorrect or correct and assigns colour to the
            # corresponding row, also increase number of correct and incorrect
            if i[1] == i[2]:
                question_label.config(bg="#98eda6",
                                      highlightbackground="#55c968",
                                      highlightthickness=1)
                user_answer_label.config(bg="#98eda6",
                                         highlightbackground="#55c968",
                                         highlightthickness=1)
                answer_label.config(bg="#98eda6",
                                    highlightbackground="#55c968",
                                    highlightthickness=1)
                self.num_correct += 1
            else:
                question_label.config(bg="#ed9898",
                                      highlightbackground="#d14b4b",
                                      highlightthickness=1)
                user_answer_label.config(bg="#ed9898",
                                         highlightbackground="#d14b4b",
                                         highlightthickness=1)
                answer_label.config(bg="#ed9898",
                                    highlightbackground="#d14b4b",
                                    highlightthickness=1)
                self.num_incorrect += 1

        # Frame for the general stats like total correct or incorrect
        self.general_stats_frame = Frame(self.stats_box)
        self.general_stats_frame.pack()

        # next three labels are the stats, I had to pack them in this order else it
        # wouldn't format it correctly.
        self.total_questions_label = Label(self.general_stats_frame, font=("Arial", "10"),
                                           text="Total Questions: {}".format(len(statistics)), bg="#e1dcfc",
                                           highlightthickness=1,
                                           highlightbackground="#6855cb",
                                           pady=10, padx=5)
        self.total_questions_label.pack(side=LEFT, padx=10, pady=10)

        self.total_incorrect_label = Label(self.general_stats_frame, font=("Arial", "10"),
                                           text="Total Incorrect: {}".format(self.num_incorrect), bg="#f8cecc",
                                           highlightthickness=1,
                                           highlightbackground="#c95651",
                                           pady=10, padx=5)
        self.total_incorrect_label.pack(side=RIGHT, padx=10, pady=10)

        self.total_correct_label = Label(self.general_stats_frame, font=("Arial", "10"),
                                         text="Total Correct: {}".format(self.num_correct), bg="#d5e8d4",
                                         highlightthickness=1,
                                         highlightbackground="#54c94e",
                                         pady=10, padx=5)
        self.total_correct_label.pack(padx=10, pady=10)

        # frame for the buttons
        self.control_stats_frame = Frame(self.stats_box, padx=10, pady=10)
        self.control_stats_frame.pack(side=BOTTOM)

        # button to close stats
        self.dismiss_button = Button(self.control_stats_frame,
                                     font=("Arial", "14"),
                                     text="Dismiss", bg="#FFE6CC",
                                     highlightbackground="#e39545",
                                     highlightthickness=1,
                                     command=partial(self.close_stats, partner))
        self.dismiss_button.pack()

    # function so that you can scroll wiht the mouse wheel
    def _on_mousewheel(self, event):
        self.stats_table.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # close Stats function
    def close_stats(self, partner):
        partner.to_stats_btn.config(state=NORMAL)
        self.stats_box.destroy()


class DisplayHelp:

    def __init__(self, partner):
        # set up dialogue box and background colour
        background = "#DAE8FC"
        self.help_box = Toplevel()

        # disable help button
        partner.to_help_btn.config(state=DISABLED)

        # if users press cross at top, closes help and
        # 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300, height=200,
                                bg=background)
        self.help_frame.grid()

        self.help_heading = Label(self.help_frame,
                                  text="Help / Information", bg=background,
                                  font=("Arial", "23", "bold"))
        self.help_heading.grid(row=0)

        help_text = "To engage in this quiz you will be presented with a Quote from a " \
                    "Movie at the top. below there will be 4 buttons, each with there " \
                    "own movie title on them. All you need to do is guess the movie that" \
                    "feature that quote.\n\n If you get it right you should see the button" \
                    "you clicked turn green. If you got it wrong you should see the button" \
                    "you clicked turn red and the correct option turn green. When you have" \
                    "chosen your answer and are ready to move on click the next round button" \
                    "to be presented with a new question for as many rounds as you have chose.\n\n" \
                    "At the bottom there should be some statistics to show you how well you are" \
                    "going but if you would like to see your past questions and answers you" \
                    "can click the 'statistics' button at the bottom middle of the screen."

        self.help_text_label = Label(self.help_frame, bg=background,
                                     text=help_text, wraplength=370,
                                     justify="left", font=("Arial", "12"))
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "14", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help,
                                                     partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

    # closes help dialogue (used by button and x at top of dialogue)
    def close_help(self, partner):
        # Put help button back tp normal...
        partner.to_help_btn.config(state=NORMAL)
        self.help_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    Menu()
    root.mainloop()
