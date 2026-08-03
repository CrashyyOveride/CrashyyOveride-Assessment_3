import tkinter as tk
import random
import game_logic

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Game")
        self.root.configure(bg="black")
        self.root.attributes("-fullscreen", True)
        
        self.root.bind("<Escape>", lambda event: self.root.destroy())


        self.default_menu = (
            "Test Game\n\n\n"
            "1. Start Game\n"
            "2. Credits\n"
            "3. Developer Note\n\n\n"
            "Enter Choice Below:"
        )

        self.menu_label = tk.Label(
            self.root,
            text=self.default_menu,
            font=("American Typewriter", 24),
            fg="white",
            bg="black",
            justify="center"
        )
        self.menu_label.pack(expand=True, fill="both")

        input_frame = tk.Frame(self.root, bg="black")
        input_frame.pack(pady=(0, 100))

        prompt_label = tk.Label(input_frame, text="> ", font=("American Typewriter", 24), fg="white", bg="black")
        prompt_label.pack(side="left")

        self.user_input = tk.Entry(
            input_frame,
            font=("American Typewriter", 24),
            fg="white",
            bg="#222222",
            width=15,
            insertbackground="white",
            bd=0,
            highlightthickness=0
        )
        self.user_input.pack(side="left")
        self.user_input.focus_set()

        self.root.bind('<Return>', self.handle_menu_choice)

    def handle_menu_choice(self, event):
        choice = self.user_input.get().strip()
        self.user_input.delete(0, tk.END)

        if choice == "1":
            self.menu_label.config(text="LAUNCHING GAME....\n")
        elif choice == "2":
            self.menu_label.config(text="Credits\n\nType 0 to go back.")
        elif choice == "3":
            self.menu_label.config(text="Developer Note\n\nI worked on this game and \n I'm pretty proud of it :)\n\nType 0 to go back.")
        elif choice == "0":
            self.menu_label.config(text=self.default_menu)
        else:
            self.menu_label.config(text=f"INVALID CHOICE: '{choice}'\n\nPlease select 1, 2, or 3.")



if __name__ == "__main__":
    window = tk.Tk()
    app = Game(window)
    window.mainloop()
