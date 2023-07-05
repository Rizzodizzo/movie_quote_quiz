from tkinter import *
from functools import partial


class Converter:
    def __init__(self):
        button_font = ("Arial", "14")

        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()

        self.button_frame = Frame(padx=30, pady=30)
        self.button_frame.grid(row=0)

        self.statistics = Button(self.button_frame,
                                 text="Statistics",
                                 font=button_font, width=12,
                                 bg="#DAE8FC",
                                 command=self.to_stats)
        self.statistics.grid(row=1, column=0,
                             padx=5, pady=5)

    def to_stats(self):
        DisplayStats(self)


class DisplayStats:
    def __init__(self, partner):
        self.stats_box = Toplevel()

        # disable the statistics button when stats is open
        partner.statistics.config(state=DISABLED)

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

        for i in range(100):
            item_label = Label(self.table_inner_frame, text="Question " + str(i + 1),
                               padx=10, pady=5, width=25, height=3,
                               wraplength=170)
            item_label.grid(row=i, column=0, sticky="ew")

            value_label = Label(self.table_inner_frame, text="User answer " + str(i + 1),
                                padx=10, pady=5, width=15, height=3,
                                wraplength=100)
            value_label.grid(row=i, column=1, sticky="ew")

            description_label = Label(self.table_inner_frame, text="answer " + str(i + 1),
                                      padx=10, pady=5, width=15, height=3,
                                      wraplength=100)
            description_label.grid(row=i, column=2, sticky="ew")

            if i % 2 == 0:
                item_label.config(bg="#98eda6",
                                  highlightbackground="#55c968",
                                  highlightthickness=1)
                value_label.config(bg="#98eda6",
                                   highlightbackground="#55c968",
                                   highlightthickness=1)
                description_label.config(bg="#98eda6",
                                         highlightbackground="#55c968",
                                         highlightthickness=1)
            else:
                item_label.config(bg="#ed9898",
                                  highlightbackground="#d14b4b",
                                  highlightthickness=1)
                value_label.config(bg="#ed9898",
                                   highlightbackground="#d14b4b",
                                   highlightthickness=1)
                description_label.config(bg="#ed9898",
                                         highlightbackground="#d14b4b",
                                         highlightthickness=1)

        # Frame for the general stats like total correct or incorrect
        self.general_stats_frame = Frame(self.stats_box)
        self.general_stats_frame.pack()

        self.total_correct_label = Label(self.general_stats_frame, font=("Arial", "10"),
                                         text="Total Questions: ___", bg="#DAE8FC",
                                         highlightthickness=1,
                                         highlightbackground="#6591d0",
                                         pady=10, padx=5)
        self.total_correct_label.pack(side=LEFT, padx=10, pady=10)

        self.percent_label = Label(self.general_stats_frame, font=("Arial", "10"),
                                   text="Total Incorrect: ___", bg="#f8cecc",
                                   highlightthickness=1,
                                   highlightbackground="#c95651",
                                   pady=10, padx=5)
        self.percent_label.pack(side=RIGHT, padx=10, pady=10)

        self.total_incorrect_label = Label(self.general_stats_frame, font=("Arial", "10"),
                                           text="Total Correct: ___", bg="#d5e8d4",
                                           highlightthickness=1,
                                           highlightbackground="#54c94e",
                                           pady=10, padx=5)
        self.total_incorrect_label.pack(padx=10, pady=10)

        # frame for the buttons
        self.control_stats_frame = Frame(self.stats_box, padx=10, pady=10)
        self.control_stats_frame.pack(side=BOTTOM)

        self.dismiss_button = Button(self.control_stats_frame,
                                     font=("Arial", "14"),
                                     text="Dismiss", bg="#FFE6CC",
                                     highlightbackground="#e39545",
                                     highlightthickness=1,
                                     command=partial(self.close_stats, partner))
        self.dismiss_button.pack()

    def _on_mousewheel(self, event):
        self.stats_table.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def close_stats(self, partner):
        partner.statistics.config(state=NORMAL)
        self.stats_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    Converter()
    root.mainloop()
