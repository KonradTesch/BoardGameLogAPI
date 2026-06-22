import PageContainer from "../components/PageContainer.tsx";
import FormCard from "../components/Cards/FormCard.tsx";
import InputField from "../components/InputField.tsx";
import DropdownSelect from "../components/Dropdowns/DropdownSelect.tsx";

function EditSessionPage(){
return (
    <PageContainer>
        <div className="mb-4">
            <h1 className="mb-1">
                <i className="bi bi-dice-6-fill" />
                <p>Board Game Title</p>
                <DropdownSelect label="Game Title" options={["Catan", "7 Wonders", "e-Mission"]} firstIsSelect={true} />s
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