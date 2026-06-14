import type {ReactNode} from "react";

interface PageHeaderProps {
        header: ReactNode;
        subHeader?: string;
    }

function PageHeader(props: PageHeaderProps) {
    return (
        <div className="mb-4">
            <h2>{props.header}</h2>
            {props.subHeader && <p className="text-body-secondary">{props.subHeader}</p> }
        </div>
    );
}

export default PageHeader;