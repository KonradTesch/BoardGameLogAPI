import type {ReactNode} from "react";

interface DangerCardProps {
        header: ReactNode;
        children: ReactNode;
    }

function DangerCard(props: DangerCardProps) {
    return (
        <div className="card mb-4 border-danger">
            <div className="card-header text-danger">
                <h5 className="mb-0">{props.header}</h5>
            </div>
            <div className="card-body">
                {props.children}
            </div>
        </div>
    );
}

export default DangerCard;