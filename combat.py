import random
import game_logic

class CombatManager:

    def __init__(self, game):
        self.game = game
        self.context = game.combat_context

    def predict_enemy_action(
        self,
        enemy,
        player
    ):

        # Low HP makes enemies play more aggressively.
        if enemy.current_health <= max(
            1,
            int(enemy.max_health * 0.25)
        ):
            return "desperate_strike"

        # Big enemies will usually go for a heavy attack.
        if (
            enemy.get_attack_power()
            >= player.get_attack_power() * 2
        ):
            return "heavy_strike"

        return "attack"

    def get_action_tell(
        self,
        enemy,
        action
    ):

        # Give the player a hint about what's coming.
        if action == "desperate_strike":

            return (
                f"{enemy.name} looks wounded and is gathering "
                "every ounce of strength for a desperate strike."
            )

        if action == "heavy_strike":

            return (
                f"{enemy.name} is winding up a heavy strike — "
                "it could hurt a lot!"
            )

        return (
            f"{enemy.name} shifts its weight and eyes you "
            "carefully; it looks ready to attack."
        )

    def execute_enemy_turn(
        self,
        enemy,
        player,
        action,
        parry=False
    ):

        base = enemy.get_attack_power()

        # Small damage variation keeps attacks less predictable.
        variance = random.randint(
            -3,
            3
        )

        damage = max(
            1,
            base + variance
        )

        if action == "desperate_strike":
            damage = int(
                damage * 1.5
            )

        elif action == "heavy_strike":
            damage = int(
                damage * 1.4
            )

        if parry:

            if random.random() < 0.6:

                counter_damage = max(
                    1,
                    player.get_attack_power()
                    + random.randint(-2, 2)
                )

                enemy.take_damage(
                    counter_damage
                )

                return (
                    f"You parry {enemy.name}'s "
                    f"{action.replace('_', ' ')}!\n"
                    f"You counterattack for "
                    f"{counter_damage} damage."
                )

            damage = int(
                damage * 1.5
            )

            player.take_damage(
                damage
            )

            return (
                f"You fail to parry "
                f"{enemy.name}'s "
                f"{action.replace('_', ' ')} "
                f"and take {damage} damage."
            )

        player.take_damage(
            damage
        )

        return (
            f"{enemy.name} uses "
            f"{action.replace('_', ' ')} "
            f"and deals {damage} damage to you."
        )

    def drop_loot(self, enemy):

        # The Lesser Dragon always drops the rune.
        if enemy.name == "Lesser Dragon":

            loot = game_logic.greatrune

            self.game.current_area.add_item(
                loot
            )

            return loot

        # The Draconic Gloomtree Sentinel always drops the rune.
        if enemy.name == "Draconic Gloomtree Sentinel":

            loot = game_logic.greatrune

            self.game.current_area.add_item(
                loot
            )

            return loot

        if enemy.name == "Soldat Vanderbilt":

            if random.random() < 0.90:

                loot = game_logic.glacialhilt

                self.game.current_area.add_item(
                    loot
                )

                return loot

            return None

        # Noid has a chance to drop vantablack great axe.
        if enemy.name == "Noid":

            if random.random() < 0.10:

                loot = game_logic.vantablack

                self.game.current_area.add_item(
                    loot
                )

                return loot

            return None

        # Most enemies have a small chance to drop something.
        if random.random() < 0.3:

            loot_options = [
                game_logic.stick,
                game_logic.greatsword,
                game_logic.kris,
                game_logic.shield
            ]

            loot = random.choice(
                loot_options
            )

            self.game.current_area.add_item(
                loot
            )

            return loot

        return None


