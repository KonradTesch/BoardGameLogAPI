import type {Player} from "../../types/Player.ts";
import {AuthContext} from "../../context/AuthContext.tsx";
import PlayerListItem from "./PlayerListItem.tsx";
import {useContext} from "react";

interface PlayerListProps {
    players: Player[];
    playersToDelete: Player[];
    onDelete: (player: Player) => void;
    onOpenStats: (player:Player) => void;
    onEditPlayer: (player: Player) => void;
    waitForLoading?: boolean;
}

function PlayerList({players, playersToDelete, onDelete, onOpenStats, onEditPlayer, waitForLoading = false}: PlayerListProps ) {

    const { isLoading } = useContext(AuthContext)!;

    return (
        <ul className="list-group list-group-flush">
                {isLoading && waitForLoading ? <p>Loading...</p> : players?.map((player: Player, index) =>(
                    ( !playersToDelete.includes(player) &&
                    <PlayerListItem
                        index={index}
                        player={player}
                        onDelete={() => onDelete(player)}
                        onOpenStats={() => onOpenStats(player)}
                        onEdit={() => onEditPlayer(player)}
                    />)
                    ))}
        </ul>
    );
}

export default PlayerList;