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

        partner.statistics.config(state=DISABLED)

        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))

        heading_label = Label(self.stats_box, text="Statistics", font=("Arial", 16, "bold"))
        heading_label.pack(pady=10)

        self.stats_table_frame = Frame(self.stats_box, width=300, height=200)
        self.stats_table_frame.pack()

        self.stats_table = Canvas(self.stats_table_frame)
        self.scrollbar = Scrollbar(self.stats_table_frame, orient="vertical", command=self.stats_table.yview)
        self.table_inner_frame = Frame(self.stats_table)

        self.table_inner_frame.bind(
            "<Configure>",
            lambda e: self.stats_table.configure(scrollregion=self.stats_table.bbox("all"))
        )

        self.stats_table.create_window((0, 0), window=self.table_inner_frame, anchor="nw")

        self.stats_table.configure(yscrollcommand=self.scrollbar.set)
        self.stats_table.bind_all("<MouseWheel>", self._on_mousewheel)

        self.stats_table.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y", padx=10, pady=10)

        for i in range(100):
            item_label = Label(self.table_inner_frame, text="Item " + str(i + 1),
                               padx=10, pady=5)
            item_label.grid(row=i, column=0)

            value_label = Label(self.table_inner_frame, text="Value " + str(i + 1),
                                padx=10, pady=5)
            value_label.grid(row=i, column=1)

            description_label = Label(self.table_inner_frame, text="Description " + str(i + 1),
                                      padx=10, pady=5)
            description_label.grid(row=i, column=2)

            if i % 2 == 0:
                item_label.config(bg="#98eda6")
                value_label.config(bg="#98eda6")
                description_label.config(bg="#98eda6")
            else:
                item_label.config(bg="#ed9898")
                value_label.config(bg="#ed9898")
                description_label.config(bg="#ed9898")

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
