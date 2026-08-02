import tkinter as tk

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

class Character:
    def __init__(self, name: str, health: int, attack_power: int):
        self.name = name
        self.max_health = health
        self.current_health = health
        self.base_attack = attack_power
        self.is_alive = True
        self.equipped_weapon = None

    def get_attack_power(self):
        if self.equipped_weapon:
            return self.base_attack + self.equipped_weapon.bonus_damage
        return self.base_attack

    def take_damage(self, amount: int):
        self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0
            self.is_alive = False
            
class Ally(Character):
    def __init__(self, name: str, health: int, attack_power: int, can_use_magic: bool):
        super().__init__(name, health, attack_power)
        self.can_use_magic = can_use_magic # Exiled will be False, anyone else will be True

    def heal_target(self, target: Character, amount: int):
        if self.is_alive and target.is_alive:
            target.current_health = min(target.max_health, target.current_health + amount)

class Enemy(Character):
    def __init__(self, name: str, health: int, attack_power: int, is_boss: bool, primary_zone: str ="Any"):
        super().__init__(name, health, attack_power)
        self.is_boss = is_boss
        self.primary_zone = primary_zone
        self.is_attackable = True

        def trigger_status_effect(self):
            """Placeholder"""
            pass

class Weapon:
    def __init__(self, name: str, bonus_damage: int, rarity: str):
        self.name = name
        self.bonus_damage = bonus_damage
        self.rarity = rarity

### HERE ARE ALL CHARACTERS :)))

player = Ally(name="Exiled", health=100, attack_power=15, can_use_magic=False)
ernest = Ally(name="Ernest Blackwood", health=120, attack_power=18, can_use_magic=True)
mary = Ally(name="Mary Althea", health=9999, attack_power=0, can_use_magic=True)

bandit = Enemy(name="Gilded Gold Underling", health=30, attack_power=8, is_boss=False)
orsted = Enemy(name="Orsted Drake", health=999999999999999, attack_power=99999999999, is_boss=True)
orsted.is_attackable = False

soldat =  Enemy(name="Soldat Vanderbilt", health=130, attack_power=30, is_boss=False)

### Dungeon 1 Monsters & Boss
orb = Enemy(name="Orb", health=20, attack_power=5, is_boss=False)
noid = Enemy(name="Noid", health=45, attack_power=12, is_boss=False)
lesser_dragon = Enemy(name="Lesser Dragon", health=350, attack_power=40, is_boss=True)

















if __name__ == "__main__":
    window = tk.Tk()
    app = Game(window)
    window.mainloop()
