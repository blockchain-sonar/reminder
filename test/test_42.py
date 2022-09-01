from unittest import TestCase
import unittest

class Test42(TestCase):
	def setUp(self):
		"Hook method for setting up the test fixture before exercising it."
		pass

	def tearDown(self):
		"Hook method for deconstructing the test fixture after testing it."
		pass

	def test(self):
		self.assertEqual(42, 42)
