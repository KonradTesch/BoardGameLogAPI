import IconButton from "../Button/IconButton.tsx";
import type {Player} from "../../types/Player.ts";

interface PlayerListProps {
    index: number;
    player: Player;
    onDelete: () => void;
    onOpenStats: () => void;
    onEdit: () => void;
}

function PlayerListItem(props: PlayerListProps) {
    return (
        <li className="list-group-item d-flex justify-content-between align-items-center" key={props.index}>
            <span>{props.player.name}</span>
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

export default PlayerListItem;