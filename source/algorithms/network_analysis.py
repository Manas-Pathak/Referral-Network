"""
Network analysis algorithms for the referral network.

This module contains algorithms for analyzing referral patterns and user influence.
"""

from typing import List, Tuple, Dict, Set
from collections import deque
from ..models.user import User


class NetworkAnalyzer:
    """
    Provides algorithms for analyzing referral network patterns and metrics.
    """
    
    @staticmethod
    def get_total_referrals(user_id: int, users: Dict[int, User]) -> int:
        """
        Calculate total referrals (direct + indirect) for a user.
        
        Uses BFS to traverse the referral tree and count all reachable users.
        
        Args:
            user_id: ID of the user to analyze
            users: Dictionary of all users in the network
            
        Returns:
            Total number of referrals (direct + indirect)
        """
        if user_id not in users:
            return 0
        
        visited = set()
        queue = deque([user_id])
        total = 0
        
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
                
            visited.add(current)
            
            # Count direct referrals
            current_user = users[current]
            for referred_id in current_user.get_referrals():
                if referred_id not in visited:
                    queue.append(referred_id)
                    total += 1
        
        return total
    
    @staticmethod
    def get_top_referrers(k: int, users: Dict[int, User]) -> List[Tuple[int, int]]:
        """
        Get the top k referrers ranked by their total referral count.
        
        Guidance on picking k:
        - For small networks (< 100 users): k = 3-5 provides meaningful ranking
        - For medium networks (100-1000 users): k = 5-10 shows top performers
        - For large networks (> 1000 users): k = 10-20 gives broader perspective
        - Consider business needs: k should be large enough to identify actionable insights
          but small enough to focus on top performers
        
        Args:
            k: Number of top referrers to return
            users: Dictionary of all users in the network
            
        Returns:
            List of tuples (user_id, total_referrals) sorted by referral count
        """
        referrer_counts = []
        
        for user_id, user in users.items():
            if user.get_referrals():  # Only include users who have made referrals
                total_refs = NetworkAnalyzer.get_total_referrals(user_id, users)
                referrer_counts.append((user_id, total_refs))
        
        # Sort by referral count (descending) and return top k
        referrer_counts.sort(key=lambda x: x[1], reverse=True)
        return referrer_counts[:k]
    
    @staticmethod
    def get_flow_centrality(k: int, users: Dict[int, User]) -> List[Tuple[int, float]]:
        """
        Calculate flow centrality for users in the network.
        
        Flow centrality measures how much a user acts as a "bridge" between
        different parts of the network. Higher values indicate users who
        control information flow between disconnected network segments.
        
        Args:
            k: Number of top users by flow centrality to return
            users: Dictionary of all users in the network
            
        Returns:
            List of tuples (user_id, centrality_score) sorted by centrality
        """
        centrality_scores = []
        
        for user_id, user in users.items():
            if not user.get_referrals():
                centrality_scores.append((user_id, 0.0))
                continue
            
            # Calculate flow centrality as the number of pairs of users
            # that can only communicate through this user
            centrality = NetworkAnalyzer._calculate_flow_centrality(user_id, users)
            centrality_scores.append((user_id, centrality))
        
        # Sort by centrality score (descending) and return top k
        centrality_scores.sort(key=lambda x: x[1], reverse=True)
        return centrality_scores[:k]
    
    @staticmethod
    def get_flow_centrality_optimized(k: int, users: Dict[int, User], 
                                    sample_ratio: float = 0.3) -> List[Tuple[int, float]]:
        """
        Optimized flow centrality calculation using sampling and caching.
        
        This reduces complexity from O(V³) to approximately O(V² log V) by:
        1. Sampling user pairs instead of checking all
        2. Caching shortest path distances
        3. Using more efficient path checking
        
        Args:
            k: Number of top users by flow centrality to return
            users: Dictionary of all users in the network
            sample_ratio: Fraction of user pairs to sample (0.0 to 1.0)
            
        Returns:
            List of tuples (user_id, centrality_score) sorted by centrality
        """
        if len(users) <= 100:
            # For small networks, use the exact algorithm
            return NetworkAnalyzer.get_flow_centrality(k, users)
        
        centrality_scores = []
        all_users = list(users.keys())
        n_users = len(all_users)
        
        # Pre-compute all-pairs shortest distances using Floyd-Warshall
        # This is O(V³) but only done once, then reused for all users
        distances = NetworkAnalyzer._compute_all_pairs_shortest_distances(users)
        
        # Sample user pairs for approximation
        sample_size = max(1, int(sample_ratio * n_users * (n_users - 1) / 2))
        sampled_pairs = NetworkAnalyzer._sample_user_pairs(all_users, sample_size)
        
        for user_id, user in users.items():
            if not user.get_referrals():
                centrality_scores.append((user_id, 0.0))
                continue
            
            # Calculate approximate flow centrality using sampled pairs
            centrality = NetworkAnalyzer._calculate_flow_centrality_optimized(
                user_id, users, distances, sampled_pairs
            )
            centrality_scores.append((user_id, centrality))
        
        # Sort by centrality score (descending) and return top k
        centrality_scores.sort(key=lambda x: x[1], reverse=True)
        return centrality_scores[:k]
    
    @staticmethod
    def _compute_all_pairs_shortest_distances(users: Dict[int, User]) -> Dict[Tuple[int, int], int]:
        """
        Compute all-pairs shortest distances using Floyd-Warshall algorithm.
        
        Args:
            users: Dictionary of all users in the network
            
        Returns:
            Dictionary mapping (user1, user2) to shortest distance
        """
        all_users = list(users.keys())
        n_users = len(all_users)
        
        # Initialize distances
        distances = {}
        for i, user1 in enumerate(all_users):
            for j, user2 in enumerate(all_users):
                if i == j:
                    distances[(user1, user2)] = 0
                elif user2 in users[user1].get_referrals():
                    distances[(user1, user2)] = 1
                else:
                    distances[(user1, user2)] = float('inf')
        
        # Floyd-Warshall algorithm
        for k in all_users:
            for i in all_users:
                for j in all_users:
                    if distances[(i, k)] + distances[(k, j)] < distances[(i, j)]:
                        distances[(i, j)] = distances[(i, k)] + distances[(k, j)]
        
        return distances
    
    @staticmethod
    def _sample_user_pairs(all_users: List[int], sample_size: int) -> List[Tuple[int, int]]:
        """
        Randomly sample user pairs for approximation.
        
        Args:
            all_users: List of all user IDs
            sample_size: Number of pairs to sample
            
        Returns:
            List of sampled user pairs
        """
        import random
        pairs = []
        n_users = len(all_users)
        
        # Generate all possible pairs
        all_pairs = [(all_users[i], all_users[j]) 
                     for i in range(n_users) 
                     for j in range(i+1, n_users)]
        
        # Sample randomly
        if sample_size >= len(all_pairs):
            return all_pairs
        else:
            return random.sample(all_pairs, sample_size)
    
    @staticmethod
    def _calculate_flow_centrality_optimized(user_id: int, users: Dict[int, User],
                                           distances: Dict[Tuple[int, int], int],
                                           sampled_pairs: List[Tuple[int, int]]) -> float:
        """
        Calculate approximate flow centrality using pre-computed distances.
        
        Args:
            user_id: ID of the user to calculate centrality for
            users: Dictionary of all users in the network
            distances: Pre-computed all-pairs shortest distances
            sampled_pairs: List of sampled user pairs
            
        Returns:
            Approximate flow centrality score
        """
        centrality = 0.0
        
        for user1, user2 in sampled_pairs:
            if user1 != user_id and user2 != user_id:
                # Check if user_id is on the shortest path between user1 and user2
                if NetworkAnalyzer._is_on_shortest_path_optimized(
                    user1, user2, user_id, users, distances
                ):
                    centrality += 1.0
        
        # Scale up the result based on sampling ratio
        total_pairs = len(users) * (len(users) - 1) / 2
        sample_ratio = len(sampled_pairs) / total_pairs
        return centrality / sample_ratio if sample_ratio > 0 else 0.0
    
    @staticmethod
    def _is_on_shortest_path_optimized(start: int, end: int, intermediate: int,
                                      users: Dict[int, User],
                                      distances: Dict[Tuple[int, int], int]) -> bool:
        """
        Check if intermediate user is on the shortest path using pre-computed distances.
        
        Args:
            start: Starting user ID
            end: Ending user ID
            intermediate: User ID to check if on path
            users: Dictionary of all users in the network
            distances: Pre-computed all-pairs shortest distances
            
        Returns:
            True if intermediate is on shortest path, False otherwise
        """
        # If no path exists, intermediate can't be on it
        if distances[(start, end)] == float('inf'):
            return False
        
        # Check if intermediate is on the shortest path
        # A node v is on the shortest path from s to t if:
        # dist(s, v) + dist(v, t) == dist(s, t)
        return (distances[(start, intermediate)] + 
                distances[(intermediate, end)] == 
                distances[(start, end)])

    @staticmethod
    def _calculate_flow_centrality(user_id: int, users: Dict[int, User]) -> float:
        """
        Calculate flow centrality for a specific user.
        
        This is a simplified version that counts how many user pairs
        have their shortest path go through the given user.
        
        Args:
            user_id: ID of the user to calculate centrality for
            users: Dictionary of all users in the network
            
        Returns:
            Flow centrality score
        """
        if user_id not in users:
            return 0.0
        
        centrality = 0.0
        all_users = list(users.keys())
        
        # Count pairs where this user is on the shortest path
        for i, user1 in enumerate(all_users):
            for user2 in all_users[i+1:]:
                if user1 != user_id and user2 != user_id:
                    # Check if user_id is on the shortest path between user1 and user2
                    if NetworkAnalyzer._is_on_shortest_path(user1, user2, user_id, users):
                        centrality += 1.0
        
        return centrality
    
    @staticmethod
    def _is_on_shortest_path(start: int, end: int, intermediate: int, 
                            users: Dict[int, User]) -> bool:
        """
        Check if intermediate user is on the shortest path between start and end.
        
        Args:
            start: Starting user ID
            end: Ending user ID
            intermediate: User ID to check if on path
            users: Dictionary of all users in the network
            
        Returns:
            True if intermediate is on shortest path, False otherwise
        """
        # Simple BFS to find shortest path
        if start not in users or end not in users:
            return False
        
        visited = set()
        queue = deque([(start, [start])])
        
        while queue:
            current, path = queue.popleft()
            if current in visited:
                continue
                
            visited.add(current)
            
            if current == end:
                # Found path, check if intermediate is on it
                return intermediate in path
            
            # Add all referred users to queue
            current_user = users[current]
            for referred_id in current_user.get_referrals():
                if referred_id not in visited:
                    new_path = path + [referred_id]
                    queue.append((referred_id, new_path))
        
        return False
