"""
Network Growth Simulation and Bonus Optimization

This module implements the network growth simulation (Part 4) and referral bonus
optimization (Part 5) for the Mercor Challenge.
"""

from typing import List, Callable, Optional
import math


class SimulationConfig:
    """Configuration for network growth simulation."""
    
    def __init__(self, 
                 initial_referrers: int = 100,
                 referral_capacity: int = 10,
                 max_bonus: int = 1000,
                 bonus_increment: int = 10):
        """
        Initialize simulation configuration.
        
        Args:
            initial_referrers: Number of active referrers at start
            referral_capacity: Maximum referrals per referrer
            max_bonus: Maximum bonus amount to search
            bonus_increment: Bonus rounding increment
        """
        self.initial_referrers = initial_referrers
        self.referral_capacity = referral_capacity
        self.max_bonus = max_bonus
        self.bonus_increment = bonus_increment


# Default configuration
DEFAULT_CONFIG = SimulationConfig()


def simulate(p: float, days: int) -> List[float]:
    """
    Simulate network growth over time and return cumulative expected referrals.
    
    Model Parameters:
    - Initial referrers: 100 active referrers
    - Referral capacity: Each referrer can make up to 10 successful referrals
    - Time unit: Discrete steps called days
    
    Args:
        p: Probability that an active user will successfully refer someone on any given day
        days: Number of days to simulate
        
    Returns:
        List where element at index i is the cumulative total expected referrals at end of day i
    """
    INITIAL_REFERRERS = 100
    REFERRAL_CAPACITY = 10
    
    # Track active referrers and their remaining capacity
    active_referrers = INITIAL_REFERRERS
    referrer_capacities = [REFERRAL_CAPACITY] * INITIAL_REFERRERS
    
    cumulative_referrals = []
    total_referrals = 0.0
    
    for day in range(days):
        daily_referrals = 0.0
        
        # Each active referrer has probability p of making a successful referral
        for i in range(active_referrers):
            if referrer_capacities[i] > 0:
                # Expected value: p referrals per day
                daily_referrals += p
                referrer_capacities[i] -= p
                
                # If capacity is exhausted, mark as inactive
                if referrer_capacities[i] <= 0:
                    active_referrers -= 1
        
        total_referrals += daily_referrals
        cumulative_referrals.append(total_referrals)
        
        # Early termination if no active referrers remain
        if active_referrers <= 0:
            # Pad remaining days with the same total
            while len(cumulative_referrals) < days:
                cumulative_referrals.append(total_referrals)
            break
    
    return cumulative_referrals


def simulate_network_growth(
    initial_users: int,
    target_users: int,
    adoption_prob: Callable[[int], float],
    max_days: int
) -> dict:
    """
    Simulate network growth from initial users to target users.
    
    Args:
        initial_users: Starting number of users in the network
        target_users: Target number of users to reach
        adoption_prob: Function that returns adoption probability for current user count
        max_days: Maximum number of days to simulate
        
    Returns:
        Dictionary with keys:
        - success: Boolean indicating if target was reached
        - days_taken: Number of days taken (or max_days if not reached)
        - final_users: Final number of users in the network
    """
    if initial_users <= 0 or max_days <= 0:
        raise ValueError("initial_users and max_days must be positive")
    
    if target_users <= 0:
        raise ValueError("target_users must be positive")
    
    if target_users <= initial_users:
        raise ValueError("target_users must be greater than initial_users")
    
    if initial_users >= target_users:
        return {
            'success': True,
            'days_taken': 0,
            'final_users': initial_users
        }
    
    # Each user has a referral capacity (like in the original simulate function)
    REFERRAL_CAPACITY = 10
    
    current_users = initial_users
    days_taken = 0
    
    # Track remaining referral capacity for each user
    user_capacities = [REFERRAL_CAPACITY] * initial_users
    
    for day in range(max_days):
        # Get adoption probability for current user count
        try:
            prob = adoption_prob(current_users)
        except:
            # If adoption_prob function fails, use a default
            prob = 0.1
        
        # Validate probability
        if prob < 0 or prob > 1:
            raise ValueError(f"Adoption probability must be between 0 and 1, got {prob}")
        
        # Calculate new users for this day based on remaining capacity
        new_users = 0
        active_users = 0
        
        for i in range(len(user_capacities)):
            if user_capacities[i] > 0:
                active_users += 1
                # Each active user has probability prob of making a successful referral
                if prob > 0:
                    # Expected value: prob referrals per day
                    daily_referrals = prob
                    user_capacities[i] -= daily_referrals
                    
                    # If capacity is exhausted, mark as inactive
                    if user_capacities[i] <= 0:
                        user_capacities[i] = 0
                    
                    new_users += daily_referrals
        
        # Round to nearest integer for realistic simulation
        new_users = round(new_users)
        current_users += new_users
        
        days_taken = day + 1
        
        # Check if target reached
        if current_users >= target_users:
            return {
                'success': True,
                'days_taken': days_taken,
                'final_users': current_users
            }
        
        # Early termination if no active users remain
        if active_users == 0:
            break
    
    # Target not reached within max_days or capacity exhausted
    return {
        'success': False,
        'days_taken': days_taken,
        'final_users': current_users
    }


