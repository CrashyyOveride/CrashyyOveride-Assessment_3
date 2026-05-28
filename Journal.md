## Development Journal
___An incremental tracking log documenting the development lifecycle milestones, structural pivots, technical pitfalls, and troubleshooting workflows encountered during the production of this software application.___


<br>
<br>
<br>
<br>
<br>

# Journal Entry: May 17, 2026

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
        print("You escaped from Matej's diddy evil house!!!")
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

