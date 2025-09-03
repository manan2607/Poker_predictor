import random
from collections import Counter

# Card values and suits for representation
SUITS = ['c', 'd', 'h', 's']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
RANK_MAP = {rank: i for i, rank in enumerate(RANKS)}

# Helper function to generate a full deck
def generate_deck():
    """Generates a standard 52-card deck."""
    return [f'{rank}{suit}' for suit in SUITS for rank in RANKS]

# --- Hand Evaluation Logic ---
def get_hand_rank(cards):
    """
    Evaluates a 5-7 card poker hand and returns its rank.
    
    Args:
        cards (list): A list of 5, 6, or 7 card strings (e.g., ['Ah', 'Kh', 'Qh', 'Jh', 'Th']).
        
    Returns:
        tuple: A tuple representing the hand's rank. Higher value means better hand.
               (rank_id, high_card_1, high_card_2, ...)
    """
    if len(cards) < 5:
        return (0, 0, 0, 0, 0, 0) # Invalid hand
    
    # Extract ranks and suits
    card_values = sorted([RANK_MAP[c[0]] for c in cards], reverse=True)
    card_suits = [c[1] for c in cards]
    
    # Check for flushes
    suit_counts = Counter(card_suits)
    is_flush = any(count >= 5 for count in suit_counts.values())
    if is_flush:
        flush_suit = next(suit for suit, count in suit_counts.items() if count >= 5)
        flush_cards = sorted([RANK_MAP[c[0]] for c in cards if c[1] == flush_suit], reverse=True)
    
    # Check for straights
    unique_ranks = sorted(list(set(card_values)), reverse=True)
    is_straight = False
    straight_high_card = 0
    if len(unique_ranks) >= 5:
        for i in range(len(unique_ranks) - 4):
            if unique_ranks[i] == unique_ranks[i+1] + 1 == unique_ranks[i+2] + 2 == unique_ranks[i+3] + 3 == unique_ranks[i+4] + 4:
                is_straight = True
                straight_high_card = unique_ranks[i]
                break
        # Special case for Ace-low straight (A-5)
        if not is_straight and set(unique_ranks) >= set([3, 2, 1, 0, 12]):
            is_straight = True
            straight_high_card = 3 # Represents a 5-high straight

    # Royal Flush (rank 9)
    if is_flush and is_straight and straight_high_card == RANK_MAP['A']:
        return (9, RANK_MAP['A'])
    
    # Straight Flush (rank 8)
    if is_flush and is_straight:
        return (8, straight_high_card)
        
    # Four of a Kind (rank 7)
    rank_counts = Counter(card_values)
    if 4 in rank_counts.values():
        quad_rank = next(rank for rank, count in rank_counts.items() if count == 4)
        kicker = sorted([r for r in card_values if r != quad_rank], reverse=True)[0]
        return (7, quad_rank, kicker)

    # Full House (rank 6)
    if 3 in rank_counts.values() and 2 in rank_counts.values():
        trips_rank = next(rank for rank, count in rank_counts.items() if count == 3)
        pair_rank = next(rank for rank, count in rank_counts.items() if count == 2)
        return (6, trips_rank, pair_rank)

    # Flush (rank 5)
    if is_flush:
        return (5, *flush_cards[:5])

    # Straight (rank 4)
    if is_straight:
        return (4, straight_high_card)

    # Three of a Kind (rank 3)
    if 3 in rank_counts.values():
        trips_rank = next(rank for rank, count in rank_counts.items() if count == 3)
        kickers = sorted([r for r in card_values if r != trips_rank], reverse=True)[:2]
        return (3, trips_rank, *kickers)

    # Two Pair (rank 2)
    pairs = [rank for rank, count in rank_counts.items() if count == 2]
    if len(pairs) >= 2:
        pairs.sort(reverse=True)
        kicker = sorted([r for r in card_values if r not in pairs], reverse=True)[0]
        return (2, pairs[0], pairs[1], kicker)

    # Pair (rank 1)
    if 2 in rank_counts.values():
        pair_rank = next(rank for rank, count in rank_counts.items() if count == 2)
        kickers = sorted([r for r in card_values if r != pair_rank], reverse=True)[:3]
        return (1, pair_rank, *kickers)

    # High Card (rank 0)
    return (0, *card_values[:5])

