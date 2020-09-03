import unittest
import numpy as np
import os
import shutil

from pygeneses.envs.prima_vita.player_class import Player
from pygeneses.envs.prima_vita import PrimaVita

class TestPlayerClass(unittest.TestCase):

    def test_initial_x_y(self):
        player = Player(i=1, log_dir=".", tob=10, energy=200, x=100, y=300)
        self.assertEqual(player.action_history, [[100, 300]])

    def test_add_parent_single_parent(self):
        player = Player(i=10, log_dir=".", tob=10, energy=200)
        player.add_parent(id=1, tob=0)
        self.assertEqual(player.action_history[1][0], 1)
        self.assertEqual(player.action_history[1][1], 0)

    def test_add_parent_two_parents(self):
        player = Player(i=10, log_dir=".", tob=10, energy=200)
        player.add_parent(id=1, tob=0, mate_id=2, mate_tob=3)
        self.assertEqual(player.action_history[1][0][0], 1)
        self.assertEqual(player.action_history[1][0][1], 0)
        self.assertEqual(player.action_history[1][1][0], 2)
        self.assertEqual(player.action_history[1][1][1], 3)

    def test_write_data(self):
        model = PrimaVita(log_dir_info="test")
        if not os.path.exists(model.log_dir):
            os.mkdir(model.log_dir)

        player = Player(i=1, log_dir=model.log_dir, tob=10, energy=200)
        player.write_data(time=10, alive_count=10)

        self.assertTrue(os.path.exists(os.path.join(model.log_dir, "10-1.npy")))

        shutil.rmtree(model.log_dir)

    def test_update_history_action_less_equal_9(self):
        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.states.append([-1, -1])
        player.update_history(action=7, time=10, reward=-2)

        check_vals = [7, 10, -2, 200, 0, 0, [-1, -1]]

        for i in range(len(check_vals)):
            with self.subTest("Check action history for an action <= 9", i=i):
                self.assertEqual(player.action_history[-1][i], check_vals[i])

    def test_update_history_action_asexual_reproduction(self):
        player = Player(i=10, log_dir=".", tob=10, energy=200, x=0, y=0)
        player.states.append([-1, -1])
        player.update_history(action=10, time=10, reward=-2, )

        check_vals = [7, 10, -2, 200, 0, 0, [-1, -1]]

        for i in range(len(check_vals)):
            with self.subTest("Check action history for failed action", i=i):
                self.assertEqual(player.action_history[-1][i], check_vals[i])