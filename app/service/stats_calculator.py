from sqlalchemy.orm import Session
from app.repositories.player_repository import PlayerRepository
from app.repositories.game_session_repository import GameSessionRepository
from app.repositories.board_game_repository import BoardGameRepository


def get_player_session_count(player_repo, player_id, game_id):
    session_count = len(player_repo.get_player_scores_for_game(player_id, game_id))
    return session_count

def get_player_total_session_count(player_repo, player_id: int):
    session_count = len(player_repo.get_player_scores_all(player_id))
    return session_count

def get_player_game_wins(player_repo, player_id, game_id):
    scores = player_repo.get_player_scores_for_game(player_id, game_id)

    wins = 0
    plays = 0
    for score in scores:
        plays += 1
        if score.winner:
            wins += 1

    percentage = wins / plays * 100

    return wins, round(percentage, 2)


def get_total_player_wins(player_repo, player_id):
    scores = player_repo.get_player_scores_all(player_id)

    wins = 0
    plays = 0
    for score in scores:
        plays += 1
        if score.winner:
            wins += 1

    percentage = wins / plays * 100

    return wins, round(percentage, 2)


def get_average_player_score(player_repo, player_id, game_id):
    scores = player_repo.get_player_scores_for_game(player_id, game_id)

    total_score = 0

    for score in scores:
        total_score += score.score

    average = total_score / len(scores)

    return round(average, 2)


def get_best_player_score(player_repo, player_id, game_id):
    scores = player_repo.get_player_scores_for_game(player_id, game_id)

    best_score = scores[0].score

    for score in scores:
        if score.score > best_score:
            best_score = score.score

    return best_score


def get_player_stats(db: Session, player_id):
    player_repo = PlayerRepository(db)

    player_stats = {}

    total = {}

    total["session_count"] = get_player_total_session_count(player_repo, player_id)
    total["wins"], total ["win_rate"] = get_total_player_wins(player_repo, player_id)

    player_stats["Total"] = total

    player_games = player_repo.get_player_games(player_id)

    for game in player_games:
        game_stats = {}

        game_stats["session_count"] = get_player_session_count(player_repo, player_id, game.id)
        game_stats["wins"], game_stats["win_rate"] = get_player_game_wins(player_repo, player_id, game.id)
        game_stats["avg_score"] = get_average_player_score(player_repo, player_id, game.id)
        game_stats["best_score"] = get_best_player_score(player_repo, player_id, game.id)

        player_stats[game.title] = game_stats

    return player_stats


def get_games(game_session_repo, user_id, game_id):
    game_sessions = game_session_repo.get_user_game_session_by_game(user_id, game_id)

    best_score = game_sessions[0].session_players[0].score
    best_player = game_sessions[0].session_players[0].player.name

    for session in game_sessions:
        for player in session.session_players:
            if player.score > best_score:
                best_score = player.score
                best_player = player.player.name


    return len(game_sessions), best_score, best_player


def get_game_stats(db: Session, user_id):
    game_session_repo = GameSessionRepository(db)
    board_game_repo = BoardGameRepository(db)

    user_game_stats = {}

    total = {}

    total_sessions = game_session_repo.get_user_game_sessions_all(user_id)

    total["session_count"] = len(total_sessions)

    user_game_stats["All Games"] = total

    games = board_game_repo.get_user_games(user_id)

    for game in games:
        game_stats= {}

        game_sessions = game_session_repo.get_user_game_session_by_game(user_id, game.id)

        game_stats["session_count"], game_stats["best_score"], game_stats["best_player"] = get_games(game_session_repo, user_id, game.id)

        user_game_stats[game.title] = game_stats

    return user_game_stats
