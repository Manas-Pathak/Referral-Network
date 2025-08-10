"""
Tests for Part 1: Core Referral Network Structure

This test suite validates the basic referral network functionality including:
- User and referral management
- Basic network operations
- User model functionality
"""

import unittest
from source.core.referral_network import ReferralNetwork
from source.models.user import User


class TestPart1CoreStructure(unittest.TestCase):
    """Test cases for Part 1: Core Referral Network Structure."""
    
    def setUp(self):
        """Set up a fresh network for each test."""
        self.network = ReferralNetwork()
    
    def test_user_management(self):
        """Test user management operations."""
        # Test adding new users
        self.assertTrue(self.network.add_user(1))
        self.assertTrue(self.network.add_user(2))
        self.assertIn(1, self.network.users)
        self.assertIn(2, self.network.users)
        
        # Test adding duplicate user
        self.assertFalse(self.network.add_user(1))
        self.assertEqual(self.network.get_network_size(), 2)
        
        # Test empty network
        self.assertEqual(len(self.network.users), 2)
    
    def test_basic_referral_operations(self):
        """Test basic referral functionality."""
        self.network.add_user(1)
        self.network.add_user(2)
        self.network.add_user(3)
        
        # Test successful referral
        self.assertTrue(self.network.add_referral(1, 2))
        self.assertIn(2, self.network.get_direct_referrals(1))
        self.assertEqual(self.network.referrer_map[2], 1)
        
        # Test multiple referrals
        self.assertTrue(self.network.add_referral(1, 3))
        direct_refs = self.network.get_direct_referrals(1)
        self.assertEqual(len(direct_refs), 2)
        self.assertIn(2, direct_refs)
        self.assertIn(3, direct_refs)
    
    def test_referral_validation(self):
        """Test referral validation and error handling."""
        self.network.add_user(1)
        
        # Test referring nonexistent user
        with self.assertRaises(ValueError):
            self.network.add_referral(1, 2)
        
        # Test nonexistent referrer
        self.network.add_user(2)
        with self.assertRaises(ValueError):
            self.network.add_referral(3, 2)
    
    def test_user_model_functionality(self):
        """Test User model core functionality."""
        user = User(1)
        
        # Test user initialization
        self.assertEqual(user.user_id, 1)
        self.assertEqual(len(user.get_referrals()), 0)
        self.assertIsNone(user.get_referrer())
        self.assertFalse(user.has_referrer())
        
        # Test setting referrer
        user.set_referrer(2)
        self.assertEqual(user.get_referrer(), 2)
        self.assertTrue(user.has_referrer())
        
        # Test adding referral
        user.add_referral(3)
        self.assertIn(3, user.get_referrals())
    
    def test_network_operations(self):
        """Test network-level operations."""
        # Test network size
        self.assertEqual(self.network.get_network_size(), 0)
        
        self.network.add_user(1)
        self.assertEqual(self.network.get_network_size(), 1)
        
        # Test single user network
        self.assertEqual(len(self.network.get_direct_referrals(1)), 0)
        self.assertEqual(self.network.get_total_referrals(1), 0)


if __name__ == '__main__':
    unittest.main()
