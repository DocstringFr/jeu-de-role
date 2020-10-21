import random
import sys


class Character:
    def __init__(self, name, health=50):
        self.name = name
        self.health = health

    @property
    def damage(self):
        return random.randint(5, 15)

    @property
    def is_dead(self):
        return self.health <= 0

    def attack(self, character) -> int:
        """Attack character
        Args:
            character: Character to attack

        Returns:
            int: damage inflicted to character
        """
        damage = self.damage
        character.health -= damage
        print(f"⚔️  {self.name} inflige {damage} points de dégats️ à {character.name}")
        return damage


class Player(Character):
    def __init__(self, name):
        super().__init__(name)
        self.number_of_potions = 3

    def take_potion(self):
        """Take potion from inventory"""
        if self.number_of_potions > 0:
            potion_health = random.randint(15, 50)
            self.health += potion_health
            self.number_of_potions -= 1
            print(f"Vous récupérez {potion_health} points de vie ❤️ ({self.number_of_potions} 🧪 restantes)")
        else:
            print("Vous n'avez plus de potions...")


class Enemy(Character):
    def __init__(self):
        name = random.choice(["Loup", "Dragon", "Lion"])
        super().__init__(name)


class Game:
    def __init__(self):
        self.player = Player(input("Entrez le nom de votre joueur : "))
        self.enemy = Enemy()
        self.skip_turn = False

    def start(self):
        """Start game loop"""
        while True:
            if self.skip_turn:
                print("Vous passez ce tour...")
                self.skip_turn = False
            else:
                user_input = self._ask_user_input()
                self._play(user_choice=user_input)

            if self.enemy.is_dead:
                print("Tu as gagné 💪")
                break

            self.enemy.attack(character=self.player)

            if self.player.is_dead:
                print("Tu as perdu 😢")
                break

            self._print_health()

        print("Fin du jeu.")
        sys.exit()

    def _play(self, user_choice):
        """Execute player's action
        Args:
            user_choice (str): The user's chosen action
        """
        if user_choice == "1":
            self.player.attack(character=self.enemy)
        elif user_choice == "2":
            self.player.take_potion()
            self.skip_turn = True

    def _print_health(self):
        """Print player and enemy's health"""
        print(f"Il vous reste {self.player.health} points de vie.")
        print(f"Il reste {self.enemy.health} points de vie à l'ennemi.")
        print("-" * 50)

    @staticmethod
    def _ask_user_input() -> str:
        """Ask user to choose between attack and potion
        Returns:
            str: User's choice
        """
        user_choice = ""
        while user_choice not in ["1", "2"]:
            user_choice = input("Souhaitez-vous attaquer (1) ou utiliser une potion (2) ? ")

        return user_choice


def main():
    game = Game()
    game.start()


if __name__ == '__main__':
    main()
