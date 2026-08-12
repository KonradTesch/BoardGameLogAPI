import {type ChangeEvent, useId} from "react";

interface DropdownSelectProps {
    label?: string;
    value: number | null;
    options: Map<number, string>;
    firstIsSelect?: boolean;
    onChange: (e: ChangeEvent<HTMLSelectElement>) => void;
}

function DropdownSelect({label, value, options, firstIsSelect = false, onChange}: DropdownSelectProps) {

    const id = useId();

    return (
        <>
            {label && <label htmlFor={id}>{label}</label>}
            <select className="form-select" id={id} value={String(value)} aria-label={label} onChange={onChange}>
            {firstIsSelect && <option value="">Select</option>}
            {Array.from(options).map(([id, option]) => <option value={id}>{option}</option>)}
            </select>
        </>
    );
}

export default DropdownSelect;