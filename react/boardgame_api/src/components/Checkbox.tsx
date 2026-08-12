import {type ChangeEvent, useId} from "react";

interface CheckBoxProps {
    label?: string;
    value: boolean;
    onChange?: (e: ChangeEvent<HTMLInputElement>) => void;
}

function Checkbox(props: CheckBoxProps) {

    const id = useId();

    return (
        <div className="form-check">
            <input className="form-check-input" type="checkbox" value="" id={id} onChange={props.onChange} />
            {props.label &&
            <label className="form-check-label" htmlFor={id}>
                {props.label}
            </label>
            }
        </div>
    );
}

export default Checkbox;