def start_encounter(
    game,
    dungeon
):

    # Grab the next enemy waiting in the dungeon.
    enemy = dungeon.get_current_enemy()

    if enemy is None:

        game.game_state = "gameplay"

        game.menu_label.config(
            text=(
                "This dungeon has been cleared.\n\n"
                + dungeon.get_details()
            )
        )

        return

    manager = CombatManager(
        game
    )

    predicted = manager.predict_enemy_action(
        enemy,
        game_logic.player
    )

    game.combat_context = {
        "dungeon": dungeon,
        "enemy": enemy,
        "player": game_logic.player,
        "predicted_enemy_action": predicted,
        "loot_on_ground": None,
        "post_combat": False,
        "boss_intro": enemy.name == "Ancient True Dragon Lucidusax"
    }

    game.game_state = "combat"

    if enemy.name == "Ancient True Dragon Lucidusax":

        game.menu_label.config(
            text=(
                "\n\n\n"
                f"{'ANCIENT TRUE DRAGON LUCIDUSAX':^70}\n\n"
                "Before the first flame was kindled,\n"
                "before kingdoms rose beneath the heavens,\n"
                "there were dragons who knew no master.\n\n"
                "You have climbed beyond the world of men,\n"
                "beyond the earth, beyond the clouds,\n"
                "and into a place where such beings still endure.\n\n"
                "The air grows still.\n"
                "The sky darkens.\n"
                "Something ancient has noticed you.\n\n"
                "Lucidusax, the ancient true dragon,\n"
                "turns its gaze toward the Exiled.\n\n"
                "\"Mortal...\n"
                "you have wandered far beyond your place.\"\n\n"
                "\"Turn back now,\n"
                "or be remembered among the forgotten dead.\"\n\n"
                "\"For I am Lucidusax.\n"
                "And this sky is mine.\"\n\n\n"
                f"{'Type \"continue\" to begin combat.':^70}"
            )
        )

        return

    tell = manager.get_action_tell(
        enemy,
        predicted
    )

    enemy_health_percent = (
        enemy.current_health / enemy.max_health
        if enemy.max_health > 0
        else 0
    )

    player_health_percent = (
        game_logic.player.current_health
        / game_logic.player.max_health
        if game_logic.player.max_health > 0
        else 0
    )

    bar_length = 20

    enemy_filled = int(
        bar_length * enemy_health_percent
    )

    player_filled = int(
        bar_length * player_health_percent
    )

    enemy_bar = (
        "["
        + "=" * enemy_filled
        + " " * (bar_length - enemy_filled)
        + "]"
    )

    player_bar = (
        "["
        + "=" * player_filled
        + " " * (bar_length - player_filled)
        + "]"
    )

    enemy_line = (
        f"{enemy.name} "
        f"(HP: {enemy.current_health}/{enemy.max_health})"
    )

    player_line = (
        f"YOUR HP: "
        f"{game_logic.player.current_health}/"
        f"{game_logic.player.max_health}"
    )

    prompt = (
        f"{'YOU ENTER COMBAT!':^70}\n\n"
        f"{enemy_line:>70}\n"
        f"{enemy_bar:>70}\n\n"
        f"TELL: {tell}\n\n\n"
        f"{player_line:<70}\n"
        f"{player_bar:<70}\n\n"
        f"{'Choose your action:':^70}\n"
        f"{'attack / parry / flee':^70}\n"
        f"{'(Type \"attack\", \"parry\", \"flee\")':^70}\n"
    )

    game.menu_label.config(
        text=prompt
    )


