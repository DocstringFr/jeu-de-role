from unittest import TestCase

import characters


class TestCharacter(TestCase):

    def setUp(self):
        self.player = characters.Character(name="Paul", health=100, strength=1)
        self.enemy = characters.Dragon()

    def test_health_str(self):
        self.player.health = 50
        self.assertEqual(self.player.health_str, f"{'🟩' * 50} 50")

    def test_icon(self):
        self.assertEqual(self.player.icon, "🤖")

    def test_is_enemy(self):
        self.assertEqual(self.player.is_enemy, False)

    def test_is_alive(self):
        self.assertEqual(self.player.is_alive, True)
        self.player.health = -1
        self.assertEqual(self.player.is_alive, False)

    def test_multiple_attacks(self):
        is_dead = True
        while is_dead:
            is_dead = self.player.attack(enemy=self.enemy, super_attack=False)
        self.assertEqual(is_dead, self.enemy.is_dead)

    def test_normal_attack_from_player(self):
        is_dead = self.player.attack(enemy=self.enemy, super_attack=False)
        self.assertEqual(is_dead, self.enemy.is_dead)

    def test_super_attack_from_player(self):
        is_dead = self.player.attack(enemy=self.enemy, super_attack=True)
        self.assertEqual(is_dead, self.enemy.is_dead)

    def test_normal_attack_from_enemy(self):
        is_dead = self.enemy.attack(enemy=self.player, super_attack=False)
        self.assertEqual(is_dead, self.player.is_dead)

    def test_super_attack_from_enemy(self):
        is_dead = self.enemy.attack(enemy=self.player, super_attack=True)
        self.assertEqual(is_dead, self.player.is_dead)

    def test__default_attack(self):
        enemy_health = self.enemy.health
        damage = self.player._default_attack(enemy=self.enemy)
        self.assertEqual(self.enemy.health, enemy_health - damage)

    def test__super_attack(self):
        player_strength = self.player.strength
        enemy_health = self.enemy.health
        damage = self.player._super_attack(enemy=self.enemy)
        self.assertEqual(self.enemy.health, enemy_health - damage)
        self.assertEqual(self.player.strength, player_strength)

    def test__take_inventory(self):
        player_nbr_of_potions = self.player.potions
        potions_taken = self.player._take_inventory(character=self.enemy)
        self.assertEqual(self.enemy.potions, 0)
        self.assertEqual(self.player.potions, player_nbr_of_potions + potions_taken)

    def test_take_potion(self):
        player_health = self.player.health
        health_recovered = self.player.take_potion()
        self.assertEqual(self.player.health, player_health + health_recovered)

    def test_take_potion_inventory_empty(self):
        self.player.potions = 0
        player_health = self.player.health
        health_recovered = self.player.take_potion()
        self.assertEqual(health_recovered, 0)
        self.assertEqual(self.player.health, player_health)


class TestEnemy(TestCase):

    def setUp(self):
        self.enemy = characters.Enemy()

    def test_init_enemy(self):
        for _ in range(50):
            enemy = characters.Enemy()
            self.assertIn(enemy.potions, [0, 1, 2])


class TestEnemies(TestCase):
    def test_generate_number_of_enemies(self):
        for i in range(5):
            enemies = characters.Enemies.generate(number_of_enemies=i)
            self.assertEqual(len(enemies), i)

    def test_generate_enemies_classes(self):
        enemies = characters.Enemies.generate(number_of_enemies=3)
        for enemy in enemies:
            self.assertIn(enemy.__class__, characters.Enemies.classes)

    def test_generate_enemies_order(self):
        enemies = characters.Enemies.generate(number_of_enemies=50)
        enemies_health_order = [enemy.health for enemy in enemies]
        flag = 0
        for i in range(1, len(enemies_health_order)):
            if enemies_health_order[i] < enemies_health_order[i - 1]:
                flag = 1

        self.assertEqual(flag, 0)