def days_to_target(
    initial_users: int,
    target_users: int,
    adoption_prob: Callable[[int], float]
) -> Optional[int]:
    """
    Calculate the minimum number of days required to reach a target number of users.
    
    Args:
        initial_users: Starting number of users in the network
        target_users: Target number of users to reach
        adoption_prob: Function that returns adoption probability for current user count
        
    Returns:
        Minimum number of days required to reach the target, or None if target is unachievable
    """
    if initial_users <= 0 or target_users <= 0:
        raise ValueError("initial_users and target_users must be positive")
    
    if target_users <= initial_users:
        raise ValueError("target_users must be greater than initial_users")
    
    if initial_users >= target_users:
        return 0
    
    # Use simulation to find the answer
    # Start with a reasonable upper bound
    max_days = 1000
    result = simulate_network_growth(initial_users, target_users, adoption_prob, max_days)
    
    if result['success']:
        return result['days_taken']
    else:
        return None


def min_bonus_for_target(
    days: int, 
    target_hires: int, 
    adoption_prob: Callable[[int], float], 
    eps: float = 1e-3
) -> Optional[float]:
    """
    Find the minimum bonus amount required to achieve a hiring target.
    
    This function efficiently searches for the minimum bonus using binary search,
    leveraging the monotonic nature of the adoption probability function.
    
    Args:
        days: Number of days available for hiring
        target_hires: Target number of hires to achieve
        adoption_prob: Function that returns adoption probability for a given bonus amount
        eps: Precision for probability comparison (default: 1e-3)
        
    Returns:
        Minimum bonus amount (rounded UP to nearest $10) required to achieve target,
        or None if target is unachievable with any finite bonus
        
    Time Complexity: O(log B * D) where:
    - B is the range of bonus values to search (typically 1000)
    - D is the number of days (for simulation)
    
    The binary search over bonus space takes O(log B) iterations, and each iteration
    requires running the simulation which takes O(D) time. Therefore, the total time
    complexity is O(log B * D).
    """
    # Handle edge cases
    if days <= 0 or target_hires <= 0:
        return None
    
    # Binary search over bonus amounts
    # Start with reasonable bounds: $0 to $1000
    left_bonus = 0
    right_bonus = 1000
    
    # Check if target is achievable with maximum bonus
    max_prob = adoption_prob(right_bonus)
    if max_prob > 0:
        max_simulation = simulate(max_prob, days)
        if max_simulation[-1] < target_hires:
            return None  # Target unachievable
    
    # Binary search for minimum bonus
    while left_bonus < right_bonus:
        mid_bonus = (left_bonus + right_bonus) // 2
        
        # Get adoption probability for this bonus
        prob = adoption_prob(mid_bonus)
        
        # Simulate with this probability
        simulation_result = simulate(prob, days)
        total_referrals = simulation_result[-1]
        
        if total_referrals >= target_hires:
            # This bonus works, try to find a smaller one
            right_bonus = mid_bonus
        else:
            # This bonus is too low
            left_bonus = mid_bonus + 1
    
    # Find the exact minimum bonus that works
    # Start from left_bonus and check each $10 increment
    for bonus in range(left_bonus, left_bonus + 20, 10):
        prob = adoption_prob(bonus)
        simulation_result = simulate(prob, days)
        if simulation_result[-1] >= target_hires:
            min_bonus = bonus
            break
    else:
        # If no bonus found in range, use the calculated value
        min_bonus = math.ceil(left_bonus / 10) * 10
    
    # Ensure we never return 0 as a valid bonus (since it gives 0 probability)
    if min_bonus == 0:
        min_bonus = 10
    
    # Verify the result
    final_prob = adoption_prob(min_bonus)
    final_simulation = simulate(final_prob, days)
    
    if final_simulation[-1] >= target_hires:
        return float(min_bonus)
    else:
        # This shouldn't happen with proper binary search, but safety check
        return None
