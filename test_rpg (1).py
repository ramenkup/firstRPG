import unittest, sys, json, os, io
from unittest.mock import patch
import rpg
from rpg import *
from contextlib import redirect_stdout

def compare_files(f1, f2):
    f1 = open(f1)
    f2 = open(f2)
    l1 = f1.readline()
    line_no = 0
    while l1:
        line_no += 1
        # add line numbers
        l2 = f2.readline()
        if not l2:
            print('line number:', line_no)
            print('missing l2, no match for:', repr(l1))
            return False
        l1 = l1.rstrip() # avoid cross-platform eol character issues
        l2 = l2.rstrip()
        if l1 != l2:
            print('line number:', line_no)
            print('l1:', repr(l1))
            print('l2:', repr(l2))
            return False
        l1 = f1.readline()
    l2 = f2.readline()
    if l2:
        print('line number:', line_no + 1)
        print('extra l2:', repr(l2))
        return False
    return True

class TestRPG(unittest.TestCase):

    def setUp(self):
        self.rich = Fighter('Rich')
        self.thompson = Fighter('Thompson')

    def test_init(self):
        self.assertEqual('Rich', self.rich.name)
        self.assertEqual(10, self.rich.hit_points)
        self.assertIsNone(self.rich.__init__("Thompson"))
        
    def test_repr(self):
        self.assertEqual('Rich (HP: 10)', repr(self.rich))
        
    def test_take_damage(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.assertIsNone(self.rich.take_damage(5))
            self.assertEqual(5, self.rich.hit_points)
            self.assertEqual('\tRich has 5 hit points remaining.\n', buf.getvalue())
        with io.StringIO() as buf, redirect_stdout(buf):
            self.rich.take_damage(5)
            self.assertEqual(0, self.rich.hit_points)
            self.assertEqual('\tAlas, Rich has fallen!\n', buf.getvalue())
        
    def test_attack(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            with patch('random.randrange', side_effect=[12, 5]):
                self.assertIsNone(self.rich.attack(self.thompson))
                self.assertEqual(5, self.thompson.hit_points)
                self.assertEqual(10, self.rich.hit_points)
                out = ('Rich attacks Thompson!\n\tHits for 5 hit points!\n' +
                       '\tThompson has 5 hit points remaining.\n')
                self.assertEqual(out, buf.getvalue())
        with io.StringIO() as buf, redirect_stdout(buf):
            with patch('random.randrange', side_effect=[11]):
                self.assertIsNone(self.rich.attack(self.thompson))
                self.assertEqual(5, self.thompson.hit_points)
                self.assertEqual(10, self.rich.hit_points)
                out = 'Rich attacks Thompson!\n\tMisses!\n'
                self.assertEqual(out, buf.getvalue())
                
    def test_is_alive(self):
        self.rich.hit_points = 0
        self.assertFalse(self.rich.is_alive())
        self.rich.hit_points = -1
        self.assertFalse(self.rich.is_alive())
        self.rich.hit_points = 2
        self.assertTrue(self.rich.is_alive())
        self.rich.hit_points = 1
        self.assertTrue(self.rich.is_alive())
            
    def test_combat_round(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            with patch('random.randrange', side_effect=[5, 5, 10, 10]):
                self.assertIsNone(combat_round(self.rich, self.thompson))
                self.assertEqual(10, self.thompson.hit_points)
                self.assertEqual(10, self.rich.hit_points)
                out = ('Simultaneous!\nRich attacks Thompson!\n\tMisses!\n' + 
                       'Thompson attacks Rich!\n\tMisses!\n')
                self.assertEqual(out, buf.getvalue())
        with io.StringIO() as buf, redirect_stdout(buf):
            with patch('random.randrange', side_effect=[2, 1, 11, 11]):
                self.assertIsNone(combat_round(self.rich, self.thompson))
                self.assertEqual(10, self.thompson.hit_points)
                self.assertEqual(10, self.rich.hit_points)
                out = ('Rich attacks Thompson!\n\tMisses!\n' + 
                       'Thompson attacks Rich!\n\tMisses!\n')
                self.assertEqual(out, buf.getvalue())
        with io.StringIO() as buf, redirect_stdout(buf):
            with patch('random.randrange', side_effect=[1, 2, 11, 11]):
                self.assertIsNone(combat_round(self.rich, self.thompson))
                self.assertEqual(10, self.thompson.hit_points)
                self.assertEqual(10, self.rich.hit_points)
                out = ('Thompson attacks Rich!\n\tMisses!\n' +
                       'Rich attacks Thompson!\n\tMisses!\n')
                self.assertEqual(out, buf.getvalue())
        self.thompson.hit_points = 2
        with io.StringIO() as buf, redirect_stdout(buf):
            with patch('random.randrange', side_effect=[2, 1, 12, 5]):
                self.assertIsNone(combat_round(self.rich, self.thompson))
                self.assertEqual(-3, self.thompson.hit_points)
                self.assertEqual(10, self.rich.hit_points)
                out = ('Rich attacks Thompson!\n\tHits for 5 hit points!\n' +
                       '\tAlas, Thompson has fallen!\n')
                self.assertEqual(out, buf.getvalue())
        self.thompson.hit_points = 2
        self.rich.hit_points = 2
        with io.StringIO() as buf, redirect_stdout(buf):
            with patch('random.randrange', side_effect=[1, 2, 12, 5]):
                self.assertIsNone(combat_round(self.rich, self.thompson))
                self.assertEqual(2, self.thompson.hit_points)
                self.assertEqual(-3, self.rich.hit_points)
                out = ('Thompson attacks Rich!\n\tHits for 5 hit points!\n' +
                       '\tAlas, Rich has fallen!\n')
                self.assertEqual(out, buf.getvalue())
                
    def test_main(self):
        out = 'rpg_main_out.txt'
        if os.path.isfile(out):
            os.remove(out)
        se = [3, 5, 12, 4, 10, 6, 1, 14, 3, 18, 2, 2, 1, 20, 5, 10, 4, 3, 15, 5]
        with open(out, 'w') as fp:
            with patch('builtins.input', side_effect=['\n', '\n', '\n', '\n']):
                with patch('random.randrange', side_effect=se):
                    sys.stdout = fp
                    main()
        sys.stdout = sys.__stdout__
        self.assertTrue(compare_files('rpg_main_out_correct.txt', out))
        
test = unittest.defaultTestLoader.loadTestsFromTestCase(TestRPG)
results = unittest.TextTestRunner().run(test)
sys.stdout = sys.__stdout__
sys.stdin = sys.__stdin__
print('Correctness score = ', str((results.testsRun - len(results.errors) - len(results.failures)) / results.testsRun * 100) + '%')
