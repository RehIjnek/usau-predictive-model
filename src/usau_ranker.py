# chatgpt generated, tweaked by Kenji Her
# need to figure out data strucs for parameters + fixing iterator

import numpy as np

def calculate_game_rating(opponent_rating, win, winning_score, losing_score):
    """Computes game rating based on opponent rating and score differential."""
    x = compute_score_differential(winning_score, losing_score)
    return opponent_rating + x if win else opponent_rating - x

def compute_score_differential(winning_score, losing_score):
    """Computes the rating differential x based on the score."""
    r = losing_score / (winning_score - 1)

    score_diff = winning_score - losing_score
    
    if score_diff == 1:
        return 125
    elif winning_score > 2 * losing_score:
        return 600
    else:
        return int(125 + 475 * ((np.sin(min(1.0, (1 - r) / 0.5)) * (0.4 * np.pi)) / np.sin(0.4 * np.pi)))

def compute_score_weight(winning_score, losing_score):
    """Computes the score weight based on winning and total score."""
    total_score = winning_score + losing_score
    if winning_score >= 13 or total_score >= 19:
        return 1.0
    return min(1.0, np.sqrt((winning_score + max(losing_score, np.floor((winning_score - 1) / 2))) / (19)))

def compute_date_weight(week, total_weeks):
    """Computes the date weight based on how recent the game was played."""
    return 0.5 * (2 ** (week / total_weeks))

def compute_team_rating(games, initial_rating=1000, iterations=1000):
    """Iteratively computes team ratings based on game results."""
    team_ratings = {team: initial_rating for team in set([g['team'] for g in games])}
    
    for _ in range(iterations):
        new_ratings = {}
        for team in team_ratings:
            game_ratings = []
            weight_sum = 0
            
            for game in [g for g in games if g['team'] == team]:
                opponent_rating = team_ratings[game['opponent']]
                game_rating = calculate_game_rating(opponent_rating, game['win'], game['winning_score'], game['losing_score'])
                score_weight = compute_score_weight(game['winning_score'], game['losing_score'])
                date_weight = compute_date_weight(game['week'], game['total_weeks'])
                weight = score_weight * date_weight
                
                game_ratings.append(game_rating * weight)
                weight_sum += weight
            
            new_ratings[team] = sum(game_ratings) / weight_sum if weight_sum > 0 else initial_rating
        
        team_ratings = new_ratings
    
    return team_ratings
