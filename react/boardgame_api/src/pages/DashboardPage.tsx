import WideCard from "../components/WideCard.tsx";
import InfoCard from "../components/InfoCard.tsx";
import '../styles/DashboardPage.css';
import * as React from "react";


function DashboardPage() {
    return (
        <>
            <div className="flex-body">
            <WideCard title={<><i className="bi bi-calendar-week-fill"></i> Game Sessions</>}>
                <div className="info-card-grid" style={{"--card-width": "14rem"} as React.CSSProperties}>
                        <InfoCard body="Some quick example text to build on the card title and make up the bulk of the card’s content. Lorem ipsum und so weiter. "/>
                        <InfoCard body="Some quick example text to build on the card title and make up the bulk of the card’s content. "/>
                        <InfoCard body="Some quick example "/>
                        <InfoCard body="Some quick example text to build on the card title and make up the bulk of the card’s content."/>
                        <InfoCard body="Some quick example text to build on the card title and make up the bulk of the card’s content."/>
                        <InfoCard body="Some quick example text to build on the card title and make up the bulk of the card’s content."/>
                        <InfoCard body="Some quick example text to build on the card title and make up the bulk of the card’s content."/>
                        <InfoCard body="Some quick example text to build on the card title and make up the bulk of the card’s content."/>
                    </div>
            </WideCard>
            <WideCard title={<><i className="bi bi-calendar-week-fill"></i> Game Sessions</>}>
                <div className="info-card-grid" style={{"--card-width": "14rem"} as React.CSSProperties}>
                        <InfoCard body="Some quick example text to build on the card title and make up the bulk of the card’s content. Lorem ipsum und so weiter."/>
                        <InfoCard body="Some quick example text to build on the card title and make up the bulk of the card’s content. "/>
                        <InfoCard body="Some quick example "/>
                        <InfoCard body="Some quick example text to build on the card title and make up the bulk of the card’s content."/>
                        <InfoCard body="Some quick example text to build on the card title and make up the bulk of the card’s content."/>
                        <InfoCard body="Some quick example text to build on the card title and make up the bulk of the card’s content."/>
                        <InfoCard body="Some quick example text to build on the card title and make up the bulk of the card’s content."/>
                        <InfoCard body="Some quick example text to build on the card title and make up the bulk of the card’s content."/>
                    </div>
            </WideCard>
        </div>
        </>

    );
}

export default DashboardPage;