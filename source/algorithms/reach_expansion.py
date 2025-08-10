"""
Unique reach expansion algorithms for referral networks.

This module implements greedy algorithms for finding users who can expand
the network's reach with minimal overlap.
"""

from typing import List, Tuple, Dict, Set
from ..models.user import User


class ReachExpander:
    """
    Implements algorithms for finding users who can expand network reach.
    """
    
    @staticmethod
    def get_unique_reach_expansion(k: int, users: Dict[int, User]) -> List[Tuple[int, int]]:
        """
        Find top k users by unique reach expansion using greedy algorithm.
        
        This algorithm finds users who can bring the most new users to the network
        with minimal overlap with already selected users.
        
        Args:
            k: Number of top users to return
            users: Dictionary of all users in the network
            
        Returns:
            List of tuples (user_id, unique_reach) sorted by unique reach
        """
        if k <= 0:
            return []
        
        # Get all users who have made referrals
        potential_referrers = []
        for user_id, user in users.items():
            if user.get_referrals():
                potential_referrers.append(user_id)
        
        if not potential_referrers:
            return []
        
        # Greedy selection: at each step, pick the user who adds the most new reach
        selected_users = set()
        total_reach = set()
        results = []
        
        for step in range(min(k, len(potential_referrers))):
            best_user = None
            best_new_reach = -1  # Allow users with 0 new reach
            
            for user_id in potential_referrers:
                if user_id in selected_users:
                    continue
                
                # Calculate new reach this user would add
                user_reach = ReachExpander._get_user_reach(user_id, users)
                new_reach = len(user_reach - total_reach)
                
                if new_reach > best_new_reach:
                    best_new_reach = new_reach
                    best_user = user_id
            
            if best_user is None:
                break
            
            # Add best user to selection
            selected_users.add(best_user)
            user_reach = ReachExpander._get_user_reach(best_user, users)
            total_reach.update(user_reach)
            
            results.append((best_user, len(user_reach)))
            
            # Continue even if new_reach is 0, as long as we haven't reached k
            # Don't break here - we want to select k users even if some add 0 new reach
        
        # Sort by unique reach (descending)
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    @staticmethod
    def _get_user_reach(user_id: int, users: Dict[int, User]) -> Set[int]:
        """
        Get the complete reach (direct + indirect referrals) of a user.
        
        Args:
            user_id: ID of the user to analyze
            users: Dictionary of all users in the network
            
        Returns:
            Set of user IDs in this user's reach
        """
        if user_id not in users:
            return set()
        
        reach = set()
        stack = [user_id]
        
        while stack:
            current = stack.pop()
            if current in reach:
                continue
                
            # Don't include the user themselves in their reach
            if current != user_id:
                reach.add(current)
            
            # Add all users this user has referred
            current_user = users[current]
            for referred_id in current_user.get_referrals():
                if referred_id not in reach:
                    stack.append(referred_id)
        
        return reach
    
    @staticmethod
    def get_network_coverage(selected_users: List[int], users: Dict[int, User]) -> float:
        """
        Calculate the percentage of network covered by selected users.
        
        Args:
            selected_users: List of user IDs to analyze
            users: Dictionary of all users in the network
            
        Returns:
            Coverage percentage (0.0 to 1.0)
        """
        if not selected_users or not users:
            return 0.0
        
        total_users = len(users)
        covered_users = set()
        
        for user_id in selected_users:
            if user_id in users:
                user_reach = ReachExpander._get_user_reach(user_id, users)
                covered_users.update(user_reach)
        
        return len(covered_users) / total_users if total_users > 0 else 0.0
