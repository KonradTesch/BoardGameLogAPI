import IconButton from "../Button/IconButton.tsx";
import type {BoardGame} from "../../types/BoardGame.ts";
import {useState} from "react";
import Button from "../Button/Button.tsx";
import InputField from "../InputField.tsx";

interface BoardGameListProps {
    boardGame: BoardGame;
    onDelete: () => void;
    onOpenStats: () => void;
    onEdit: (editTitle: string) => void;
}

function BoardGameListItem(props: BoardGameListProps) {

    const [ editTitle, setEditTitle ] = useState<string>("");
    const [ editMode, setEditMode ] = useState<boolean>(false);

    const handleSetEditMode = () => {
        setEditMode(true);
        setEditTitle(props.boardGame.title);
    }

    const handleEditBoardGame = () => {
        setEditMode(false);

        props.onEdit(editTitle)
    }

    return (
        <li className="list-group-item d-flex justify-content-between align-items-center">
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
                            onClick={handleEditBoardGame}
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
                    onClick={handleSetEditMode}
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