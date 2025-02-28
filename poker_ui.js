document.addEventListener('DOMContentLoaded', function() {
    // Card display elements
    const hole1 = document.getElementById('hole1');
    const hole2 = document.getElementById('hole2');
    const flop1 = document.getElementById('flop1');
    const flop2 = document.getElementById('flop2');
    const flop3 = document.getElementById('flop3');
    const turn = document.getElementById('turn');
    const river = document.getElementById('river');
    
    // Input elements
    const card1Rank = document.getElementById('card1-rank');
    const card1Suit = document.getElementById('card1-suit');
    const card2Rank = document.getElementById('card2-rank');
    const card2Suit = document.getElementById('card2-suit');
    const numOpponents = document.getElementById('num-opponents');
    const potSize = document.getElementById('pot-size');
    const playerStack = document.getElementById('player-stack');
    const position = document.getElementById('position');
    
    // Button elements
    const analyzeButton = document.getElementById('analyze-preflop');
    const continueToFlopButton = document.getElementById('continue-to-flop');
    const resetHandButton = document.getElementById('reset-hand');
    
    // Results elements
    const preflopResults = document.getElementById('preflop-results');
    const handTypeElement = document.getElementById('hand-type');
    const handStrengthElement = document.getElementById('hand-strength');
    const recommendationElement = document.getElementById('recommendation');
    const recommendationReasonElement = document.getElementById('recommendation-reason');
    const opponentBets = document.getElementById('opponent-bets');
    const opponentBetInputs = document.getElementById('opponent-bet-inputs');
    const flopInput = document.getElementById('flop-input');
    
    // Card suit symbols
    const suitSymbols = {
        'h': '♥',
        'd': '♦',
        'c': '♣',
        's': '♠'
    };
    
    // Card rank display (T becomes 10)
    const rankDisplay = {
        '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
        'T': '10', 'J': 'J', 'Q': 'Q', 'K': 'K', 'A': 'A'
    };
    
    // Function to update card display
    function updateCardDisplay(cardElement, rank, suit) {
        if (!rank || !suit) {
            cardElement.className = 'card empty';
            cardElement.innerHTML = '';
            return;
        }
        
        const suitName = suit === 'h' ? 'hearts' : 
                        suit === 'd' ? 'diamonds' : 
                        suit === 'c' ? 'clubs' : 'spades';
        
        cardElement.className = `card ${suitName}`;
        cardElement.innerHTML = `
            <div class="rank">${rankDisplay[rank]}</div>
            <div class="suit">${suitSymbols[suit]}</div>
            <div class="rank" style="transform: rotate(180deg);">${rankDisplay[rank]}</div>
        `;
    }
    
    // Function to calculate preflop hand strength
    function calculatePreflopStrength(card1, card2) {
        // Check for pairs
        if (card1.rank === card2.rank) {
            const rankValue = getRankValue(card1.rank);
            if (rankValue >= 10) { // JJ, QQ, KK, AA
                return { type: 'premium_pair', strength: 0.85 };
            } else if (rankValue >= 7) { // 77, 88, 99, TT
                return { type: 'medium_pair', strength: 0.7 };
            } else { // 22, 33, 44, 55, 66
                return { type: 'small_pair', strength: 0.55 };
            }
        }
        
        // Suited cards
        const suited = card1.suit === card2.suit;
        
        // Sort by rank value
        const card1Value = getRankValue(card1.rank);
        const card2Value = getRankValue(card2.rank);
        const highCard = card1Value > card2Value ? card1 : card2;
        const lowCard = card1Value > card2Value ? card2 : card1;
        const highValue = getRankValue(highCard.rank);
        const lowValue = getRankValue(lowCard.rank);
        
        // Check for Broadway cards (T, J, Q, K, A)
        const broadway = highValue >= 10 && lowValue >= 10;
        
        // Check for connected cards (consecutive ranks)
        const connected = highValue - lowValue === 1;
        const oneGap = highValue - lowValue === 2;
        
        // Categorize hand
        if (broadway && suited) {
            return { type: 'suited_broadway', strength: 0.8 };
        } else if (broadway) {
            return { type: 'broadway', strength: 0.7 };
        } else if (suited && connected) {
            return { type: 'suited_connector', strength: 0.65 };
        } else if (connected && highValue >= 10) {
            return { type: 'high_connector', strength: 0.6 };
        } else if (suited && highCard.rank === 'A') {
            return { type: 'ace_suited', strength: 0.65 };
        } else if (suited && oneGap) {
            return { type: 'suited_one_gapper', strength: 0.55 };
        } else if (connected) {
            return { type: 'connector', strength: 0.5 };
        } else if (suited) {
            return { type: 'suited', strength: 0.45 };
        } else if (highCard.rank === 'A') {
            return { type: 'ace_high', strength: 0.4 };
        } else {
            return { type: 'unconnected', strength: 0.3 };
        }
    }
    
    // Function to get rank value
    function getRankValue(rank) {
        const rankValues = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
            'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
        };
        return rankValues[rank];
    }
    
    // Function to get betting recommendation
    function getBettingRecommendation(handType, handStrength, potOdds, position) {
        if (position === "small_blind") {
            if (handStrength >= 0.8) { // Very strong hand
                return {
                    action: "Raise",
                    reason: "You have a very strong hand in the small blind. Consider raising 4-5x the big blind.",
                    class: "raise"
                };
            } else if (handStrength >= 0.6) { // Strong hand
                return {
                    action: "Call/Raise",
                    reason: "You have a strong hand. Consider completing the blind or raising 3x the big blind.",
                    class: "raise"
                };
            } else if (handStrength >= 0.4) { // Medium hand
                if (potOdds > handStrength) {
                    return {
                        action: "Fold",
                        reason: "Your hand is marginal and the pot odds aren't favorable. Consider folding to a raise.",
                        class: "fold"
                    };
                }
                return {
                    action: "Call",
                    reason: "Your hand has potential. Consider completing the blind if no raises.",
                    class: "call"
                };
            } else { // Weak hand
                return {
                    action: "Fold",
                    reason: "Your hand is weak. It's best to fold unless you can see a free flop.",
                    class: "fold"
                };
            }
        } else if (position === "big_blind") {
            if (handStrength >= 0.8) { // Very strong hand
                return {
                    action: "Raise",
                    reason: "You have a very strong hand in the big blind. Consider raising 3-4x if there's action.",
                    class: "raise"
                };
            } else if (handStrength >= 0.6) { // Strong hand
                return {
                    action: "Call/Raise",
                    reason: "You have a strong hand. Consider raising if there's one limper, call if raised.",
                    class: "raise"
                };
            } else if (handStrength >= 0.4) { // Medium hand
                if (potOdds > handStrength) {
                    return {
                        action: "Check/Fold",
                        reason: "Your hand is marginal. Check if no raise, fold to significant action.",
                        class: "fold"
                    };
                }
                return {
                    action: "Check/Call",
                    reason: "Your hand has potential. Check if possible, call small raises.",
                    class: "call"
                };
            } else { // Weak hand
                return {
                    action: "Check/Fold",
                    reason: "Your hand is weak. Check if possible, fold to any raise.",
                    class: "fold"
                };
            }
        } else if (position === "under_the_gun" || position.startsWith("under_the_gun_plus")) {
            if (handStrength >= 0.8) { // Very strong hand
                return {
                    action: "Raise",
                    reason: "You have a very strong hand in early position. Open with 3x the big blind.",
                    class: "raise"
                };
            } else if (handStrength >= 0.65) { // Strong hand
                return {
                    action: "Raise",
                    reason: "You have a strong hand. Consider opening with 2.5x the big blind.",
                    class: "raise"
                };
            } else { // Medium or weak hand
                return {
                    action: "Fold",
                    reason: "Your hand isn't strong enough to open from early position.",
                    class: "fold"
                };
            }
        } else if (position === "middle_position" || position === "middle_position_1" || position === "hijack") {
            if (handStrength >= 0.8) { // Very strong hand
                return {
                    action: "Raise",
                    reason: "You have a very strong hand. Open with 2.5-3x the big blind.",
                    class: "raise"
                };
            } else if (handStrength >= 0.5) { // Strong to medium hand
                return {
                    action: "Raise",
                    reason: "You have a playable hand in middle position. Consider raising 2.5x the big blind.",
                    class: "raise"
                };
            } else { // Weak hand
                return {
                    action: "Fold",
                    reason: "Your hand is too weak for this position. Wait for a better spot.",
                    class: "fold"
                };
            }
        } else if (position === "cutoff" || position === "button") {
            if (handStrength >= 0.8) { // Very strong hand
                return {
                    action: "Raise",
                    reason: "You have a very strong hand in late position. Raise 2.5-3x the big blind.",
                    class: "raise"
                };
            } else if (handStrength >= 0.4) { // Medium to strong hand
                return {
                    action: "Raise",
                    reason: "You have a playable hand in late position. Consider stealing with 2-2.5x the big blind.",
                    class: "raise"
                };
            } else { // Weak hand
                if (potOdds < 0.2) { // If it's cheap to see a flop
                    return {
                        action: "Call",
                        reason: "Consider calling if everyone limped, otherwise fold.",
                        class: "call"
                    };
                }
                return {
                    action: "Fold",
                    reason: "Your hand is weak. It's best to wait for a better opportunity.",
                    class: "fold"
                };
            }
        } else { // Unknown position
            if (handStrength >= 0.8) {
                return {
                    action: "Raise",
                    reason: "You have a very strong hand. Consider raising 3x the big blind.",
                    class: "raise"
                };
            } else if (handStrength >= 0.6) {
                return {
                    action: "Call",
                    reason: "You have a strong hand. Consider calling or raising if there's minimal action.",
                    class: "call"
                };
            } else {
                return {
                    action: "Fold",
                    reason: "Your hand isn't strong enough to play out of position.",
                    class: "fold"
                };
            }
        }
    }
    
    // Function to generate opponent bet inputs based on player position
    function generateOpponentBetInputs(count) {
        opponentBetInputs.innerHTML = '';
        
        // Get player position
        const playerPos = position.value;
        let activePlayers = 0;
        
        // Determine how many players have already acted based on position
        switch(playerPos) {
            case 'early':
                // In early position, almost no one has acted yet
                activePlayers = 1; // Maybe just the big blind
                break;
            case 'middle':
                // In middle position, early positions have already acted
                activePlayers = Math.ceil(count * 0.3);
                break;
            case 'late':
                // In late position, most players have already acted
                activePlayers = Math.ceil(count * 0.7);
                break;
            case 'button':
                // On the button, almost everyone has acted except blinds
                activePlayers = count - 2;
                break;
        }
        
        // Ensure activePlayers is at least 0 and at most the total count
        activePlayers = Math.max(0, Math.min(activePlayers, count));
        
        // Create a header explaining the betting situation
        const header = document.createElement('div');
        header.innerHTML = `<p>Based on your ${playerPos} position, ${activePlayers} player(s) have already acted:</p>`;
        opponentBetInputs.appendChild(header);
        
        // Create inputs only for players who have already acted
        for (let i = 0; i < activePlayers; i++) {
            const div = document.createElement('div');
            div.innerHTML = `
                <label for="opponent-${i+1}-bet">Opponent ${i+1} bet:</label>
                <input type="number" id="opponent-${i+1}-bet" min="0" value="0">
            `;
            opponentBetInputs.appendChild(div);
        }
        
        // Add a note about players who haven't acted yet
        if (activePlayers < count) {
            const note = document.createElement('div');
            note.innerHTML = `<p class="note">The remaining ${count - activePlayers} player(s) will act after you.</p>`;
            opponentBetInputs.appendChild(note);
        }
        
        opponentBets.classList.remove('hidden');
    }
    
    // Function to get all opponent bets
    function getOpponentBets() {
        const bets = [];
        const count = parseInt(numOpponents.value);
        let total = 0;
        
        // Get player position
        const playerPos = position.value;
        let activePlayers = 0;
        
        // Determine how many players have already acted based on position
        switch(playerPos) {
            case 'early':
                activePlayers = 1; // Maybe just the big blind
                break;
            case 'middle':
                activePlayers = Math.ceil(count * 0.3);
                break;
            case 'late':
                activePlayers = Math.ceil(count * 0.7);
                break;
            case 'button':
                activePlayers = count - 2;
                break;
        }
        
        // Ensure activePlayers is at least 0 and at most the total count
        activePlayers = Math.max(0, Math.min(activePlayers, count));
        
        // Only consider bets from players who have already acted
        for (let i = 0; i < activePlayers; i++) {
            const betInput = document.getElementById(`opponent-${i+1}-bet`);
            if (betInput) {
                const bet = parseFloat(betInput.value) || 0;
                bets.push(bet);
                total += bet;
            }
        }
        
        return { bets, total };
    }
    
    // Event listeners for card selection
    card1Rank.addEventListener('change', updateHoleCards);
    card1Suit.addEventListener('change', updateHoleCards);
    card2Rank.addEventListener('change', updateHoleCards);
    card2Suit.addEventListener('change', updateHoleCards);
    
    function updateHoleCards() {
        updateCardDisplay(hole1, card1Rank.value, card1Suit.value);
        updateCardDisplay(hole2, card2Rank.value, card2Suit.value);
    }
    
    // Function to get position name based on total players and position
    function getPositionName(totalPlayers, playerPosition) {
        if (playerPosition === 1) {
            return "small_blind";
        } else if (playerPosition === 2) {
            return "big_blind";
        }

        const positions = {
            9: {
                3: "under_the_gun",
                4: "under_the_gun_plus_1",
                5: "under_the_gun_plus_2",
                6: "middle_position_1",
                7: "hijack",
                8: "cutoff",
                9: "button"
            },
            8: {
                3: "under_the_gun",
                4: "under_the_gun_plus_1",
                5: "middle_position_1",
                6: "hijack",
                7: "cutoff",
                8: "button"
            },
            7: {
                3: "under_the_gun",
                4: "middle_position_1",
                5: "hijack",
                6: "cutoff",
                7: "button"
            },
            6: {
                3: "under_the_gun",
                4: "middle_position",
                5: "cutoff",
                6: "button"
            },
            5: {
                3: "under_the_gun",
                4: "cutoff",
                5: "button"
            },
            4: {
                3: "cutoff",
                4: "button"
            },
            3: {
                3: "button"
            }
        };

        return positions[totalPlayers]?.[playerPosition] || "unknown";
    }

    // Function to update position options based on number of players
    function updatePositionOptions() {
        const totalPlayers = parseInt(numOpponents.value) + 1; // +1 to include the player
        position.innerHTML = ''; // Clear existing options

        // Add options for each valid position
        for (let i = 1; i <= totalPlayers; i++) {
            const posName = getPositionName(totalPlayers, i);
            const option = document.createElement('option');
            option.value = posName;
            option.textContent = posName.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
            position.appendChild(option);
        }
    }

    // Event listener for number of opponents
    numOpponents.addEventListener('change', function() {
        updatePositionOptions();
        const count = parseInt(this.value);
        if (count > 0) {
            generateOpponentBetInputs(count);
        } else {
            opponentBets.classList.add('hidden');
        }
    });

    // Initialize position options
    updatePositionOptions();
    
    // Event listener for position change
    position.addEventListener('change', function() {
        const count = parseInt(numOpponents.value);
        if (count > 0) {
            generateOpponentBetInputs(count);
        }
    });
    
    // Event listener for analyze button
    analyzeButton.addEventListener('click', function() {
        // Validate hole cards
        if (!card1Rank.value || !card1Suit.value || !card2Rank.value || !card2Suit.value) {
            alert('Please select both hole cards');
            return;
        }
        
        // Get card objects
        const card1 = { rank: card1Rank.value, suit: card1Suit.value };
        const card2 = { rank: card2Rank.value, suit: card2Suit.value };
        
        // Calculate hand strength
        const handResult = calculatePreflopStrength(card1, card2);
        
        // Display hand type and strength
        handTypeElement.textContent = handResult.type.replace('_', ' ');
        handStrengthElement.textContent = `${Math.round(handResult.strength * 100)}%`;
        
        // Calculate pot odds
        const { total: totalBets } = getOpponentBets();
        let potOdds = 0;
        if (totalBets > 0) {
            potOdds = totalBets / (parseFloat(potSize.value) + totalBets);
        }
        
        // Get recommendation
        const recommendation = getBettingRecommendation(
            handResult.type,
            handResult.strength,
            potOdds,
            position.value
        );
        
        // Display recommendation
        recommendationElement.textContent = `Recommended Action: ${recommendation.action}`;
        recommendationElement.className = `recommendation ${recommendation.class}`;
        recommendationReasonElement.textContent = recommendation.reason;
        
        // Show results
        preflopResults.classList.remove('hidden');
    });
    
    // Event listener for continue to flop button
    continueToFlopButton.addEventListener('click', function() {
        flopInput.classList.remove('hidden');
    });
    
    // Event listener for reset button
    resetHandButton.addEventListener('click', function() {
        // Reset hole cards
        card1Rank.value = '';
        card1Suit.value = '';
        card2Rank.value = '';
        card2Suit.value = '';
        updateHoleCards();
        
        // Reset community cards
        updateCardDisplay(flop1, '', '');
        updateCardDisplay(flop2, '', '');
        updateCardDisplay(flop3, '', '');
        updateCardDisplay(turn, '', '');
        updateCardDisplay(river, '', '');
        
        // Reset results
        preflopResults.classList.add('hidden');
        flopInput.classList.add('hidden');
        
        // Reset opponent bets
        opponentBets.classList.add('hidden');
        opponentBetInputs.innerHTML = '';
    });
    
    // Initialize opponent bet inputs
    generateOpponentBetInputs(parseInt(numOpponents.value));
});