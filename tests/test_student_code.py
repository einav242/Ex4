import sys
from unittest import TestCase

import pygame

from student_code import Student_code
from unittest import TestCase


class TestStudent_code(TestCase):

    def test_algo(self):
        count = 0
        s = Student_code(1)
        self.assertEqual(None, s.ag)
        self.assertEqual(len(s.list_pok), len(s.get_list_pokemon()))
        for i in range(len(s.list_pok)):
            self.assertEqual(s.list_pok[i].type, s.get_list_pokemon()[i].type)
            self.assertEqual(s.list_pok[i].value, s.get_list_pokemon()[i].value)
            self.assertEqual(s.list_pok[i].type, s.get_list_pokemon()[i].type)

