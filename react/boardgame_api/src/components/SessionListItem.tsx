import type {GameSession} from "../types/GameSession.ts";
import IconButton from "./Button/IconButton.tsx";

interface SessionListItemProps {
    index: number
    session: GameSession;
    onDelete: () => void;
    onOpenDetails: () => void;
}

function SessionListItem(props: SessionListItemProps){

    const handleEditSession = async () => {

    }

    return (
        <li className="list-group-item d-flex justify-content-between align-items-center" key={props.index}>
            <span>{new Date(props.session.date).toLocaleDateString()}</span>
            <span>{props.session.gameName}</span>
            <div className="d-flex gap-2">
                <IconButton
                    icon="pencil-fill"
                    onClick={handleEditSession}
                    title="Edit"
                />
                <IconButton
                    icon="bar-chart-fill"
                    onClick={props.onOpenDetails}
                    title="Show Details"
                    data-bs-toggle="modal"
                    data-bs-target="#sessionDetailModal"
                />
                <IconButton
                    icon="trash-fill"
                    onClick={props.onDelete}
                    title="Delete"
                />
            </div>
        </li>
);
}

export default SessionListItem;