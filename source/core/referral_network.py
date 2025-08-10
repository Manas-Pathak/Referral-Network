"""
Referral Network system that manages users and their referral relationships.

This module provides the main ReferralNetwork class that orchestrates all
referral network operations using separated, focused modules.

Design Choices:
- Used adjacency list representation (referrals dict) for efficient direct referral queries
- Added referrer_map for O(1) lookups of who referred each user
- Chose set data structures for O(1) membership testing and duplicate prevention
- Implemented cycle detection using DFS to maintain acyclic constraint

API Design:
- add_user() returns boolean for idempotent behavior
- add_referral() returns boolean and raises ValueError for invalid users
- Query methods return copies to prevent external modification
- All methods validate user existence before processing
"""

import logging
from typing import Set, List, Tuple, Dict, Optional
from ..models.user import User
from ..constraints.validator import ReferralValidator
from ..algorithms.network_analysis import NetworkAnalyzer
from ..algorithms.reach_expansion import ReachExpander

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReferralNetwork:
    """
    A referral network that manages users and their referral relationships.
    
    This class implements a directed acyclic graph (DAG) structure to model
    referral networks while enforcing business rules and constraints.
    """
    
    def __init__(self):
        """Initialize an empty referral network."""
        self.users: Dict[int, User] = {}
        self.referrer_map: Dict[int, int] = {}  # Maps user_id to their referrer_id
    
    def add_user(self, user_id: int) -> bool:
        """
        Add a user to the network.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            True if user was added, False if user already exists
            
        Raises:
            ValueError: If user_id is invalid (negative or None)
        """
        if user_id is None or user_id < 0:
            raise ValueError("User ID must be a non-negative integer")
            
        if user_id in self.users:
            return False
        
        self.users[user_id] = User(user_id)
        return True
    
    def add_referral(self, referrer_id: int, candidate_id: int) -> bool:
        """
        Add a referral relationship between two users.
        
        Args:
            referrer_id: ID of the user making the referral
            candidate_id: ID of the user being referred
            
        Returns:
            True if referral was added successfully
            
        Raises:
            ValueError: If either user doesn't exist
        """
        # Validate users exist
        if referrer_id not in self.users:
            raise ValueError(f"Referrer {referrer_id} does not exist")
        if candidate_id not in self.users:
            raise ValueError(f"Candidate {candidate_id} does not exist")
        
        # Check business rules
        is_valid, error_msg = ReferralValidator.can_add_referral(
            referrer_id, candidate_id, self.users
        )
        
        if not is_valid:
            return False
        
        # Add referral
        referrer = self.users[referrer_id]
        candidate = self.users[candidate_id]
        
        referrer.add_referral(candidate_id)
        candidate.set_referrer(referrer_id)
        
        # Update referrer map for O(1) lookups
        self.referrer_map[candidate_id] = referrer_id
        
        return True
    
    def get_direct_referrals(self, user_id: int) -> Set[int]:
        """
        Get users directly referred by the specified user.
        
        Args:
            user_id: ID of the user to query
            
        Returns:
            Set of user IDs directly referred by this user
        """
        if user_id not in self.users:
            return set()
        
        user = self.users[user_id]
        return user.get_referrals().copy()  # Return copy to prevent external modification
    
    def get_total_referrals(self, user_id: int) -> int:
        """
        Calculate total referrals (direct + indirect) for a user.
        
        Args:
            user_id: ID of the user to analyze
            
        Returns:
            Total number of referrals (direct + indirect)
        """
        if user_id not in self.users:
            return 0
        
        return NetworkAnalyzer.get_total_referrals(user_id, self.users)
    
    def get_top_referrers(self, k: int) -> List[Tuple[int, int]]:
        """
        Get the top k referrers ranked by their total referral count.
        
        Args:
            k: Number of top referrers to return
            
        Returns:
            List of tuples (user_id, total_referrals) sorted by referral count
        """
        if k <= 0:
            return []
        
        return NetworkAnalyzer.get_top_referrers(k, self.users)
    
    def get_unique_reach_expansion(self, k: int) -> List[Tuple[int, int]]:
        """
        Get top k referrers based on unique reach expansion.
        
        Args:
            k: Number of top referrers to return
            
        Returns:
            List of tuples (user_id, unique_reach_count) sorted by unique reach
        """
        if k <= 0:
            return []
        
        return ReachExpander.get_unique_reach_expansion(k, self.users)
    
    def get_flow_centrality(self, k: int) -> List[Tuple[int, float]]:
        """
        Get top k users based on flow centrality.
        
        Args:
            k: Number of top users to return
            
        Returns:
            List of tuples (user_id, centrality_score) sorted by centrality
        """
        if k <= 0:
            return []
        
        return NetworkAnalyzer.get_flow_centrality(k, self.users)
    
    def get_flow_centrality_optimized(self, k: int, sample_ratio: float = 0.3) -> List[Tuple[int, float]]:
        """
        Get top k users based on flow centrality using optimized algorithm.
        
        Args:
            k: Number of top users to return
            sample_ratio: Ratio of user pairs to sample for optimization
            
        Returns:
            List of tuples (user_id, centrality_score) sorted by centrality
        """
        if k <= 0:
            return []
        
        return NetworkAnalyzer.get_flow_centrality_optimized(k, self.users, sample_ratio)
    
    def get_network_size(self) -> int:
        """
        Get the total number of users in the network.
        
        Returns:
            Number of users in the network
        """
        return len(self.users)
    
    def get_user(self, user_id: int) -> Optional[User]:
        """
        Get a user by ID.
        
        Args:
            user_id: ID of the user to retrieve
            
        Returns:
            User object if found, None otherwise
        """
        return self.users.get(user_id)
    
    def get_referrer(self, user_id: int) -> Optional[int]:
        """
        Get the referrer ID for a given user.
        
        Args:
            user_id: ID of the user to query
            
        Returns:
            Referrer ID if user was referred, None otherwise
        """
        return self.referrer_map.get(user_id)
    
    def has_user(self, user_id: int) -> bool:
        """
        Check if a user exists in the network.
        
        Args:
            user_id: ID of the user to check
            
        Returns:
            True if user exists, False otherwise
        """
        return user_id in self.users
    
    def validate_network(self) -> List[str]:
        """
        Validate the network for any constraint violations.
        
        Returns:
            List of validation error messages (empty if network is valid)
        """
        errors = []
        
        # Check for cycles
        for user_id in self.users:
            if self._has_cycle(user_id):
                errors.append(f"Cycle detected involving user {user_id}")
        
        # Check for orphaned users (users with referrers that don't exist)
        for candidate_id, referrer_id in self.referrer_map.items():
            if referrer_id not in self.users:
                errors.append(f"User {candidate_id} has non-existent referrer {referrer_id}")
        
        return errors
    
    def clear(self) -> None:
        """Clear all users and referrals from the network."""
        self.users.clear()
        self.referrer_map.clear()
    
    def __repr__(self) -> str:
        """String representation of the network."""
        return f"ReferralNetwork(users={len(self.users)}, referrals={len(self.referrer_map)})"
    
    def export_network(self) -> Dict:
        """
        Export the network data for serialization.
        
        Returns:
            Dictionary containing network data
        """
        network_data = {
            'users': {},
            'referrals': {}
        }
        
        # Export user data
        for user_id, user in self.users.items():
            network_data['users'][user_id] = {
                'referrals': list(user.get_referrals()),
                'referrer': user.get_referrer()
            }
        
        return network_data
    
    def import_network(self, network_data: Dict) -> bool:
        """
        Import network data from a dictionary.
        
        Args:
            network_data: Dictionary containing network data
            
        Returns:
            True if import was successful, False otherwise
        """
        try:
            self.clear()
            
            # Import users first
            for user_id in network_data.get('users', {}):
                self.add_user(int(user_id))
            
            # Import referrals
            for user_id, user_data in network_data.get('users', {}).items():
                user_id = int(user_id)
                
                # Add referrals
                for referral_id in user_data.get('referrals', []):
                    self.add_referral(user_id, int(referral_id))
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to import network: {e}")
            return False
    
    def _has_cycle(self, start_user_id: int) -> bool:
        """
        Check if there's a cycle starting from the given user.
        
        Args:
            start_user_id: ID of the user to start cycle detection from
            
        Returns:
            True if a cycle is detected, False otherwise
        """
        visited = set()
        rec_stack = set()
        
        def dfs(user_id: int) -> bool:
            if user_id in rec_stack:
                return True  # Cycle detected
            
            if user_id in visited:
                return False
            
            visited.add(user_id)
            rec_stack.add(user_id)
            
            user = self.users.get(user_id)
            if user:
                for referral_id in user.get_referrals():
                    if dfs(referral_id):
                        return True
            
            rec_stack.remove(user_id)
            return False
        
        return dfs(start_user_id)
