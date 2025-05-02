import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import random
import json

# The color scheme of the app
bgcolor = "#1c1c1e"
bgsecondary = "#3a3a3c"
cardcolor_front = "#5e5ce6"
cardcolor_back = "#ffc300"
cardcolor_empty = "#001d3d"
blacktext = "#1c1c1e"
whitetext = "#f2f2f7"
title = "#ff375f"
btncolor = "#f2f2f7"

window = tk.Tk()
window.title("Flashcards+")
window.geometry("600x700")
window.configure(bg=bgcolor)

# List to store flashcards (question, answer pairs)
flashcards = []
current_card = 0
showing_answer = False

def add_card():
    global flashcards
    question = question_entry.get().strip()
    answer = answer_entry.get().strip()
    
    if question and answer:
        flashcards.append((question, answer))
        question_entry.delete(0, tk.END)
        answer_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Flashcard added!")
        progress.config(text=f"{current_card + 1} / {len(flashcards)}")
        if len(flashcards) == 1:
            show_card()
    else:
        messagebox.showerror("Error", "Please enter both question and answer.")

def show_card():
    global showing_answer
    if flashcards:
        showing_answer = False
        canvas.itemconfig(card_text, text=flashcards[current_card][0], fill=whitetext)
        canvas.config(bg=cardcolor_front)
    else:
        canvas.itemconfig(card_text, text="Add some cards to start!")
        canvas.config(bg=cardcolor_empty)

def flip_card():
    global showing_answer
    if flashcards:
        if showing_answer:
            canvas.itemconfig(card_text, text=flashcards[current_card][0], fill=whitetext)
            canvas.config(bg=cardcolor_front)
            showing_answer = False
        else:
            canvas.itemconfig(card_text, text=flashcards[current_card][1], fill=blacktext)
            canvas.config(bg=cardcolor_back)
            showing_answer = True

def next_card():
    global current_card
    if flashcards:
        if current_card + 1 >= len(flashcards): # Show the first card after reaching the last card
            current_card = 0
        else:
            current_card += 1
        progress.config(text=f"{current_card + 1} / {len(flashcards)}")
        show_card()

def prev_card():
    global current_card
    if flashcards:
        if current_card == 0: # Show the last card after reaching the first card
            current_card = len(flashcards) - 1
        else:
            current_card -= 1
        progress.config(text=f"{current_card + 1} / {len(flashcards)}")
        show_card()

def delete_card():
    global flashcards, current_card
    if flashcards:
        flashcards.pop(current_card)
        if current_card >= len(flashcards):
            current_card = 0
        if flashcards:
            show_card()
        else:
            canvas.itemconfig(card_text, text="Add some cards to start!")
            canvas.config(bg=cardcolor_empty)
        progress.config(text=f"{current_card + 1} / {len(flashcards)}")
        messagebox.showinfo("Success", "Card deleted!")

def shuffle_cards():
    global flashcards, current_card
    if flashcards:
        random.shuffle(flashcards)
        current_card = 0
        show_card()
        progress.config(text=f"{current_card + 1} / {len(flashcards)}")
        messagebox.showinfo("Success", "Cards shuffled!")

def view_all_cards():
    if not flashcards:
        messagebox.showinfo("Info", "No cards to display!")
        return
    
    view_window = tk.Toplevel(window)
    view_window.title("All Flashcards")
    view_window.geometry("600x400")
    
    # Create Treeview for table data
    tree = ttk.Treeview(view_window, columns=("#", "Front", "Back"), show="headings")
    tree.heading("#", text="#")
    tree.heading("Front", text="Front")
    tree.heading("Back", text="Back")
    tree.column("#", width=50, anchor="center")
    tree.column("Front", width=250)
    tree.column("Back", width=250)
    tree.pack(padx=10, pady=10, fill="both", expand=True)
        
    # Add scrollbar
    scrollbar = ttk.Scrollbar(view_window, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)
        
    # Insert flashcards into table
    for i, (question, answer) in enumerate(flashcards, 1): # enumarate() function loops through a list and get both the index and the value at the same time
        tree.insert("", "end", values=(i, question, answer))

def save_set():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")],
        title="Save Flashcards"
        # Example of a file path: C:\Documents\my_flashcards.json
    )
    if file_path:  # Check if the user selected a file (didn't cancel)
        try:
            with open(file_path, 'w') as f: # Opens the selected file in write mode to prepare for writing the JSON data
                                            # with ... as f: ensures the file is closed automatically after writing
                json.dump(flashcards, f) # Converts the flashcards list to JSON format and writes it to the file.
            messagebox.showinfo("Success", "Cards saved successfully!")
        except Exception as e: # Prevents potential errors
            messagebox.showerror("Error", f"Failed to save cards: {str(e)}")

def new_set():
    global flashcards, current_card, showing_answer
    save = messagebox.askquestion(title="Save Current Set", message="Would you like to save this current set before creating a new one?")
    if save == "yes":
        save_set()
    # Clear all existing flashcards
    flashcards = []
    current_card = 0
    showing_answer = False
    progress.config(text=f"0 / 0")
    messagebox.showinfo("Success", "New flashcard set created!")
    canvas.itemconfig(card_text, text="Add some cards to start!")
    canvas.config(bg=cardcolor_empty)

