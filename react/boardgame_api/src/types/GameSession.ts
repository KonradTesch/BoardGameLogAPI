import type {InfoText} from "./InfoText.ts";

export interface SessionPlayerResponse {
    playerId: number;
    playerName: string;
    score: number;
    winner: boolean;
}

export interface GameSessionResponse {
    id: number;
    date: string;
    gameId: number;
    gameName: string,
    sessionPlayers: SessionPlayerResponse[]
}

export interface SessionPlayerRequest {
    playerId: number;
    score: number;
    winner: boolean;
}

export interface GameSessionRequest {
    date: string;
    gameId: number;
    sessionPlayers: SessionPlayerRequest[]
}

export interface SessionPlayerFormRow {
    rowId: string;
    playerId: number | null;
    score: number;
    winner: boolean;
    info?: InfoText;
}