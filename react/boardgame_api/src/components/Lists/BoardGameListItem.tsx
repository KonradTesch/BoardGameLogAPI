import IconButton from "../Button/IconButton.tsx";
import type {BoardGame} from "../../types/BoardGame.ts";
import {useState} from "react";
import Button from "../Button/Button.tsx";
import InputField from "../InputField.tsx";

interface BoardGameListProps {
    index: number;
    boardGame: BoardGame;
    onDelete: () => void;
    onOpenStats: () => void;
    onEdit: (editTitle: string) => void;
}

function BoardGameListItem(props: BoardGameListProps) {

    const [ editTitle, setEditTitle ] = useState<string>("");
    const [ editMode, setEditMode ] = useState<boolean>(false);

    const handleEditMode = () => {
        setEditMode(true);
        setEditTitle(props.boardGame.title);
    }

    return (
        <li className="list-group-item d-flex justify-content-between align-items-center" key={props.index}>
            {editMode
                ?
                <>
                    <InputField
                    type="text"
                    value={editTitle}
                    onChange={(e) => setEditTitle(e.target.value)}
                    />
                    <div className="d-flex gap-2">
                        <Button
                            label="Cancel"
                            onClick={() => setEditMode(false)}
                            variant={"secondary"}
                        />
                        <Button
                            label="Edit"
                            onClick={() => props.onEdit(editTitle)}
                            variant={"primary"}
                            />
                    </div>
                </>
                :
                <>
                    <span>{props.boardGame.title}</span>
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
                </>}
        </li>
);
}

export default BoardGameListItem;