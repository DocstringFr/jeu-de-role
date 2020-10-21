from unittest import TestCase
from unittest.mock import patch

import characters
import game


class TestMenuItem(TestCase):
    def test_menu_item_nbr_of_items(self):
        game.MenuItem.nbr_of_items = 0
        for _ in range(5):
            game.MenuItem()

        self.assertEqual(game.MenuItem.nbr_of_items, 5)

    def test_exec(self):
        menu_item = game.MenuItem(run="ALLCAP".lower)
        result = menu_item.exec()
        self.assertEqual(result, "allcap")


class TestGame(TestCase):
    def setUp(self):
        self.game = game.Game()
        self.game.player = self.game._create_player(name="TestPlayer")
        self.game.enemies = characters.Enemies.generate(number_of_enemies=5)

    @patch('builtins.input', return_value="1")
    def test__choose_difficulty(self, mock_input):
        difficulty = self.game._choose_difficulty()
        self.assertEqual(difficulty, 1)

    @patch('builtins.input', return_value="Valerian")
    def test__create_player_name(self, mock_input):
        player = self.game._create_player()
        self.assertEqual(player.name, "Valerian")

    @patch('builtins.input', return_value="1")
    def test__menu_input(self, mock_input):
        selected_menu = self.game._menu_input()
        self.assertEqual(selected_menu, self.game.menu[0])

    @patch('builtins.input', return_value="1")
    def test__get_user_choice(self, mock_input):
        menu_item_1 = game.MenuItem(run=print)
        menu_item_2 = game.MenuItem(run=print)
        menu_item_3 = game.MenuItem(run=print)
        menu_item = self.game._get_user_choice(items=[menu_item_1, menu_item_2, menu_item_3])
        self.assertEqual(menu_item, menu_item_1)

    def test__enemy_attack(self):
        player_health = self.game.player.health
        total_damage = self.game._enemy_attack()
        self.assertEqual(self.game.player.health, player_health - total_damage)

    @patch('builtins.input', return_value="1")
    def test__attack(self, mock_input):
        enemy_attacked = self.game.enemies[0]
        enemy_is_dead = self.game._attack(magic=False)
        if enemy_is_dead:
            self.assertNotIn(enemy_attacked, self.game.enemies)
        else:
            self.assertIn(enemy_attacked, self.game.enemies)
        self.assertEqual(enemy_is_dead, enemy_attacked.is_dead)

    def test__take_potion(self):
        player_health = self.game.player.health
        health_granted = self.game._take_potion()
        self.assertEqual(self.game.player.health, player_health + health_granted)

    @patch('builtins.input', return_value="1")
    def test__ask_enemy_to_attack(self, mock_input):
        enemy = self.game._ask_enemy_to_attack()
        self.assertEqual(enemy, self.game.enemies[0])

    def test__ask_enemy_to_attack_one_left(self):
        self.game.enemies = [self.game.enemies.pop(0)]
        enemy = self.game._ask_enemy_to_attack()
        self.assertEqual(enemy, self.game.enemies[0])
