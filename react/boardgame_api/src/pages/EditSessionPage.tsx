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
import {useNavigate} from "react-router-dom";
import {ROUTES} from "../types/routes.ts";
import {AuthContext} from "../context/AuthContext.tsx";
import {validateSessionForm} from "../util/ValidateSessionInput.ts";

function EditSessionPage(){

    const navigate = useNavigate();

    const { boardGames, players, addSession } = useContext(UserDataContext)!;
    const { user } = useContext(AuthContext)!;

    const [boardGameId, setBoardGameId] = useState<number | null>(null);
    // sv-SE locale formats as YYYY-MM-DD, which <input type="date"> requires.
    const [date, setDate] = useState(() => new Date().toLocaleDateString("sv-SE"));
    const [sessionPlayerRows, setSessionPlayerRows] = useState<SessionPlayerFormRow[]>(() =>[ {rowId: crypto.randomUUID(),playerId: null, score:"", winner:false}])


    const [hasSubmitted, setHasSubmitted] = useState(false)
    const [addSessionInfo, setAddSessionInfo] = useState<InfoText>({message: ""})

    const sortedBoardGames = useMemo(
        () => boardGames.toSorted((a, b) => a.title.localeCompare(b.title, undefined, { sensitivity: "base" })),
        [boardGames]
    );
    const sortedPlayers = useMemo(
        () => players.toSorted((a, b) => a.name.localeCompare(b.name, undefined, { sensitivity: "base" })),
        [players]
    );
    const errors = useMemo(
        () => validateSessionForm(boardGameId, date, sessionPlayerRows),
        [boardGameId, date, sessionPlayerRows]
    );

    const boardGameOptions = new Map<number, string>(sortedBoardGames.map((boardGame: BoardGame) => [boardGame.id, boardGame.title]))

    const hasErrors = Boolean(errors.boardGame || errors.date || errors.duplicatePlayers)
    || Object.keys(errors.rows).length > 0;

    const handleCreateSession = async () => {
        setHasSubmitted(true);

        if (hasErrors)
            return;

        const sessionPlayers: SessionPlayerRequest[] = sessionPlayerRows
            .filter((row: SessionPlayerFormRow) => row.playerId !== null)
            .map((row) => ({
                playerId: row.playerId as number,
                score: Number(row.score),
                winner: row.winner
            }))

        const newSession: GameSessionRequest = {
            date: date,
            gameId: Number(boardGameId),
            sessionPlayers: sessionPlayers,
        }

        const addSessionResult = await addSession((newSession));

        if (addSessionResult.success) {
            setAddSessionInfo({message: addSessionResult.message, variant: "success"})
            navigate(ROUTES.dashboard.to(user!.id))
        }
        else {
            setAddSessionInfo({message: addSessionResult.error, variant: "warning"})
        }
    }

    const handleAddPlayer = () => {
        const newPlayer: SessionPlayerFormRow = {rowId: crypto.randomUUID(), playerId: null,score: "", winner:false };

        setSessionPlayerRows(prev => [...prev, newPlayer]);
    }

    const handleChangePlayerID = (setIndex: number, newPlayerId: number | null) => {
        setSessionPlayerRows(prev => prev.map((sessionPlayer, index) =>
            index === setIndex
            ? {...sessionPlayer, playerId: newPlayerId}
            : sessionPlayer
        ))
    }

    const handleChangeScore = (setIndex: number, newScore: string) => {
        setSessionPlayerRows(prev => prev.map((sessionPlayer , index) =>
            index === setIndex
            ? {...sessionPlayer, score: newScore}
            : sessionPlayer
        ))
    }

    const handleChangeWinner = (setIndex: number, isWinner: boolean)=> {
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
                    onChange={(e) => setBoardGameId(e.target.value === "" ? null :  Number(e.target.value))}
                />
            </h3>
            {hasSubmitted && errors.boardGame &&
                <InformationText infoText={{
                message: errors.boardGame,
                variant: "danger"
            }} />}
            <p className="text-body-secondary mb-0">
                <InputField
                    label={<><i className="bi bi-calendar-event" /> Date</>}
                    type="date"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                />
                {hasSubmitted && errors.date &&
                <InformationText infoText={{
                message: errors.date,
                variant: "danger"
            }} />}
            </p>
        </div>
        <FormCard header="Score">
            <PlayerTable
                sessionPlayerRows={sessionPlayerRows}
                sortedPlayers={sortedPlayers}
                onChangePlayerId={handleChangePlayerID}
                onChangeScore={handleChangeScore}
                onChangeWinner={handleChangeWinner}
                onRemoveSessionPlayer={handleRemovePlayer}
                hasSubmitted={hasSubmitted}
                errors={errors}
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