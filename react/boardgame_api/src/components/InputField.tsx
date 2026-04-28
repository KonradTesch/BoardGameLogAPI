import { useId } from 'react';

interface InputFiledProps {
    label: string;
    type: string;
    placeholder?: string;
    value: string;
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onBlur?: () => void;
}

function InputField(props: InputFiledProps) {
    const id = useId();

    return (
        <div className="mb-3">
            <label htmlFor={id} className="form-label">{props.label}</label>
            <input type={props.type}
                   className="form-control"
                   id={id}
                   placeholder={props.placeholder}
                   value={props.value}
                   onChange={props.onChange}
                   onBlur={props.onBlur}
            />
        </div>
    );
}

export default InputField;