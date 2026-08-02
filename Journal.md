## Development Journal
___An incremental tracking log documenting the development lifecycle milestones, structural pivots, technical pitfalls, and troubleshooting workflows encountered during the production of this software application.___


<br>
<br>
<br>
<br>
<br>

# Journal Entry: May 10 - May 17, 2026

## Project: Python Text-Based RPG (Prototype 1)

### Current Progress
Today I built the initial prototype for a text-based RPG in Python. This version serves as a rough structural plan and my first training module to get comfortable with core programming concepts. 

The game currently uses nested dictionaries to manage the map layout, room data, and item locations. A basic `while` loop drives the gameplay, allowing players to navigate using `go` commands and collect items with `get` commands. I also implemented a functional inventory tracking system, a monster encounter event, and deterministic win/loss conditions.

### Current Training Code Script

```python
def showInstructions():
    print('''
RPG Test_1
==========
Commands:
go [direction]
get [item]
      ''')

def status():
    print("---------------")
    print(f"Current Room: {currentRoom}")
    print(f"Inventory: {inventory}")

    if "items" in rooms[currentRoom]:
        for item in rooms[currentRoom]["items"]:
            print(f"You see a {item}!")


def starting_scene():
    print("You inner voice is trying to speak with you.")
    print("It says to get out, anything will do just get out")
    
currentRoom = "Hall"

rooms = {
            "Dining Room" : {
                        "south" : "Garden",
                        "west" : "Hall",
                        "items" : ["Potion", "bread"] 
                            },
            "Garden" : {
                         "north" : "Dining Room",
                        "items" : ["Flower"]
                        },
            "Hall" : {
                        "south": "Bedroom",
                        "east" : "Garden",
                        "items" : ["Key"]
                     },
            "Bedroom" : {
                        "north" : "Hall",
                        "south" : "Garden",
                        "enemy_1" : "Monster"
                        }
        }


inventory = []

showInstructions()

starting_scene()


while True:

    status()
    move = input(">")
    move = move.split(" ", 1)
    if move[0] == "go":
        direction = move[1].lower()
        if move[1] in rooms[currentRoom]:
            currentRoom = rooms[currentRoom][move[1]]
            print(f"you now in {currentRoom}!")
        else:
            print(f"you can't go {move[1]}!")
            
    elif move[0] == "get":
        item_target = move[1].capitalize()

        if "items" in rooms[currentRoom] and item_target in rooms[currentRoom]["items"]:
            print(f"you got a {item_target}!")
            inventory.append(item_target)
            rooms[currentRoom]["items"].remove(item_target)
            print(inventory)
        else:
            print(f"You don't see a {item_target} here!")

        
    if "Key" in inventory and "Potion" in inventory:
        print("You escaped from Matej's Evil House!!!")
        break
    if "enemy_1" in rooms[currentRoom] and rooms[currentRoom]["enemy_1"] == "Monster":
        if "Potion" in inventory:
            print("You throw the potion onto the monster")
            print("The monster reveals itself as MATEJ")
            print("MATEJ weaken goes back into the house, letting you free")
            print("YOU WIN!")
            break
        else:
            print("There was a monster here!!!!")
            print("You have been eaten!")
            print("GAME OVER ")
            break
```

### Known Issues to Fix
* **Input Vulnerability:** The game crashes with an `IndexError` if a user inputs an empty command or presses enter without text because `move[0]` or `move[1]` fails.
* **Input Sensitivity:** Commands and room names are case-sensitive, which can disrupt the user experience.

### Next Steps & Evolution
* **Robust Input Validation:** Add boundary checks to input handling to prevent runtime crashes when players enter blank or single-word strings.
* **Advanced OOP Architecture:** Move away from procedural dictionaries and implement advanced **Object-Oriented Programming (OOP)**. This includes creating dedicated classes for `Room`, `Player`, `Item`, and `Enemy`, utilizing **inheritance** for entity types, and using **encapsulation** to safely manage game states.
* **GUI Development with Tkinter:** Transition the game from a command-line script into a desktop application using the **Tkinter** library.
* **UX/UI Enhancement:** Apply core User Experience (UX) and User Interface (UI) design principles to the new interface by implementing structural typography, consistent padding, clean layouts, and visual status indicators to make navigation intuitive.

# Journal Entry: May 18 - July 2, 2026

## Project: Python Text-Based RPG (Friendly Characters & Narrative Design)

### Current Progress
Today I shifted focus from core programming mechanics to world-building and narrative design. I mapped out the initial cast of characters, factions, and encounter-based narratives that will populate the game world. 

The core narrative design relies on an emergent, high-stakes system where non-player characters (NPCs) directly alter gameplay dynamics through random events. I established a balanced mix of potential allies, roaming military obstacles, and an invincible wandering boss to give the surface world a dangerous, unpredictable atmosphere.

