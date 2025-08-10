"""
Core business logic for the Referral Network System.

This module contains the main classes and functions that implement
the core referral network functionality as specified in the assignment.
"""

from .referral_network import ReferralNetwork
from .simulation import simulate, days_to_target, min_bonus_for_target

__all__ = [
    'ReferralNetwork',
    'simulate',
    'days_to_target', 
    'min_bonus_for_target'
]
