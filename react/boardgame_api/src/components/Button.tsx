import type {ReactNode} from "react";
import type {BootstrapVariant} from "../types/BootstrapVariant.ts";

interface ButtonProps{
    label: ReactNode;
    onClick?: () => void;
    variant?: BootstrapVariant;
    disabled?: boolean;
    [key: string]: unknown;
}

function Button({label, onClick, variant = "primary", disabled, ...rest}: ButtonProps) {

    return (<button
        type="button"
        className={"btn btn-" + variant}
        onClick={onClick}
        disabled={disabled}
        {...rest}
    >
        {label}
    </button>);
}

export default Button;