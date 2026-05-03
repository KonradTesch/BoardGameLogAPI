import { createContext, useState } from "react";
import type { ReactNode } from "react";

interface User {
    id: number;
    username: string;
}

interface AuthContextType {
    user: User | null;
    setUser: (user: User | null) => void;
}

export const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);

    return (
        <AuthContext.Provider value={{ user, setUser }}>
            {children}
        </AuthContext.Provider>
    );
}