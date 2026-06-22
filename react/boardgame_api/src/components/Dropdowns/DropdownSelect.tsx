interface DropdownSelectProps {
    label: string;
    options: Map<number, string>;
    firstIsSelect?: boolean;
}

function DropdownSelect({label, options, firstIsSelect = false}: DropdownSelectProps) {
    return (
        <select className="form-select" aria-label={label}>
            {firstIsSelect && <option value="">Select</option>}
            {Array.from(options).map(([index, option]) => <option value={index}>{option}</option>)}
        </select>
    );
}

export default DropdownSelect;