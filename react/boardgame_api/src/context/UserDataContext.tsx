import type {BoardGame} from "../types/BoardGame.ts";
import type {Player} from "../types/Player.ts";
import {createContext, type ReactNode, useState} from "react";

interface UserDateContextType {
    boardGames: BoardGame[];
    addBoardGame: (newBoardGame: BoardGame) => void;
    removeBoardGame: (delBoardGame: BoardGame) => void;
    players: Player[];
    addPlayer: (newPlayer: Player) => void;
    removePlayer: (delPlayer: Player) => void;
}

export const UserDataContext = createContext<UserDateContextType | null>(null)

export function UserDateProvider({ children }: { children: ReactNode}) {
    const [boardGames, setBoardGames] = useState<BoardGame[]>([]);
    const [players, setPlayers] = useState<Player[]>([]);

    const addBoardGame = (newBoardGame: BoardGame) => {
        setBoardGames(prev => [...prev, newBoardGame]);
    };

    const removeBoardGame = (delBoardGame: BoardGame) => {
        setBoardGames(prev => prev.filter((boardGame) => boardGame !== delBoardGame));
    }

    const addPlayer = (newPlayer: Player) => {
        setPlayers(prev => [...prev, newPlayer]);
    };

    const removePlayer = (delPlayer: Player) => {
        setPlayers(prev => prev.filter((player) => player !== delPlayer));
    };

    return (
        <UserDataContext.Provider value={{boardGames, addBoardGame, removeBoardGame, players, addPlayer, removePlayer}}>
            {children}
        </UserDataContext.Provider>
    )
}