import dialogue
import time
import random

# Basic area class for locations in the game.

class Area:

    def __init__(
        self,
        name: str,
        description: str,
        zone_type: str = "Standard"
    ):
        self.name = name
        self.description = description
        self.zone_type = zone_type
        self.exits = {}
        self.items = []
        self.npcs = []
        self.is_safe = True

    # Connect this area to other areas.
    def set_exits(
        self,
        north=None,
        south=None,
        east=None,
        west=None
    ):
        if north:
            self.exits["north"] = north

        if south:
            self.exits["south"] = south

        if east:
            self.exits["east"] = east

        if west:
            self.exits["west"] = west

    # Add an NPC to the area.
    def add_npc(self, npc):
        if npc not in self.npcs:
            self.npcs.append(npc)

    # Add an item to the area.
    def add_item(self, weapon):
        if weapon not in self.items:
            self.items.append(weapon)

    # Find an NPC by name.
    def get_npc_by_name(self, name):
        for npc in self.npcs:
            if npc.name.lower() == name.lower():
                return npc

        return None

    # Find an item by name.
    def get_item_by_name(self, name):
        for item in self.items:
            if item.name.lower() == name.lower():
                return item

        return None

    # Display the area's information.
    def get_details(self):
        available_directions = (
            ", ".join(
                self.exits.keys()
            ).upper()
            if self.exits
            else "NONE"
        )

        details = (
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"LOCATION: {self.name.upper()}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        )

        if self.npcs:
            details += "--PEOPLE HERE--\n"

            for npc in self.npcs:
                details += f"{npc.name}\n"

            details += "\n"

        if self.items:
            details += "--WEAPONS HERE--\n"

            for item in self.items:
                details += f"{item.name}\n"

            details += "\n"

        details += (
            f"PATHWAYS:  [ {available_directions} ]\n\n"
            "──────────────────────────────────────────────────────────────────────────\n"
            "COMMANDS\n"
            "──────────────────────────────────────────────────────────────────────────\n"
            "go [direction]       │  Travel to Areas                   \n"
            "inventory            │  Check your weapons and gear       \n"
            "pray                 │  Pray in a safe area               \n"
            "talk [npc_name]      │  Talk to an NPC in the area        \n"
            "take [weapon_name]   │  Pick up a weapon from the ground  \n"
            "equip [weapon_name]  │  Equip a weapon from your inventory\n"
            "menu                 │  Return to the main menu           \n"
            "══════════════════════════════════════════════════════════════════════════"
        )

        return details

    # Pick a random thought during travel.
    def get_travel_monologue(self):
        monologues = [
            " I wonder...  "
        ]

        return random.choice(monologues)


# Handles the small travel animation.

class TravelSequence:

    def __init__(
        self,
        origin,
        destination,
        delay=0.8
    ):
        self.origin = origin
        self.destination = destination
        self.delay = delay

    # Play the travel sequence.
    def play(self):
        print()
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(
            f"TRAVELING: {self.origin.name.upper()} "
            f"→ {self.destination.name.upper()}"
        )
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        # Simple loading effect.
        for symbol in [".", "..", "..."]:
            print(f"Traveling{symbol}")
            time.sleep(self.delay)

        print()
        print(f'"{self.origin.get_travel_monologue()}"')
        time.sleep(0)

        print()
        print(
            f"You arrive at {self.destination.name.upper()}."
        )
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print()


# Controls the player's current location and travel.

class Game:

    def __init__(self, starting_area):
        self.current_area = starting_area
        self.travel_sequence = None

    # Move the player through a connected area.
    def travel(self, direction):
        direction = direction.lower().strip()

        if direction not in self.current_area.exits:
            print()
            print(
                f"You cannot travel {direction} from "
                f"{self.current_area.name}."
            )
            print()
            return False

        destination = self.current_area.exits[direction]

        if isinstance(destination, SecretArea):
            if destination.is_locked:
                print()
                print(
                    "The path ahead is blocked."
                )
                print(
                    "This area is locked."
                )
                print()
                return False

        self.travel_sequence = TravelSequence(
            self.current_area,
            destination
        )

        self.travel_sequence.play()

        self.current_area = destination

        print(self.current_area.get_details())

        return True

    # Return the player's current area.
    def get_current_area(self):
        return self.current_area


# Used for areas that need a passcode.

class SecretArea(Area):

    def __init__(
        self,
        name: str,
        description: str,
        passcode: str
    ):
        super().__init__(
            name,
            description,
            "Secret"
        )

        self.passcode = passcode
        self.is_locked = True

    # Check if the player entered the correct password.
    def unlock(self, entered_passcode):
        if str(entered_passcode).lower() == self.passcode.lower():
            self.is_locked = False
            return True

        return False

    # Show locked information if needed.
    def get_details(self):
        if self.is_locked:
            return (
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "LOCATION: ??? [ LOCKED ]\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "This area is protected.\n"
                "You must enter the correct passcode.\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "AVAILABLE COMMANDS:\n"
                " unlock [passcode] (Attempt to bypass lock)\n"
                " go south (Return to safety)\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            )

        return super().get_details()


# Keeps track of enemies and dungeon progress.

class Dungeon(Area):

    def __init__(
        self,
        name: str,
        description: str,
        danger_level: int,
        enemies: list
    ):
        super().__init__(
            name,
            description,
            "Dungeon"
        )

        self.danger_level = danger_level
        self.is_safe = False
        self.enemies = enemies
        self.current_enemy_index = 0

    # Get the next living enemy.
    def get_current_enemy(self):
        while self.current_enemy_index < len(self.enemies):
            enemy = self.enemies[
                self.current_enemy_index
            ]

            if enemy.is_alive:
                return enemy

            self.current_enemy_index += 1

        return None

    # Check if every enemy is defeated.
    def is_cleared(self):
        return self.get_current_enemy() is None

    # Restore all enemies when resetting the dungeon.
    def reset_dungeon(self):
        self.current_enemy_index = 0

        for enemy in self.enemies:
            enemy.current_health = enemy.max_health
            enemy.is_alive = True


# Mountain areas are dangerous but still considered safe.

class MountainArea(Dungeon):

    def __init__(
        self,
        name: str,
        description: str,
        danger_level: int,
        enemies: list
    ):
        super().__init__(
            name,
            description,
            danger_level,
            enemies
        )

        self.zone_type = "Mountain"
        self.is_safe = False


# Base class for characters in the game.

class Character:

    def __init__(
        self,
        name: str,
        health: int,
        attack_power: int
    ):
        self.name = name
        self.max_health = health
        self.current_health = health
        self.base_attack = attack_power
        self.is_alive = True
        self.equipped_weapon = None
        self.inventory = None

    # Calculate attack damage with the equipped weapon.
    def get_attack_power(self):
        if self.equipped_weapon:
            return (
                self.base_attack
                + self.equipped_weapon.bonus_damage
            )

        return self.base_attack

    # Deal damage to the character.
    def take_damage(self, amount: int):
        amount = max(
            0,
            int(amount)
        )

        self.current_health -= amount

        if self.current_health <= 0:
            self.current_health = 0
            self.is_alive = False

    # Heal the character.
    def heal(self, amount: int):
        if not self.is_alive:
            return False

        old_health = self.current_health

        self.current_health = min(
            self.max_health,
            self.current_health + max(0, amount)
        )

        return self.current_health > old_health


# Allies are characters that can help the player.

class Ally(Character):

    def __init__(
        self,
        name: str,
        health: int,
        attack_power: int,
        can_use_magic: bool
    ):
        super().__init__(
            name,
            health,
            attack_power
        )

        self.can_use_magic = can_use_magic

    # Allow an ally to heal another character.
    def heal_target(
        self,
        target: Character,
        amount: int
    ):
        if self.is_alive and target.is_alive:
            target.heal(amount)


# Enemies use the same basic stats as other characters.

class Enemy(Character):

    def __init__(
        self,
        name: str,
        health: int,
        attack_power: int,
        is_boss: bool,
        primary_zone: str = "Any"
    ):
        super().__init__(
            name,
            health,
            attack_power
        )

        self.is_boss = is_boss
        self.primary_zone = primary_zone
        self.is_attackable = True

    # Reserved for future enemy effects.
    def trigger_status_effect(self):
        pass


# Weapons store their basic information.

class Weapon:

    def __init__(
        self,
        name: str,
        bonus_damage: int,
        rarity: str,
        description: str
    ):
        self.name = name
        self.bonus_damage = bonus_damage
        self.rarity = rarity
        self.description = description
        self.is_relic = False


# Relics are special versions of weapons.

class Relic(Weapon):

    def __init__(
        self,
        name: str,
        bonus_damage: int,
        rarity: str,
        description: str,
        is_relic: bool
    ):
        super().__init__(
            name,
            bonus_damage,
            rarity,
            description
        )

        self.is_relic = is_relic


# NPCs use dialogue trees to handle conversations.

class NPC:

    def __init__(
        self,
        name,
        description,
        dialogue_tree
    ):
        self.name = name
        self.description = description
        self.dialogue_tree = dialogue_tree

    # Start a new conversation.
    def start_conversation(self):
        self.dialogue_tree.reset()
        return self.dialogue_tree.get_current_node()

    # Select a dialogue option.
    def say(self, choice_key):
        return self.dialogue_tree.choose(
            choice_key
        )


# Main player character.

player = Ally(
    name="Exiled",
    health=100,
    attack_power=15,
    can_use_magic=False
)


# Friendly NPC characters.

ernest = Ally(
    name="Ernest Blackwood",
    health=120,
    attack_power=18,
    can_use_magic=True
)

mary = Ally(
    name="Mary Althea",
    health=9999,
    attack_power=0,
    can_use_magic=True
)

soldat = Ally(
    name="Soldat Vanderbilt",
    health=9999,
    attack_power=120,
    can_use_magic=False
)



# (these two will be used for the sequel).

bandit = Enemy(
    name="Gilded Gold Underling",
    health=30,
    attack_power=8,
    is_boss=False
)

orsted = Enemy(
    name="Orsted Drake",
    health=999999999999999,
    attack_power=99999999999,
    is_boss=True
)

# Surface enemies 

soldat_mad = Enemy(
    name="Soldat Vanderbilt",
    health=60,
    attack_power=30,
    is_boss=False
)


# Dungeon enemies and bosses.

orb = Enemy(
    name="Orb",
    health=25,
    attack_power=6,
    is_boss=False
)

noid = Enemy(
    name="Noid",
    health=45,
    attack_power=10,
    is_boss=False
)

drakonid = Enemy(
    name="drakonid",
    health=70,
    attack_power=16,
    is_boss=False
)

lesser_dragon = Enemy(
    name="Lesser Dragon",
    health=150,
    attack_power=25,
    is_boss=True
)

warden = Enemy(
    name="Deeproot Warden",
    health=110,
    attack_power=20,
    is_boss=False
)

shadow = Enemy(
    name="Shadowroot Spirits",
    health=130,
    attack_power=24,
    is_boss=False
)

draconic = Enemy(
    name="Draconic Gloomtree Sentinel",
    health=300,
    attack_power=45,
    is_boss=True
)

chaos_orb = Enemy(
    name="Chaos Orb",
    health=220,
    attack_power=35,
    is_boss=False
)

sky_gargoyle = Enemy(
    name="Sky Gargoyle",
    health=300,
    attack_power=45,
    is_boss=False
)

agheel = Enemy(
    name="Great Dragon Agheel the Watchkeeper",
    health=650,
    attack_power=60,
    is_boss=True
)

lucidusax = Enemy(
    name="Ancient True Dragon Lucidusax",
    health=1200,
    attack_power=80,
    is_boss=True
)


# Common weapons.

dagger = Weapon(
    name="Dagger",
    bonus_damage=5,
    rarity="Common",
    description="This small blade can be bought in any shop."
)

shield = Weapon(
    name="Shield",
    bonus_damage=5,
    rarity="Common",
    description="This shield can be bought in any shop."
)

longsword = Weapon(
    name="Longsword",
    bonus_damage=6,
    rarity="Common",
    description="This longsword can be bought in any shop."
)

greatsword = Weapon(
    name="Greatsword",
    bonus_damage=7,
    rarity="Common",
    description="This greatsword can be bought in any shop."
)

stick = Weapon(
    name="Stick",
    bonus_damage=0,
    rarity="Common",
    description=(
        "This item can be found while exploring deep paths, "
        "venturing outside dungeons. This is a totally normal "
        "stick, with only one effect which is a debuff called "
        "'Embarrassment' which decreases ones self image. "
        "(This effect has no true value towards anything in the "
        "game, it just why are you holding a stick?)"
    )
)


# Rare weapons.

kris = Weapon(
    name="Holy Kris",
    bonus_damage=10,
    rarity="Rare",
    description=(
        "This weapon is the same as a dagger, however this one "
        "was embedded with holy divinity. This dagger can glow "
        "when it is equiped, making it an alternate light source."
    )
)

vantablack = Weapon(
    name="Vantablack Great Axe",
    bonus_damage=15,
    rarity="Rare",
    description=(
        "This weapon's surface is coated in a 'void' that absorbs "
        "95% of all visible light. The eye cannot see its edges "
        "or depth. To look at the weapon is to stare into an empty "
        "black hole. This Great Axe is gained by venturing into "
        "the darkest part in Ashenhollow, where you might find it. "
        "Some say, Noids have a hand in creating these weapons "
        "but none truly knows."
    )
)

twinlight = Weapon(
    name="Twinlight Odachi",
    bonus_damage=20,
    rarity="Rare",
    description=(
        "This sword has a chance to drop from the lesser dragon "
        "boss in Ashenhollow. This weapon was made from the lands "
        "of reeds, made from a star named 'Twin' that fell from "
        "the sky some time ago. On the base of the sword, there "
        "is a symbol '死' in a forgein language that you don't "
        "understand?"
    )
)

thorn = Weapon(
    name="Gilded Thorn",
    bonus_damage=20,
    rarity="Rare",
    description=(
        "This sword is the most prized item that the Gilded Gold "
        "has. It's hilt is covered in pure gold and is rumoured "
        "to be made out of thin sharp stems of roses."
    )
)


# Legacy weapons.

gravewarden = Weapon(
    name="Gravewarden",
    bonus_damage=30,
    rarity="Legacy",
    description=(
        "Left to decay in the vast fields outside of Ashenhollow, "
        "this grim weapon is invisible to normal eyes. It reveals "
        "its true form only to those who live in death."
    )
)

silencedagger = Weapon(
    name="Parthanlán's Silence",
    bonus_damage=35,
    rarity="Legacy",
    description=(
        "Belonged to the founder of the hideout. It was designed "
        "to slip past guards and heavy gates without making a "
        "single sound. This dagger was forged with the agonizing "
        "screams of the founder's companions after countless brutal "
        "dungeon dives. It stands as a tragic monument to the "
        "friends he lost along the way. This dagger also gives "
        "the player a guaranteed first-strike ambush attack when "
        "entering combat that completely bypasses enemy protection."
    )
)

glacialhilt = Weapon(
    name="Replica Glacial Hilt",
    bonus_damage=20,
    rarity="Legacy",
    description=(
        "A man-made imitation of the legendary hilt resting at "
        "the peak of Anatoli. This item was crafted through the "
        "generations of countless blacksmiths that came before you, "
        "each perfecting the imperfection. It leaks weak "
        "'Polar Vortex' aura."
    )
)


# Relics.

goditem = Relic(
    name="Matej's Old Axe",
    bonus_damage=-10,
    rarity="Relic",
    description=(
        "This axe can be attained if only certain conditions are met."
    ),
    is_relic=False
)

greatrune = Relic(
    name="Orsted's Great Rune",
    bonus_damage=0,
    rarity="Relic",
    description=(
        "This item is dropped by the first two bosses in the game, "
        "this item generates an uneasy aura while holding it, so best "
        "not hold onto it for too long."
    ),
    is_relic=True
)


# Hidden location that needs a password.

parthalanhideout = SecretArea(
    name="Parthanlán's hideout",
    description="This sercet area is very sercet",
    passcode="Password"
)

parthalanhideout.add_item(
    silencedagger
)


# Main areas outside the dungeons.

landing_zone = Area(
    name="Drop Zone",
    description="Barren wasteland...",
    zone_type="Standard"
)

oakhaven = Area(
    name="Oakhaven",
    description=(
        "This area is the starting point, where the Exiled (You) "
        "lands, it's filled with busy streets and a large wall "
        "circling around the town."
    ),
    zone_type="Standard"
)

anatoli = MountainArea(
    name="Anatoli Mountain Base",
    description=(
        "This town is located far north up into the mountains. "
        "It is fully engulfed with snow all year round, leading "
        "to the lacking amount of people in this area. Anatoli "
        "has a secret tall tale, which explains the effects of "
        "the ever-lasting winter; 'High upon thee highest point "
        "on the highest mountain, lay rest a great being. It's "
        "hidden within the clouds, unable to be viewed from down "
        "here.' This great being is the main reason why this town "
        "is stuck inside a winter state. The Ice covered Longsword, "
        "and it's hilt emits 'Polar Vortex' which is far beyond "
        "subzero. It gets warmer as it travels down the mountain "
        "face, so it does get to a point of livability. This town "
        "is also where Soldat Vanderbilt was born."
    ),
    danger_level=2,
    enemies=[
        soldat_mad
    ]
)

shadowsedge = Area(
    name="Shadowsegde",
    description=(
        "Perched on the edge of the Gloomwood forest, Shadowsedge "
        "serves as a vital frontier outpost rahter than a permanent "
        "home. Travelers who come this far to this bleak settlement "
        "call it a glorified checkpoint. To keep the forest's rot "
        "infected enemies at bat, the outpost has eight-meter-high "
        "walls encircling the town hall and the local population. "
        "The buildings are made from the very greyscale wood that "
        "haunts the Gloomwood forest dungeon, as only through "
        "intense purification process does this corrupted wood "
        "become stable enough to build with."
    ),
    zone_type="Standard"
)

skylift = Area(
    name="Sky Lift",
    description=(
        "This lift is the grand entrance to the lands high up "
        "upon the clouds. You feel a sense of familiarity however "
        "you can't quite understand where it's coming from?"
    ),
    zone_type="Standard"
)

skytemple = Dungeon(
    name="Sky Temple",
    description=(
        "Once leaving the earthly plain of existence, the lift "
        "is destroyed by a fireball that came from the highest "
        "peak of these clouds. Now unable to go back, you must "
        "continue forward to the highest point, travelling by "
        "ruins that you can interact with."
    ),
    danger_level=4,
    enemies=[
        chaos_orb,
        sky_gargoyle,
        agheel,
    ]
)

blindboartavern = Area(
    name="The Blind Boar Tavern",
    description=(
        "The air is thick with the scent of roasted meat and stale "
        "ale. In the corner, a fireplace crackles softly. Locals "
        "gather around heavy oak tables, whispering about dangerous "
        "dungeon dives."
    )
)


# Dungeon areas and their enemy lists.

ashenhollow = Dungeon(
    name="Ashenhollow",
    description=(
        "You have completed this dungeon! You sense of saddness "
        "when seeing a corpse of a dragon."
    ),
    danger_level=1,
    enemies=[
        orb,
        noid,
        drakonid,
        lesser_dragon
    ]
)

gloomwood = Dungeon(
    name="Gloomwood Forest",
    description=(
        "The unatural look of the underground sky is caused by "
        "unique rock formations and natural process on the cavern "
        "roof where the rock can mirror light from above the ground. "
        "However, this light is only the imitation, and is on a grey "
        "scale causing the trees here to become decayed and rotted."
    ),
    danger_level=2,
    enemies=[
        orb,
        warden,
        shadow,
        draconic
    ]
)

ventusazura = Dungeon(
    name="Ventus Azura",
    description=(
        "At the absolute apex of the clouds sits Ventus Azura, "
        "the Sky fortress. It is not empty with ancient symbols "
        "and signs, but an active home to the most horrifying "
        "beings that are allowed on this plain of existence: "
        "True Dragons. They are the only beings capable of "
        "mastering and using wild magic at will. These dragons "
        "are fierce and massive, not bound by time or space. "
        "They stand at sizes that can only be perceived fully "
        "from another stratum."
    ),
    danger_level=5,
    enemies=[
        lucidusax
    ]
)


# Connects the different areas together.

anatoli.set_exits(
    south=landing_zone
)

landing_zone.set_exits(
    north=anatoli,
    south=oakhaven
)

oakhaven.set_exits(
    north=landing_zone,
    south=blindboartavern,
    west=gloomwood,
    east=ashenhollow
)

blindboartavern.set_exits(
    north=oakhaven
)

ashenhollow.set_exits(
    west=oakhaven
)

gloomwood.set_exits(
    east=oakhaven,
    north=parthalanhideout,
    south=shadowsedge
)

parthalanhideout.set_exits(
    south=gloomwood
)

shadowsedge.set_exits(
    north=gloomwood,
    south=skylift
)

skylift.set_exits(
    north=shadowsedge,
    east=skytemple
)

skytemple.set_exits(
    west=skylift,
    east=ventusazura
)

ventusazura.set_exits(
    west=skytemple
)


# Set up the NPCs and their dialogue.

ernest_npc = NPC(
    name="Ernest",
    description="Drunken fellow, knows more then he leads on",
    dialogue_tree=dialogue.create_ernest_dialogue()
)

mary_npc = NPC(
    name="Mary",
    description=(
        "A mysterious sage. She seems to know much "
        "about ancient magic and the dungeons."
    ),
    dialogue_tree=dialogue.create_mary_dialogue()
)

soldat_npc = NPC(
    name="Soldat",
    description=(
        "Commander of the Northern Expedition. "
        "He leads roughly ten men through the northern mountains "
        "and commands considerable respect from his squad."
    ),
    dialogue_tree=dialogue.create_soldat_dialogue()
)


# Locations --- NPC & Items

anatoli.add_npc(
    soldat_npc
)

oakhaven.add_npc(
    mary_npc
)

blindboartavern.add_npc(
    ernest_npc
)


# Places the starting items in the world.

oakhaven.add_item(
    dagger
)

blindboartavern.add_item(
    longsword
)

ashenhollow.add_item(
    twinlight
)

gloomwood.add_item(
    thorn
)


# Start the game at the Landing Zone.

game = Game(
    starting_area=landing_zone
)

current_area = game.current_area
