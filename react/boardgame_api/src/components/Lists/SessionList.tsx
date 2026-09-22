import type {GameSessionResponse} from "../../types/GameSession.ts";
import {useContext} from "react";
import {AuthContext} from "../../context/AuthContext.tsx";
import SessionListItem from "./SessionListItem.tsx";

interface SessionListProps {
    sessions: GameSessionResponse[] | null;
    sessionsToDelete: number[];
    onDelete: (sessionId: number) => void;
    onOpenDetails: (sessionId: number) => void;
    onEditSession: (sessionId: number) => void;
    waitForLoading?: boolean;
}

function SessionList({sessions, sessionsToDelete, onDelete, onOpenDetails, onEditSession, waitForLoading = false}: SessionListProps) {

    const { isLoading } = useContext(AuthContext)!;

    return (
        <ul className="list-group list-group-flush">
                {isLoading && waitForLoading ? <p>Loading...</p> : sessions?.map((session: GameSessionResponse) =>(
                    ( !sessionsToDelete.includes(session.id) &&
                    <SessionListItem
                        session={session}
                        onDelete={() => onDelete(session.id)}
                        onOpenDetails={() => onOpenDetails(session.id)}
                        onEditSession={() => onEditSession(session.id)}
                        key={session.id}
                    />)
                    ))}
        </ul>
    );
}

export default SessionList;