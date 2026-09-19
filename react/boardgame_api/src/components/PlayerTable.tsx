import type {SessionPlayerFormRow} from "../types/GameSession.ts";
import DropdownSelect from "./Dropdowns/DropdownSelect.tsx";
import type {Player} from "../types/Player.ts";
import Checkbox from "./Checkbox.tsx";
import Button from "./Button/Button.tsx";
import InformationText from "./Text/InformationText.tsx";
import type {SessionFormErrors} from "../util/ValidateSessionInput.ts";

interface PlayerTableProps {
    sessionPlayerRows: SessionPlayerFormRow[];
    sortedPlayers: Player[];
    onChangePlayerId: (index: number, newId: number | null) => void;
    onChangeScore: (index: number, newScore: string) => void;
    onChangeWinner: (index: number, newWinnerValue: boolean) => void;
    onRemoveSessionPlayer: (index: number) => void;
    hasSubmitted: boolean;
    errors: SessionFormErrors;
}

function PlayerTable(props: PlayerTableProps) {

    const playerOptions = new Map<number, string>(props.sortedPlayers.map((player: Player) => [player.id, player.name]));

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
                {props.sessionPlayerRows.map((sessionPlayer: SessionPlayerFormRow, index: number) => {
                        const rowErrors = props.hasSubmitted ? props.errors.rows[sessionPlayer.rowId] : undefined;

                        return (
                            <tr key={sessionPlayer.rowId}>
                                <td>
                                    <DropdownSelect
                                        options={playerOptions}
                                        value={sessionPlayer.playerId}
                                        onChange={(e) => props.onChangePlayerId(index, e.target.value === "" ? null : Number(e.target.value))}
                                        firstIsSelect={true}
                                    />

                                    {rowErrors?.player
                                        && <InformationText infoText={{
                                            message: rowErrors.player,
                                            variant: "danger"
                                        }}/>}
                                </td>
                                <td style={{width: "7rem"}}>
                                    <input
                                        className="form-control"
                                        type="number"
                                        step="any"
                                        aria-label="Player Score"
                                        value={sessionPlayer.score}
                                        onChange={(e) => props.onChangeScore(index, e.target.value)}
                                    />
                                    {rowErrors?.score
                                        && <InformationText infoText={{
                                            message: rowErrors.score,
                                            variant: "danger"
                                        }}/>}
                                </td>
                                <td style={{width: "4rem"}}>
                                    <div className="d-flex justify-content-center align-items-center">
                                        <Checkbox value={sessionPlayer.winner}
                                                  onChange={(e) => props.onChangeWinner(index, e.target.checked)}/>
                                    </div>
                                </td>
                                <td style={{width: "3rem"}}>
                                    <Button
                                        label={<i className="bi bi-x-lg"/>}
                                        variant="secondary"
                                        onClick={() => props.onRemoveSessionPlayer(index)}
                                    />
                                </td>
                            </tr>
                        );
                    }
                )}
                </tbody>
            </table>
            {props.hasSubmitted
                && props.errors.duplicatePlayers
                && <InformationText infoText={{message: props.errors.duplicatePlayers, variant: "danger"}} />
                }
        </>
    )
}

export default PlayerTable;