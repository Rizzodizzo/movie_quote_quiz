from tkinter import *
from functools import partial  # to prevent unwantned windows


class Converter:

    def __init__(self):
        # common format for all buttons
        # Arial size 14 bold with white text
        button_font = ("Arial", "14")

        # Set up GUI Frame
        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()

        self.button_frame = Frame(padx=30, pady=30)
        self.button_frame.grid(row=0)

        self.help_info_button = Button(self.button_frame,
                                       text="Help / info",
                                       font=button_font, width=12,
                                       bg="#DAE8FC",
                                       command=self.to_help)
        self.help_info_button.grid(row=1, column=0,
                                   padx=5, pady=5)

    def to_help(self):
        DisplayHelp(self)


class DisplayHelp:

    def __init__(self, partner):
        # set up dialogue box and background colour
        background = "#DAE8FC"
        self.help_box = Toplevel()

        # disable help button
        partner.help_info_button.config(state=DISABLED)

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
        partner.help_info_button.config(state=NORMAL)
        self.help_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    Converter()
    root.mainloop()
