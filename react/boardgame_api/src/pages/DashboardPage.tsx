import InfoCard from "../components/InfoCard.tsx";
import '../styles/DashboardPage.css';
import * as React from "react";
import PageContainer from "../components/PageContainer.tsx";
import FormCard from "../components/FormCard.tsx";


function DashboardPage() {
    return (
        <PageContainer>
            <FormCard header={<><i className="bi bi-calendar-week-fill"></i> Game Sessions</>}>
                <ul className="list-group list-group-flush">
                    <li className="list-group-item" >An item</li>
                    <li className="list-group-item">A second item</li>
                    <li className="list-group-item">A third item</li>
                    <li className="list-group-item">A fourth item</li>
                    <li className="list-group-item">And a fifth one</li>
                </ul>
            </FormCard>
            <FormCard header={<><i className="bi bi-calendar-week-fill"></i> Game Sessions</>}>
                <div className="info-card-grid" style={{"--card-width": "14rem"} as React.CSSProperties}>
                    <InfoCard
                        body="Some quick example text to build on the card title and make up the bulk of the card’s content. Lorem ipsum und so weiter."/>
                    <InfoCard body="Some quick example text to build on the card title and make up the bulk of the card’s content. "/>
                    <InfoCard body="Some quick example "/>
                    <InfoCard body="Some quick example text to build on the card title and make up the bulk of the card’s content."/>
                    <InfoCard body="Some quick example text to build on the card title and make up the bulk of the card’s content."/>
                    <InfoCard body="Some quick example text to build on the card title and make up the bulk of the card’s content."/>
                    <InfoCard body="Some quick example text to build on the card title and make up the bulk of the card’s content."/>
                    <InfoCard body="Some quick example text to build on the card title and make up the bulk of the card’s content."/>
                </div>
            </FormCard>

        </PageContainer>

    );
}

export default DashboardPage;