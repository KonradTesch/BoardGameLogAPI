import IconButton from "../Button/IconButton.tsx";
import type {BoardGame} from "../../types/BoardGame.ts";

interface BoardGameListProps {
    index: number;
    boardGame: BoardGame;
    onDelete: () => void;
    onOpenStats: () => void;
    onEdit: () => void;
}

function BoardGameListItem(props: BoardGameListProps) {
    return (
        <li className="list-group-item d-flex justify-content-between align-items-center" key={props.index}>
            <span>{props.boardGame.title}</span>
            <div className="d-flex gap-2">
                <IconButton
                    icon="pencil-fill"
                    onClick={props.onEdit}
                    title="Edit"
                />
                <IconButton
                    icon="bar-chart-fill"
                    onClick={props.onOpenStats}
                    title="Show Details"
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

export default BoardGameListItem;