def load_set():
    global flashcards, current_card
    save = messagebox.askquestion(title="Save Current Set", message="Would you like to save this current set before loading a new one?")
    if save == "yes":
        save_set()
    # Clear all existing flashcards
    flashcards = []
    current_card = 0
    showing_answer = False
    progress.config(text=f"0 / 0")
    canvas.itemconfig(card_text, text="Add some cards to start!")
    canvas.config(bg=cardcolor_empty)
    
    file_path = filedialog.askopenfilename(
        filetypes=[("JSON files", "*.json")],
        title="Load Flashcards"
    )
    if file_path:  # Check if the user selected a file (didn't cancel)
        try:
            with open(file_path, 'r') as f: # Opens the selected file in read mode to prepare for reading the JSON data
                                            # with ... as f: ensures the file is closed automatically after reading
                loaded_cards = json.load(f) # Converts JSON format to the flashcards list
            # Validate loaded data
            if not isinstance(loaded_cards, list) or not all(isinstance(card, (list, tuple)) and len(card) == 2 for card in loaded_cards):
                raise ValueError("Invalid flashcard data format")
            flashcards = loaded_cards
            current_card = 0
            progress.config(text=f"{current_card + 1} / {len(flashcards)}")
            show_card()
            messagebox.showinfo("Success", "Cards loaded successfully!")
        except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
            messagebox.showerror("Error", f"Failed to load cards: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
# GUI Elements
tk.Label(text="Flashcards+", font=("Arial Black", 40, "bold"), bg=bgcolor, fg=title, pady=10).pack()

canvas = tk.Canvas(window, width=400, height=200, highlightthickness=0, bg=cardcolor_empty)
canvas.pack(pady=20)
card_text = canvas.create_text(200, 100, text="Add some cards to start!", font=("Arial", 14), width=280, justify="center", fill=whitetext)

flip_button = tk.Button(window, text="Flip Card", command=flip_card, highlightbackground=bgcolor, bg=btncolor, fg=blacktext, font=("Arial", 12))
flip_button.pack(pady=5)

# Frame for Next and Previous buttons
nav_frame = tk.Frame(window, bg=bgcolor)
nav_frame.pack(pady=5)

prev_button = tk.Button(nav_frame, text="◄", command=prev_card, highlightbackground=bgcolor, bg=btncolor, fg=blacktext, font=("Arial", 12))
prev_button.grid(row=0, column=0, padx=5)

progress = tk.Label(nav_frame, text="0 / 0", bg=bgcolor, fg=whitetext, font=("Arial", 12))
progress.grid(row=0, column=1, padx=5)

next_button = tk.Button(nav_frame, text="►", command=next_card, highlightbackground=bgcolor, bg=btncolor, fg=blacktext, font=("Arial", 12))
next_button.grid(row=0, column=2, padx=5)

# Frame for Delete, Shuffle, and View All buttons
button_frame = tk.Frame(window, bg=bgcolor)  # Added bg=bgcolor
button_frame.pack(pady=5)

delete_button = tk.Button(button_frame, text="Delete Card", command=delete_card, highlightbackground=bgcolor, bg=btncolor, fg=blacktext, font=("Arial", 12))
delete_button.grid(row=0, column=0, padx=5)

shuffle_button = tk.Button(button_frame, text="Shuffle Cards", command=shuffle_cards, highlightbackground=bgcolor, bg=btncolor, fg=blacktext, font=("Arial", 12))
shuffle_button.grid(row=0, column=1, padx=5)

view_all_button = tk.Button(button_frame, text="View All Cards", command=view_all_cards, highlightbackground=bgcolor, bg=btncolor, fg=blacktext, font=("Arial", 12))
view_all_button.grid(row=0, column=2, padx=5)

# Add card frame
add_frame = tk.Frame(window, bg=bgcolor)
add_frame.pack(pady=10)

tk.Label(add_frame, text="Front:", bg=bgcolor, fg=whitetext, font=("Arial", 12)).grid(row=0, column=0)
question_entry = tk.Entry(add_frame, width=30, bg=bgsecondary, highlightbackground=bgcolor, fg=whitetext, font=("Arial", 12))
question_entry.grid(row=0, column=1, padx=5)

tk.Label(add_frame, text="Back:", bg=bgcolor, fg=whitetext, font=("Arial", 12)).grid(row=1, column=0)
answer_entry = tk.Entry(add_frame, width=30, bg=bgsecondary, highlightbackground=bgcolor, fg=whitetext, font=("Arial", 12))
answer_entry.grid(row=1, column=1, padx=5)

add_button = tk.Button(add_frame, text="Add Card", command=add_card, highlightbackground=bgcolor, bg=btncolor, fg=blacktext, font=("Arial", 12))
add_button.grid(row=2, column=0, columnspan=2, padx=5)

# File frame
file_frame = tk.Frame(window, bg=bgcolor)
file_frame.pack(pady=10)

save_button = tk.Button(file_frame, text="Save File", command=save_set, highlightbackground=bgcolor, bg=btncolor, fg=blacktext, font=("Arial", 12))
save_button.grid(row=0, column=0, padx=5)
new_button = tk.Button(file_frame, text="New File", command=new_set, highlightbackground=bgcolor, bg=btncolor, fg=blacktext, font=("Arial", 12))
new_button.grid(row=0, column=1, padx=5)
load_button = tk.Button(file_frame, text="Load File", command=load_set, highlightbackground=bgcolor, bg=btncolor, fg=blacktext, font=("Arial", 12))
load_button.grid(row=0, column=2, padx=5)

tk.mainloop()