import type {SessionPlayer} from "../types/GameSession.ts";

interface ScoreListProps {
    players: SessionPlayer[];
}

function ScoreList(props: ScoreListProps) {

    const sortedPlayers = [...props.players].sort((a, b) => b.score - a.score);

    return (
        <ul className="list-group list-group-flush">
            {sortedPlayers.map((player: SessionPlayer, index) => (
                <li className="list-group-item d-flex justify-content-between align-items-center" key={"sore-" + index}>
                <span>
                    {player.winner && <i className="bi bi-trophy-fill text-warning"></i>}
                    <span>{player.name}</span>
                </span>
                <span className="badge bg-primary rounded-pill fs-6">{player.score}</span>
            </li>
            ))}

        </ul>
    );
}

export default ScoreList;