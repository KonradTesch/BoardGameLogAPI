import { createContext, useState } from "react";
import type { ReactNode } from "react";
import type { User } from "../types/User.ts";

interface AuthContextType {
    user: User | null;
    setUser: (user: User | null) => void;
    isLoading: boolean;
    setIsLoading: (isLoading: boolean) => void;
}

export const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    return (
        <AuthContext.Provider value={{ user, setUser, isLoading, setIsLoading }}>
            {children}
        </AuthContext.Provider>
    );
}