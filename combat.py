import tkinter as tk
import random
import game_logic
import combat
from tkinter import font as tkfont

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Game")
        self.root.configure(bg="black")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda event: self.root.destroy())
        
        self.game_state = "menu"
        self.current_area = game_logic.landing_zone
        self.last_safe_area = game_logic.landing_zone

        self.dungeon_progress = 0 

        self.combat_context = None

        self.index_frame = None
        self.index_text = None
        
        self.default_menu = (
            "Test Game\n\n\n"
            "1. Start Game\n"
            "2. Credits\n"
            "3. Developer Note\n"
            "4. Index\n\n"
            "Enter Choice Below:"
        )
        
        self.menu_label = tk.Label(
            self.root, 
            text=self.default_menu, 
            font=("American Typewriter", 24), 
            fg="white", 
            bg="black", 
            justify="center",
            wraplength=1200
        )
        self.menu_label.pack(expand=True, fill="both")
        
        input_frame = tk.Frame(self.root, bg="black")
        input_frame.pack(pady=(0, 100))
        self.input_frame = input_frame
        
        prompt_label = tk.Label(input_frame, text="> ", font=("American Typewriter", 24), fg="white", bg="black")
        prompt_label.pack(side="left")
        
        self.root.bind('<Return>', self.route_input)
        
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

    def route_input(self, event):
        raw_text = self.user_input.get().strip()
        self.user_input.delete(0, tk.END)
        
        if self.game_state == "menu":
            self.handle_menu_choice(raw_text)
        elif self.game_state == "gameplay":
            self.handle_gameplay_command(raw_text)
        elif self.game_state == "combat":
            combat.handle_combat_input(self, raw_text)
        else:
            self.game_state = "gameplay"
            self.menu_label.config(text=self.current_area.get_details())

    def handle_menu_choice(self, choice):
        if choice == "1":
            self.game_state = "gameplay"
            self._hide_index_if_shown()
            self.menu_label.config(text=self.current_area.get_details())
        elif choice == "2":
            self._hide_index_if_shown()
            self.menu_label.config(text="Credits\n\nType 0 to go back.")
        elif choice == "3":
            self._hide_index_if_shown()
            self.menu_label.config(text="Developer Note\n\nI worked on this game and \n I'm pretty proud of it :)\n\nType 0 to go back.")
        elif choice == "4":
            self.game_state = "menu"
            self.show_index()
        elif choice == "0":
            self._hide_index_if_shown()
            self.game_state = "menu"
            self.menu_label.config(text=self.default_menu)
        else:
            self._hide_index_if_shown()
            self.menu_label.config(text=f"INVALID CHOICE: '{choice}'\n\nPlease select 1, 2, 3, or 4.")

    def _hide_index_if_shown(self):
        if self.index_frame:
            self.index_frame.pack_forget()
            self.index_frame.destroy()
            self.index_frame = None
            self.index_text = None

        if not self.menu_label.winfo_ismapped():
            try:
                if getattr(self, "input_frame", None) and self.input_frame.winfo_exists():
                    self.menu_label.pack(expand=True, fill="both", before=self.input_frame)
                else:
                    self.menu_label.pack(expand=True, fill="both")
            except Exception:
                self.menu_label.pack(expand=True, fill="both")

    def show_index(self):
        if self.menu_label.winfo_ismapped():
            self.menu_label.pack_forget()

        self.index_frame = tk.Frame(self.root, bg="black")
        self.index_frame.pack(expand=True, fill="both", padx=40, pady=20)

        scrollbar = tk.Scrollbar(self.index_frame)
        scrollbar.pack(side="right", fill="y")

        text_font = tkfont.Font(family="American Typewriter", size=16)
        self.index_text = tk.Text(
            self.index_frame,
            font=text_font,
            fg="white",
            bg="black",
            wrap="word",
            yscrollcommand=scrollbar.set,
            bd=0,
            highlightthickness=0,
            padx=10,
            pady=10
        )
        self.index_text.pack(expand=True, fill="both", side="left")
        scrollbar.config(command=self.index_text.yview)

        self.index_text.tag_config("header", foreground="#FFFFFF", font=(None, 18, "bold"))
        self.index_text.tag_config("weapon", foreground="#4FA3FF")   # blue
        self.index_text.tag_config("character", foreground="#7CFF8A")# green
        self.index_text.tag_config("enemy", foreground="#FF6B6B")    # red
        self.index_text.tag_config("location", foreground="#FFD66B") # yellow/gold
        self.index_text.tag_config("muted", foreground="#AAAAAA")
        self.index_text.tag_config("section", foreground="#FFFFFF", font=(None, 17, "bold"))

        weapons = []
        characters = []
        enemies = []
        locations = []

        for name, obj in vars(game_logic).items():
            if name.startswith("_"):
                continue
            try:
                if isinstance(obj, game_logic.Weapon):
                    weapons.append(obj)
                    continue
            except Exception:
                pass
            try:
                if isinstance(obj, game_logic.Enemy):
                    enemies.append(obj)
                    continue
            except Exception:
                pass
            try:
                if isinstance(obj, game_logic.Ally):
                    characters.append(obj)
                    continue
            except Exception:
                pass
            try:
                if isinstance(obj, game_logic.Area):
                    locations.append(obj)
                    continue
            except Exception:
                pass

        weapons.sort(key=lambda w: getattr(w, "name", "").lower())
        characters.sort(key=lambda c: getattr(c, "name", "").lower())
        enemies.sort(key=lambda e: getattr(e, "name", "").lower())
        locations.sort(key=lambda l: getattr(l, "name", "").lower())

        self.index_text.insert("end", "INDEX\n", "header")
        self.index_text.insert("end", "\nWeapons\n", "section")
        if weapons:
            for w in weapons:
                line = f"-- {w.name} (Damage: {w.bonus_damage}, Rarity: {w.rarity})\n"
                self.index_text.insert("end", line, "weapon")
        else:
            self.index_text.insert("end", "  (none)\n\n", "muted")

        self.index_text.insert("end", "\nCharacters / Allies\n", "section")
        if characters:
            for c in characters:
                line = f"-- {c.name} (HP: {c.current_health}/{c.max_health}, ATK: {c.base_attack}\n"
                self.index_text.insert("end", line, "character")
        else:
            self.index_text.insert("end", "  (none)\n\n", "muted")

        self.index_text.insert("end", "\nEnemies\n", "section")
        if enemies:
            for e in enemies:
                line = f"-- {e.name} (HP: {e.current_health}/{e.max_health}, ATK: {e.base_attack}, Boss: {e.is_boss})\n"
                self.index_text.insert("end", line, "enemy")
        else:
            self.index_text.insert("end", "  (none)\n\n", "muted")

        self.index_text.insert("end", "\nLocations\n", "section")
        if locations:
            for loc in locations:
                exits = ", ".join(k.upper() for k in getattr(loc, "exits", {}).keys()) or "NONE"
                line = f"-- {loc.name} (Type: {loc.zone_type})\n"
                self.index_text.insert("end", line, "location")
        else:
            self.index_text.insert("end", "  (none)\n\n", "muted")

        self.index_text.insert("end", "\nType 0 and press Enter to return to the main menu.", "muted")

        self.index_text.config(state="disabled")

    def handle_gameplay_command(self, command):
        clean_command = command.lower().strip()
        output_buffer = ""
        
        if clean_command.startswith("go "):
            direction = clean_command.replace("go ", "").strip()
            if direction in self.current_area.exits:
                self.current_area = self.current_area.exits[direction]
                output_buffer += f"You travel {direction}. \n\n"

                if getattr(self.current_area, "is_safe", False):
                    self.last_safe_area = self.current_area

                if isinstance(self.current_area, game_logic.Dungeon):
                    combat.start_encounter(self, self.current_area)
                    return
                else:
                    self.menu_label.config(text=output_buffer + self.current_area.get_details())
            else:
                self.menu_label.config(text=f'Blocked! There is no exit to the "{direction}".')
        elif clean_command == "menu":
            self.game_state = "menu"
            self.menu_label.config(text=self.default_menu)
        else:
            self.menu_label.config(text=f"Unknown command: '{command}'\nTry 'go north' or 'menu'\n\n" + self.current_area.get_details())
         
if __name__ == "__main__":
    window = tk.Tk()
    app = Game(window)
    window.mainloop()
