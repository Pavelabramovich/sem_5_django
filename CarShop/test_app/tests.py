from django.test import TestCase
from .validators import is_address, is_phone_number

class YourTestClass(TestCase):

    # @classmethod
   #  def setUpTestData(cls):
   #     print("setUpTestData: Run once to set up non-modified data for all class methods.")
   #     pass

  #  def setUp(self):
  #      print("setUp: Run once for every test method to setup clean data.")
  #      pass

    def test1_phone_validator(self):
        test_str = "+375 (29) 654-34-98"
        self.assertTrue(is_phone_number(test_str))

    def test2_phone_validator(self):
        test_str = "+375 (28) 654-34 98"
        self.assertFalse(is_phone_number(test_str))

    def test3_phone_validator(self):
        test_str = "+375  (   29  ) 544-    33     -      90"
        self.assertTrue(is_phone_number(test_str))

    def test1_address_validator(self):
        test_str = "London, city Windy street 15"
        self.assertTrue(is_address(test_str))

    def test2_address_validator(self):
        test_str = "hsdjh a3Q EWYW3AWTYHt 42y5 q"
        self.assertFalse(is_address(test_str))

