import type {BoardGame} from "../types/BoardGame.ts";
import type {Player} from "../types/Player.ts";
import {createContext, type ReactNode, useCallback, useContext, useEffect, useState} from "react";
import {AuthContext} from "./AuthContext.tsx";

interface UserDateContextType {
    boardGames: BoardGame[];
    addBoardGame: (newBoardGame: BoardGame) => void;
    removeBoardGame: (delBoardGame: BoardGame) => void;
    players: Player[];
    addPlayer: (newPlayer: Player) => void;
    removePlayer: (delPlayer: Player) => void;
}

export const UserDataContext = createContext<UserDateContextType | null>(null)

export function UserDataProvider({ children }: { children: ReactNode}) {
    const [boardGames, setBoardGames] = useState<BoardGame[]>([]);
    const [players, setPlayers] = useState<Player[]>([]);

    const { user } = useContext(AuthContext)!;

    const refreshBoardGames = useCallback(async () => {
        const boardGamesResponse = await fetch(`/api/user/${user?.id}/board-games/`, {
            method: "GET",
            credentials: "include"
        })

        if (boardGamesResponse.ok) {
            const boardGames = await boardGamesResponse.json();
            setBoardGames(boardGames);
        }
    }, [user])

    const refreshPlayers = useCallback(async () => {
        const playersResponse = await fetch(`/api/user/${user?.id}/players/`, {
            method: "GET",
            credentials: "include"
        })

        if (playersResponse.ok) {
            const players = await playersResponse.json();
            setPlayers(players);
        }
    }, [user]);
    
    useEffect(() => {
        if (user) {
            void refreshBoardGames();
            void refreshPlayers();
        }
    }, [user, refreshPlayers, refreshBoardGames]);

    const addBoardGame = (newBoardGame: BoardGame) => {
        setBoardGames(prev => [...prev, newBoardGame]);
        void refreshBoardGames();
    };

    const removeBoardGame = (delBoardGame: BoardGame) => {
        setBoardGames(prev => prev.filter((boardGame) => boardGame !== delBoardGame));
        void refreshBoardGames()
    }

    const addPlayer = (newPlayer: Player) => {
        setPlayers(prev => [...prev, newPlayer]);
        void refreshPlayers();
    };

    const removePlayer = (delPlayer: Player) => {
        setPlayers(prev => prev.filter((player) => player !== delPlayer));
        void refreshPlayers();
    };

    return (
        <UserDataContext.Provider value={{boardGames, addBoardGame, removeBoardGame, players, addPlayer, removePlayer}}>
            {children}
        </UserDataContext.Provider>
    )
}