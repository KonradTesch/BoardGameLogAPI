import InfoCard from "../components/InfoCard.tsx";
import '../styles/DashboardPage.css';
import * as React from "react";
import PageContainer from "../components/PageContainer.tsx";
import FormCard from "../components/FormCard.tsx";
import {useContext, useEffect, useState} from "react";
import {AuthContext} from "../context/AuthContext.tsx";
import type {GameSession} from "../types/GameSession.ts";
import type {InfoText} from "../types/InfoText.ts";
import InformationText from "../components/InformationText.tsx";

function DashboardPage() {

    const { user } = useContext(AuthContext)!;
    const { isLoading } = useContext(AuthContext)!;

    const [ sessions, setSessions] = useState<GameSession[] | null>(null)
    const [sessionsInfo, setSessionsInfo] = useState<InfoText>({message:""})

    const getGameSession = async () => {
        const game_session = await fetch(`/api/user/${user?.id}/sessions/`, {
        method: "GET",
        credentials: "include"
        });

        if (game_session.ok) {
            const data = await game_session.json();
            setSessions(data)
        }
        else {
            setSessionsInfo({message:"Error loading game sessions.", variant: "warning"})
        }

    }

    useEffect(() => {
        if (user) {
            void getGameSession();
        }
    }, [user]);

    return (
        <PageContainer>
            <FormCard header={<><i className="bi bi-calendar-week-fill"></i> Game Sessions</>}>
                {sessionsInfo.message && <InformationText infoText={sessionsInfo} />}
                <ul className="list-group list-group-flush">
                    {isLoading ? <p>Lädt...</p> : sessions?.map((session: GameSession, index) =>(
                        <li className="list-group-item" key={index}>{session.date}</li>
                        ))}
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