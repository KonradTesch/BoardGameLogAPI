import {type ReactNode, useContext} from "react";
import {AuthContext} from "../../context/AuthContext.tsx";

interface DashboardListProps {
    waitForLoading?: boolean;
    children: ReactNode;
}

function DashboardList( { waitForLoading = false, children}: DashboardListProps){

    const { isLoading } = useContext(AuthContext)!;

    return (
        <ul className="list-group list-group-flush">
                {isLoading && waitForLoading ? <p>Loading...</p> : children}
        </ul>
    );
}

export default DashboardList;