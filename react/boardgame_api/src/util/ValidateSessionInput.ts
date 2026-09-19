import type {SessionPlayerFormRow} from "../types/GameSession.ts";

export interface RowErrors {
    player?: string;
    score?: string;
}

export interface SessionFormErrors {
    boardGame?: string;
    date?: string;
    duplicatePlayers?: string;
    rows: Record<string, RowErrors>;   // Key is the row id
}

export function validateSessionForm(
    boardGameId: number | null,
    date: string,
    rows: SessionPlayerFormRow[]
): SessionFormErrors {
    const errors: SessionFormErrors = { rows: {} };

    if (boardGameId === null) errors.boardGame = "Choose a boardgame";
    if (date > new Date().toLocaleDateString("sv-SE")) errors.date = "The date is in the future.";

    const seen = new Set<number>();
    for (const row of rows) {
        const rowErrors: RowErrors = {};

        if (row.playerId === null) {
            rowErrors.player = "Choose a player.";
        } else if (seen.has(row.playerId)) {
            errors.duplicatePlayers = "Table has double players.";
        } else {
            seen.add(row.playerId);
        }

        if (row.score.trim() === "") {
            rowErrors.score = "Enter a score.";
        } else if (Number.isNaN(Number(row.score))) {
            rowErrors.score = "Score is not a number.";
        }

        if (Object.keys(rowErrors).length > 0) errors.rows[row.rowId] = rowErrors;
    }

    return errors;
}