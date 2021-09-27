import unittest
# import sys
# sys.path.append('/admin/sorting')
from models_oop import Calculator, Contacts, Grade


class TestCalculator(unittest.TestCase):

    def test_add(self):
        instance = Calculator(6, 3)
        res = instance.add()
        self.assertEqual(res, 9)

    def test_subtract(self):
        instance = Calculator(6, 3)
        res = instance.subtract()
        self.assertEqual(res, 3)

    def test_multiple(self):
        instance = Calculator(6, 3)
        res = instance.multiple()
        self.assertEqual(res, 18)

    def test_divide(self):
        instance = Calculator(6, 3)
        res = instance.divide()
        self.assertEqual(res, 2)


class TestContacts(unittest.TestCase):

    def test_get_contact(self):
        ls = []
        ls.append(Contacts.set_contact('Tom','010-1234','tom@test.com','Seoul'))
        ls.append(Contacts.set_contact('Jane', '010-3334', 'jane@test.com', 'Incheon'))
        ls.append(Contacts.set_contact('Kim', '010-7734', 'kim@test.com', 'Busan'))
        ls = Contacts.get_contacts(ls)
        self.assertEqual(ls[0].name, 'Tom')

    def test_del_contact(self):
        ls = []
        ls.append(Contacts.set_contact('Tom','010-1234','tom@test.com','Seoul'))
        ls.append(Contacts.set_contact('Jane', '010-3334', 'jane@test.com', 'Incheon'))
        ls.append(Contacts.set_contact('Kim', '010-7734', 'kim@test.com', 'Busan'))
        ls = Contacts.del_contact(ls, 'Tom')
        print([x.to_string() for x in ls])
        self.assertEqual(len(ls), 2)


class TestGrade(unittest.TestCase):
    def test_avg(self):
        grade = Grade('Han',60,80,70)
        # print(grade.return_grade())
        self.assertEqual(grade.name, 'Han')
        self.assertEqual(grade.return_grade(), 'C')


if __name__ == '__main__':
    unittest.main()