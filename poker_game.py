#!/usr/bin/env python3

from poker_assistant import Card, Deck, HandEvaluator, PokerSimulator

def get_valid_card_input(prompt):
    """Get valid card input from the user."""
    while True:
        try:
            card_str = input(prompt).strip()
            if card_str.lower() == 'q':
                return None
            Card(card_str)  # Validate the card format
            return card_str
        except ValueError as e:
            print(f"Error: {e}")
            print("Please use format like 'Ah' for Ace of hearts, or 'q' to quit.")

def get_valid_number_input(prompt, min_value=0):
    """Get valid number input from the user."""
    while True:
        try:
            value = float(input(prompt))
            if value >= min_value:
                return value
            print(f"Please enter a number >= {min_value}")
        except ValueError:
            print("Please enter a valid number")

def get_betting_recommendation(hand_type, hand_strength, pot_odds, position):
    """Get betting recommendation based on hand strength and other factors."""
    if hand_strength >= 0.8:  # Very strong hand
        return "Raise", "You have a very strong hand. Consider raising 3-4x the big blind."
    elif hand_strength >= 0.6:  # Strong hand
        if position in ['late', 'button']:
            return "Raise/Call", "You have a strong hand in late position. Consider raising 2-3x the big blind or calling."
        return "Call", "You have a strong hand. Consider calling or raising if there's minimal action before you."
    elif hand_strength >= 0.4:  # Medium hand
        if pot_odds > hand_strength:
            return "Fold", "Your hand is marginal and the pot odds aren't favorable. Consider folding."
        if position in ['late', 'button']:
            return "Call", "Your hand has potential in late position. Consider calling if the price is right."
        return "Check/Fold", "Your hand is marginal. Check if possible, fold to significant action."
    else:  # Weak hand
        return "Fold", "Your hand is weak. It's best to fold and wait for a better opportunity."

def main():
    print("Welcome to Texas Hold'em Poker Assistant!")
    print("This program will help you make decisions during your poker game.")
    print("\nAt any point, enter 'q' to quit.")
    
    simulator = PokerSimulator()
    
    while True:
        simulator.reset_game()
        print("\n=== New Hand ===")
        
        # Get hole cards
        print("\nEnter your hole cards:")
        card1 = get_valid_card_input("First card (e.g., 'Ah'): ")
        if card1 is None:
            break
        card2 = get_valid_card_input("Second card (e.g., 'Kh'): ")
        if card2 is None:
            break
        
        simulator.set_hole_cards([card1, card2])
        
        # Get game state information
        print("\nEnter game state information:")
        simulator.num_opponents = int(get_valid_number_input("Number of opponents (1-9): ", 1))
        simulator.pot_size = get_valid_number_input("Current pot size: ", 0)
        simulator.player_stack = get_valid_number_input("Your stack size: ", 0)
        
        # Get position
        while True:
            position = input("Your position (early/middle/late/button): ").lower()
            if position in ['early', 'middle', 'late', 'button']:
                simulator.position = position
                break
            print("Invalid position. Please choose from: early, middle, late, or button")
        
        # Calculate preflop hand strength
        hand_type, hand_strength = simulator.calculate_preflop_strength()
        print(f"\nHand Analysis:")
        print(f"Hand Type: {hand_type}")
        print(f"Hand Strength: {hand_strength:.2%}")
        
        # Get opponent actions
        total_bets = 0
        for i in range(simulator.num_opponents):
            bet = get_valid_number_input(f"Opponent {i+1} bet amount (0 for check/fold): ", 0)
            simulator.opponent_bets.append(bet)
            total_bets += bet
        
        # Calculate pot odds if there are bets
        pot_odds = 0
        if total_bets > 0:
            pot_odds = total_bets / (simulator.pot_size + total_bets)
        
        # Get betting recommendation
        action, reason = get_betting_recommendation(hand_type, hand_strength, pot_odds, simulator.position)
        print(f"\nRecommended Action: {action}")
        print(f"Reason: {reason}")
        
        if simulator.stage == 'preflop':
            print("\nWould you like to continue to the flop? (y/n)")
            if input().lower() != 'y':
                continue
            
            # Get flop cards
            print("\nEnter the flop cards:")
            flop1 = get_valid_card_input("First flop card: ")
            if flop1 is None:
                break
            flop2 = get_valid_card_input("Second flop card: ")
            if flop2 is None:
                break
            flop3 = get_valid_card_input("Third flop card: ")
            if flop3 is None:
                break
            
            simulator.set_community_cards([flop1, flop2, flop3])
            
            # Evaluate hand with flop
            current_hand = simulator.evaluator.evaluate_hand(simulator.hole_cards + simulator.community_cards)
            print(f"\nYour current hand: {current_hand['type']}")
            print("Cards: " + " ".join(str(card) for card in current_hand['cards']))
        
        print("\nWould you like to play another hand? (y/n)")
        if input().lower() != 'y':
            break
    
    print("\nThanks for using the Poker Assistant!")

if __name__ == '__main__':
    main()