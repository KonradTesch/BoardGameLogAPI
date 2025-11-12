from db_manager import DataManager

data_manager = DataManager()

def get_player_game_wins(player_id, game_id):
    scores = data_manager.get_player_scores_for_game(player_id, game_id)

    wins = 0
    plays = 0
    for score in scores:
        plays += 1
        if score.winner:
            wins += 1

    percentage = wins / plays * 100

    return wins, percentage


def get_total_player_wins(player_id):
    scores = data_manager.get_player_scores_all(player_id)

    wins = 0
    plays = 0
    for score in scores:
        plays += 1
        if score.winner:
            wins += 1

    percentage = wins / plays * 100

    return wins, percentage


def get_average_player_score(player_id, game_id):
    scores = data_manager.get_player_scores_for_game(player_id, game_id)

    total_score = 0

    for score in scores:
        total_score += score.score

    average = total_score / len(scores)

    return average


def get_best_player_score(player_id, game_id):
    scores = data_manager.get_player_scores_for_game(player_id, game_id)

    best_score = scores[0]

    for score in scores:
        if score.score > best_score.score:
            best_score = score

    return best_score


def get_player_stats(player_id):
    player_stats = {}

    total = {}

    total["wins"], total ["win_rate"] = get_total_player_wins(player_id)

    player_stats["total"] = total

    player_games = data_manager.get_player_games(player_id)

    for game in player_games:
        game_stats = {}

        game_stats["wins"], game_stats["win_rate"] = get_player_game_wins(player_id, game.id)
        game_stats["avg_score"] = get_average_player_score(player_id, game.id)
        game_stats["best_score"] = get_best_player_score(player_id, game.id)

        player_stats[game.title] = game_stats

    return player_stats


def get_games(user_id, game_id):
    game_sessions = data_manager.get_user_game_session_by_game(user_id, game_id)

    best_score = game_sessions[0].session_players[0].score
    best_player = game_sessions[0].session_players[0].player.name

    for session in game_sessions:
        for player in session.session_players:
            if player.score > best_score:
                best_score = player.score
                best_player = player.player.name


    return len(game_sessions), best_score, best_player


def get_game_stats(user_id)
    user_game_stats = {}

    total = {}

    total_sessions = data_manager.get_user_game_sessions_all(user_id)

    total["session_count"] = len(total_sessions)

    user_game_stats["total"] = total

    games = data_manager.get_user_games(user_id)

    for game in games:
        game_stats= {}

        game_sessions = data_manager.get_user_game_session_by_game(user_id, game.id)

        game_stats["session_count"], game_stats["best_score"], game_stats["best_player"] = get_games(user_id, game.id)

        user_game_stats[game.title] = game_stats

    return user_game_stats









