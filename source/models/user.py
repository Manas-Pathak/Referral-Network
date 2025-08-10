"""
User model for the referral network system.

This module defines the User class and related user management functionality.
"""

from typing import Set, Optional


class User:
    """
    Represents a user in the referral network.
    
    Each user has a unique ID and can be part of referral relationships.
    """
    
    def __init__(self, user_id: int):
        """
        Initialize a new user.
        
        Args:
            user_id: Unique identifier for the user
        """
        self.user_id = user_id
        self.referrals: Set[int] = set()  # Users this user has referred
        self.referrer: Optional[int] = None  # User who referred this user
    
    def add_referral(self, candidate_id: int) -> bool:
        """
        Add a referral to another user.
        
        Args:
            candidate_id: ID of the user being referred
            
        Returns:
            True if referral was added successfully
        """
        if candidate_id not in self.referrals:
            self.referrals.add(candidate_id)
            return True
        return False
    
    def set_referrer(self, referrer_id: int) -> None:
        """
        Set the user who referred this user.
        
        Args:
            referrer_id: ID of the referring user
        """
        self.referrer = referrer_id
    
    def has_referrer(self) -> bool:
        """
        Check if this user has a referrer.
        
        Returns:
            True if user has a referrer, False otherwise
        """
        return self.referrer is not None
    
    def get_referrer(self) -> Optional[int]:
        """
        Get the ID of the user who referred this user.
        
        Returns:
            Referrer ID or None if no referrer
        """
        return self.referrer
    
    def get_referrals(self) -> Set[int]:
        """
        Get all users this user has referred.
        
        Returns:
            Set of user IDs that this user has referred
        """
        return self.referrals.copy()
    
    def __repr__(self) -> str:
        """String representation of the user."""
        return f"User(id={self.user_id}, referrals={len(self.referrals)}, referrer={self.referrer})"
