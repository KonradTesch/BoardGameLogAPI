import type {SessionPlayerFormRow} from "../types/GameSession.ts";
import DropdownSelect from "./Dropdowns/DropdownSelect.tsx";
import type {Player} from "../types/Player.ts";
import Checkbox from "./Checkbox.tsx";
import Button from "./Button/Button.tsx";
import InformationText from "./Text/InformationText.tsx";

interface PlayerTableProps {
    sessionPlayerRows: SessionPlayerFormRow[];
    sortedPlayers: Player[];
    onChangePlayerId: (index: number, newId: number) => void;
    onChangeScore: (index: number, newScore: number) => void;
    onChangeWinner: (index: number, newWinnerValue: boolean) => void;
    onRemoveSessionPlayer: (index: number) => void;
    hasSubmitted: boolean;
}

function PlayerTable(props: PlayerTableProps) {

    const playerOptions = new Map<number, string>(props.sortedPlayers.map((player: Player) => [player.id, player.name]));

    const checkForDoublePlayers = () : boolean => {
        let playerIds = new Set<number>();

        for (const sessionPlayer of props.sessionPlayerRows) {
            if (sessionPlayer.playerId === null)
                continue;

            if (  playerIds.has(sessionPlayer.playerId)) {
                return true;
            }

            playerIds.add(sessionPlayer.playerId);
        }
        return false;
    }

    return (
        <>
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
                                onChange={(e) =>props.onChangePlayerId(index, Number(e.target.value))}
                                firstIsSelect={true}
                            />
                            {(sessionPlayer.info && sessionPlayer.info.message)&& <InformationText infoText={sessionPlayer.info}/>}
                            {props.hasSubmitted && sessionPlayer.playerId == null &&
                            <InformationText infoText={{message: "Choose a player.", variant:"danger"}} />
                            }
                        </td>
                        <td style={{ width: "7rem" }}>
                            <input
                                className="form-control"
                                type="number"
                                aria-label="Player Score"
                                value={sessionPlayer.score}
                                onChange={(e) => props.onChangeScore(index, Number(e.target.value))}/>
                        </td>
                        <td style={{ width: "4rem" }}>
                            <div className="d-flex justify-content-center align-items-center">
                                <Checkbox value={sessionPlayer.winner} onChange={(e) => props.onChangeWinner(index, e.target.checked)}/>
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
            {props.hasSubmitted && checkForDoublePlayers() &&
                <InformationText infoText={{message: "Table has double players.", variant: "danger"}} />}
        </>

    )
}

export default PlayerTable;