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

function DashboardPage() {

    const navigate = useNavigate();

    const { user } = useContext(AuthContext)!;

    const [ sessions, setSessions] = useState<GameSession[] | null>(null)
    const [ selectedSession, setSelectedSession ] = useState<GameSession | null>(null)
    const [ sessionsToDelete, setSessionsToDelete ] = useState<GameSession[]>([]);
    const [ sessionsInfo, setSessionsInfo] = useState<InfoText>({message:""})

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

    const handleCancelDelete = () => {
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
            <FormCard header={<><i className="bi bi-calendar-week-fill"></i> Game Sessions</>}>
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
                            <button className="btn btn-link alert-link" onClick={handleCancelDelete}>Undo</button>
                        </div>
                    </div>}
                {sessionsInfo.message && <InformationText infoText={sessionsInfo} />}
                <div className="d-flex justify-content-center">
                    <Button label={<><i className="bi bi-plus-lg" /> Add Session</>} variant="success" onClick={handleAddSession}/>
                </div>
            </FormCard>
        </PageContainer>

    );
}

export default DashboardPage;