import type {ReactNode} from "react";

interface FormCardProps {
        header: ReactNode | string;
        children: ReactNode;
    }

function FormCard(props: FormCardProps) {
    return (
        <div className="card mb-4">
            <div className="card-header">
                <h5 className="mb-0">{props.header}</h5>
            </div>
            <div className="card-body">
                {props.children}
            </div>
        </div>
    );
}

export default FormCard;