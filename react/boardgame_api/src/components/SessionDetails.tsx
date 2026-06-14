import type {GameSession} from "../types/GameSession.ts";
import FormCard from "./FormCard.tsx";
import ScoreList from "./ScoreList.tsx";

interface SessionDetailsProps {
    session: GameSession;
}

function SessionDetails(props: SessionDetailsProps) {
    return (<>
        <div className="mb-4">
            <h1 className="mb-1"><i className="bi bi-dice-6-fill"></i> {props.session.gameName}</h1>
            <p className="text-body-secondary mb-0">
                <i className="bi bi-calendar-event"></i> {new Date(props.session.date).toLocaleDateString()}
            </p>
        </div>
        <FormCard header="Score">
            <ScoreList players={props.session.players} />
        </FormCard>
    </>);
}

export default SessionDetails;