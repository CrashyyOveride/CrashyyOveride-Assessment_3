import tkinter as tk
import game_logic
import combat
from items import Inventory
from tkinter import font as tkfont
import random

class Game:

    def __init__(self, root):

        self.root = root
        self.root.title("Game")
        self.root.configure(bg="black")
        self.root.attributes("-fullscreen", True)

        self.root.bind(
            "<Escape>",
            lambda event: self.root.destroy()
        )

        self.game_state = "menu"

        self.current_area = game_logic.landing_zone
        self.last_safe_area = game_logic.landing_zone

        self.dungeon_progress = 0
        self.combat_context = None

        self.player_inventory = Inventory(
            max_slots=20
        )

        game_logic.player.inventory = (
            self.player_inventory
        )

        self.current_npc = None
        self.index_frame = None
        self.index_text = None

        self.story_pages = [
            (
                "THE EXILED\n\n"
                "The world you once knew is no longer the same.\n\n"
                "You have fallen from the heavens above.\n\n"
                "Your past may be lost.\n\n"
                "You are known only as the Exiled.\n\n"
                "A wanderer with no home, no title, and no clear memory.\n\n"
                "Arise ye, Exiled.\n\n"
                "Step beyond the gates of life and death.\n\n"
                "And discover what waits beyond the skies."
            ),

            (
                "YOUR JOURNEY\n\n"
                "Explore the world.\n\n"
                "Defeat the dungeons.\n\n"
                "Discover weapons and items.\n\n"
                "Uncover the truth behind the world.\n\n"
                "Your story begins now."
            )
        ]

        self.story_page = 0

        self.default_menu = (
            "                                           \n"
            "  ███████╗ ██╗  ██╗ ██╗   ██╗ ██████╗  ██████╗ ██████╗ ███╗   ██╗███████╗\n"
            "  ██╔════╝ ██║ ██╔╝ ╚██╗ ██╔╝ ██╔══██╗██╔═══██╗██╔══██╗████╗  ██║██╔════╝\n"
            "  ███████╗ █████╔╝   ╚████╔╝  ██████╔╝██║   ██║██████╔╝██╔██╗ ██║█████╗  \n"
            "  ╚════██║ ██╔██╗     ╚██╔╝   ██╔══██╗██║   ██║██╔══██╗██║╚██╗██║██╔══╝  \n"
            "  ███████║ ██║╚██╗     ██║    ██████╔╝╚██████╔╝██║  ██║██║ ╚████║███████╗\n"
            "  ╚══════╝ ╚═╝ ╚═╝     ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝\n"
            "                                           \n"
            "  [1]  START GAME                          \n"
            "  [2]  CREDITS                             \n"
            "  [3]  DEVELOPER NOTE                      \n"
            "  [4]  INDEX                               \n"
            "                                           \n"
        )

        self.menu_label = tk.Label(
            self.root,
            text=self.default_menu,
            font=("Courier New", 18),
            fg="#E8E3D8",
            bg="#0B0B0B",
            justify="center",
            anchor="center"
        )

        self.menu_label.pack(
            expand=True,
            fill="both",
            padx=40,
            pady=(40, 20)
        )

        input_frame = tk.Frame(
            self.root,
            bg="black"
        )

        input_frame.pack(
            pady=(0, 70)
        )

        self.input_frame = input_frame

        prompt_label = tk.Label(
            input_frame,
            text="> ",
            font=("American Typewriter", 18),
            fg="#AAAAAA",
            bg="black"
        )

        prompt_label.pack(
            side="left"
        )

        self.user_input = tk.Entry(
            input_frame,
            font=("American Typewriter", 18),
            fg="white",
            bg="#1A1A1A",
            width=18,
            insertbackground="white",
            bd=0,
            highlightthickness=1,
            highlightbackground="#333333",
            highlightcolor="#666666"
        )

        self.user_input.pack(
            side="left"
        )

        self.user_input.focus_set()

        self.root.bind(
            "<Return>",
            self.route_input
        )

    def route_input(self, event=None):

        raw_text = self.user_input.get().strip()

        self.user_input.delete(
            0,
            tk.END
        )

        if not raw_text:

            if self.game_state == "gameplay":

                self.menu_label.config(
                    text=(
                        "Please enter a command.\n\n"
                        + self.current_area.get_details()
                    )
                )

            elif self.game_state == "combat":

                self.menu_label.config(
                    text=(
                        "Please choose: "
                        "attack / defend / flee"
                    )
                )

            elif self.game_state == "dialogue":

                self.menu_label.config(
                    text=(
                        "Please choose one of "
                        "the dialogue options."
                    )
                )

            elif self.game_state == "story":

                self.next_story_page()

            else:

                self.menu_label.config(
                    text=self.default_menu
                )

            return

        if self.game_state == "menu":

            self.handle_menu_choice(
                raw_text
            )

        elif self.game_state == "story":

            self.handle_story_input(
                raw_text
            )

        elif self.game_state == "gameplay":

            self.handle_gameplay_command(
                raw_text
            )

        elif self.game_state == "dialogue":

            self.handle_dialogue_choice(
                raw_text
            )

        elif self.game_state == "combat":

            combat.handle_combat_input(
                self,
                raw_text
            )

    def handle_menu_choice(self, choice):

        choice = choice.strip()

        if choice == "1":

            self.game_state = "story"
            self.story_page = 0

            self._hide_index_if_shown()

            self.menu_label.config(
                text=self.story_pages[self.story_page]
                + "\n\n"
                + "Press Enter to continue."
            )

        elif choice == "2":

            self._hide_index_if_shown()

            self.menu_label.config(
                text=(
                    "Credits\n\n"
                    "Created by Matej.\n\n"
                    "Type 0 to go back."
                )
            )

        elif choice == "3":

            self._hide_index_if_shown()

            self.menu_label.config(
                text=(
                    "Developer Note\n\n"
                    "I worked on this game and\n"
                    "I'm pretty proud of it :)\n\n"
                    "Type 0 to go back."
                )
            )

        elif choice == "4":

            self.game_state = "menu"
            self.show_index()

        elif choice == "0":

            self._hide_index_if_shown()

            self.game_state = "menu"

            self.menu_label.config(
                text=self.default_menu
            )

        else:

            self._hide_index_if_shown()

            self.menu_label.config(
                text=(
                    f"INVALID CHOICE: '{choice}'\n\n"
                    "Please select 1, 2, 3, or 4."
                )
            )

    def handle_story_input(self, choice):

        if choice == "0":

            self.game_state = "menu"
            self.story_page = 0

            self.menu_label.config(
                text=self.default_menu
            )

            return

        self.next_story_page()

    def next_story_page(self):

        if self.game_state != "story":
            return

        self.story_page += 1

        if self.story_page >= len(self.story_pages):

            self.game_state = "gameplay"
            self.story_page = 0

            self.current_area = game_logic.landing_zone
            self.last_safe_area = game_logic.landing_zone

            self.menu_label.config(
                text=self.current_area.get_details()
            )

            return

        self.menu_label.config(
            text=(
                self.story_pages[self.story_page]
                + "\n\n"
                + "Press Enter to continue."
            )
        )

    def _hide_index_if_shown(self):

        if self.index_frame:

            self.index_frame.pack_forget()
            self.index_frame.destroy()

            self.index_frame = None
            self.index_text = None

        if not self.menu_label.winfo_ismapped():

            self.menu_label.pack(
                expand=True,
                fill="both",
                padx=100,
                pady=(40, 20),
                before=self.input_frame
            )

    def show_index(self):

        if self.menu_label.winfo_ismapped():

            self.menu_label.pack_forget()

        self.index_frame = tk.Frame(
            self.root,
            bg="black"
        )

        self.index_frame.pack(
            expand=True,
            fill="both",
            padx=100,
            pady=30
        )

        scrollbar = tk.Scrollbar(
            self.index_frame,
            bg="#222222",
            troughcolor="black"
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        text_font = tkfont.Font(
            family="American Typewriter",
            size=14
        )

        self.index_text = tk.Text(
            self.index_frame,
            font=text_font,
            fg="#E8E8E8",
            bg="black",
            wrap="word",
            yscrollcommand=scrollbar.set,
            bd=0,
            highlightthickness=0,
            padx=20,
            pady=20,
            spacing1=3,
            spacing2=2,
            spacing3=6
        )

        self.index_text.pack(
            expand=True,
            fill="both",
            side="left"
        )

        scrollbar.config(
            command=self.index_text.yview
        )

        self.index_text.tag_config(
            "header",
            foreground="#FFFFFF",
            font=("American Typewriter", 17, "bold")
        )

        self.index_text.tag_config(
            "weapon",
            foreground="#6FAFFF"
        )

        self.index_text.tag_config(
            "character",
            foreground="#7CFF8A"
        )

        self.index_text.tag_config(
            "enemy",
            foreground="#FF7777"
        )

        self.index_text.tag_config(
            "location",
            foreground="#FFD66B"
        )

        self.index_text.tag_config(
            "muted",
            foreground="#888888"
        )

        self.index_text.tag_config(
            "section",
            foreground="#FFFFFF",
            font=("American Typewriter", 15, "bold")
        )

        weapons = []
        characters = []
        enemies = []
        locations = []

        for name, obj in vars(game_logic).items():

            if name.startswith("_"):
                continue

            if isinstance(
                obj,
                game_logic.Weapon
            ):

                weapons.append(obj)

            elif isinstance(
                obj,
                game_logic.Enemy
            ):

                enemies.append(obj)

            elif isinstance(
                obj,
                game_logic.Ally
            ):

                characters.append(obj)

            elif isinstance(
                obj,
                game_logic.Area
            ):

                locations.append(obj)

        weapons.sort(
            key=lambda w: w.name.lower()
        )

        characters.sort(
            key=lambda c: c.name.lower()
        )

        enemies.sort(
            key=lambda e: e.name.lower()
        )

        locations.sort(
            key=lambda l: l.name.lower()
        )

        self.index_text.insert(
            "end",
            "INDEX\n",
            "header"
        )

        self.index_text.insert(
            "end",
            "\nWeapons\n",
            "section"
        )

        if weapons:

            for weapon in weapons:

                line = (
                    f"-- {weapon.name} "
                    f"(Damage: {weapon.bonus_damage}, "
                    f"Rarity: {weapon.rarity})\n"
                )

                self.index_text.insert(
                    "end",
                    line,
                    "weapon"
                )

        else:

            self.index_text.insert(
                "end",
                "  (none)\n",
                "muted"
            )

        self.index_text.insert(
            "end",
            "\nCharacters / Allies\n",
            "section"
        )

        if characters:

            for character in characters:

                line = (
                    f"-- {character.name} "
                    f"(HP: {character.current_health}/"
                    f"{character.max_health}, "
                    f"ATK: {character.base_attack})\n"
                )

                self.index_text.insert(
                    "end",
                    line,
                    "character"
                )

        else:

            self.index_text.insert(
                "end",
                "  (none)\n",
                "muted"
            )

        self.index_text.insert(
            "end",
            "\nEnemies\n",
            "section"
        )

        if enemies:

            for enemy in enemies:

                line = (
                    f"-- {enemy.name} "
                    f"(HP: {enemy.current_health}/"
                    f"{enemy.max_health}, "
                    f"ATK: {enemy.base_attack}, "
                    f"Boss: {enemy.is_boss})\n"
                )

                self.index_text.insert(
                    "end",
                    line,
                    "enemy"
                )

        else:

            self.index_text.insert(
                "end",
                "  (none)\n",
                "muted"
            )

        self.index_text.insert(
            "end",
            "\nLocations\n",
            "section"
        )

        if locations:

            for location in locations:

                line = (
                    f"-- {location.name} "
                    f"(Type: {location.zone_type})\n"
                )

                self.index_text.insert(
                    "end",
                    line,
                    "location"
                )

        else:

            self.index_text.insert(
                "end",
                "  (none)\n",
                "muted"
            )

        self.index_text.insert(
            "end",
            "\nType 0 and press Enter "
            "to return to the main menu.",
            "muted"
        )

        self.index_text.config(
            state="disabled"
        )

    def handle_gameplay_command(
        self,
        command
    ):

        clean_command = (
            command.lower().strip()
        )

        if not clean_command:

            self.menu_label.config(
                text=(
                    "Please enter a command.\n\n"
                    + self.current_area.get_details()
                )
            )

            return

        if clean_command.startswith("go "):

            direction = (
                clean_command[3:].strip()
            )

            if direction in self.current_area.exits:

                destination = (
                    self.current_area.exits[
                        direction
                    ]
                )

                self.start_travel(
                    direction,
                    destination
                )

            else:

                self.menu_label.config(
                    text=(
                        f'Blocked! There is no exit to '
                        f'the "{direction}".\n\n'
                        + self.current_area.get_details()
                    )
                )

        elif clean_command == "inventory":

            self.menu_label.config(
                text=(
                    self.player_inventory.list_items()
                    + "\n\n"
                    + self.current_area.get_details()
                )
            )

        elif clean_command == "pray":

            if getattr(
                self.current_area,
                "is_safe",
                False
            ):

                if (
                    game_logic.gravewarden
                    not in self.player_inventory.items
                    and game_logic.gravewarden
                    not in self.current_area.items
                    and random.random() < 0.05
                ):

                    self.current_area.add_item(
                        game_logic.gravewarden
                    )

                    self.menu_label.config(
                        text=(
                            "You kneel and pray.\n\n"
                            "Something ancient answers your prayer.\n\n"
                            "Gravewarden has appeared.\n\n"
                            + self.current_area.get_details()
                        )
                    )

                    return

                healed = (
                    self.player_inventory.heal_player(
                        game_logic.player
                    )
                )

                if healed:

                    self.menu_label.config(
                        text=(
                            "You kneel and pray.\n\n"
                            "A peaceful warmth flows through you.\n"
                            f"You are restored to "
                            f"{game_logic.player.current_health}/"
                            f"{game_logic.player.max_health} HP.\n\n"
                            + self.current_area.get_details()
                        )
                    )

                else:

                    self.menu_label.config(
                        text=(
                            "You kneel and pray.\n\n"
                            "You are already at full health.\n\n"
                            + self.current_area.get_details()
                        )
                    )

            else:

                self.menu_label.config(
                    text=(
                        "You cannot pray safely here.\n\n"
                        "The area is too dangerous.\n\n"
                        + self.current_area.get_details()
                    )
                )

        elif clean_command.startswith("talk "):

            npc_name = (
                clean_command[5:].strip()
            )

            npc = (
                self.current_area.get_npc_by_name(
                    npc_name
                )
            )

            if npc:

                self.game_state = "dialogue"
                self.current_npc = npc

                node = (
                    npc.start_conversation()
                )

                self._display_dialogue_node(
                    node
                )

            else:

                self.menu_label.config(
                    text=(
                        f"There's no one called "
                        f"'{npc_name}' here.\n\n"
                        + self.current_area.get_details()
                    )
                )

        elif clean_command.startswith("take "):

            weapon_name = (
                clean_command[5:].strip()
            )

            weapon = (
                self.current_area.get_item_by_name(
                    weapon_name
                )
            )

            if weapon:

                if self.player_inventory.add_item(
                    weapon
                ):

                    self.current_area.items.remove(
                        weapon
                    )

                    self.menu_label.config(
                        text=(
                            f"You picked up "
                            f"{weapon.name}!\n"
                            f"(+{weapon.bonus_damage} damage)\n\n"
                            + self.current_area.get_details()
                        )
                    )

                else:

                    self.menu_label.config(
                        text=(
                            "Your inventory is full!\n\n"
                            + self.current_area.get_details()
                        )
                    )

            else:

                self.menu_label.config(
                    text=(
                        f"There's no "
                        f"'{weapon_name}' here.\n\n"
                        + self.current_area.get_details()
                    )
                )

        elif clean_command.startswith("equip "):

            weapon_name = (
                clean_command[6:].strip()
            )

            weapon = (
                self.player_inventory.get_item_by_name(
                    weapon_name
                )
            )

            if weapon:

                if self.player_inventory.equip_weapon(
                    weapon,
                    game_logic.player
                ):

                    self.menu_label.config(
                        text=(
                            f"You equipped "
                            f"{weapon.name}!\n"
                            f"(+{weapon.bonus_damage} damage)\n\n"
                            + self.current_area.get_details()
                        )
                    )

            else:

                self.menu_label.config(
                    text=(
                        f"You don't have "
                        f"'{weapon_name}' "
                        "in your inventory.\n\n"
                        + self.current_area.get_details()
                    )
                )

        elif clean_command.startswith("unlock "):

            if isinstance(
                self.current_area,
                game_logic.SecretArea
            ):

                passcode = (
                    clean_command[7:].strip()
                )

                if self.current_area.unlock(
                    passcode
                ):

                    self.menu_label.config(
                        text=(
                            "The barrier that was hidding it disappears.\n\n"
                            + self.current_area.get_details()
                        )
                    )

                else:

                    self.menu_label.config(
                        text=(
                            "Incorrect passcode.\n\n"
                            + self.current_area.get_details()
                        )
                    )

            else:

                self.menu_label.config(
                    text=(
                        "There is nothing here to unlock.\n\n"
                        + self.current_area.get_details()
                    )
                )

        elif clean_command == "menu":

            self.game_state = "menu"

            self.menu_label.config(
                text=self.default_menu
            )

        else:

            self.menu_label.config(
                text=(
                    f"Unknown command: '{command}'\n\n"
                    + self.current_area.get_details()
                )
            )

    def start_travel(
        self,
        direction,
        destination
    ):

        self.game_state = "traveling"

        origin = self.current_area

        self.menu_label.config(
            text=(
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"TRAVELING: {origin.name.upper()} "
                f"→ {destination.name.upper()}\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Traveling."
            )
        )

        self._travel_step(
            origin,
            destination,
            direction,
            0
        )

    def _travel_step(
        self,
        origin,
        destination,
        direction,
        step
    ):

        if self.game_state != "traveling":
            return

        symbols = [
            ".",
            "..",
            "..."
        ]

        if step < len(symbols):

            self.menu_label.config(
                text=(
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"TRAVELING: {origin.name.upper()} "
                    f"→ {destination.name.upper()}\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"Traveling{symbols[step]}"
                )
            )

            self.root.after(
                350,
                lambda: self._travel_step(
                    origin,
                    destination,
                    direction,
                    step + 1
                )
            )

            return

        self.current_area = destination

        if getattr(
            self.current_area,
            "is_safe",
            False
        ):

            self.last_safe_area = (
                self.current_area
            )

        monologue = (
            origin.get_travel_monologue()
        )

        self.menu_label.config(
            text=(
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"TRAVELING: {origin.name.upper()} "
                f"→ {destination.name.upper()}\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f'"{monologue}"\n\n'
                f"You arrive at "
                f"{destination.name.upper()}."
            )
        )

        self.root.after(
            700,
            lambda: self.finish_travel(
                destination
            )
        )

    def finish_travel(
        self,
        destination
    ):

        if self.game_state != "traveling":
            return

        if isinstance(
            destination,
            game_logic.Dungeon
        ):

            if destination.is_cleared():

                self.game_state = "gameplay"

                self.menu_label.config(
                    text=(
                        "You return to the "
                        "completed dungeon.\n\n"
                        + destination.get_details()
                    )
                )

            else:

                self.game_state = "combat"

                combat.start_encounter(
                    self,
                    destination
                )

            return

        self.game_state = "gameplay"

        self.menu_label.config(
            text=destination.get_details()
        )

    def _display_dialogue_node(
        self,
        node
    ):

        if not node:

            self.game_state = "gameplay"
            self.current_npc = None

            self.menu_label.config(
                text=self.current_area.get_details()
            )

            return

        options_text = ""

        for key, (text, _) in node.options.items():

            options_text += (
                f"{key}. {text}\n"
            )

        display = (
            f"{node.text}\n\n"
            f"{options_text}"
        )

        self.menu_label.config(
            text=display
        )

    def handle_dialogue_choice(
        self,
        choice
    ):

        if not self.current_npc:

            self.game_state = "gameplay"

            self.menu_label.config(
                text=self.current_area.get_details()
            )

            return

        next_node = (
            self.current_npc.say(
                choice
            )
        )

        if next_node is None:

            current_node = (
                self.current_npc.dialogue_tree
                .get_current_node()
            )

            self.menu_label.config(
                text=(
                    "Invalid dialogue choice.\n\n"
                    + current_node.text
                    + "\n\n"
                    + "\n".join(
                        f"{key}. {text}"
                        for key, (text, _) in
                        current_node.options.items()
                    )
                )
            )

            return

        if next_node.options:

            self._display_dialogue_node(
                next_node
            )

        else:

            self.game_state = "gameplay"
            self.current_npc = None

            self.menu_label.config(
                text=(
                    "*Conversation ended*\n\n"
                    + self.current_area.get_details()
                )
            )


if __name__ == "__main__":

    window = tk.Tk()

    app = Game(
        window
    )

    window.mainloop()
