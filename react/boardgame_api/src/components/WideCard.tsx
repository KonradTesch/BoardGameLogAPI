import type { ReactNode} from "react";

interface WideCardProps {
    title: ReactNode;
    children: ReactNode;
}

function WideCard(props: WideCardProps){
    return (
        <div className="card" style={{minWidth: "20rem"}}>
            <h5 className="card-header">{props.title}</h5>
                <div className="card-body p-0">
                    {props.children}
                </div>
        </div>
    )
}

export default WideCard;