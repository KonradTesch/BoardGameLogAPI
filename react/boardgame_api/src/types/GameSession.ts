interface SessionPlayer {
    name: string;
    score: number;
    winner: boolean;
}

export interface GameSession {
    date: string;
    gameName: string,
    players: SessionPlayer[]
}