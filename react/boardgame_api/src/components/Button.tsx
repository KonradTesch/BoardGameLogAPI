import type {ReactNode} from "react";

interface SubmitButtonProps{
    variant: string;
    label: string | ReactNode;
    onClick: () => void;
    disabled?: boolean;
}

function Button(props: SubmitButtonProps) {

    return <button type="button" className={"btn btn-" + props.variant} onClick={props.onClick} disabled={props.disabled}>{props.label}</button>;
}

export default Button;