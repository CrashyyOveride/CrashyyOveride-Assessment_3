class Inventory:

    def __init__(
        self,
        max_slots=20
    ):
        self.items = []
        self.max_slots = max_slots

        self.equipped_weapon = None

    # Add Item
    def add_item(self, weapon):

        if weapon is None:
            return False

        if weapon.name == "Orsted's Great Rune":

            self.items.append(
                weapon
            )

            return True

        if len(self.items) >= self.max_slots:
            return False

        # Don't add the same item twice.
        if weapon in self.items:
            return False

        self.items.append(
            weapon
        )

        return True

    # Remove an item from the bag.
    def remove_item(self, weapon):

        if weapon in self.items:

            if weapon == self.equipped_weapon:
                self.equipped_weapon = None

            self.items.remove(
                weapon
            )

            return True

        return False

    # Find an item by its name.
    def get_item_by_name(self, name):

        if not name:
            return None

        for weapon in self.items:

            if (
                weapon.name.lower()
                == name.lower()
            ):
                return weapon

        return None

    # Equip the selected weapon.
    def equip_weapon(
        self,
        weapon,
        character=None
    ):

        if weapon not in self.items:
            return False

        self.equipped_weapon = weapon

        # Keep the player equipment synced.
        if character is not None:
            character.equipped_weapon = weapon

        return True

    # Take off the current weapon.
    def unequip_weapon(
        self,
        character=None
    ):

        self.equipped_weapon = None

        if character is not None:
            character.equipped_weapon = None

        return True

    # Show what's currently in the inventory.
    def list_items(self):

        if not self.items:
            return "Inventory is empty."

        lines = [
            "INVENTORY:",
            f"Slots: {len(self.items)}/{self.max_slots}"
        ]

        for i, weapon in enumerate(
            self.items,
            1
        ):

            equipped = (
                " [EQUIPPED]"
                if weapon == self.equipped_weapon
                else ""
            )

            lines.append(
                f"  {i}. {weapon.name} "
                f"(+{weapon.bonus_damage} DMG, "
                f"{weapon.rarity})"
                f"{equipped}"
            )

        return "\n".join(
            lines
        )

    # Fully heal the player.
    def heal_player(
        self,
        player
    ):

        if not player.is_alive:
            return False

        if (
            player.current_health
            >= player.max_health
        ):
            return False

        player.current_health = (
            player.max_health
        )

        return True