# --- Main Functions ---
def calculate_win_probability(my_cards, board_cards, num_opponents, num_simulations=5000):
    """
    Calculates the winning probability using Monte Carlo simulation.
    
    Args:
        my_cards (list): My two hole cards.
        board_cards (list): The community cards on the board.
        num_opponents (int): Number of opponents.
        num_simulations (int): The number of simulations to run.
        
    Returns:
        float: The estimated win probability (0.0 to 1.0).
    """
    wins = 0
    ties = 0

    deck = generate_deck()
    known_cards = my_cards + board_cards
    
    # Remove known cards from the deck
    for card in known_cards:
        if card in deck:
            deck.remove(card)
    
    # If the number of cards in the deck is less than required for opponents + community,
    # the simulation is not possible.
    if len(deck) < num_opponents * 2 + (5 - len(board_cards)):
        return 0.0

    for _ in range(num_simulations):
        temp_deck = list(deck)
        random.shuffle(temp_deck)

        # Deal opponent and remaining community cards
        opponent_hands = [temp_deck.pop() for _ in range(num_opponents * 2)]
        remaining_board = [temp_deck.pop() for _ in range(5 - len(board_cards))]
        
        full_board = board_cards + remaining_board
        
        my_hand_rank = get_hand_rank(my_cards + full_board)
        
        is_winner = True
        is_tie = False
        
        for i in range(num_opponents):
            opponent_hand = opponent_hands[i*2:(i+1)*2]
            opponent_hand_rank = get_hand_rank(opponent_hand + full_board)
            
            if my_hand_rank < opponent_hand_rank:
                is_winner = False
                break
            elif my_hand_rank == opponent_hand_rank:
                is_tie = True
        
        if is_winner:
            if is_tie:
                ties += 1
            else:
                wins += 1

    return (wins + ties / (num_opponents + 1)) / num_simulations

def make_decision(win_probability, pot_size, opponent_bet, opponent_aggressiveness):
    """
    AI's decision logic based on probability, pot odds, and opponent model.
    
    Args:
        win_probability (float): The estimated win probability (0.0 to 1.0).
        pot_size (float): The current size of the pot.
        opponent_bet (float): The bet made by the opponent.
        opponent_aggressiveness (float): A value from 0.0 to 1.0 representing
                                         the opponent's play style.
                                         
    Returns:
        str: The recommended action ('Fold', 'Call', or 'Raise').
    """
    # Define thresholds
    aggressive_threshold = 0.6 + (0.15 * opponent_aggressiveness)
    call_threshold = 0.4 - (0.1 * (1 - opponent_aggressiveness))

    # Calculate pot odds
    if (pot_size + opponent_bet) == 0:
        pot_odds = 1.0
    else:
        pot_odds = opponent_bet / (pot_size + opponent_bet)

    # 1. Bluffing Logic (low probability, low pot_odds)
    # The AI will bluff with a low chance if the win probability is terrible and opponent is not aggressive
    if win_probability < 0.2 and opponent_aggressiveness < 0.5:
        if random.random() < 0.1:  # 10% chance to bluff
            return "Bluff Raise"

    # 2. Raise Logic (high probability, great hand)
    if win_probability > aggressive_threshold:
        return "Raise"

    # 3. Pot Odds Logic (the core 'Call' decision)
    if win_probability > pot_odds:
        # Check if the hand is strong enough to call.
        if win_probability > call_threshold:
            return "Call"
        else:
            # If win_probability > pot_odds but below call threshold, it's a weak call.
            # This is a good spot to add a check/fold behavior to avoid -EV.
            return "Fold"

    # 4. Default Fold (low probability and poor pot odds)
    return "Fold"
