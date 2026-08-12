import {type ReactNode, useId} from 'react';

interface InputFieldProps {
    label?: ReactNode;
    type: string;
    placeholder?: string;
    value?: string;
    onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onBlur?: () => void;
    disabled?: boolean;
}

function InputField(props: InputFieldProps) {
    const id = useId();

    return (
        <div>
            {props.label && <label htmlFor={id} className="form-label">{props.label}</label>}
            <input type={props.type}
                   className="form-control"
                   id={id}
                   placeholder={props.placeholder}
                   value={props.value}
                   onChange={props.onChange}
                   onBlur={props.onBlur}
                   disabled={props.disabled}
            />
        </div>
    );
}

export default InputField;