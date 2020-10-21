import random


class Character:
    """Base class for all characters"""

    def __init__(self, name="default", health=100, strength=1.0):
        self.name = name
        self.health = health
        self.strength = strength
        self.potions = 3

    def __str__(self):
        s = f"{self.icon} {self.name:10} => {self.health_str}"
        if self.potions > 0:
            s += f" {'🧪' * self.potions}"

        return s

    @property
    def health_icon(self):
        return "🟩"

    @property
    def health_str(self) -> str:
        """Show character's health with green bar"""
        return f"{self.health_icon * self.health} {self.health}"

    @property
    def icon(self) -> str:
        """Icon for character"""
        return "🤖"

    @property
    def is_enemy(self) -> bool:
        """Whether or not character is of type enemy"""
        return isinstance(self, Enemy)

    @property
    def is_alive(self) -> bool:
        """Whether character is still alive or not"""
        return self.health > 0

    @property
    def is_dead(self) -> bool:
        """Whether character is dead or not"""
        return not self.is_alive

    def attack(self, enemy, super_attack=False):
        """Attack enemy with a default or super attack
        Args:
            enemy (Character): Enemy to attack
            super_attack (bool): Use the super attack instead of the default one

        Returns:
            bool: Whether enemy died from the attack or not
        """
        self._super_attack(enemy=enemy) if super_attack else self._default_attack(enemy=enemy)
        if enemy.is_dead:
            print(f"☠️  {enemy.name} a été défait par {self.name} !")
            self._take_inventory(character=enemy)
            return True
        return False

    def _default_attack(self, enemy) -> int:
        """Default attack

        Args:
            enemy (Character): Enemy to attack

        Returns:
            int: Damage points inflicted to enemy
        """
        damage = round(random.randint(5, 10) * self.strength)
        enemy.health -= damage
        print(f"💥 {self.name} attaque {enemy.name} et lui inflige {damage} points de dégats.")
        return damage

    def _super_attack(self, enemy) -> int:
        """Magical attack with super strength

        Args:
            enemy (Character): Enemy to attack

        Returns:
            int: Damage points inflicted to enemy
        """
        self.strength *= 2
        damage = self._default_attack(enemy=enemy)
        self._health_malus()
        self.strength /= 2
        return damage

    def _health_malus(self) -> int:
        """Apply health malus to character
        Returns:
            int: random malus applied (between 5 and 15)
        """
        health_malus = random.randint(5, 15)
        self.health -= health_malus
        print(f"🤕  {self.name} lui fait perdre {health_malus} points de vie.")
        return health_malus

    def _take_inventory(self, character) -> int:
        """Take the inventory of another character
        Args:
            character (Character): Character from whom the inventory is taken

        Returns:
            int: Number of potions taken from the character
        """
        number_of_potions = character.potions
        print(f"🧪 {self.name} récupère les {number_of_potions} potions de {character.name}.")
        self.potions += number_of_potions
        character.potions = 0
        return number_of_potions

    def take_potion(self) -> int:
        """Take a potion from inventory
        Returns:
            int: health granted by ingested potion
        """
        if self.potions > 0:
            potion_health = random.randint(25, 75)
            self.health += potion_health
            self.potions -= 1
            print(f"🧪 {self.name} prend une potion et gagne {potion_health} points de vie.")
            print(self)
            return potion_health

        print(f"{self.name} n'a plus de potions")
        return 0


class Enemy(Character):
    """Base class for all enemies"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.potions = random.randint(0, 2)


class Sorcier(Character):
    def __init__(self, name, health):
        super().__init__(name=name, health=health, strength=3)

    @property
    def icon(self):
        return "🧙"

    @property
    def health_icon(self):
        return "❤️"


class Loup(Enemy):
    weight = 20

    def __init__(self):
        super().__init__(name=self.__class__.__name__, health=25, strength=1.5)

    @property
    def icon(self):
        return "🐺"


class Dragon(Enemy):
    weight = 10

    def __init__(self):
        super().__init__(name=self.__class__.__name__, health=50, strength=1)

    @property
    def icon(self):
        return "🐉"


class Lion(Enemy):
    weight = 2

    def __init__(self):
        super().__init__(name=self.__class__.__name__, health=15, strength=4)

    @property
    def icon(self):
        return "🦁"


class Enemies:
    classes = [Loup, Dragon, Lion]

    @staticmethod
    def generate(number_of_enemies):
        enemies_classes = random.choices(Enemies.classes,
                                         weights=[cls.weight for cls in Enemies.classes],
                                         k=number_of_enemies)
        enemies = []
        for enemy in enemies_classes:
            enemies.append(enemy())

        return sorted(enemies, key=lambda x: x.health)
