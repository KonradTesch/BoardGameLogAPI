interface InfoCardProps {
    body: string;
}


function InfoCard(props: InfoCardProps) {
return (
    <div className="card" style={{minHeight: "18rem"}}>
        <div className="card-body">
            <h5 className="card-title">Card title</h5>
            <h6 className="card-subtitle mb-2 text-body-secondary">Card subtitle</h6>
            <p className="card-text">{props.body}</p>
            <a href="#" className="card-link">Card link</a>
            <a href="#" className="card-link">Another link</a>
        </div>
    </div>
);
}

export default InfoCard;