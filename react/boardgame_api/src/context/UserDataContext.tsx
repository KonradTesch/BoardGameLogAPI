import type {BoardGame} from "../types/BoardGame.ts";
import type {Player} from "../types/Player.ts";
import {createContext, type ReactNode, useCallback, useContext, useEffect, useState} from "react";
import {AuthContext} from "./AuthContext.tsx";
import {getDetailStringOrDefault} from "../util/util.ts";

type RequestResult =
        | { success: true, message: string }
        | { success: false, error: string };

interface UserDateContextType {
    boardGames: BoardGame[];
    addBoardGame: (newBoardGame: BoardGame) => void;
    removeBoardGame: (delBoardGame: BoardGame) => void;
    players: Player[];
    addPlayer: (newPlayerName: string) => Promise<RequestResult>;
    removePlayer: (delPlayer: Player) => Promise<RequestResult>;
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
    }, [user])

    useEffect(() => {
        if (user) {
            void refreshPlayers();
            void refreshBoardGames();
        }
    }, [user, refreshPlayers, refreshBoardGames]);

    const addPlayer = async (newPlayerName: string): Promise<RequestResult> => {
        const addPlayerResponse = await fetch(`/api/user/${user?.id}/players/`, {
            method: "POST",
            credentials: "include",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({"name": newPlayerName})
        })

        const data = await addPlayerResponse.json();
        if (addPlayerResponse.ok) {
            setPlayers(prev => [...prev, data as Player])
            return {success: true, message: "Player added successfully."};
        }

        return {success: false, error: getDetailStringOrDefault(data.detail, "Unknown error, try again later.")};
    }

    const removePlayer = async  (delPlayer: Player) => {
        const removePlayerResponse = await fetch(`/api/user/${user.id}/players/`, {
            method: "DELETE",
            credentials: "include",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({"id": delPlayer.id})
        })

        const data = await removePlayerResponse.json();
        if (removePlayerResponse.ok) {
            setPlayers(prev =>prev.filter((x: Player) => x.id !== delPlayer.id))
            return {success: true, message: "Player removed successfully."};
        }

        return {success: false, error: getDetailStringOrDefault(data.detail, "Unknown error, try again.")};
    };

    const addBoardGame = (newBoardGame: BoardGame) => {
        const addBoardGameRequest = fetch(`/api/user/${user?.id}/board-games/`, {
            method: "POST",
            credentials: "include",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({"boardGame": newBoardGame})
        })
        setBoardGames(prev => [...prev, newBoardGame]);
    };

    const removeBoardGame = (delBoardGame: BoardGame) => {
        setBoardGames(prev => prev.filter((boardGame) => boardGame !== delBoardGame));
        void refreshBoardGames()
    }

    return (
        <UserDataContext.Provider value={{boardGames, addBoardGame, removeBoardGame, players, addPlayer, removePlayer}}>
            {children}
        </UserDataContext.Provider>
    )
}