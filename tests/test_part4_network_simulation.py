"""
Tests for Part 4: Network Simulation

This test suite validates the network simulation functionality including:
- Growth simulation
- Target achievement calculations
- Parameter validation
- Edge case handling
"""

import unittest
from source.core.simulation import simulate_network_growth, days_to_target
from source.examples.adoption_functions import example_adoption_prob


class TestPart4NetworkSimulation(unittest.TestCase):
    """Test cases for Part 4: Network Simulation."""
    
    def test_basic_simulation(self):
        """Test basic network growth simulation."""
        # Test basic simulation
        result = simulate_network_growth(
            initial_users=10,
            target_users=20,
            adoption_prob=example_adoption_prob,
            max_days=30
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('success', result)
        self.assertIn('days_taken', result)
        self.assertIn('final_users', result)
        
        # Test zero probability
        result = simulate_network_growth(
            initial_users=10,
            target_users=20,
            adoption_prob=lambda x: 0,
            max_days=30
        )
        self.assertFalse(result['success'])
        
        # Test high probability
        result = simulate_network_growth(
            initial_users=10,
            target_users=20,
            adoption_prob=lambda x: 0.9,
            max_days=30
        )
        self.assertTrue(result['success'])
    
    def test_simulation_edge_cases(self):
        """Test simulation edge cases and parameter validation."""
        # Test capacity exhaustion - with high probability, target should be reached quickly
        result = simulate_network_growth(
            initial_users=95,
            target_users=100,
            adoption_prob=lambda x: 0.5,
            max_days=10
        )
        self.assertTrue(result['success'])  # With 0.5 probability, 95 users can easily reach 100
        
        # Test negative probability
        with self.assertRaises(ValueError):
            simulate_network_growth(
                initial_users=10,
                target_users=20,
                adoption_prob=lambda x: -0.1,
                max_days=30
            )
        
        # Test probability greater than one
        with self.assertRaises(ValueError):
            simulate_network_growth(
                initial_users=10,
                target_users=20,
                adoption_prob=lambda x: 1.1,
                max_days=30
            )
    
    def test_days_to_target_calculations(self):
        """Test days to target calculations."""
        # Test achievable target
        days = days_to_target(
            initial_users=10,
            target_users=20,
            adoption_prob=example_adoption_prob
        )
        self.assertIsInstance(days, int)
        self.assertGreater(days, 0)
        
        # Test unachievable target (very low probability)
        days = days_to_target(
            initial_users=95,
            target_users=100,
            adoption_prob=lambda x: 0.001  # Very low probability
        )
        self.assertIsNone(days)
        
        # Test zero probability
        days = days_to_target(
            initial_users=10,
            target_users=20,
            adoption_prob=lambda x: 0
        )
        self.assertIsNone(days)
        
        # Test small target
        days = days_to_target(
            initial_users=10,
            target_users=11,
            adoption_prob=lambda x: 0.5
        )
        self.assertIsInstance(days, int)
        self.assertGreaterEqual(days, 0)
    
    def test_simulation_consistency_and_bounds(self):
        """Test simulation consistency and boundary conditions."""
        # Test simulation consistency
        result1 = simulate_network_growth(
            initial_users=10,
            target_users=20,
            adoption_prob=example_adoption_prob,
            max_days=30
        )
        
        result2 = simulate_network_growth(
            initial_users=10,
            target_users=20,
            adoption_prob=example_adoption_prob,
            max_days=30
        )
        
        # Results should be consistent for same parameters
        self.assertEqual(result1['success'], result2['success'])
        
        # Test simulation monotonicity
        result_small = simulate_network_growth(
            initial_users=10,
            target_users=15,
            adoption_prob=example_adoption_prob,
            max_days=30
        )
        
        result_large = simulate_network_growth(
            initial_users=10,
            target_users=20,
            adoption_prob=example_adoption_prob,
            max_days=30
        )
        
        # Larger target should take more days (if both succeed)
        if result_small['success'] and result_large['success']:
            self.assertGreaterEqual(result_large['days_taken'], result_small['days_taken'])
        
        # Test bounds
        if result1['success']:
            self.assertGreaterEqual(result1['final_users'], 20)
            self.assertGreaterEqual(result1['days_taken'], 0)
            self.assertLessEqual(result1['days_taken'], 30)
    
    def test_parameter_validation(self):
        """Test parameter validation in simulation functions."""
        # Test invalid initial users
        with self.assertRaises(ValueError):
            simulate_network_growth(
                initial_users=-1,
                target_users=20,
                adoption_prob=example_adoption_prob,
                max_days=30
            )
        
        # Test invalid target users (target <= initial)
        with self.assertRaises(ValueError):
            simulate_network_growth(
                initial_users=10,
                target_users=10,
                adoption_prob=example_adoption_prob,
                max_days=30
            )
        
        # Test invalid max days
        with self.assertRaises(ValueError):
            simulate_network_growth(
                initial_users=10,
                target_users=20,
                adoption_prob=example_adoption_prob,
                max_days=0
            )
        
        # Test days_to_target parameter validation
        with self.assertRaises(ValueError):
            days_to_target(
                initial_users=0,
                target_users=20,
                adoption_prob=example_adoption_prob
            )
        
        with self.assertRaises(ValueError):
            days_to_target(
                initial_users=10,
                target_users=10,
                adoption_prob=example_adoption_prob
            )


if __name__ == '__main__':
    unittest.main()
