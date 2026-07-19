import '../styles/DashboardPage.css';
import PageContainer from "../components/PageContainer.tsx";
import FormCard from "../components/Cards/FormCard.tsx";
import Button from "../components/Button/Button.tsx";
import {useContext, useEffect, useRef, useState} from "react";
import {AuthContext} from "../context/AuthContext.tsx";
import type {GameSession} from "../types/GameSession.ts";
import type {InfoText} from "../types/InfoText.ts";
import InformationText from "../components/Text/InformationText.tsx";
import SessionList from "../components/Lists/SessionList.tsx";
import ContentModal from "../components/Modals/ContentModal.tsx";
import SessionDetails from "../components/SessionDetails.tsx";
import {useNavigate} from "react-router-dom";
import {ROUTES} from "../types/routes.ts";
import DashboardList from "../components/Lists/DashboardList.tsx";
import type {Player} from "../types/Player.ts";
import PlayerListItem from "../components/Lists/PlayerListItem.tsx";
import {UserDataContext} from "../context/UserDataContext.tsx";
import InputField from "../components/InputField.tsx";
import type {BoardGame} from "../types/BoardGame.ts";
import BoardGameListItem from "../components/Lists/BoardGameListItem.tsx";

function DashboardPage() {

    const navigate = useNavigate();

    const { user } = useContext(AuthContext)!;
    const { players, addPlayer, removePlayer, boardGames, addBoardGame, removeBoardGame } = useContext(UserDataContext)!;

    const [ sessions, setSessions] = useState<GameSession[] | null>(null)
    const [ selectedSession, setSelectedSession ] = useState<GameSession | null>(null)
    const [ sessionsToDelete, setSessionsToDelete ] = useState<GameSession[]>([]);
    const [ sessionsInfo, setSessionsInfo] = useState<InfoText>({message:""})

    const [ isAddingPlayer, setIsAddingPlayer ] = useState<boolean>(false)
    const [ addPlayerName, setAddPlayerName ] = useState<string>("")
    const [ playerInfo, setPlayerInfo ] = useState<InfoText>({message:""})

    const [ isAddingBoardGame, setIsAddingBoardGame ] = useState<boolean>(false)
    const [ addBoardGameName, setAddBoardGameName ] = useState<string>("")
    const [ boardGameInfo, setBoardGameInfo ] = useState<InfoText>({message:""})

    const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
    const sessionsToDeleteRef = useRef<GameSession[]>([]);

    const getGameSession = async () => {
        const game_session = await fetch(`/api/user/${user?.id}/sessions/`, {
        method: "GET",
        credentials: "include"
        });

        if (game_session.ok) {
            const data = await game_session.json();
            setSessions(data)
        }
        else {
            setSessionsInfo({message:"Error loading game sessions.", variant: "warning"})
        }
    }

    useEffect(() => {
        if (user) {
            void getGameSession();
        }
    }, [user]);

    const handleSessionsToDelete = (session: GameSession) => {
        sessionsToDeleteRef.current = [...sessionsToDeleteRef.current, session];
        setSessionsToDelete(prev =>  [...prev, session]);

        if (timerRef.current) {
            clearTimeout(timerRef.current);
        }

        timerRef.current = setTimeout(async () => {
            await deleteSessions(sessionsToDeleteRef.current);
            setSessionsToDelete([]);
            sessionsToDeleteRef.current = [];
        }, 10000)
    };

    const handleCancelDeleteSession = () => {
        if (timerRef.current) {
            clearTimeout(timerRef.current);
        }
        setSessionsToDelete([]);
        sessionsToDeleteRef.current = [];
    };

    const deleteSessions = async (pendingSessions: GameSession[]) => {
        let errors: number[] = []
        for (const session of pendingSessions) {
            const response = await fetch(`/api/user/${user?.id}/sessions/${session.id}`, {
                method: "DELETE",
                credentials: "include"
            })

            if (response.ok) {
                setSessions(prev => prev?.filter((x) => x !== session) ?? null)
            }
            else {
                errors = [...errors, session.id]
            }
        }
        if (errors.length > 0) {
            setSessionsInfo({message: `Error deleting sessions. IDs:(${errors.join(", ")}`})
        }
        else {
            setSessionsInfo({message: ""})
        }
    };

    const handleOpenDetails = (session: GameSession) => {
        setSelectedSession(session);
    };

    const handleEditSession = (session: GameSession) => {
        navigate(ROUTES.editSessions.to(user!.id))
    }

    const handleAddSession = () => {
        navigate(ROUTES.editSessions.to(user!.id))
    }

    const handleDeletePlayer = async (player: Player) => {
        const removePlayerResult = await removePlayer(player);

        if (removePlayerResult.success) {
            setPlayerInfo({message: removePlayerResult.message, variant: "success"});
        }
        else {
            setPlayerInfo({message: removePlayerResult.error, variant: "danger"});
        }
    }

    const handleOpenPlayerStats = (player: Player) => {

    }

    const handleEditPlayer = (player: Player) => {

    }

    const handleAddPlayer = async () => {
        const addPlayerResult = await addPlayer(addPlayerName)

        if (addPlayerResult.success) {
            setPlayerInfo({message: addPlayerResult.message, variant: "success"})
        }
        else{
            setPlayerInfo({message: addPlayerResult.error, variant: "warning"})
        }

        setAddPlayerName("");
        setIsAddingPlayer(false);
    }

    const handleCancelAddPlayer = () => {
        setAddPlayerName("");
        setIsAddingPlayer(false);
    }

    const handleAddBoardGame = async () => {
        const AddBoardGameResult = await addBoardGame(addBoardGameName);

        setAddBoardGameName("");

        if (AddBoardGameResult.success) {
            setBoardGameInfo({message: AddBoardGameResult.message, variant: "success"});
        }
        else {
            setBoardGameInfo({message: AddBoardGameResult.error, variant:"warning"})
        }
    }

    const handleDeleteBoardGame = async (boardGame: BoardGame) => {
        const removeBoardGameResult = await removeBoardGame(boardGame);

        if (removeBoardGameResult.success) {
            setBoardGameInfo({message: removeBoardGameResult.message, variant: "success"});
        }
        else {
            setBoardGameInfo({message: removeBoardGameResult.error, variant: "warning"});
        }
    }

    const handleEditBoardGame = (boardGame: BoardGame) => {

    }

    const handleOpenBoardGameStats = (boardGame: BoardGame) => {

    }

    const handleCancelAddBoardGame = () => {
        setIsAddingBoardGame(false);
        setAddBoardGameName("");
    }

    return (
        <PageContainer>
            <ContentModal
                id="sessionDetailModal"
                title={"Session Info"}
                footer={
                    <>
                        <Button label="Edit" onClick={() =>handleEditSession(selectedSession!)}/>
                        <Button label="Close" data-bs-dismiss="modal" variant="secondary" />
                    </>
                    }>
                {selectedSession && <SessionDetails session={selectedSession}/>}
            </ContentModal>
            <FormCard header={<><i className="bi bi-calendar-week-fill" /> Game Sessions</>}>
                <SessionList
                    sessions={sessions}
                    sessionsToDelete={sessionsToDelete}
                    onDelete={handleSessionsToDelete}
                    onOpenDetails={handleOpenDetails}
                    onEditSession={handleEditSession}
                    waitForLoading={true}
                />
                {sessionsToDelete.length > 0 &&
                    <div className="d-flex justify-content-center">
                        <div className="alert alert-warning m-0 py-0" role="alert">You're about to delete {sessionsToDelete.length} session{sessionsToDelete.length > 1 && "s"}.
                            <button className="btn btn-link alert-link" onClick={handleCancelDeleteSession}>Undo</button>
                        </div>
                    </div>}
                {sessionsInfo.message && <InformationText infoText={sessionsInfo} />}
                <div className="d-flex justify-content-center">
                    <Button label={<><i className="bi bi-plus-lg" /> Add Session</>} variant="success" onClick={handleAddSession}/>
                </div>
            </FormCard>
            <FormCard header={<><i className="bi bi-person-fill" /> Players</>}>
                <DashboardList waitForLoading={true}>
                    {players?.map((player: Player, index: number) =>(
                    <PlayerListItem
                        index={index}
                        player={player}
                        onDelete={() => handleDeletePlayer(player)}
                        onOpenStats={() => handleOpenPlayerStats(player)}
                        onEdit={() => handleEditPlayer(player)}
                    />))}
                    { isAddingPlayer &&
                    <li className="list-group-item d-flex justify-content-between align-items-center" key="-1">
                        <span>
                            <InputField
                                label="Name"
                                type="text"
                                value={addPlayerName}
                                onChange={(e) => setAddPlayerName(e.target.value)}/>
                        </span>
                        <div className="d-flex gap-2">
                            <Button
                                label="Cancel"
                                variant="secondary"
                                onClick={handleCancelAddPlayer}
                            />
                            <Button
                                label="Add"
                                variant="success"
                                onClick={handleAddPlayer}
                                disabled={!addPlayerName}
                            />

                        </div>
                    </li>
                    }
                </DashboardList>
                {playerInfo.message && <InformationText infoText={playerInfo} />}
                { !isAddingPlayer &&
                <div className="d-flex justify-content-center">
                    <Button
                        label={<><i className="bi bi-plus-lg" /> Add Player</>}
                        variant="success"
                        onClick={() => setIsAddingPlayer(true)}
                        disabled={isAddingPlayer}
                    />
                </div>
                }
            </FormCard>

            <FormCard header={<><i className="bi bi-dice-5-fill" /> Board Games</>}>
                <DashboardList waitForLoading={true}>
                    {boardGames?.map((boardGame: BoardGame, index: number) =>(
                    <BoardGameListItem
                        index={index}
                        boardGame={boardGame}
                        onDelete={() => handleDeleteBoardGame(boardGame)}
                        onOpenStats={() => handleOpenBoardGameStats(boardGame)}
                        onEdit={() => handleEditBoardGame(boardGame)}
                    />))}
                    { isAddingBoardGame &&
                    <li className="list-group-item d-flex justify-content-between align-items-center p-1" key="-1">
                        <span>
                            <InputField
                                label="Name"
                                type="text"
                                value={addBoardGameName}
                                onChange={(e) => setAddBoardGameName(e.target.value)}/>
                        </span>
                        <div className="d-flex gap-2">
                            <Button
                                label="Cancel"
                                variant="secondary"
                                onClick={handleCancelAddBoardGame}
                            />
                            <Button
                                label="Add"
                                variant="success"
                                onClick={handleAddBoardGame}
                                disabled={!addBoardGameName}
                            />

                        </div>
                    </li>
                    }
                </DashboardList>
                {boardGameInfo.message && <InformationText infoText={boardGameInfo} />}
                { !isAddingBoardGame &&
                <div className="d-flex justify-content-center">
                    <Button
                        label={<><i className="bi bi-plus-lg" /> Add Board Game</>}
                        variant="success"
                        onClick={() => setIsAddingBoardGame(true)}
                        disabled={isAddingBoardGame}
                    />
                </div>
                }
            </FormCard>
        </PageContainer>

    );
}

export default DashboardPage;