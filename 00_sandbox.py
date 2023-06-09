import tkinter as tk
import colorsys
import random
import string

button_colors = ['#FFC2D6', '#B8E6C7', '#FFD9B3', '#C2E8FF', '#FFB3FF', '#B8E8FF', '#FFC299', '#D9FFB3'] * 37


def animate_button(button):
    button.config(relief=tk.SUNKEN)


def reset_button(button):
    button.config(relief=tk.RAISED)


def key_pressed(event):
    key = event.keysym.lower()
    if key == 'backspace':
        entry_text = entry_var.get()
        if entry_text:
            entry_var.set(entry_text[:-1])
    elif key == 'space':
        animate_button(button_map[' '])
        entry_var.set(entry_var.get() + ' ')
        window.after(100, lambda: reset_button(button_map[' ']))
    elif key == 'grave':
        entry_var.set('')
    elif key in button_map:
        animate_button(button_map[key])
        entry_var.set(entry_var.get() + key)
        window.after(100, lambda: reset_button(button_map[key]))


def generate_random_text():
    word_list = [
        'apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape', 'honeydew', 'imbe', 'jackfruit',
        'kiwi', 'lemon', 'mango', 'nectarine', 'orange', 'pear', 'quince', 'raspberry', 'strawberry', 'tangerine'
    ]
    random_text = ' '.join(random.sample(word_list, 5))
    random_label.config(text=random_text)


def clear_entry():
    entry_var.set('')


def create_button(row, column, key):
    button = tk.Button(window, text=key, width=4, height=2, bg=button_colors[(row * 14 + column) % num_colors])
    button.grid(row=row, column=column, padx=4, pady=4)
    button_map[key.lower()] = button
    button_ids.append(button)


window = tk.Tk()
window.title("Button Animation")

button_map = {}
button_ids = []

rows = [
    ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '', '', '', ''],
    ['', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\', '', '', ''],
    ['', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", '', '', '', ''],
    ['', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', '', '', '', ''],
    ['']
]

num_colors = min(len(rows[0])-2, len(button_colors))

for i, row in enumerate(rows):
    for j, key in enumerate(row):
        if key == '':
            continue
        create_button(i, j, key)

space_button = tk.Button(window, text='Space', width=30, height=2, bg=button_colors[-2])
space_button.grid(row=4, column=0, columnspan=14, padx=4, pady=4)
button_map[' '] = space_button
button_ids.append(space_button)

backspace_button = tk.Button(window, text='Backspace', width=8, height=2, bg=button_colors[-1])
backspace_button.grid(row=4, column=10, columnspan=2, padx=4, pady=4)
button_map['backspace'] = backspace_button
button_ids.append(backspace_button)

entry_var = tk.StringVar()
entry = tk.Entry(window, textvariable=entry_var, width=50, font=("Arial", 16), bd=4)
entry.grid(row=5, column=0, columnspan=16, padx=10, pady=10)

random_label = tk.Label(window, text='', font=("Arial", 12))
random_label.grid(row=6, column=0, columnspan=16, padx=10, pady=10)

generate_button = tk.Button(window, text='Generate Random Text', width=18, height=2, command=generate_random_text)
generate_button.grid(row=7, column=0, columnspan=8, padx=4, pady=4)

clear_button = tk.Button(window, text='Clear Entry (`)', width=12, height=2, command=clear_entry)
clear_button.grid(row=7, column=8, columnspan=8, padx=4, pady=4)

window.bind('<KeyPress>', key_pressed)

window.mainloop()
