"""
Example adoption probability functions for the Referral Network System.

This module provides example functions that model how referral bonuses
affect the probability of successful referrals.
"""

from typing import Callable


def example_adoption_prob(bonus: int) -> float:
    """
    Example adoption probability function.
    
    This function models the relationship between referral bonus amount
    and the probability of a successful referral. It demonstrates a
    realistic scenario where higher bonuses increase adoption probability
    but with diminishing returns.
    
    Args:
        bonus: The referral bonus amount in dollars
        
    Returns:
        Probability of successful referral (0.0 to 1.0)
    """
    if bonus <= 0:
        return 0.0
    
    # Base probability increases with bonus, but with diminishing returns
    # Formula: 0.1 + 0.9 * (1 - e^(-bonus/100))
    import math
    base_prob = 0.1
    max_increase = 0.9
    sensitivity = 100.0
    
    probability = base_prob + max_increase * (1 - math.exp(-bonus / sensitivity))
    
    # Ensure probability is between 0 and 1
    return max(0.0, min(1.0, probability))


def create_test_adoption_prob(base_prob: float = 0.5, sensitivity: float = 100.0) -> Callable[[int], float]:
    """
    Create a customizable adoption probability function for testing.
    
    Args:
        base_prob: Base probability when bonus is 0 (should be 0.0)
        sensitivity: How quickly probability increases with bonus (higher = slower increase)
        
    Returns:
        A callable function that takes bonus and returns probability
    """
    def adoption_prob(bonus: int) -> float:
        if bonus <= 0:
            return base_prob
        
        import math
        max_increase = 1.0 - base_prob
        probability = base_prob + max_increase * (1 - math.exp(-bonus / sensitivity))
        return max(0.0, min(1.0, probability))
    
    return adoption_prob
