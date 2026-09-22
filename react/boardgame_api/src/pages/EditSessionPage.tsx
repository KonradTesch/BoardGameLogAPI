import {useContext} from "react";
import {UserDataContext} from "../context/UserDataContext.tsx";
import {useParams} from "react-router-dom";

import SessionForm from "../components/Forms/SessionForm.tsx";


function EditSessionPage(){

    const { sessionId } = useParams();
    const { sessions, isLoading } = useContext(UserDataContext)!;

    if ( sessionId && isLoading) return <p>Is Loading...</p>

    const session = sessionId
        ? sessions.find(s => s.id === Number(sessionId))
        : undefined;

    if (sessionId && !session) return <p>Session not found.</p>

    return <SessionForm initialSession={session} key={sessionId ?? "new"} />
}

export default EditSessionPage;