def handle_combat_input(
    game,
    command_raw
):

    # Make sure there is still an active fight.
    if not game.combat_context:

        game.game_state = "gameplay"

        game.menu_label.config(
            text=game.current_area.get_details()
        )

        return

    cmd = command_raw.lower().strip()

    manager = CombatManager(
        game
    )

    output_lines = []

    enemy = game.combat_context["enemy"]
    player = game.combat_context["player"]
    dungeon = game.combat_context["dungeon"]

    if game.combat_context.get(
        "boss_intro"
    ):

        if cmd == "continue":

            game.combat_context[
                "boss_intro"
            ] = False

            predicted = manager.predict_enemy_action(
                enemy,
                player
            )

            game.combat_context[
                "predicted_enemy_action"
            ] = predicted

            tell = manager.get_action_tell(
                enemy,
                predicted
            )

            enemy_health_percent = (
                enemy.current_health
                / enemy.max_health
                if enemy.max_health > 0
                else 0
            )

            player_health_percent = (
                player.current_health
                / player.max_health
                if player.max_health > 0
                else 0
            )

            bar_length = 20

            enemy_filled = int(
                bar_length * enemy_health_percent
            )

            player_filled = int(
                bar_length * player_health_percent
            )

            enemy_bar = (
                "["
                + "=" * enemy_filled
                + " " * (
                    bar_length - enemy_filled
                )
                + "]"
            )

            player_bar = (
                "["
                + "=" * player_filled
                + " " * (
                    bar_length - player_filled
                )
                + "]"
            )

            enemy_line = (
                f"{enemy.name} "
                f"(HP: {enemy.current_health}/"
                f"{enemy.max_health})"
            )

            player_line = (
                f"YOUR HP: "
                f"{player.current_health}/"
                f"{player.max_health}"
            )

            prompt = (
                f"{'YOU ENTER COMBAT!':^70}\n\n"
                f"{enemy_line:>70}\n"
                f"{enemy_bar:>70}\n\n"
                f"TELL: {tell}\n\n\n"
                f"{player_line:<70}\n"
                f"{player_bar:<70}\n\n"
                f"{'Choose your action:':^70}\n"
                f"{'attack / parry / flee':^70}\n"
                f"{'(Type \"attack\", \"parry\", \"flee\")':^70}\n"
            )

            game.menu_label.config(
                text=prompt
            )

            return

        game.menu_label.config(
            text=(
                "The ancient dragon watches you.\n\n"
                "Type 'continue' to begin combat."
            )
        )

        return

    if game.combat_context.get(
        "post_combat"
    ):

        if cmd == "leave":

            game.current_area = (
                game.last_safe_area
            )

            game.game_state = "gameplay"
            game.combat_context = None

            game.menu_label.config(
                text=(
                    "You leave the dungeon.\n\n"
                    + game.current_area.get_details()
                )
            )

            return

        if cmd == "continue":

            dungeon.current_enemy_index += 1

            next_enemy = dungeon.get_current_enemy()

            if next_enemy:

                next_predicted = (
                    manager.predict_enemy_action(
                        next_enemy,
                        player
                    )
                )

                game.combat_context.update({
                    "enemy": next_enemy,
                    "predicted_enemy_action": next_predicted,
                    "loot_on_ground": None,
                    "post_combat": False
                })

                tell = manager.get_action_tell(
                    next_enemy,
                    next_predicted
                )

                enemy_health_percent = (
                    next_enemy.current_health
                    / next_enemy.max_health
                    if next_enemy.max_health > 0
                    else 0
                )

                player_health_percent = (
                    player.current_health
                    / player.max_health
                    if player.max_health > 0
                    else 0
                )

                bar_length = 20

                enemy_filled = int(
                    bar_length * enemy_health_percent
                )

                player_filled = int(
                    bar_length * player_health_percent
                )

                enemy_bar = (
                    "["
                    + "=" * enemy_filled
                    + " " * (
                        bar_length - enemy_filled
                    )
                    + "]"
                )

                player_bar = (
                    "["
                    + "=" * player_filled
                    + " " * (
                        bar_length - player_filled
                    )
                    + "]"
                )

                enemy_line = (
                    f"{next_enemy.name} "
                    f"(HP: {next_enemy.current_health}/"
                    f"{next_enemy.max_health})"
                )

                player_line = (
                    f"YOUR HP: "
                    f"{player.current_health}/"
                    f"{player.max_health}"
                )

                prompt = (
                    f"{'YOU ENTER COMBAT!':^70}\n\n"
                    f"{enemy_line:>70}\n"
                    f"{enemy_bar:>70}\n\n"
                    f"TELL: {tell}\n\n\n"
                    f"{player_line:<70}\n"
                    f"{player_bar:<70}\n\n"
                    f"{'Choose your action:':^70}\n"
                    f"{'attack / parry / flee':^70}\n"
                    f"{'(Type \"attack\", \"parry\", \"flee\")':^70}\n"
                )

                game.menu_label.config(
                    text=prompt
                )

            else:

                game.combat_context = None
                game.game_state = "gameplay"

                output_lines.append(
                    "You continue deeper into the dungeon."
                )

                output_lines.append(
                    "Dungeon Cleared!"
                )

                game.menu_label.config(
                    text=(
                        "\n\n".join(output_lines)
                        + "\n\n"
                        + game.current_area.get_details()
                    )
                )

            return

        game.menu_label.config(
            text=(
                "You defeated the enemy.\n\n"
                "Type 'continue' to continue through "
                "the dungeon or 'leave' to leave."
            )
        )

        return

    # Handle loot before letting the player continue.
    if game.combat_context.get(
        "loot_on_ground"
    ):

        loot = game.combat_context[
            "loot_on_ground"
        ]

        if cmd.startswith("take "):

            weapon_name = cmd[5:].strip()

            if (
                loot
                and loot.name.lower()
                == weapon_name.lower()
            ):

                if game.player_inventory.add_item(
                    loot
                ):

                    game.combat_context[
                        "loot_on_ground"
                    ] = None

                    # Remove the item once it is picked up.
                    if loot in game.current_area.items:
                        game.current_area.items.remove(
                            loot
                        )

                    output_lines.append(
                        f"You picked up {loot.name}!"
                    )

                    game.combat_context[
                        "post_combat"
                    ] = True

                    output_lines.append(
                        "\nType 'continue' to continue "
                        "through the dungeon or "
                        "'leave' to leave."
                    )

                    game.menu_label.config(
                        text="\n\n".join(
                            output_lines
                        )
                    )

                else:

                    output_lines.append(
                        "Your inventory is full!"
                    )

                    game.menu_label.config(
                        text=(
                            "\n\n".join(output_lines)
                            + "\n\n"
                            f"Type 'take {loot.name}'."
                        )
                    )

                return

            else:

                output_lines.append(
                    "That's not the weapon on the ground."
                )

                game.menu_label.config(
                    text="\n\n".join(output_lines)
                )

                return

        else:

            loot_name = loot.name

            game.menu_label.config(
                text=(
                    f"Type 'take {loot_name}' "
                    "to pick it up."
                )
            )

            return

    if cmd == "attack":

        # Add a little randomness to player damage.
        damage = max(
            1,
            player.get_attack_power()
            + random.randint(-2, 2)
        )

        enemy.take_damage(
            damage
        )

        output_lines.append(
            f"You attack {enemy.name} "
            f"for {damage} damage."
        )

    elif cmd == "parry":

        output_lines.append(
            "You prepare to parry the incoming attack."
        )

    elif cmd == "flee":

        # Fleeing has a 50/50 chance of working.
        if random.random() < 0.5:

            game.current_area = (
                game.last_safe_area
            )

            game.game_state = "gameplay"
            game.combat_context = None

            game.menu_label.config(
                text=(
                    "You successfully fled!\n\n"
                    + game.current_area.get_details()
                )
            )

            return

        output_lines.append(
            "You failed to flee! "
            "The enemy takes advantage and attacks you."
        )

    else:

        tell = manager.get_action_tell(
            enemy,
            game.combat_context[
                "predicted_enemy_action"
            ]
        )

        game.menu_label.config(
            text=(
                f"Unknown command: '{command_raw}'.\n\n"
                f"TELL: {tell}\n\n"
                "Choose: attack / parry / flee"
            )
        )

        return

    if not enemy.is_alive:

        if enemy.name == "Ancient True Dragon Lucidusax":

            game.game_state = "ending"
            game.combat_context = None

            game.menu_label.config(
                text=(
                    "\n\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    "                    THE SKIES ARE FREE\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "Lucidusax falls.\n\n"
                    "But far beyond the clouds, something stirs.\n\n"
                    "The skies may be free...\n"
                    "but freedom has a price.\n\n"
                    "And somewhere beyond the edge of the heavens,\n "
                    "another story waits to begin.\n\n"
                    "SKYBORNE: SKIES END\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    "                         THE END\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                )
            )


            return

        output_lines.append(
            f"You defeated {enemy.name}!"
        )

        loot = manager.drop_loot(
            enemy
        )

        if loot:

            output_lines.append(
                f"\n{enemy.name} dropped: "
                f"{loot.name}!"
            )

            output_lines.append(
                f"Type 'take {loot.name}' "
                "to pick it up."
            )

            game.combat_context[
                "loot_on_ground"
            ] = loot

        else:

            game.combat_context[
                "post_combat"
            ] = True

            output_lines.append(
                "Type 'continue' to continue "
                "through the dungeon or "
                "'leave' to leave."
            )

        game.menu_label.config(
            text="\n\n".join(
                output_lines
            )
        )

        return

    predicted = game.combat_context[
        "predicted_enemy_action"
    ]

    parry_flag = (
        cmd == "parry"
    )

    # Enemy gets its turn after the player's action.
    enemy_turn_msg = (
        manager.execute_enemy_turn(
            enemy,
            player,
            predicted,
            parry=parry_flag
        )
    )

    output_lines.append(
        enemy_turn_msg
    )

    if not player.is_alive:

        # Reset the player after a defeat.
        player.current_health = (
            player.max_health
        )

        player.is_alive = True

        game.current_area = (
            game.last_safe_area
        )

        game.game_state = "gameplay"
        game.combat_context = None

        output_lines.append(
            "\nYou have been defeated..."
        )

        output_lines.append(
            "You awaken at your last safe area."
        )

        game.menu_label.config(
            text="\n\n".join(
                output_lines
            )
            + "\n\n"
            + game.current_area.get_details()
        )

        return

    next_predicted = (
        manager.predict_enemy_action(
            enemy,
            player
        )
    )

    game.combat_context[
        "predicted_enemy_action"
    ] = next_predicted

    tell = manager.get_action_tell(
        enemy,
        next_predicted
    )

    enemy_health_percent = (
        enemy.current_health
        / enemy.max_health
        if enemy.max_health > 0
        else 0
    )

    player_health_percent = (
        player.current_health
        / player.max_health
        if player.max_health > 0
        else 0
    )

    bar_length = 20

    enemy_filled = int(
        bar_length * enemy_health_percent
    )

    player_filled = int(
        bar_length * player_health_percent
    )

    enemy_bar = (
        "["
        + "=" * enemy_filled
        + " " * (
            bar_length - enemy_filled
        )
        + "]"
    )

    player_bar = (
        "["
        + "=" * player_filled
        + " " * (
            bar_length - player_filled
        )
        + "]"
    )

    enemy_line = (
        f"{enemy.name} "
        f"(HP: {enemy.current_health}/"
        f"{enemy.max_health})"
    )

    player_line = (
        f"YOUR HP: "
        f"{player.current_health}/"
        f"{player.max_health}"
    )

    prompt = (
        f"{'YOU ENTER COMBAT!':^70}\n\n"
        f"{enemy_line:>70}\n"
        f"{enemy_bar:>70}\n\n"
        f"TELL: {tell}\n\n\n"
        f"{player_line:<70}\n"
        f"{player_bar:<70}\n\n"
        f"{'Choose your action:':^70}\n"
        f"{'attack / parry / flee':^70}\n"
        f"{'(Type \"attack\", \"parry\", \"flee\")':^70}\n"
    )

    game.menu_label.config(
        text=prompt
    )
