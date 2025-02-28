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

def get_position_name(total_players, player_position):
    """Get the poker position name based on total players and position."""
    if player_position == 1:
        return "small_blind"
    elif player_position == 2:
        return "big_blind"
    elif total_players == 9:
        positions = {
            3: "under_the_gun",
            4: "under_the_gun_plus_1",
            5: "under_the_gun_plus_2",
            6: "middle_position_1",
            7: "hijack",
            8: "cutoff",
            9: "button"
        }
        return positions.get(player_position, "unknown")
    elif total_players == 8:
        positions = {
            3: "under_the_gun",
            4: "under_the_gun_plus_1",
            5: "middle_position_1",
            6: "hijack",
            7: "cutoff",
            8: "button"
        }
        return positions.get(player_position, "unknown")
    elif total_players == 7:
        positions = {
            3: "under_the_gun",
            4: "middle_position_1",
            5: "hijack",
            6: "cutoff",
            7: "button"
        }
        return positions.get(player_position, "unknown")
    elif total_players == 6:
        positions = {
            3: "under_the_gun",
            4: "middle_position",
            5: "cutoff",
            6: "button"
        }
        return positions.get(player_position, "unknown")
    elif total_players == 5:
        positions = {
            3: "under_the_gun",
            4: "cutoff",
            5: "button"
        }
        return positions.get(player_position, "unknown")
    elif total_players == 4:
        positions = {
            3: "cutoff",
            4: "button"
        }
        return positions.get(player_position, "unknown")
    elif total_players == 3:
        positions = {
            3: "button"
        }
        return positions.get(player_position, "unknown")
    return "unknown"

def get_betting_recommendation(hand_type, hand_strength, pot_odds, position, is_blind=False):
    """Get betting recommendation based on hand strength and other factors."""
    if position == "small_blind":
        if hand_strength >= 0.8:  # Very strong hand
            return "Raise", "You have a very strong hand in the small blind. Consider raising 4-5x the big blind."
        elif hand_strength >= 0.6:  # Strong hand
            return "Call/Raise", "You have a strong hand. Consider completing the blind or raising 3x the big blind."
        elif hand_strength >= 0.4:  # Medium hand
            if pot_odds > hand_strength:
                return "Fold", "Your hand is marginal and the pot odds aren't favorable. Consider folding to a raise."
            return "Call", "Your hand has potential. Consider completing the blind if no raises."
        else:  # Weak hand
            return "Fold", "Your hand is weak. It's best to fold unless you can see a free flop."
    
    elif position == "big_blind":
        if hand_strength >= 0.8:  # Very strong hand
            return "Raise", "You have a very strong hand in the big blind. Consider raising 3-4x if there's action."
        elif hand_strength >= 0.6:  # Strong hand
            return "Call/Raise", "You have a strong hand. Consider raising if there's one limper, call if raised."
        elif hand_strength >= 0.4:  # Medium hand
            if pot_odds > hand_strength:
                return "Check/Fold", "Your hand is marginal. Check if no raise, fold to significant action."
            return "Check/Call", "Your hand has potential. Check if possible, call small raises."
        else:  # Weak hand
            return "Check/Fold", "Your hand is weak. Check if possible, fold to any raise."
    
    elif position == "under_the_gun":
        if hand_strength >= 0.8:  # Very strong hand
            return "Raise", "You have a very strong hand in early position. Open with 3x the big blind."
        elif hand_strength >= 0.65:  # Strong hand
            return "Raise", "You have a strong hand. Consider opening with 2.5x the big blind."
        else:  # Medium or weak hand
            return "Fold", "Your hand isn't strong enough to open from under the gun."
    
    elif position in ["middle_position", "cutoff"]:
        if hand_strength >= 0.8:  # Very strong hand
            return "Raise", "You have a very strong hand. Open with 2.5-3x the big blind."
        elif hand_strength >= 0.5:  # Strong to medium hand
            return "Raise", "You have a playable hand in middle/cutoff. Consider raising 2.5x the big blind."
        else:  # Weak hand
            return "Fold", "Your hand is too weak for this position. Wait for a better spot."
    
    elif position == "button":
        if hand_strength >= 0.8:  # Very strong hand
            return "Raise", "You have a very strong hand on the button. Raise 2.5-3x the big blind."
        elif hand_strength >= 0.4:  # Medium to strong hand
            return "Raise", "You have a playable hand on the button. Consider stealing with 2-2.5x the big blind."
        else:  # Weak hand
            if pot_odds < 0.2:  # If it's cheap to see a flop
                return "Call", "Consider calling if everyone limped, otherwise fold."
            return "Fold", "Your hand is weak. It's best to wait for a better opportunity."
    
    else:  # Unknown position
        if hand_strength >= 0.8:
            return "Raise", "You have a very strong hand. Consider raising 3x the big blind."
        elif hand_strength >= 0.6:
            return "Call", "You have a strong hand. Consider calling or raising if there's minimal action."
        else:
            return "Fold", "Your hand isn't strong enough to play out of position."

def main():
    print("Welcome to Texas Hold'em Poker Assistant!")
    print("This program will help you make decisions during your poker game.")
    print("\nAt any point, enter 'q' to quit.")
    
    simulator = PokerSimulator()
    
    while True:
        simulator.reset_game()
        print("\n=== New Hand ===")
        
        # Get total players and position
        while True:
            try:
                total_players = int(input("Total number of players (3-9): "))
                if 3 <= total_players <= 9:
                    break
                print("Please enter a number between 3 and 9")
            except ValueError:
                print("Please enter a valid number")
        
        while True:
            try:
                player_position = int(input(f"Your position (1-{total_players}, 1=small blind): "))
                if 1 <= player_position <= total_players:
                    break
                print(f"Please enter a number between 1 and {total_players}")
            except ValueError:
                print("Please enter a valid number")
        
        position = get_position_name(total_players, player_position)
        simulator.position = position
        print(f"Your position: {position.replace('_', ' ').title()}")
        
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
        simulator.num_opponents = total_players - 1
        simulator.pot_size = get_valid_number_input("Current pot size: ", 0)
        simulator.player_stack = get_valid_number_input("Your stack size: ", 0)
        
        # Calculate preflop hand strength
        hand_type, hand_strength = simulator.calculate_preflop_strength()
        print(f"\nHand Analysis:")
        print(f"Hand Type: {hand_type}")
        print(f"Hand Strength: {hand_strength:.2%}")
        
        # Get opponent actions
        total_bets = 0
        for i in range(1, total_players):
            relative_pos = (player_position + i) % total_players
            if relative_pos == 0:
                relative_pos = total_players
            pos_name = get_position_name(total_players, relative_pos).replace('_', ' ').title()
            bet = get_valid_number_input(f"{pos_name} bet amount (0 for check/fold): ", 0)
            simulator.opponent_bets.append(bet)
            total_bets += bet
        
        # Calculate pot odds if there are bets
        pot_odds = 0
        if total_bets > 0:
            pot_odds = total_bets / (simulator.pot_size + total_bets)
        
        # Get betting recommendation
        is_blind = position in ["small_blind", "big_blind"]
        action, reason = get_betting_recommendation(hand_type, hand_strength, pot_odds, position, is_blind)
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