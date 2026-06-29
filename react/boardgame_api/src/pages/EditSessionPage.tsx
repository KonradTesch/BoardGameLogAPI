import PageContainer from "../components/PageContainer.tsx";
import FormCard from "../components/Cards/FormCard.tsx";
import InputField from "../components/InputField.tsx";
import DropdownSelect from "../components/Dropdowns/DropdownSelect.tsx";
import {useContext, useMemo} from "react";
import {UserDataContext} from "../context/UserDataContext.tsx";
import type {BoardGame} from "../types/BoardGame.ts";

function EditSessionPage(){

    const { boardGames } = useContext(UserDataContext)!;

    const sortedBoardGames = useMemo(() => boardGames.toSorted((a, b) => a.title.localeCompare(b.title, undefined, { sensitivity: "base" })), [boardGames]);

    return (
    <PageContainer>
        <div className="mb-4">
            <h1 className="mb-1">
                <i className="bi bi-dice-6-fill" />
                <p>Board Game Title</p>
                <DropdownSelect label="Game Title" options={  new Map<number, string>(sortedBoardGames.map((boardGame: BoardGame) => [boardGame.id, boardGame.title]))} firstIsSelect={true} />s
            </h1>
            <p className="text-body-secondary mb-0">
                <i className="bi bi-calendar-event" />
                <InputField label="Date" type="date" />
            </p>
        </div>
        <FormCard header="Score">
            <p>List</p>
        </FormCard>
    </PageContainer>
);
}

export default EditSessionPage;