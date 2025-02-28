#!/usr/bin/env python3

import random
import itertools
from collections import Counter

class Card:
    """Represents a playing card with rank and suit."""
    RANKS = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    SUITS = {'h': 'hearts', 'd': 'diamonds', 'c': 'clubs', 's': 'spades'}
    
    def __init__(self, card_str):
        """Initialize a card from a 2-character string like 'Ah' for Ace of hearts."""
        if len(card_str) != 2:
            raise ValueError(f"Invalid card format: {card_str}. Use format like 'Ah' for Ace of hearts.")
        
        rank, suit = card_str[0].upper(), card_str[1].lower()
        
        if rank not in self.RANKS:
            raise ValueError(f"Invalid rank: {rank}. Valid ranks are: {', '.join(self.RANKS.keys())}")
        if suit not in self.SUITS:
            raise ValueError(f"Invalid suit: {suit}. Valid suits are: {', '.join(self.SUITS.keys())}")
            
        self.rank = rank
        self.rank_value = self.RANKS[rank]
        self.suit = suit
        self.suit_name = self.SUITS[suit]
    
    def __str__(self):
        return f"{self.rank}{self.suit}"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit
    
    def __hash__(self):
        return hash((self.rank, self.suit))

class Deck:
    """Represents a deck of 52 playing cards."""
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset the deck to a full 52-card deck."""
        self.cards = [Card(r + s) for r in Card.RANKS.keys() for s in Card.SUITS.keys()]
        self.dealt_cards = []
    
    def shuffle(self):
        """Shuffle the remaining cards in the deck."""
        random.shuffle(self.cards)
    
    def deal(self, n=1):
        """Deal n cards from the deck."""
        if n > len(self.cards):
            raise ValueError(f"Cannot deal {n} cards. Only {len(self.cards)} cards left in deck.")
        
        dealt = []
        for _ in range(n):
            card = self.cards.pop()
            self.dealt_cards.append(card)
            dealt.append(card)
        
        return dealt if n > 1 else dealt[0]
    
    def remove_cards(self, cards):
        """Remove specific cards from the deck."""
        for card in cards:
            if isinstance(card, str):
                card = Card(card)
            if card in self.cards:
                self.cards.remove(card)
                self.dealt_cards.append(card)
            else:
                raise ValueError(f"Card {card} is not in the deck.")

class HandEvaluator:
    """Evaluates poker hands and calculates hand strength."""
    # Hand rankings from highest to lowest
    HAND_RANKINGS = {
        'straight_flush': 8,
        'four_of_a_kind': 7,
        'full_house': 6,
        'flush': 5,
        'straight': 4,
        'three_of_a_kind': 3,
        'two_pair': 2,
        'pair': 1,
        'high_card': 0
    }
    
    @staticmethod
    def evaluate_hand(cards):
        """Evaluate a poker hand (5-7 cards) and return the hand type and relevant cards."""
        if len(cards) < 5:
            raise ValueError("Need at least 5 cards to evaluate a poker hand.")
        
        # Find the best 5-card hand if more than 5 cards are provided
        if len(cards) > 5:
            return HandEvaluator._find_best_hand(cards)
        
        # Sort cards by rank value (high to low)
        sorted_cards = sorted(cards, key=lambda card: card.rank_value, reverse=True)
        
        # Check for each hand type from highest to lowest
        # Straight flush
        flush_cards = HandEvaluator._check_flush(sorted_cards)
        straight_cards = HandEvaluator._check_straight(sorted_cards)
        if flush_cards and straight_cards:
            # Check if the same 5 cards form both a flush and a straight
            straight_flush_cards = [card for card in straight_cards if card in flush_cards]
            if len(straight_flush_cards) >= 5:
                return {'type': 'straight_flush', 'cards': straight_cards, 'rank': 8}
        
        # Four of a kind
        four_kind = HandEvaluator._check_n_of_a_kind(sorted_cards, 4)
        if four_kind:
            kickers = [card for card in sorted_cards if card.rank != four_kind[0].rank][:1]
            return {'type': 'four_of_a_kind', 'cards': four_kind + kickers, 'rank': 7}
        
        # Full house
        three_kind = HandEvaluator._check_n_of_a_kind(sorted_cards, 3)
        if three_kind:
            pair = HandEvaluator._check_n_of_a_kind([c for c in sorted_cards if c.rank != three_kind[0].rank], 2)
            if pair:
                return {'type': 'full_house', 'cards': three_kind + pair, 'rank': 6}
        
        # Flush
        if flush_cards:
            return {'type': 'flush', 'cards': flush_cards[:5], 'rank': 5}
        
        # Straight
        if straight_cards:
            return {'type': 'straight', 'cards': straight_cards, 'rank': 4}
        
        # Three of a kind
        if three_kind:
            kickers = [card for card in sorted_cards if card.rank != three_kind[0].rank][:2]
            return {'type': 'three_of_a_kind', 'cards': three_kind + kickers, 'rank': 3}
        
        # Two pair
        pairs = HandEvaluator._check_pairs(sorted_cards)
        if len(pairs) >= 2:
            kickers = [card for card in sorted_cards if card.rank != pairs[0][0].rank and card.rank != pairs[1][0].rank][:1]
            return {'type': 'two_pair', 'cards': pairs[0] + pairs[1] + kickers, 'rank': 2}
        
        # Pair
        if pairs:
            kickers = [card for card in sorted_cards if card.rank != pairs[0][0].rank][:3]
            return {'type': 'pair', 'cards': pairs[0] + kickers, 'rank': 1}
        
        # High card
        return {'type': 'high_card', 'cards': sorted_cards[:5], 'rank': 0}
    
    @staticmethod
    def _find_best_hand(cards):
        """Find the best 5-card hand from a set of 6 or 7 cards."""
        best_hand = None
        best_score = -1
        
        for hand_combo in itertools.combinations(cards, 5):
            hand_result = HandEvaluator.evaluate_hand(list(hand_combo))
            hand_score = hand_result['rank']
            
            # If this hand is better than our current best, update
            if hand_score > best_score:
                best_hand = hand_result
                best_score = hand_score
            elif hand_score == best_score:
                # If same hand type, compare the cards
                current_cards = hand_result['cards']
                best_cards = best_hand['cards']
                
                # Compare cards by rank value
                for i in range(len(current_cards)):
                    if current_cards[i].rank_value > best_cards[i].rank_value:
                        best_hand = hand_result
                        break
                    elif current_cards[i].rank_value < best_cards[i].rank_value:
                        break
        
        return best_hand
    
    @staticmethod
    def _check_flush(cards):
        """Check if the cards contain a flush."""
        suits = Counter(card.suit for card in cards)
        flush_suit = next((suit for suit, count in suits.items() if count >= 5), None)
        
        if flush_suit:
            flush_cards = [card for card in cards if card.suit == flush_suit]
            return flush_cards[:5]  # Return the 5 highest cards of the flush
        return None
    
    @staticmethod
    def _check_straight(cards):
        """Check if the cards contain a straight."""
        # Remove duplicate ranks
        unique_ranks = []
        seen_ranks = set()
        
        for card in cards:
            if card.rank not in seen_ranks:
                unique_ranks.append(card)
                seen_ranks.add(card.rank)
        
        # Sort by rank value
        unique_ranks.sort(key=lambda card: card.rank_value, reverse=True)
        
        # Check for A-5-4-3-2 straight
        if len(unique_ranks) >= 5:
            if (unique_ranks[0].rank == 'A' and 
                any(c.rank == '5' for c in unique_ranks) and
                any(c.rank == '4' for c in unique_ranks) and
                any(c.rank == '3' for c in unique_ranks) and
                any(c.rank == '2' for c in unique_ranks)):
                # Find the actual cards for the A-5-4-3-2 straight
                ace = next(c for c in unique_ranks if c.rank == 'A')
                five = next(c for c in unique_ranks if c.rank == '5')
                four = next(c for c in unique_ranks if c.rank == '4')
                three = next(c for c in unique_ranks if c.rank == '3')
                two = next(c for c in unique_ranks if c.rank == '2')
                return [five, four, three, two, ace]  # Ace is low in this case
        
        # Check for regular straights
        for i in range(len(unique_ranks) - 4):
            if (unique_ranks[i].rank_value - unique_ranks[i+4].rank_value == 4):
                return unique_ranks[i:i+5]
        
        return None
    
    @staticmethod
    def _check_n_of_a_kind(cards, n):
        """Check if the cards contain n of a kind."""
        rank_counts = Counter(card.rank for card in cards)
        for rank, count in rank_counts.items():
            if count >= n:
                # Get the n cards of the same rank
                return [card for card in cards if card.rank == rank][:n]
        return None
    
    @staticmethod
    def _check_pairs(cards):
        """Find all pairs in the cards and return them sorted by rank."""
        pairs = []
        rank_counts = Counter(card.rank for card in cards)
        
        for rank, count in rank_counts.items():
            if count >= 2:
                pair_cards = [card for card in cards if card.rank == rank][:2]
                pairs.append(pair_cards)
        
        # Sort pairs by rank value (highest first)
        pairs.sort(key=lambda pair: pair[0].rank_value, reverse=True)
        return pairs

class PokerSimulator:
    """Simulates Texas Hold'em poker hands and calculates win probabilities."""
    def __init__(self):
        self.deck = Deck()
        self.evaluator = HandEvaluator()
        self.community_cards = []
        self.hole_cards = []
        self.num_opponents = 0
        self.pot_size = 0
        self.player_stack = 0
        self.opponent_bets = []
        self.position = 'early'  # early, middle, late, or button
        self.stage = 'preflop'  # preflop, flop, turn, river
    
    def reset_game(self):
        """Reset the game state."""
        self.deck.reset()
        self.deck.shuffle()
        self.community_cards = []
        self.hole_cards = []
        self.opponent_bets = []
        self.stage = 'preflop'
    
    def set_hole_cards(self, cards):
        """Set the player's hole cards."""
        if isinstance(cards[0], str):
            self.hole_cards = [Card(c) for c in cards]
        else:
            self.hole_cards = cards
        # Remove these cards from the deck
        self.deck.remove_cards(self.hole_cards)
    
    def set_community_cards(self, cards):
        """Set the community cards."""
        if isinstance(cards[0], str):
            self.community_cards = [Card(c) for c in cards]
        else:
            self.community_cards = cards
        # Remove these cards from the deck
        self.deck.remove_cards(self.community_cards)
        
        # Update the game stage based on the number of community cards
        if len(self.community_cards) == 3:
            self.stage = 'flop'
        elif len(self.community_cards) == 4:
            self.stage = 'turn'
        elif len(self.community_cards) == 5:
            self.stage = 'river'
    
    def calculate_preflop_strength(self, hole_cards=None):
        """Calculate the strength of hole cards before the flop."""
        if hole_cards is None:
            hole_cards = self.hole_cards
        
        # Convert string cards to Card objects if needed
        if isinstance(hole_cards[0], str):
            hole_cards = [Card(c) for c in hole_cards]
        
        # Basic hand strength categories
        # Pairs
        if hole_cards[0].rank == hole_cards[1].rank:
            rank_value = hole_cards[0].rank_value
            if rank_value >= 10:  # JJ, QQ, KK, AA
                return 'premium_pair', 0.85
            elif rank_value >= 7:  # 77, 88, 99, TT
                return 'medium_pair', 0.7
            else:  # 22, 33, 44, 55, 66
                return 'small_pair', 0.55
        
        # Suited cards
        suited = hole_cards[0].suit == hole_cards[1].suit
        
        # Sort by rank value
        sorted_cards = sorted(hole_cards, key=lambda card: card.rank_value, reverse=True)
        high_card, low_card = sorted_cards[0], sorted_cards[1]
        
        # Check for Broadway cards (T, J, Q, K, A)
        broadway = high_card.rank_value >= 10 and low_card.rank_value >= 10
        
        # Check for connected cards (consecutive ranks)
        connected = high_card.rank_value - low_card.rank_value == 1
        one_gap = high_card.rank_value - low_card.rank_value == 2
        
        # Categorize hand
        if broadway and suited:
            return 'suited_broadway', 0.8
        elif broadway:
            return 'broadway', 0.7
        elif suited and connected:
            return 'suited_connector', 0.65
        elif connected and high_card.rank_value >= 10:
            return 'high_connector', 0.6
        elif suited and high_card.rank == 'A':
            return 'ace_suited', 0.65
        elif suited and one_gap:
            return 'suited_one_gapper', 0.55
        elif connected:
            return 'connector', 0.5
        elif suited:
            return 'suited', 0.45
        elif high_card.rank == 'A':
            return 'ace_high', 0.4
        else:
            return 'unconnected', 0.3