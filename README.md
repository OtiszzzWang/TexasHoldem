# Texas Hold'em Poker Assistant

A web-based tool that helps poker players make better decisions during Texas Hold'em games by analyzing hand strength and providing strategic recommendations.

## Overview

The Texas Hold'em Poker Assistant is designed to help both novice and experienced poker players improve their decision-making during games. It analyzes your hole cards and the community cards at different stages of the game (preflop, flop, turn, and river) and provides recommendations based on hand strength, position, and pot odds.

## Features

- Visual poker table interface with card representation
- Hand strength calculation and analysis
- Position-based betting recommendations
- Game stage progression (preflop → flop → turn → river)
- Consideration of pot odds and opponent actions
- Real-time advice tailored to your specific game situation

## Installation

1. Clone this repository to your local machine:
   ```
   git clone https://github.com/yourusername/TexasHoldem.git
   cd TexasHoldem
   ```

2. No additional installation is required as this is a browser-based application.

## Usage

1. Open `index.html` in your web browser.

2. **Preflop Stage:**
   - Select your two hole cards using the rank and suit dropdowns
   - Enter the number of opponents you're playing against
   - Input the current pot size and your stack size
   - Select your position at the table (early, middle, late, or button)
   - Click "Analyze Preflop Hand" to get your recommendation

3. **Flop Stage:**
   - After analyzing your preflop hand, click "Continue to Flop"
   - Select the three community cards that appeared on the flop
   - Click "Analyze Flop" to get updated recommendations

4. **Turn and River Stages:**
   - Continue through the hand as community cards are revealed
   - Get updated recommendations at each stage

5. **Start a New Hand:**
   - Click "New Hand" at any point to reset and start over

## Understanding the Results

### Hand Types

The assistant categorizes your starting hand into various types:

- **Premium Pairs**: JJ, QQ, KK, AA
- **Medium Pairs**: 77, 88, 99, TT
- **Small Pairs**: 22, 33, 44, 55, 66
- **Broadway Cards**: Any two cards 10 or higher (T, J, Q, K, A)
- **Suited Connectors**: Connected cards of the same suit
- **Suited Gappers**: Cards of the same suit with one rank gap
- **Offsuit Connectors**: Connected cards of different suits
- **High Cards**: Hands with at least one high card that don't fit other categories

### Hand Strength

Hand strength is displayed as a percentage, indicating how strong your hand is relative to all possible hands. The higher the percentage, the stronger your hand.

### Recommendations

The assistant provides one of the following recommendations based on your hand strength, position, and the game situation:

- **Raise**: Your hand is strong enough to raise
- **Call**: Your hand is worth calling a bet
- **Check/Fold**: Your hand is marginal; check if possible, fold to significant action
- **Fold**: Your hand is weak and should be folded

Each recommendation comes with a brief explanation of the reasoning behind it.

## Position-Based Strategy

The assistant takes your table position into account when making recommendations:

- **Early Position**: More conservative play is recommended
- **Middle Position**: Slightly more aggressive than early position
- **Late Position**: More aggressive play is possible
- **Button**: Most aggressive position, as you'll act last on all post-flop streets

## Limitations

- The assistant provides general strategic advice but cannot account for specific opponent tendencies or table dynamics
- The recommendations are based on mathematical probabilities and general poker strategy, not guaranteed winning moves
- The tool does not consider advanced concepts like range analysis or multi-street planning

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.