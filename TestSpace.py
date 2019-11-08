import unittest
from DataUtilities import *
from DataTransformer import *

#TODO: implement test cases
class TestTransformer(unittest.TestCase):
    
    def test_get_roster_mean_basestat(self):
        self.assertEqual(True,True)

    def test_get_roster_mean_all_stats(self):
        self.assertEqual(True,True)

    def test_get_roster_sdv_basestat(self):
        self.assertEqual(True,True)

    def get_roster_sdv_all_stats(self):
        self.assertEqual(True,True)

    def test_get_total_attack_effectiveness(self):
        self.assertEqual(True,True)
        
    def test_get_most_effective_attack_effectiveness(self):
        self.assertEqual(True,True)

    def test_evaluate_matchup_total(self):
        self.assertEqual(True,True)

    def test_evaluate_matchup_most_effective(self):
        self.assertEqual(True,True)
    
    def test_get_highest_speed_flag(self):
        self.assertEqual(True,True)
  
    def test_get_sdv_roster_usage_rates(self):
        self.assertEqual(True,True)

    def test_get_mean_roster_usage_rates(self):
        self.assertEqual(True,True)

class TestUtilities(unittest.TestCase):
    
    def test_get_roster_as_list(self):
        roster = "[[a], b'', c     d]"
        desired = ['a','b','cd']
        self.assertEqual(get_roster_as_list(roster),desired)

    def test_get_defense_effectiveness_list_single(self):
        def_eff_l = get_defense_effectiveness_list('Grass','Grass')
        desired = [1,1,2,2,.5,1,2,1,1,2,.5,.5,.5,1,2,1,1,1]
        self.assertEqual(def_eff_l,desired)

    def test_get_defense_effectiveness_list_double(self):
        def_eff_l = get_defense_effectiveness_list('Grass','Fire')
        desired = [1.0,1.0,2.0,2.0,1.0,2.0,1.0,1.0,.5,1.0,1.0,.25,.5,1.0,1.0,1.0,1,.5]
        self.assertEqual(def_eff_l,desired)


    def test_get_attack_effectiveness_simple(self):
        desired = 2
        self.assertEqual(get_attack_effectiveness('Fire', ['Grass']),desired)

        desired = .5
        self.assertEqual(get_attack_effectiveness('Water', ['Grass']),desired)

        desired = 1
        self.assertEqual(get_attack_effectiveness('Normal', ['Normal']),desired)

        desired = 2**-1.5
        self.assertEqual(get_attack_effectiveness('Normal', ['Ghost']),desired)

    def test_get_attack_effectiveness_double(self):
        desired = 4
        self.assertEqual(get_attack_effectiveness('Fire', ['Grass','Bug']),desired)

        desired = .5
        self.assertEqual(get_attack_effectiveness('Water', ['Grass','Normal']),desired)

        desired = 1
        self.assertEqual(get_attack_effectiveness('Dark', ['Rock']),desired)

        desired = .25
        self.assertEqual(get_attack_effectiveness('Fire', ['Water','Rock']),desired)

        desired = 2**-1.5
        self.assertEqual(get_attack_effectiveness('Normal', ['Ghost','Dark']),desired)
     

if __name__ == '__main__':
    # Run only the tests in the specified classes
    test_classes_to_run = [TestTransformer, TestUtilities]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)

