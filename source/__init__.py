"""
Referral Network System

A comprehensive system for managing and analyzing referral networks.
"""

from .core.referral_network import ReferralNetwork
from .core.simulation import simulate, days_to_target, min_bonus_for_target
from .models.user import User
from .constraints.validator import ReferralValidator
from .algorithms.network_analysis import NetworkAnalyzer
from .algorithms.reach_expansion import ReachExpander
from .examples.adoption_functions import example_adoption_prob

__all__ = [
    'ReferralNetwork',
    'simulate',
    'days_to_target', 
    'min_bonus_for_target',
    'User', 
    'ReferralValidator',
    'NetworkAnalyzer',
    'ReachExpander',
    'example_adoption_prob'
]
