"""
Business rule validation for the referral network.

This module handles all constraint checking including:
- No self-referrals
- Unique referrer constraint
- Acyclic graph constraint
"""

from typing import Dict, Set, Optional
from ..models.user import User


class ReferralValidator:
    """
    Validates referral network business rules and constraints.
    """
    
    @staticmethod
    def can_add_referral(referrer_id: int, candidate_id: int, 
                         users: Dict[int, User]) -> tuple[bool, str]:
        """
        Check if a referral can be added based on business rules.
        
        Args:
            referrer_id: ID of the user making the referral
            candidate_id: ID of the user being referred
            users: Dictionary of all users in the network
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if both users exist
        if referrer_id not in users:
            return False, f"Referrer {referrer_id} does not exist"
        if candidate_id not in users:
            return False, f"Candidate {candidate_id} does not exist"
        
        # No self-referrals
        if referrer_id == candidate_id:
            return False, "Users cannot refer themselves"
        
        # Unique referrer constraint
        if users[candidate_id].has_referrer():
            return False, f"User {candidate_id} already has a referrer"
        
        # Check for cycles
        if ReferralValidator._would_create_cycle(referrer_id, candidate_id, users):
            return False, "Referral would create a cycle in the network"
        
        return True, ""
    
    @staticmethod
    def _would_create_cycle(referrer_id: int, candidate_id: int, 
                           users: Dict[int, User]) -> bool:
        """
        Check if adding a referral would create a cycle.
        
        Uses DFS to detect cycles in the directed graph.
        
        Args:
            referrer_id: ID of the user making the referral
            candidate_id: ID of the user being referred
            users: Dictionary of all users in the network
            
        Returns:
            True if cycle would be created, False otherwise
        """
        # If candidate would refer back to referrer, that's a cycle
        if candidate_id == referrer_id:
            return True
        
        # Check if candidate can reach referrer through existing referrals
        visited = set()
        stack = [candidate_id]
        
        while stack:
            current = stack.pop()
            if current in visited:
                continue
                
            visited.add(current)
            
            # If we can reach the referrer, that's a cycle
            if current == referrer_id:
                return True
            
            # Add all users that current user has referred
            if current in users:
                for referred_user in users[current].get_referrals():
                    if referred_user not in visited:
                        stack.append(referred_user)
        
        return False
    
    @staticmethod
    def validate_network_integrity(users: Dict[int, User]) -> tuple[bool, list[str]]:
        """
        Validate the entire network for integrity issues.
        
        Args:
            users: Dictionary of all users in the network
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        for user_id, user in users.items():
            # Check that referrer exists
            if user.has_referrer():
                referrer_id = user.get_referrer()
                if referrer_id not in users:
                    errors.append(f"User {user_id} has non-existent referrer {referrer_id}")
            
            # Check that referred users exist
            for referred_id in user.get_referrals():
                if referred_id not in users:
                    errors.append(f"User {user_id} refers to non-existent user {referred_id}")
        
        is_valid = len(errors) == 0
        return is_valid, errors
