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
    addBoardGame: (newBoardGameTite: string) => Promise<RequestResult>;
    removeBoardGame: (delBoardGame: BoardGame) => Promise<RequestResult>;
    editBoardGame: (editBoardGameTite: string, editBoardGameId: number) => Promise<RequestResult>;
    players: Player[];
    addPlayer: (newPlayerName: string) => Promise<RequestResult>;
    removePlayer: (delPlayer: Player) => Promise<RequestResult>;
    editPlayer: (editPlayerName: string, editPlayerId: number) => Promise<RequestResult>;
}

export const UserDataContext = createContext<UserDateContextType | null>(null)

export function UserDataProvider({ children }: { children: ReactNode}) {
    const [boardGames, setBoardGames] = useState<BoardGame[]>([]);
    const [players, setPlayers] = useState<Player[]>([]);

    const { user } = useContext(AuthContext)!;

    const getBoardGames = useCallback(async () => {
        const boardGamesResponse = await fetch(`/api/user/${user?.id}/board-games/`, {
            method: "GET",
            credentials: "include"
        })

        if (boardGamesResponse.ok) {
            const boardGames = await boardGamesResponse.json();
            setBoardGames(boardGames);
        }
    }, [user])

    const getPlayers = useCallback(async () => {
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
            void getPlayers();
            void getBoardGames();
        }
    }, [user, getPlayers, getBoardGames]);

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

    const removePlayer = async  (delPlayer: Player): Promise<RequestResult> => {
        const removePlayerResponse = await fetch(`/api/user/${user?.id}/players/${delPlayer.id}`, {
            method: "DELETE",
            credentials: "include"
        })


        if (removePlayerResponse.ok) {
            setPlayers(prev =>prev.filter((x: Player) => x.id !== delPlayer.id))
            return {success: true, message: "Player removed successfully."};
        }
        else {
            const data = await removePlayerResponse.json();
            return {success: false, error: getDetailStringOrDefault(data.detail, "Unknown error, try again later.")};
        }

        };

    const editPlayer = async (editPlayerName: string, editPlayerId: number): Promise<RequestResult> => {
        const editPlayerResponse = await fetch(`/api/user/${user?.id}/players/${editPlayerId}`, {
            method: "PATCH",
            credentials: "include",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({"newName": editPlayerName})
        })

        const data = await editPlayerResponse.json();

        if (editPlayerResponse.ok) {
            setPlayers(prev => prev.map(player => player.id === data.id
                    ? {...player, name: editPlayerName}
                    : player
                )
            );
            return {success: true, message: "Player edited successfully."};
        }
        else {
            return {success: false, error: getDetailStringOrDefault(data.detail, "Unknown error, try again later.")};
        }
    }

    const addBoardGame = async (newBoardGameTitle: string): Promise<RequestResult> => {
        const addBoardGameResponse = await fetch(`/api/user/${user?.id}/board-games/`, {
            method: "POST",
            credentials: "include",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({"title": newBoardGameTitle})
        })

        const data = await addBoardGameResponse.json();
        if (addBoardGameResponse.ok) {
            setBoardGames(prev => [...prev, data as BoardGame]);
            return {success: true, message: "Board game added successfully."};
        }
        else {
           return {success: false, error: getDetailStringOrDefault(data.detail, "Unknown error, try again later.")};
        }

    };

    const removeBoardGame = async (delBoardGame: BoardGame): Promise<RequestResult> => {
        const removeBoardgameResponse = await fetch(`/api/user/${user?.id}/board-games/${delBoardGame.id}`, {
            method: "DELETE",
            credentials: "include"
        })


        if (removeBoardgameResponse.ok) {
            setBoardGames(prev => prev.filter((x: BoardGame) => x.id !== delBoardGame.id));
            return {success: true, message: "Board game removed successfully."};
        }
        else {
            const data = await removeBoardgameResponse.json();
            return {success: false, error: getDetailStringOrDefault(data.detail, "Unknown error, try again later.")};
        }
    }

    const editBoardGame = async (editBoardgameTitle: string, editBoardGameId: number): Promise<RequestResult> => {
        const editBoardGameResponse = await fetch(`/api/user/${user?.id}/board-games/${editBoardGameId}`, {
            method: "PATCH",
            credentials: "include",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({"newTitle": editBoardgameTitle})
        })

        const data = await editBoardGameResponse.json();

        if (editBoardGameResponse.ok) {
            setBoardGames(prev => prev.map(boardGame => boardGame.id === editBoardGameId
                    ? {...boardGame, title: editBoardgameTitle}
                    : boardGame
                )
            );
            return {success: true, message: "Board game edited successfully."};
        }
        else {
            return {success: false, error: getDetailStringOrDefault(data.detail, "Unknown error, try again later.")};
        }
    }

    return (
        <UserDataContext.Provider value={{boardGames, addBoardGame, removeBoardGame, editBoardGame, players, addPlayer, removePlayer, editPlayer}}>
            {children}
        </UserDataContext.Provider>
    )
}