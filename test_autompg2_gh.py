import unittest
from autompg import AutoMPG, AutoMPGData

class TestAutomobile(unittest.TestCase):

    def test_equals(self):
        car1 = AutoMPG("Nissan", "Murano", 2020, 21)
        car2 = AutoMPG("Nissan", "Murano", 2020, 21)
        self.assertEqual(car1, car2)
        self.assertEqual(car1, car1)
        self.assertEqual(car1.make, car2.make)
        self.assertEqual(car1.model, car2.model)
        self.assertEqual(car1.year, car2.year)
        self.assertEqual(car1.mpg, car2.mpg)
    def test_not_equals(self):
        car1 = AutoMPG("Nissan", "Murano", 2020, 45)
        car2 = AutoMPG("Nissan", "Murano", 2020, 21)
        car3 = AutoMPG("Nissan", "Murano", 2018, 21)
        car4 = AutoMPG("Toyota", "RAV4", 2018, 21)
        self.assertNotEqual(car1, car2)
        self.assertNotEqual(car1, car3)
        self.assertNotEqual(car3, car4)
    def test_less_than(self):
        car1 = AutoMPG("Toyota", "RAV4", 2023, 56)
        car2 = AutoMPG("Toyota", "RAV4", 2017, 40)
        car3 = AutoMPG("Honda", "Accord", 2019, 20)
        self.assertLess(car2, car1)
        self.assertLess(car3, car2)
        self.assertLess(car2.year, car1.year)
        self.assertLess(car3.mpg, car2.mpg)
    def test_hash(self):
        car1 = AutoMPG("Toyota", "RAV4", 2023, 56)
        car2 = AutoMPG("Toyota", "RAV4", 2017, 40)
        car3 = AutoMPG("Toyota", "RAV4", 2017, 40)
        s1 = {car1, car2}
        s2 = {car1, car2, car3}
        self.assertEqual(s1, s2)
    def test_string(self):
        car1 = AutoMPG("Toyota", "RAV4", 2023, 56)
        self.assertEqual(car1.__str__(), '2023 Toyota RAV4')
    def test_repr(self):
        car1 = AutoMPG("Toyota", "RAV4", 2023, 56.0)
        self.assertEqual(car1.__repr__(), "AutoMPG('Toyota', 'RAV4', 2023, 56.0)")



class TestAutomobileData(unittest.TestCase):

    def test_data_list_equal(self):
        ret1 = AutoMPGData().data
        ret2 = AutoMPGData().data
        car3 = AutoMPGData().data[2]
        car1_make = AutoMPGData().data[4].make
        car2_make = AutoMPGData().data[5].make
        self.assertEqual(ret1, ret2)
        self.assertEqual(car3, AutoMPGData().data[2])
        self.assertEqual(car1_make, car2_make)
    def test_data_list_not_equal(self):
        car1 = AutoMPGData().data[4]
        car2 = AutoMPGData().data[15]
        car1_year = AutoMPGData().data[50].year
        car2_year = AutoMPGData().data[1].year
        self.assertNotEqual(car1, car2)
        self.assertNotEqual(car1_year, car2_year)
    def test_instance(self):
        car1 = AutoMPGData().data[2]
        self.assertIsInstance(car1, AutoMPG)

if __name__ == '__main__':
    unittest()