from tkinter import *


class DisplayStats:
    def __init__(self, window):
        self.window = window
        self.window.title("Scrollable Table")

        # Create the main heading
        heading_label = Label(window, text="Statistics", font=("Arial", 16, "bold"))
        heading_label.pack(pady=10)

        # Create a frame for the table
        table_frame = Frame(window)
        table_frame.pack(pady=10)

        # Create the scrollable table
        self.create_table(table_frame)

    def create_table(self, frame):
        # Create a canvas with a scrollbar
        self.canvas = Canvas(frame)
        scrollbar = Scrollbar(frame, orient="vertical", command=self.canvas.yview)
        table_frame = Frame(self.canvas)

        table_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=table_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add sample data to the table
        for i in range(100):
            item_label = Label(table_frame, text="Item " + str(i + 1))
            item_label.grid(row=i, column=0, padx=10, pady=5)

            value_label = Label(table_frame, text="Value " + str(i + 1))
            value_label.grid(row=i, column=1, padx=10, pady=5)

            description_label = Label(table_frame, text="Description " + str(i + 1))
            description_label.grid(row=i, column=2, padx=10, pady=5)

        # Configure mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# Create the main window
window = Tk()

# Create an instance of the DisplayStats class
display_stats = DisplayStats(window)

# Run the Tkinter event loop
window.mainloop()
