import IconButton from "../Button/IconButton.tsx";
import type {Player} from "../../types/Player.ts";
import {useState} from "react";
import InputField from "../InputField.tsx";
import Button from "../Button/Button.tsx";

interface PlayerListProps {
    index: number;
    player: Player;
    onDelete: () => void;
    onOpenStats: () => void;
    onEdit: (editName: string) => void;
}

function PlayerListItem(props: PlayerListProps) {

    const [editMode, setEditMode] = useState<boolean>(false);
    const [editPlayerName, setEditPlayerName] = useState<string>("");

    const handleEditMode = () => {
        setEditMode(true);
        setEditPlayerName(props.player.name)
    }

    return (
        <li className="list-group-item d-flex justify-content-between align-items-center" key={props.index}>
            {editMode
                ?
                <>
                    <InputField
                    type="text"
                    value={editPlayerName}
                    onChange={(e) => setEditPlayerName(e.target.value)}
                    />
                    <div className="d-flex gap-2">
                        <Button
                            label="Cancel"
                            onClick={() => setEditMode(false)}
                            variant={"secondary"}
                        />
                        <Button
                            label="Edit"
                            onClick={() => props.onEdit(editPlayerName)}
                            variant={"primary"}
                            />
                    </div>
                </>
                    :
                <>
                    <span>{props.player.name}</span>
                    <div className="d-flex gap-2">
                        <IconButton
                            icon="pencil-fill"
                            onClick={handleEditMode}
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
                </>
            }

        </li>
);
}

export default PlayerListItem;