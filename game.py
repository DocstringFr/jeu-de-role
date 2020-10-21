import random
import sys
from functools import partial
from typing import List

import characters


class MenuItem:
    nbr_of_items = 1

    def __init__(self, description="Menu item", run=None):
        self.description = description
        self.option = MenuItem.nbr_of_items
        self.run = run
        MenuItem.nbr_of_items += 1

    def exec(self):
        return self.run()


class Printer:
    @staticmethod
    def start_fight(enemies):
        print("Vous tombez sur une horde d'ennemis composée de...")

        for enemy in enemies:
            print(enemy)

        print("⚔️ ️ Le combat est engagé ⚔️")

    @staticmethod
    def show_health(characters):
        for character in characters:
            if character.is_alive:
                print(character)

    @staticmethod
    def show_enemies(enemies):
        print("Quel ennemi souhaitez-vous attaquer ?")
        for i, enemy in enumerate(enemies):
            print(i + 1, ": ", enemy)


class Game:
    def __init__(self):
        self.menu = [
            MenuItem(description="Attaque normale", run=self._attack),
            MenuItem(description="Attaque magique", run=partial(self._attack, True)),
            MenuItem(description="Prendre une potion", run=self._take_potion),
            MenuItem(description="Quitter le jeu", run=self.quit),
        ]

    @staticmethod
    def _choose_difficulty() -> int:
        """Ask user to choose between 3 levels of difficulty
        Returns:
            int: Level of difficulty choosed by user
        """
        difficulty = ""
        while not (difficulty.isdigit() and difficulty in ["1", "2", "3"]):
            difficulty = input("Choisissez un niveau de difficulté (1, 2 ou 3) : ")
            if difficulty not in ["1", "2", "3"]:
                print("Svp, choisissez un niveau entre 1 et 3...")

        return int(difficulty)

    @staticmethod
    def _create_player(name=None) -> characters.Character:
        """Create a character of type Sorcier with given name
        Args:
            name (str): name of the player

        Returns:
            characters.Sorcier: Character created by user
        """
        player_name = input("Entrez le nom de votre personnage : ") if not name else name
        return characters.Sorcier(name=player_name, health=50)

    def start(self):
        self.difficulty = self._choose_difficulty()
        self.player = self._create_player()
        self.player.health *= self.difficulty
        self.enemies = characters.Enemies.generate(number_of_enemies=self.difficulty * 2)
        self.characters = [self.player] + self.enemies

        Printer.start_fight(enemies=self.enemies)

        while any(character.is_alive for character in self.characters):
            user_choice = self._menu_input()
            user_choice.exec()

            if not self.enemies:
                self.quit(reason="Win")

            self._enemy_attack()

            if not self.player.is_alive:
                self.quit(reason="Lost")

            Printer.show_health(characters=self.characters)

    def _menu_input(self):
        for item in self.menu:
            print(f"{item.option}: {item.description}")

        return self._get_user_choice(items=self.menu)

    @staticmethod
    def _get_user_choice(items: List[MenuItem]) -> MenuItem:
        """Get user choice in the list of menu items
        Args:
            items: list of MenuItems

        Returns:
            MenuItem: MenuItem selected by the user
        """
        user_choice = ""
        choice_valid = False
        while not (user_choice.isdigit() and choice_valid):
            user_choice = input("👉 Faites votre choix : ")
            if user_choice.isdigit():
                choice_valid = 1 <= int(user_choice) <= len(items)

        return items[int(user_choice) - 1]

    def _enemy_attack(self):
        """Attack from 3 random enemies on the player

        Returns:
            bool: Total damage inflicted to player
        """
        total_damage = 0
        random_enemies = random.sample(self.enemies, min(3, len(self.enemies)))  # We get at least 3 random enemies
        for attacking_enemy in random_enemies:
            total_damage += attacking_enemy._default_attack(self.player)
        return total_damage

    def _attack(self, magic=False) -> bool:
        """Attack from the player on a given enemy
        Args:
            magic (bool): Use a special magic attack

        Returns:
            bool: Whether enemy being attacked is dead or not
        """
        enemy_to_attack = self._ask_enemy_to_attack()
        enemy_is_dead = self.player.attack(enemy=enemy_to_attack, super_attack=magic)
        if enemy_is_dead:
            self.enemies.remove(enemy_to_attack)
        return enemy_is_dead

    def _take_potion(self):
        """Take potion from inventory"""
        return self.player.take_potion()

    def _ask_enemy_to_attack(self):
        """Ask which enemy to attack from the list of enemies
        Returns:
            enemy (characters.Enemy): The enemy to attack
        """
        if len(self.enemies) == 1:
            return self.enemies[0]

        Printer.show_enemies(self.enemies)

        enemy_pos = ""
        while not enemy_pos.isdigit():
            enemy_pos = input("Ennemi à attaquer : ")

        return self.enemies[int(enemy_pos) - 1]

    @staticmethod
    def quit(reason="Voluntary"):
        reasons = {"Voluntary": "Fin du jeu.",
                   "Win": "Vous avez défait tous les enemis bravo !",
                   "Lost": "Vous avez été défait. L'empire s'effondre."}

        print(reasons.get(reason))
        sys.exit()
