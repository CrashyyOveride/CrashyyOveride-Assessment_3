# TAS Software Engineering (Stage 6 Year 11) - Assessment Task 2
### Project Name: __Yet to decide__
**Student:** Tynan Kocet
**Teacher:** Mr McFarlane  

---

## Project Vision 
This project translates tactical dark-fantasy "reflexes" into strategic "resource management" using a component-based Object-Oriented Programming (OOP) framework in Python 3.14. 

### Core Gameplay Dynamics
* **The Action Economy**: Every movement, dodge, and strike consumes static Stamina points.
* **The Telegraph System**: Enemy units broadcast combat text cues ("Tells") requiring precise user reactions.
* **The Stagger Metric**: Sustained offensive actions break enemy poise thresholds to unlock high-yield critical modifiers.

---

## Software Architecture Blueprint

### Class Hierarchy
* `GameObject` (Base Identity Abstract)
    * `Item` -> `Weapon` | `Armor` | `Consumable` | `Iteem`
    * `Actor` (Shared Combat Infrastructure)
        * `Player` (Inventory arrays, item consumption logic, progressive stat state)
        * `Enemy` -> `Boss` (Dynamic telegraph loops, unique item drops)

## First Rough DRAFT of the game world building

`Oakhaven Town Hub` <---> `Dungeon Level 1 (Ashenhollow)` <---> `Dungeon Level 2 (Not Maded Yet)` <---> `Dungeon Level 3 (Not Maded Yet)` <---> `Dragon Arena (Final Boss and level)`

---

## NESA Academic Integrity Declaration
I hereby declare that this repository contains my own authentic work. Development stages, troubleshooting paths, and logic structures are systematically documented through incremental git commit hashes to prevent misrepresentation and plagiarism.
