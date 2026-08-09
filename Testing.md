# Testing

## Unit Testing

Unit testing was used to test individual functions and methods separately. This ensured that each part of the program worked correctly before being used with other modules.

| Test | Function/Method Tested | Expected Result | Result |
|---|---|---|---|
| U1 | `Inventory.add_item()` | Item is added to the inventory | Pass |
| U2 | `Inventory.get_item_by_name()` | Correct item is returned when the name matches | Pass |
| U3 | `Inventory.equip_weapon()` | Selected weapon becomes equipped | Pass |
| U4 | `Inventory.unequip_weapon()` | Equipped weapon is removed | Pass |
| U5 | `Inventory.heal_player()` | Player health is restored to maximum | Pass |
| U6 | `DialogueTree.choose()` | Correct dialogue node is selected | Pass |
| U7 | `DialogueTree.reset()` | Dialogue returns to the starting node | Pass |
| U8 | `CombatManager.predict_enemy_action()` | Appropriate enemy action is predicted | Pass |
| U9 | `CombatManager.execute_enemy_turn()` | Enemy attacks and damage is applied | Pass |
| U10 | `CombatManager.drop_loot()` | Correct loot is generated according to enemy | Pass |

## Subsystem Testing

Subsystem testing checked that related functions worked together within each major part of the game.

| Subsystem | Test | Expected Result | Result |
|---|---|---|---|
| Exploration | Player uses `go` command | Player moves to the selected connected area | Pass |
| Exploration | Player enters a dungeon | Combat begins if the dungeon is uncleared | Pass |
| Inventory | Player uses `take` | Item moves from the area into the inventory | Pass |
| Inventory | Player uses `equip` | Selected weapon is equipped | Pass |
| Inventory | Player uses `inventory` | Current inventory contents are displayed | Pass |
| Combat | Player attacks an enemy | Enemy loses health | Pass |
| Combat | Player parries | Parry has a chance to block and counterattack | Pass |
| Combat | Player flees | Player either escapes or receives an enemy attack | Pass |
| Combat | Enemy is defeated | Loot or the continue option is provided | Pass |
| Dialogue | Player talks to an NPC | Correct dialogue starts | Pass |
| Dialogue | Player selects an option | Correct dialogue branch is displayed | Pass |
| Dialogue | Invalid option is entered | Invalid choice message is displayed | Pass |

## System Testing

System testing checked the complete game from the player's perspective.

| Test | Action | Expected Result | Result |
|---|---|---|---|
| S1 | Start the game | Main menu is displayed | Pass |
| S2 | Start a new game | Story begins | Pass |
| S3 | Complete the story | Player enters gameplay | Pass |
| S4 | Travel between areas | Travel animation and destination are displayed | Pass |
| S5 | Enter a dungeon | Combat encounter starts | Pass |
| S6 | Defeat an enemy | Loot or next-dungeon option appears | Pass |
| S7 | Pick up loot | Item is added to inventory | Pass |
| S8 | Talk to an NPC | Dialogue system starts and options appear | Pass |
| S9 | Open the index | Weapons, characters, enemies and locations are displayed | Pass |
| S10 | Defeat the final boss | Game ending is displayed | Pass |

## Black-Box Testing

Black-box testing was performed by entering commands without examining the internal code while testing the expected behaviour.

Examples included:

- Entering `inventory` displays the player's inventory.
- Entering `go east` attempts to travel east.
- Entering `take Greatsword` attempts to collect the weapon.
- Entering `equip Greatsword` equips the weapon if it is in the inventory.
- Entering `attack` causes the player to attack.
- Entering `parry` attempts to parry the enemy attack.
- Entering `flee` attempts to escape combat.
- Entering `talk Ernest` starts Ernest's dialogue.
- Entering an invalid command produces an error message.

These tests confirmed that the game responds correctly to normal and incorrect user input.

## White-Box Testing

White-box testing was performed by examining the internal logic and different branches of the program.

Examples included:

- Checking the different conditions in `predict_enemy_action()`.
- Testing the different branches for `attack`, `parry` and `flee`.
- Checking the health conditions when a player or enemy dies.
- Checking the different loot-drop conditions for specific enemies.
- Checking the different dialogue branches.
- Checking the conditions for safe areas and praying.
- Checking the conditions for dungeon completion.
- Checking inventory capacity and duplicate-item restrictions.

This helped identify logical errors and ensured that important branches of the program could be reached and executed.

## Grey-Box Testing

Grey-box testing combined knowledge of the program's internal structure with normal user interaction.

For example, the combat system was tested by entering commands such as `attack` and `parry` while also checking that the internal health values, predicted enemy action and combat state changed correctly.

The inventory was similarly tested by collecting an item, checking that it appeared in the inventory, equipping it and checking that the player's equipment was updated.

## Quality Assurance

Quality assurance was used throughout development to improve the reliability and usability of the game.

The program was checked for:

- Invalid user input
- Incorrect dialogue choices
- Full inventories
- Duplicate items
- Player and enemy health reaching zero
- Combat victories and defeats
- Loot drops
- Dungeon completion
- Safe and unsafe areas
- NPC conversations
- Travel between locations
- Final boss completion
- Correct display of information in the index

The testing showed that the main game systems worked together correctly and that invalid inputs were handled without stopping the game.

