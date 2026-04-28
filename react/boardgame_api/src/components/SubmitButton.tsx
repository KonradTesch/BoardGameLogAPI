interface SubmitButtonProps{
    label: string;
    onClick: () => void;
    disabled?: boolean;
}

function SubmitButton(props: SubmitButtonProps) {

    return <button type="button" className="btn btn-primary" onClick={props.onClick} disabled={props.disabled}>{props.label}</button>;
}

export default SubmitButton;