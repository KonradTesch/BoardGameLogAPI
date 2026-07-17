import type {GameSession} from "../../types/GameSession.ts";
import {useContext} from "react";
import {AuthContext} from "../../context/AuthContext.tsx";
import SessionListItem from "./SessionListItem.tsx";

interface SessionListProps {
    sessions: GameSession[] | null;
    sessionsToDelete: GameSession[];
    onDelete: (session: GameSession) => void;
    onOpenDetails: (session: GameSession) => void;
    onEditSession: (session: GameSession) => void;
    waitForLoading?: boolean;
}

function SessionList({sessions, sessionsToDelete, onDelete, onOpenDetails, onEditSession, waitForLoading = false}: SessionListProps) {

    const { isLoading } = useContext(AuthContext)!;

    return (
        <ul className="list-group list-group-flush">
                {isLoading && waitForLoading ? <p>Loading...</p> : sessions?.map((session: GameSession, index) =>(
                    ( !sessionsToDelete.includes(session) &&
                    <SessionListItem
                        index={index}
                        session={session}
                        onDelete={() => onDelete(session)}
                        onOpenDetails={() => onOpenDetails(session)}
                        onEditSession={() => onEditSession(session)}
                    />)
                    ))}
        </ul>
    );
}

export default SessionList;