import type {SessionPlayerResponse} from "../../types/GameSession.ts";

interface ScoreListProps {
    players: SessionPlayerResponse[];
}

function ScoreList(props: ScoreListProps) {

    const sortedPlayers = [...props.players].sort((a, b) => b.score - a.score);

    return (
        <ul className="list-group list-group-flush">
            {sortedPlayers.map((player: SessionPlayerResponse, index) => (
                <li className="list-group-item d-flex justify-content-between align-items-center" key={"sore-" + index}>
                <span>
                    {player.winner && <i className="bi bi-trophy-fill text-warning"></i>}
                    <span>{player.playerName}</span>
                </span>
                <span className="badge bg-primary rounded-pill fs-6">{player.score}</span>
            </li>
            ))}

        </ul>
    );
}

export default ScoreList;