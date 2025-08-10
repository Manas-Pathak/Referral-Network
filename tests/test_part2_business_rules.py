"""
Tests for Part 2: Business Rule Enforcement

This test suite validates the business rule enforcement including:
- No self-referrals constraint
- Unique referrer constraint
- Acyclic network constraint
- Referral validation
"""

import unittest
from source.core.referral_network import ReferralNetwork
from source.constraints.validator import ReferralValidator
from source.models.user import User


class TestPart2BusinessRules(unittest.TestCase):
    """Test cases for Part 2: Business Rule Enforcement."""
    
    def setUp(self):
        """Set up a fresh network for each test."""
        self.network = ReferralNetwork()
        self.users = {
            1: User(1),
            2: User(2),
            3: User(3),
            4: User(4)
        }
    
    def test_self_referral_constraints(self):
        """Test that self-referrals are rejected."""
        self.network.add_user(1)
        
        # Self-referral should fail
        self.assertFalse(self.network.add_referral(1, 1))
        self.assertEqual(len(self.network.get_direct_referrals(1)), 0)
        
        # Test self-referral prevention in validator
        is_valid, error_msg = ReferralValidator.can_add_referral(1, 1, self.users)
        self.assertFalse(is_valid)
        self.assertEqual(error_msg, "Users cannot refer themselves")
    
    def test_unique_referrer_constraints(self):
        """Test that each user can only be referred by one person."""
        self.network.add_user(1)
        self.network.add_user(2)
        self.network.add_user(3)
        
        # First referral should succeed
        self.assertTrue(self.network.add_referral(1, 2))
        
        # Second referral to same user should fail
        self.assertFalse(self.network.add_referral(3, 2))
        
        # Verify only first referral exists
        self.assertIn(2, self.network.get_direct_referrals(1))
        self.assertEqual(self.network.referrer_map[2], 1)
        
        # Test unique referrer constraint in validator
        self.users[2].set_referrer(1)
        is_valid, error_msg = ReferralValidator.can_add_referral(3, 2, self.users)
        self.assertFalse(is_valid)
        self.assertIn("already has a referrer", error_msg)
    
    def test_acyclic_network_constraints(self):
        """Test that cycles are prevented."""
        self.network.add_user(1)
        self.network.add_user(2)
        self.network.add_user(3)
        self.network.add_user(4)
        
        # Create chain: 1 -> 2 -> 3
        self.assertTrue(self.network.add_referral(1, 2))
        self.assertTrue(self.network.add_referral(2, 3))
        
        # Try to create cycle: 3 -> 1
        self.assertFalse(self.network.add_referral(3, 1))
        
        # Test more complex cycle detection
        self.assertTrue(self.network.add_referral(1, 4))
        self.assertFalse(self.network.add_referral(4, 2))  # Would create cycle
        
        # Verify cycle wasn't created
        self.assertNotIn(1, self.network.get_direct_referrals(3))
        self.assertNotIn(2, self.network.get_direct_referrals(4))
    
    def test_referral_validation(self):
        """Test referral validation and error handling."""
        # Test valid referral addition
        is_valid, error_msg = ReferralValidator.can_add_referral(1, 2, self.users)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
        
        # Test nonexistent referrer
        is_valid, error_msg = ReferralValidator.can_add_referral(5, 2, self.users)
        self.assertFalse(is_valid)
        self.assertIn("does not exist", error_msg)
        
        # Test nonexistent candidate
        is_valid, error_msg = ReferralValidator.can_add_referral(1, 5, self.users)
        self.assertFalse(is_valid)
        self.assertIn("does not exist", error_msg)
    
    def test_network_integrity_validation(self):
        """Test network integrity validation."""
        # Test valid network
        is_valid, errors = ReferralValidator.validate_network_integrity(self.users)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
        # Test network with invalid referrer
        self.users[2].set_referrer(5)  # Referrer doesn't exist
        is_valid, errors = ReferralValidator.validate_network_integrity(self.users)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)


if __name__ == '__main__':
    unittest.main()
