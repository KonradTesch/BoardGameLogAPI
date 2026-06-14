export interface SessionPlayer {
    name: string;
    score: number;
    winner: boolean;
}

export interface GameSession {
    id: number;
    date: string;
    gameName: string,
    players: SessionPlayer[]
}