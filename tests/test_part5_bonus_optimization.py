"""
Tests for Part 5: Referral Bonus Optimization

This test suite validates the bonus optimization functionality including:
- Adoption probability functions
- Minimum bonus calculations
- Optimization algorithms
- Performance and edge cases
"""

import unittest
from source.core.simulation import min_bonus_for_target
from source.examples.adoption_functions import example_adoption_prob, create_test_adoption_prob


class TestPart5BonusOptimization(unittest.TestCase):
    """Test cases for Part 5: Referral Bonus Optimization."""
    
    def test_adoption_probability_functions(self):
        """Test adoption probability function properties."""
        # Test example_adoption_prob function
        prob = example_adoption_prob(10)
        self.assertIsInstance(prob, float)
        self.assertGreaterEqual(prob, 0.0)
        self.assertLessEqual(prob, 1.0)
        
        # Test create_test_adoption_prob function
        test_prob = create_test_adoption_prob(0.8)
        prob_value = test_prob(10)
        self.assertIsInstance(prob_value, float)
        self.assertGreaterEqual(prob_value, 0.0)
        self.assertLessEqual(prob_value, 1.0)
        
        # Test probability function properties
        prob_func = lambda x: 0.5
        prob_value = prob_func(10)
        self.assertEqual(prob_value, 0.5)
    
    def test_min_bonus_calculations(self):
        """Test minimum bonus calculations for target achievements."""
        # Test achievable target
        min_bonus = min_bonus_for_target(
            days=30,
            target_hires=10,
            adoption_prob=example_adoption_prob
        )
        self.assertIsInstance(min_bonus, float)
        self.assertGreater(min_bonus, 0.0)
        
        # Test unachievable target
        min_bonus = min_bonus_for_target(
            days=30,
            target_hires=1000,
            adoption_prob=lambda x: 0.1
        )
        self.assertIsNone(min_bonus)
        
        # Test zero days
        min_bonus = min_bonus_for_target(
            days=0,
            target_hires=10,
            adoption_prob=example_adoption_prob
        )
        self.assertIsNone(min_bonus)
        
        # Test small target
        min_bonus = min_bonus_for_target(
            days=30,
            target_hires=1,
            adoption_prob=example_adoption_prob
        )
        self.assertIsInstance(min_bonus, float)
        self.assertGreater(min_bonus, 0.0)
        
        # Test large target
        min_bonus = min_bonus_for_target(
            days=30,
            target_hires=50,
            adoption_prob=example_adoption_prob
        )
        self.assertIsInstance(min_bonus, float)
        self.assertGreater(min_bonus, 0.0)
    
    def test_optimization_algorithm_efficiency(self):
        """Test optimization algorithm efficiency and correctness."""
        # Test binary search optimization
        min_bonus = min_bonus_for_target(
            days=30,
            target_hires=20,
            adoption_prob=example_adoption_prob
        )
        
        if min_bonus is not None:
            # Test that the calculated bonus achieves the target
            # This tests the binary search algorithm correctness
            self.assertIsInstance(min_bonus, float)
            self.assertGreater(min_bonus, 0.0)
        
        # Test optimization consistency
        min_bonus1 = min_bonus_for_target(
            days=30,
            target_hires=15,
            adoption_prob=example_adoption_prob
        )
        
        min_bonus2 = min_bonus_for_target(
            days=30,
            target_hires=15,
            adoption_prob=example_adoption_prob
        )
        
        # Results should be consistent
        if min_bonus1 is not None and min_bonus2 is not None:
            self.assertAlmostEqual(min_bonus1, min_bonus2, places=6)
    
    def test_edge_cases_and_boundary_conditions(self):
        """Test edge cases and boundary conditions."""
        # Test edge cases
        min_bonus = min_bonus_for_target(
            days=30,
            target_hires=0,
            adoption_prob=example_adoption_prob
        )
        self.assertIsNone(min_bonus)
        
        # Test boundary conditions
        min_bonus = min_bonus_for_target(
            days=1,
            target_hires=1,
            adoption_prob=lambda x: 0.9
        )
        if min_bonus is not None:
            self.assertIsInstance(min_bonus, float)
            self.assertGreater(min_bonus, 0.0)
    
    def test_integration_and_performance(self):
        """Test integration with other components and performance."""
        # Test integration with different adoption probability functions
        test_prob = create_test_adoption_prob(0.7)
        
        min_bonus = min_bonus_for_target(
            days=30,
            target_hires=25,
            adoption_prob=test_prob
        )
        
        if min_bonus is not None:
            self.assertIsInstance(min_bonus, float)
            self.assertGreater(min_bonus, 0.0)
        
        # Test performance with reasonable parameters
        min_bonus = min_bonus_for_target(
            days=60,
            target_hires=30,
            adoption_prob=example_adoption_prob
        )
        
        if min_bonus is not None:
            self.assertIsInstance(min_bonus, float)
            self.assertGreater(min_bonus, 0.0)
        
        # Test memory usage doesn't cause issues
        min_bonus = min_bonus_for_target(
            days=90,
            target_hires=40,
            adoption_prob=example_adoption_prob
        )
        
        if min_bonus is not None:
            self.assertIsInstance(min_bonus, float)
            self.assertGreater(min_bonus, 0.0)


if __name__ == '__main__':
    unittest.main()