### Friendly Profiles

* **The Exiled (Protagonist)**
* **Ernest Blackwood** 
* **Mary Althea**

### Known Issue to Fix
* **Mary's Choice Logic:** The persistence loop for Mary Althea requires strict state tracking. The choice to dismiss her must keep her active in the encounter pool, while the choice to heal must permanently flag her as unavailable without breaking the random encounter engine.

### Next Steps & Evolution
* **Dynamic Route Branching:** Outline the specific narrative paths (such as seeking absolute redemption, embracing vengeance against the sky, or purely hunting for wealth) to match the Exiled's shifting motives. I was thinking of desigining 5 set out endings where the player can pick which ending or route he wants to go down. 
* **Event-Driven Text Triggers:** Map out the exact dialogue lines and text for tavern NPCs when they react to regional rumors, Ernest’s brawls, or the mention of Orsted.
* **The Encounter Mini-Game:** Flesh out the conceptual rules for the high-stakes survival mini-game triggered when cornered by Orsted Drake.
* **UI Narrative Indicators:** Plan how the upcoming visual layout will telegraph faction presence, ensuring players get distinct text warnings when entering areas occupied by the Gilded Gold or the Northern Expedition Squad.

# Journal Entry: July 2 - July 22, 2026

## Project: Python Text-Based RPG (Non-friendly Characters & Narrative Design)

### Current Progress
Following the development of my friendly characters, I have shifted focus to narratibe design and hostile NPCs. The enemy roster will be highly diverse, spanning everything from human adversaries to various undead enemies. 

The core idea behind my design and creation of these non-friendly characters is to give a feel into the RPG aspect of my text-based game.

### Non-friendly Profiles

* **Soldat Vanderbilt & The Northern Expedition** 
* **Orsted Drake & The Gilded Gold**
* **Orb**
* **Noid**
* **Drakonid**
* **Lesser Dragon (Boss)**

### Known Issues to Fix
* **The Orsted Curse:** I need to design a system for dialogue tracking. If the player triggers text containing the name "Orsted" while interacting with NPCs, it must instantly trigger a negative reputation event and evict them from the zone.
* **Soldat's Progression Block:** Because Soldat's squad physically blocks dungeon access, bad random-number generation could continuously lock the player out of progression. The encounter logic needs a built-in cooldown or a "pity system" to ensure players aren't completely trapped.

### Next Steps & Evolution
* **Item Tiers & Unique Mechanical Attributes:** I will begin developing my weapons and unique mechanical attributes.

# Journal Entry: July 22 - July 23, 2026

## Project: Python Text-Based RPG (Item Tiers & Unique Mechanical Attributes)

### Current Progress
Today I pivoted from character design to engineering the loot system and weapon database. I established a tiered item structure spanning Common, Rare, and Legacy rarities. The goal is to move past static name strings and build complex items that alter game loops, unlock hidden visual zones, and manipulate combat configurations. Legacy items will serve as narrative milestones, linking lore directly to player performance.

### Item Profiles (May UPDATE or ADD new weapons as I'm developing)
* **Dagger (Dagger Class)**
* **Shield (Shield Class)**
* **Longsword (Sword Class)**
* **Greatsword (Sword Class)**
* **Stick (Sword Class)**
* **Holy Kris (Dagger Class)**
* **Vantablack Great Axe (Axe Class)**
* **Twinlight Odachi (Sword Class)**
* **Gravewarden (Scythe Class)**
* **Parthalán’s Silence (Dagger Class)**
* **Replica Glacial Hilt (Special Component Class)**

### Known Issues to Fix
* **Gravewarden Visibility State:** If a player enters the vast fields without the undead state active, the engine must mask the object array. I need to make sure the item lookup function doesn't throw a key error or reveal the item prematurely during standard inventory scans.

### Next Steps & Evolution
* **Buidling the core code:** I will begin developing and refining the final game engine. This includes replacing my practice data with custom variables, proprietary classes, unique characters, and distinct traits.

# Journal Entry: July 23 - August 3, 2026

## Project: Python Text-Based RPG (UI Setup & Character Architecture)

### Current Progress
I've done the front end of the game where the starting screen and options are all done. I need to work on finishing and polishing the final combat, travel, and dialogue code in order for this game to be finish. 

### Real starting code development 
```python
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
```

### Known Issues to Fix
* **UI-to-Backend State Disconnect:** Selecting Option 1 ("LAUNCHING GAME") currently triggers a static text response. The main engine must transition seamlessly from the Tkinter event listener loop to actively pulling and parsing the generated character and enemy array configurations.

### Next Steps & Evolution
* **Building the core code:** I will begin developing and refining the final combat state machine aswell as location and travel. This includes binding the Tkinter entry field data directly to dynamic character choice variables, linking weapon object stat modifiers directly to ally attacks, and converting static menu panels into scrolling narrative text feeds.


