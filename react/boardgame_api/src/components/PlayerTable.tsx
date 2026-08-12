import type {SessionPlayerFormRow} from "../types/GameSession.ts";
import DropdownSelect from "./Dropdowns/DropdownSelect.tsx";
import type {Player} from "../types/Player.ts";
import Checkbox from "./Checkbox.tsx";
import Button from "./Button/Button.tsx";

interface PlayerTableProps {
    sessionPlayerRows: SessionPlayerFormRow[];
    sortedPlayers: Player[];
    onEditPlayerId: (index: number, newId: number) => void;
    onEditScore: (index: number, newScore: number) => void;
    onEditWinner: (index: number, newWinnerValue: boolean) => void;
    onRemoveSessionPlayer: (index: number) => void;
}

function PlayerTable(props: PlayerTableProps) {

    const playerOptions = new Map<number, string>(props.sortedPlayers.map((player: Player) => [player.id, player.name]));

    return (
        <table className="table">
            <thead>
            <tr>
                <th scope="col">Player</th>
                <th scope="col">Score</th>
                <th scope="col">Winner</th>
                <th scope="col" />
            </tr>
            </thead>
            <tbody>
            {props.sessionPlayerRows.map((sessionPlayer: SessionPlayerFormRow, index: number) => (
                <tr key={sessionPlayer.rowId}>
                    <td>
                        <DropdownSelect
                            options={playerOptions}
                            value={sessionPlayer.playerId}
                            onChange={(e) =>props.onEditPlayerId(index, Number(e.target.value))}
                            firstIsSelect={true}
                        />
                    </td>
                    <td style={{ width: "7rem" }}>
                        <input
                            className="form-control"
                            type="number"
                            aria-label="Player Score"
                            value={sessionPlayer.score}
                            onChange={(e) => props.onEditScore(index, Number(e.target.value))}/>
                    </td>
                    <td style={{ width: "4rem" }}>
                        <div className="d-flex justify-content-center align-items-center">
                            <Checkbox value={sessionPlayer.winner} onChange={(e) => props.onEditWinner(index, e.target.checked)}/>
                        </div>
                    </td>
                    <td style={{ width: "3rem" }}>
                        <Button
                            label={<i className="bi bi-x-lg" />}
                            variant="secondary"
                            onClick={() => props.onRemoveSessionPlayer(index)}
                        />
                    </td>
                </tr>
            ))}
            </tbody>
        </table>
    )
}

export default PlayerTable;