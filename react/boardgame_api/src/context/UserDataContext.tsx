import type {BoardGame} from "../types/BoardGame.ts";
import type {Player} from "../types/Player.ts";
import {createContext, type ReactNode, useCallback, useContext, useEffect, useState} from "react";
import {AuthContext} from "./AuthContext.tsx";
import {getDetailStringOrDefault} from "../util/util.ts";
import type {GameSessionRequest, GameSessionResponse} from "../types/GameSession.ts";

type RequestResult =
        | { success: true, message: string }
        | { success: false, error: string };

interface UserDateContextType {
    boardGames: BoardGame[];
    addBoardGame: (newBoardGameTite: string) => Promise<RequestResult>;
    removeBoardGame: (delBoardGameId: number) => Promise<RequestResult>;
    updateBoardGame: (updateBoardGameTite: string, updateBoardGameId: number) => Promise<RequestResult>;
    players: Player[];
    addPlayer: (newPlayerName: string) => Promise<RequestResult>;
    removePlayer: (delPlayerId: number) => Promise<RequestResult>;
    updatePlayer: (updatePlayerName: string, updatePlayerId: number) => Promise<RequestResult>;
    sessions: GameSessionResponse[];
    addSession: (newSession: GameSessionRequest) => Promise<RequestResult>;
    removeSession: (delSessionId: number) => Promise<RequestResult>;
    updateSession: (updateSession: GameSessionRequest, updateSessionId: number) => Promise<RequestResult>;
}

export const UserDataContext = createContext<UserDateContextType | null>(null)

export function UserDataProvider({ children }: { children: ReactNode}) {
    const [boardGames, setBoardGames] = useState<BoardGame[]>([]);
    const [players, setPlayers] = useState<Player[]>([]);
    const [sessions, setSessions] = useState<GameSessionResponse[]>([]);

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

    const getSessions = useCallback(async () => {
        const sessionsResponse = await fetch(`/api/user/${user?.id}/sessions/`, {
            method: "GET",
            credentials: "include"
        })

        if (sessionsResponse.ok) {
            const sessions = await sessionsResponse.json();
            setSessions(sessions);
        }
    }, [user])

    useEffect(() => {
        if (user) {
            void getPlayers();
            void getBoardGames();
            void getSessions();
        }
    }, [user, getPlayers, getBoardGames, getSessions]);

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

    const removePlayer = async  (delPlayerId: number): Promise<RequestResult> => {
        const removePlayerResponse = await fetch(`/api/user/${user?.id}/players/${delPlayerId}`, {
            method: "DELETE",
            credentials: "include"
        })


        if (removePlayerResponse.ok) {
            setPlayers(prev =>prev.filter((x: Player) => x.id !== delPlayerId))
            return {success: true, message: "Player removed successfully."};
        }
        else {
            const data = await removePlayerResponse.json();
            return {success: false, error: getDetailStringOrDefault(data.detail, "Unknown error, try again later.")};
        }

        };

    const updatePlayer = async (updatePlayerName: string, updatePlayerId: number): Promise<RequestResult> => {
        const editPlayerResponse = await fetch(`/api/user/${user?.id}/players/${updatePlayerId}`, {
            method: "PATCH",
            credentials: "include",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({"newName": updatePlayerName})
        })

        const data = await editPlayerResponse.json();

        if (editPlayerResponse.ok) {
            setPlayers(prev => prev.map(player => player.id === data.id
                    ? {...player, name: updatePlayerName}
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

    const removeBoardGame = async (delBoardGameId: number): Promise<RequestResult> => {
        const removeBoardgameResponse = await fetch(`/api/user/${user?.id}/board-games/${delBoardGameId}`, {
            method: "DELETE",
            credentials: "include"
        })


        if (removeBoardgameResponse.ok) {
            setBoardGames(prev => prev.filter((x: BoardGame) => x.id !== delBoardGameId));
            return {success: true, message: "Board game removed successfully."};
        }
        else {
            const data = await removeBoardgameResponse.json();
            return {success: false, error: getDetailStringOrDefault(data.detail, "Unknown error, try again later.")};
        }
    }

    const updateBoardGame = async (updateBoardgameTitle: string, updateBoardGameId: number): Promise<RequestResult> => {
        const editBoardGameResponse = await fetch(`/api/user/${user?.id}/board-games/${updateBoardGameId}`, {
            method: "PATCH",
            credentials: "include",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({"newTitle": updateBoardgameTitle})
        })

        const data = await editBoardGameResponse.json();

        if (editBoardGameResponse.ok) {
            setBoardGames(prev => prev.map(boardGame => boardGame.id === updateBoardGameId
                    ? {...boardGame, title: updateBoardgameTitle}
                    : boardGame
                )
            );
            return {success: true, message: "Board game edited successfully."};
        }
        else {
            return {success: false, error: getDetailStringOrDefault(data.detail, "Unknown error, try again later.")};
        }
    }

    const addSession = async (newSession: GameSessionRequest): Promise<RequestResult> => {
        const addSessionResponse = await fetch(`/api/user/${user?.id}/sessions/`, {
            method: "POST",
            credentials: "include",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(newSession)
        })

        const data = await addSessionResponse.json();
        if (addSessionResponse.ok) {
            setSessions(prev => [...prev, data as GameSessionResponse])
            return {success: true, message: "Session added successfully."};
        }
        else {
            return {success: false, error: getDetailStringOrDefault(data.detail, "Unknown error, try again later.")};
        }
    }

    const removeSession = async (delSessionId: number): Promise<RequestResult> => {
        const removeSessionResponse = await fetch(`/api/user/${user?.id}/sessions/${delSessionId}`, {
            method: "DELETE",
            credentials: "include"
        })

        if (removeSessionResponse.ok) {
            setSessions(prev => prev.filter((x: GameSessionResponse) => x.id !== delSessionId));
            return {success: true, message: "Session removed successfully."};
        }
        else {
            const data = await removeSessionResponse.json();
            return {success: false, error: getDetailStringOrDefault(data.detail, "Unknown error, try again later.")};
        }
    }

    const updateSession = async (updateSessionRequest: GameSessionRequest, updateSessionId: number): Promise<RequestResult> => {
        const updateSessionResponse = await fetch(`/api/user/${user?.id}/sessions/${updateSessionId}`, {
            method: "PATCH",
            credentials: "include",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(updateSessionRequest)
        })

        if (updateSessionResponse.ok) {
            await getSessions();
            return {success: true, message: "Session edited successfully."};
        }
        else {
            const data = await updateSessionResponse.json();
            return {success: false, error: getDetailStringOrDefault(data.detail, "Unknown error, try again later.")};
        }
    }

    return (
        <UserDataContext.Provider value={{boardGames, addBoardGame, removeBoardGame, updateBoardGame, players, addPlayer, removePlayer, updatePlayer, sessions, addSession, removeSession, updateSession}}>
            {children}
        </UserDataContext.Provider>
    )
}