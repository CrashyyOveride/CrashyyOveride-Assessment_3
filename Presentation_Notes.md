# Presentation Q&A Notes

### Question 1
Why did you choose an Object-Oriented Programming (OOP) approach over a standard procedural approach for a text RPG?

### Answer 1
OOP allows me to map game entities directly to real-world objects through code abstraction. Instead of using massive, messy nested loops to track character stats, I can create a single parent class called Actor with shared attributes like HP and Stamina. From there, the Player and Enemy classes inherit that baseline code structure cleanly. It makes the entire game modular, much easier to scale, and allows me to create original characters effortlessly by modifying attributes.

### Question 2
How did you manage player movement and location connections without using a standard grid coordinate (X, Y) map system?

### Answer 2
I used a directed Node Graph data structure implemented as a Python dictionary. Every location like Oakhaven or Dungeon Layer 1 is a distinct string key. Inside each location key is a nested dictionary mapping compass directions to destination identifiers. This allows for clean, flexible world pathing, letting me code complex non-linear elements like locked gate blocks, hidden room flags, and shortcuts looping back to the town hub.

### Question 3
What challenges did you face when migrating your game from a standard IDE terminal into a native Tkinter GUI window?

### Answer 3
The biggest hurdle was managing synchronous text display. In a standard console, code executes line-by-line using time.sleep() blocks to pace reading speeds. In a Tkinter window application, time.sleep() freezes the main thread event loop, causing the whole interface window to crash or stop responding. To solve this, I decoupled the narrative generation step from the display layer, using Tkinter's internal .after() scheduling system to animate textual outputs cleanly without locking up the UI thread.

### Question 4
Explain the mechanical trade-off design behind Orsted's Great Rune.

### Answer 4
The design uses state-flag tracking to implement a classic risk-versus-reward mechanic. When the user loots the item from the Lesser Dragon, a global Boolean flag (has_rune = True) modifies the runtime game state engine. It scales the player's maximum health attribute by fifty percent, but simultaneously acts as an active multiplier within the random generation script that controls overworld ambushes vastly increasing the hazard rate of encountering the un-attackable stalker boss, Orsted Drake.
