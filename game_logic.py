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


