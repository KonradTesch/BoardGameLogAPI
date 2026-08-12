import PageContainer from "../components/PageContainer.tsx";
import FormCard from "../components/Cards/FormCard.tsx";
import InputField from "../components/InputField.tsx";
import DropdownSelect from "../components/Dropdowns/DropdownSelect.tsx";
import {useContext, useMemo, useState} from "react";
import {UserDataContext} from "../context/UserDataContext.tsx";
import type {BoardGame} from "../types/BoardGame.ts";
import type {GameSessionRequest, SessionPlayerFormRow, SessionPlayerRequest} from "../types/GameSession.ts";
import PlayerTable from "../components/PlayerTable.tsx";
import Button from "../components/Button/Button.tsx";
import type {InfoText} from "../types/InfoText.ts";
import InformationText from "../components/Text/InformationText.tsx";

function EditSessionPage(){

    const { boardGames, players, addSession } = useContext(UserDataContext)!;

    const sortedBoardGames = useMemo(() => boardGames.toSorted((a, b) => a.title.localeCompare(b.title, undefined, { sensitivity: "base" })), [boardGames]);
    const sortedPlayers = useMemo(() => players.toSorted((a, b) => a.name.localeCompare(b.name, undefined, { sensitivity: "base" })), [players]);

    const boardGameOptions = new Map<number, string>(sortedBoardGames.map((boardGame: BoardGame) => [boardGame.id, boardGame.title]))

    const [boardGameId, setBoardGameId] = useState<number>(0);
    // sv-SE locale formats as YYYY-MM-DD, which <input type="date"> requires.
    const [date, setDate] = useState(() => new Date().toLocaleDateString("sv-SE"));
    const [sessionPlayerRows, setSessionPlayerRows] = useState<SessionPlayerFormRow[]>(() =>[ {rowId: crypto.randomUUID(),playerId: null, score:0, winner:false}])

    const [addSessionInfo, setAddSessionInfo] = useState<InfoText>({message: ""})

    const handleCreateSession = async () => {
        const sessionPlayers: SessionPlayerRequest[] = sessionPlayerRows
            .filter((row: SessionPlayerFormRow) => row.playerId !== null)
            .map((row) => ({
                playerId: row.playerId as number,
                score: row.score,
                winner: row.winner
            }))

        const newSession: GameSessionRequest = {
            date: date,
            gameId: boardGameId,
            sessionPlayers: sessionPlayers,
        }

        const addSessionResult = await addSession((newSession));

        if (addSessionResult.success) {
            setAddSessionInfo({message: addSessionResult.message, variant: "success"})
        }
        else {
            setAddSessionInfo({message: addSessionResult.error, variant: "warning"})
        }
    }

    const handleAddPlayer = () => {
        const newPlayer: SessionPlayerFormRow = {rowId: crypto.randomUUID(), playerId: null,score: 0, winner:false };

        setSessionPlayerRows(prev => [...prev, newPlayer]);
    }

    const handleEditPlayerID = (setIndex: number, newPlayerId: number) => {
        setSessionPlayerRows(prev => prev.map((sessionPlayer, index) =>
            index === setIndex
            ? {...sessionPlayer, playerId: newPlayerId}
            : sessionPlayer
        ))
    }

    const handleEditScore = (setIndex: number, newScore: number) => {
        setSessionPlayerRows(prev => prev.map((sessionPlayer , index) =>
            index === setIndex
            ? {...sessionPlayer, score: newScore}
            : sessionPlayer
        ))
    }

    const handleEditWinner = (setIndex: number, isWinner: boolean)=> {
        setSessionPlayerRows(prev => prev.map((sessionPlayer, index) =>
            index === setIndex
            ? {...sessionPlayer, winner: isWinner}
            : sessionPlayer
        ))
    }

    const handleRemovePlayer = (atIndex: number) => {
        setSessionPlayerRows(prev => prev.filter((_sessionPlayer, index) => index != atIndex))
    }

    return (
    <PageContainer>
        <div className="mb-4">
            <h3 className="mb-3">
                <p><i className="bi bi-dice-6-fill" /> Board Game Title</p>
                <DropdownSelect
                    label="Game Title"
                    options={boardGameOptions}
                    firstIsSelect={true}
                    value={boardGameId}
                    onChange={(e) => setBoardGameId(Number(e.target.value))}
                />
            </h3>
            <p className="text-body-secondary mb-0">
                <InputField
                    label={<><i className="bi bi-calendar-event" /> Date</>}
                    type="date"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                />
            </p>
        </div>
        <FormCard header="Score">
            <PlayerTable
                sessionPlayerRows={sessionPlayerRows}
                sortedPlayers={sortedPlayers}
                onEditPlayerId={handleEditPlayerID}
                onEditScore={handleEditScore}
                onEditWinner={handleEditWinner}
                onRemoveSessionPlayer={handleRemovePlayer}
            />
            <div className="d-flex justify-content-center align-items-center">
                <Button label="Add Player" variant="primary" onClick={handleAddPlayer} />
            </div>
        </FormCard>
        <Button
            label="Add Session"
            variant="success"
            onClick={handleCreateSession}
        />
        {addSessionInfo.message && <InformationText infoText={addSessionInfo} />}
    </PageContainer>
);
}

export default EditSessionPage;