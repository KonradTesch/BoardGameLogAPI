import PageContainer from "../PageContainer.tsx";
import FormCard from "../Cards/FormCard.tsx";
import InputField from "../InputField.tsx";
import DropdownSelect from "../Dropdowns/DropdownSelect.tsx";
import {useContext, useMemo, useState} from "react";
import {UserDataContext} from "../../context/UserDataContext.tsx";
import type {BoardGame} from "../../types/BoardGame.ts";
import type {
    GameSessionRequest,
    GameSessionResponse,
    SessionPlayerFormRow,
    SessionPlayerRequest
} from "../../types/GameSession.ts";
import PlayerTable from "../PlayerTable.tsx";
import Button from "../Button/Button.tsx";
import type { InfoText} from "../../types/InfoText.ts";
import InformationText from "../Text/InformationText.tsx";
import {useNavigate} from "react-router-dom";
import {ROUTES} from "../../types/routes.ts";
import {AuthContext} from "../../context/AuthContext.tsx";
import {validateSessionForm} from "../../util/ValidateSessionInput.ts";

interface SessionFormProps {
    initialSession: GameSessionResponse | undefined;
}

function SessionForm({ initialSession }: SessionFormProps) {

    const navigate = useNavigate();

    const { boardGames, players, addSession, updateSession } = useContext(UserDataContext)!;
    const { user } = useContext(AuthContext)!;

    const isEditMode = initialSession !== undefined;

    const [boardGameId, setBoardGameId] = useState<number | null>(
        () => initialSession
        ? initialSession.gameId
        :  null
    );
    // sv-SE locale formats as YYYY-MM-DD, which <input type="date"> requires.
    const [date, setDate] = useState(
        () => initialSession
        ? initialSession.date
        : new Date().toLocaleDateString("sv-SE")
    );
    const [sessionPlayerRows, setSessionPlayerRows] = useState<SessionPlayerFormRow[]>(
        () => initialSession
        ? initialSession.sessionPlayers.map(sessionPlayer => ({rowId: crypto.randomUUID(), playerId: sessionPlayer.playerId, score: String(sessionPlayer.score), winner: sessionPlayer.winner}))
        : [ {rowId: crypto.randomUUID(),playerId: null, score:"", winner:false}]
    );

    const [hasSubmitted, setHasSubmitted] = useState(false)
    const [submitSessionInfo, setSubmitSessionInfo] = useState<InfoText>({message: ""})

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


    const handleSubmitSession = async () => {
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

        const result = isEditMode
            ? await updateSession(newSession, initialSession.id)
            : await addSession((newSession));

        if (result.success) {
            setSubmitSessionInfo({message: result.message, variant: "success"})
            navigate(ROUTES.dashboard.to(user!.id))
        }
        else {
            setSubmitSessionInfo({message: result.error, variant: "warning"})
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
            label={isEditMode ? "Save Session" : "Add Session"}
            variant="success"
            onClick={handleSubmitSession}
        />
        {submitSessionInfo.message && <InformationText infoText={submitSessionInfo} />}
    </PageContainer>
);
}

export default SessionForm;