"""
Tests for Part 3: Influencer Identification

This test suite validates the influencer identification functionality including:
- Total referral calculations
- Top referrer identification
- Unique reach expansion
- Flow centrality calculations
"""

import unittest
from source.core.referral_network import ReferralNetwork


class TestPart3InfluencerIdentification(unittest.TestCase):
    """Test cases for Part 3: Influencer Identification."""
    
    def setUp(self):
        """Set up a fresh network for each test."""
        self.network = ReferralNetwork()
    
    def test_total_referral_calculations(self):
        """Test total referral count calculations."""
        # Build network: 1 -> 2 -> 3, 1 -> 4
        for i in range(1, 5):
            self.network.add_user(i)
        
        self.network.add_referral(1, 2)
        self.network.add_referral(2, 3)
        self.network.add_referral(1, 4)
        
        # Test total referrals
        self.assertEqual(self.network.get_total_referrals(1), 3)  # 2, 3, 4
        self.assertEqual(self.network.get_total_referrals(2), 1)  # 3
        self.assertEqual(self.network.get_total_referrals(3), 0)
        self.assertEqual(self.network.get_total_referrals(4), 0)
        
        # Test empty network
        empty_network = ReferralNetwork()
        self.assertEqual(empty_network.get_total_referrals(1), 0)
    
    def test_top_referrer_identification(self):
        """Test top referrer identification."""
        # Build network: 1 -> 2, 1 -> 3, 2 -> 4, 3 -> 5
        for i in range(1, 6):
            self.network.add_user(i)
        
        self.network.add_referral(1, 2)
        self.network.add_referral(1, 3)
        self.network.add_referral(2, 4)
        self.network.add_referral(3, 5)
        
        # Test top referrers
        top_refs = self.network.get_top_referrers(3)
        self.assertEqual(len(top_refs), 3)
        self.assertEqual(top_refs[0][0], 1)  # User 1 has most referrals
        self.assertEqual(top_refs[0][1], 4)  # 2 direct + 2 indirect = 4 total
        self.assertEqual(top_refs[1][0], 2)  # User 2 has second most
        self.assertEqual(top_refs[1][1], 1)  # 1 direct + 0 indirect = 1 total
        
        # Test with less than available
        top_refs = self.network.get_top_referrers(2)
        self.assertEqual(len(top_refs), 2)
        
        # Test empty network
        empty_network = ReferralNetwork()
        top_refs = empty_network.get_top_referrers(3)
        self.assertEqual(len(top_refs), 0)
    
    def test_unique_reach_expansion(self):
        """Test unique reach expansion algorithm."""
        # Build network with overlapping reach
        for i in range(1, 7):
            self.network.add_user(i)
        
        # 1 -> 2 -> 3 (reach: 2, 3)
        # 1 -> 4 -> 5 (reach: 4, 5)
        # 2 -> 6 (reach: 6)
        # Note: User 1's total reach is {2, 3, 4, 5, 6} = 5 users
        self.network.add_referral(1, 2)
        self.network.add_referral(2, 3)
        self.network.add_referral(1, 4)
        self.network.add_referral(4, 5)
        self.network.add_referral(2, 6)
        
        # Test unique reach expansion
        unique_reach = self.network.get_unique_reach_expansion(2)
        self.assertEqual(len(unique_reach), 2)
        
        # User 1 should be first (reach: 2, 3, 4, 5, 6)
        self.assertEqual(unique_reach[0][0], 1)
        self.assertEqual(unique_reach[0][1], 5)
        
        # Test no overlap scenario
        self.network.add_user(7)
        self.network.add_user(8)
        self.network.add_referral(6, 7)
        self.network.add_referral(5, 8)
        
        unique_reach = self.network.get_unique_reach_expansion(3)
        self.assertEqual(len(unique_reach), 3)
    
    def test_flow_centrality_calculations(self):
        """Test flow centrality calculations."""
        # Build network: 1 -> 2 -> 3, 1 -> 4
        for i in range(1, 5):
            self.network.add_user(i)
        
        self.network.add_referral(1, 2)
        self.network.add_referral(2, 3)
        self.network.add_referral(1, 4)
        
        # Test flow centrality
        centrality = self.network.get_flow_centrality(3)
        self.assertEqual(len(centrality), 3)
        
        # User 2 should have highest centrality (bridge between 1 and 3)
        self.assertEqual(centrality[0][0], 2)
        
        # Test simple chain
        simple_network = ReferralNetwork()
        for i in range(1, 4):
            simple_network.add_user(i)
        
        simple_network.add_referral(1, 2)
        simple_network.add_referral(2, 3)
        
        centrality = simple_network.get_flow_centrality(3)
        self.assertEqual(len(centrality), 3)
        self.assertEqual(centrality[0][0], 2)  # Middle user has highest centrality
    
    def test_large_network_performance(self):
        """Test performance with larger networks."""
        # Build larger network for performance testing
        for i in range(1, 51):
            self.network.add_user(i)
        
        # Create referral chain
        for i in range(1, 50):
            self.network.add_user(i + 1)
            self.network.add_referral(i, i + 1)
        
        # Test that operations complete in reasonable time
        top_refs = self.network.get_top_referrers(5)
        self.assertEqual(len(top_refs), 5)
        
        unique_reach = self.network.get_unique_reach_expansion(5)
        self.assertEqual(len(unique_reach), 5)
        
        # Test optimized flow centrality
        centrality = self.network.get_flow_centrality(5)
        self.assertEqual(len(centrality), 5)


if __name__ == '__main__':
    unittest.main()
