class Area:
    def __init__(self, name: str, description: str, zone_type: str = "Standard"):
        self.name = name
        self.description = description
        self.zone_type = zone_type
        self.exits = {}
        self.items = []
        self.is_safe = True

    def set_exits(self, north=None, south=None, east=None, west=None):
        if north: self.exits["north"] = north
        if south: self.exits["south"] = south
        if east: self.exits["east"] = east
        if west: self.exits["west"] = west

    def get_details(self):
        available_directions = ", ".join(self.exits.keys()).upper() if self.exits else "NONE"
        
        details = (
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"LOCATION: {self.name.upper()}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{self.description}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"PATHWAYS: [ {available_directions} ]\n\n"
            "AVAILABLE COMMANDS:\n"
            " go [north/south/east/west]  (Travel zones)\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )
        return details
    
class SecretArea(Area):
    def __init__(self, name: str, description: str, passcode: str):
        super().__init__(name, description, "Secret")
        self.passcode = passcode
        self.is_locked = True  

    def get_details(self):
        if self.is_locked:
            details = (
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"LOCATION: ??? [ LOCKED ]\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "This location is protected by a magical combination lock.\n"
                "You must enter the correct passcode to breach the barrier.\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "AVAILABLE COMMANDS:\n"
                " unlock [passcode] (Attempt to bypass lock)\n"
                " go south (Return to safety)\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            )
            return details
        return super().get_details()


class Dungeon(Area):
    def __init__(self, name: str, description: str, danger_level: int, enemies: list):
        super().__init__(name, description, "Dungeon")
        self.danger_level = danger_level
        self.is_safe = False  
        self.enemies = enemies       
        self.current_enemy_index = 0

    def get_current_enemy(self):
        if self.current_enemy_index < len(self.enemies):
            return self.enemies[self.current_enemy_index]
        return None


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
    def __init__(self, name: str, bonus_damage: int, rarity: str, description: str):
        self.name = name
        self.bonus_damage = bonus_damage
        self.rarity = rarity
        self.description = description
        self.is_relic = False
        self.orsted_apperance = False

class Relic(Weapon):
    def __init__(self, name: str, bonus_damage: int, rarity: str, description: str, orsted_apperance: bool, is_relic: bool):
        super().__init__(name, bonus_damage, rarity, description)

        self.is_relic = is_relic
        self.orsted_apperance = orsted_apperance

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

### Dungeon 2 Monsters & Boss
warden = Enemy(name="Deeproot Warden", health=90, attack_power=25, is_boss=False)
shadow = Enemy(name="Shadowroot Spirits", health=40, attack_power=30, is_boss=False)
draconic = Enemy(name="Draconic Gloomtree Sentinel", health=550, attack_power=45, is_boss=True)

### Dungeon 3 Monsters & Boss


### HERE ARE ALL WEAPONS :)))

### Common Weapons
dagger = Weapon(name="Dagger", bonus_damage=5, rarity="Common", description="This small blade can be bought in any shop.")
shield = Weapon(name="Shield", bonus_damage=5, rarity="Common", description="This shield can be bought in any shop.")
longsword = Weapon(name="Longsword", bonus_damage=5, rarity="Common", description="This longsword can be bought in any shop.")
greatsword = Weapon(name="Greatsword", bonus_damage=5, rarity="Common", description="This greatsword can be bought in any shop.")
stick = Weapon(name="Stick", bonus_damage=0, rarity="Common", description="This item can be found while exploring deep paths, venturing outside dungeons. This is a totally normal stick, with only one effect which is a debuff called 'Embarrassment' which decreases ones self image. (This effect has no true value towards anything in the game, it just why are you holding a stick?)")

### Rare Weapons
kris = Weapon(name="Holy Kris", bonus_damage=10, rarity="Rare", description="This weapon is the same as a dagger, however this one was embedded with holy divinity. This dagger can glow when it is equiped, making it an alternate light source.")
vantablack = Weapon(name="Vantablack Great Axe", bonus_damage=15, rarity="Rare", description="This weapon's surface is coated in a 'void' that absorbs 95% of all visible light. The eye cannot see its edges or depth. To look at the weapon is to stare into an empty black hole. This Great Axe is gained by venturing into the darkest part in Ashenhollow, where you might find it. Some say, Noids have a hand in creating these weapons but none truly knows.")
twinlight = Weapon(name="Twinlight Odachi", bonus_damage=20, rarity="Rare", description="This sword has a chance to drop from the lesser dragon boss in Ashenhollow. This weapon was made from the lands of reeds, made from a star named 'Twin' that fell from the sky some time ago. On the base of the sword, there is a symbol '死' in a forgein language that you don't understand?")
thorn = Weapon(name="Gilded Thorn", bonus_damage=20, rarity="Rare", description="This sword is the most prized item that the Gilded Gold has. It's hilt is covered in pure gold and is rumoured to be made out of thin sharp stems of roses.")

### Legacy Weapons
gravewarden = Weapon(name="Gravewarden", bonus_damage=50, rarity="Legacy", description="Left to decay in the vast fields outside of Ashenhollow, this grim weapon is invisible to normal eyes. It reveals its true form only to those who live in death.")
silencedagger = Weapon(name="Parthanlán's Silence", bonus_damage=50, rarity="Legacy", description="Belonged to the founder of the hideout. It was designed to slip past guards and heavy gates without making a single sound. This dagger was forged with the agonizing screams of the founder's companions after countless brutal dungeon dives. It stands as a tragic monument to the friends he lost along the way. This dagger also gives the player a guaranteed first-strike ambush attack when entering combat that completely bypasses enemy protection.")
glacialhilt = Weapon(name="Replica Glacial Hilt", bonus_damage=20, rarity="Legacy", description="A man-made imitation of the legendary hilt resting at the peak of Anatoli. This item was crafted through the generations of countless blacksmiths that came before you, each perfecting the imperfection. It leaks weak 'Polar Vortex' aura.")

### Relics

goditem = Relic(name="Matej's Old Axe", bonus_damage=999999999, rarity="Relic", description="This axe can be attained if only certain conditions are met.", orsted_apperance=False, is_relic=False)
greatrune = Relic(name="Orsted's Great Rune", bonus_damage=0, rarity="Relic", description="This item is dropped by all the dungeon bosses in the game, this item generates an uneasy aura while holding it, so best not hold onto it for too long. These Runes vastly increase the player's health, but at the cost of increasing Orsted’s appearance.", orsted_apperance=True, is_relic=True)


### HERE ARE ALL THE LOCATIONS

### Sercet Locations

parthalanhideout = Area(name="Sercet Location", description="####", zone_type="Standard" )

### Non dungeon points

landing_zone = Area(name="Drop Zone", description="####", zone_type="Standard")
oakhaven = Area(name="Oakhaven", description="This area is the starting point, where the Exiled (You) lands, it’s filled with busy streets and a large wall circling around the town. It’s home to The Blind Boar which is a famous chain of taverns throughout the lands. It’s a civilian town, so not much to do but to gather information about the dungeon that resides near the town. This town is also home to massive ruins that the town is built around. One of the most famous landmarks in this town is a huge stone called 'Pathfinder,' as it said touching this rock, provides luck in finding your way back home.", zone_type="Standard")
anatoli = Area(name="Anatoli Mountain Base", description="This town is now unlocked after beating Ashenhollow the first dungeon, it's up to you if you would like to travel to this location. This town is located far north up into the mountains, it's full of log cabins with one shop with resources you can buy there. This area is not a safe zone, so you can be encountered by enemies. It is fully engulfed with snow all year round, leading to the lacking amount of people in this area. Anatoli has a secret tall tale, which explains the effects of the ever-lasting winter; 'High upon thee highest point on the highest mountain, lay rest a great being. It's hidden within the clouds, unable to be viewed from down here.' This great being is the main reason why this town is stuck inside a winter state. The Ice covered Longsword, and it's hilt emits 'Polar Vortex' which is far beyond subzero. It gets warmer as it travels down the mountain face, so it does get to a point of livability. This town is also where Soldat Vanderbilt was born.", zone_type="North")
shadowsedge = Area(name="Shadowsegde", description="Perched on the edge of the Gloomwood forest, Shadowsedge serves as a vital frontier outpost rahter than a permanent home. Travelers who come this far to this bleak settlement call it a glorified checkpoint. To keep the forest's rot infected enemies at bat, the outpost has eight-meter-high walls encircling the town hall and the local population. The buildings are made from the very greyscale wood that haunts the Gloomwood forest dungeon, as only through intense purification process does this corrupted wood become stable enough to build with.", zone_type="Standard")
skylift = Area(name="Sky Lift", description="This lift is the grand entrance to the lands high up upon the clouds. You feel a sense of familiarity however you can't quite understand where it's coming from? This is opened once all dungeons are cleared and you have at least 2 of Orsted Great Runes.", zone_type="Standard")
skytemple = Area(name="Sky Temple", description="Once leaving the earthly plain of existence, the lift is destroyed by a fireball that came from the highest peak of these clouds. Now unable to go back, you must continue forward to the highest point, travelling by ruins that you can interact with.", zone_type="Standard")
blindboartavern = Area(name="The Blind Boar Tavern",description="The air is thick with the scent of roasted meat and stale ale. In the corner, a fireplace crackles softly. Locals gather around heavy oak tables, whispering about dangerous dungeon dives.")

### Dungeon 1
ashenhollow = Dungeon(name="Ashenhollow", description="This dungeon is crawling with low level enemies, but beware, this dungeon is home to the lesser dragon, the most powerful enemy in it.", danger_level=1, enemies=[orb, noid, lesser_dragon])

### Dungeon 2
gloomwood = Dungeon(name="Gloomwood Forest", description="The unatural look of the underground sky is caused by unique rock formations and natural process on the cavern roof where the rock can mirror light from above the ground. However, this light is only the imitation, and is on a grey scale causing the trees here to become decayed and rotted.", danger_level=2, enemies=[warden, shadow, draconic])

### Dungeon 3
ventusazura = Area(name="Ventus Azura", description="At the absolute apex of the clouds sits Ventus Azura, the Sky fortress. It is not empty with ancient symbols and signs, but an active home to the most horrifying beings that are allowed on this plain of existence: True Dragons. They are the only beings capable of mastering and using wild magic at will. These dragons are fierce and massive, not bound by time or space. They stand at sizes that only can be perceived fully from another stratum.")

anatoli.set_exits(south=landing_zone)
landing_zone.set_exits(north=anatoli, south=oakhaven)
oakhaven.set_exits(north=landing_zone, south=blindboartavern, west=gloomwood, east=ashenhollow)
blindboartavern.set_exits(north=oakhaven)

oakhaven.set_exits(north=landing_zone, west=gloomwood, east=ashenhollow)
ashenhollow.set_exits(west=oakhaven)

gloomwood.set_exits(east=oakhaven, north=parthalanhideout, south=shadowsedge)
parthalanhideout.set_exits(south=gloomwood)

shadowsedge.set_exits(north=gloomwood, south=skylift)
skylift.set_exits(north=shadowsedge)

# NOTE: To implement the "(Auto-Locked)" mechanic, we add 'east=sky_temple' here. 
# You can later block this direction in handle_gameplay_command using a condition!
skylift.set_exits(north=shadowsedge, east=skytemple)
skytemple.set_exits(west=skylift, east=ventusazura)
ventusazura.set_exits(west=skytemple)
