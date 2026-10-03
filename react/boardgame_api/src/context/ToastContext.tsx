import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from "react";
import { createPortal } from "react-dom";
import type { InfoText } from "../types/InfoText.ts";

interface Toast extends InfoText {
    id: string;
}

interface ToastContextType {
    showToast: (toast: InfoText, duration?: number) => void;
}

const ToastContext = createContext<ToastContextType | null>(null);

export function ToastProvider({ children }: { children: ReactNode }) {
    const [toasts, setToasts] = useState<Toast[]>([]);

    const removeToast = useCallback((id: string) => {
        setToasts(prev => prev.filter(toast => toast.id !== id));
    }, []);

    const showToast = useCallback((toast: InfoText, duration = 5000) => {
        const id = crypto.randomUUID();
        setToasts(prev => [...prev, { ...toast, id }]);
        setTimeout(() => removeToast(id), duration);
    }, [removeToast]);

    const value = useMemo(() => ({ showToast }), [showToast]);

    return (
        <ToastContext.Provider value={value}>
            {children}
            {createPortal(
                <div className="toast-container position-fixed bottom-0 end-0 p-3">
                    {toasts.map(toast => (
                        <div
                            key={toast.id}
                            className={`toast show text-bg-${toast.variant ?? "primary"}`}
                            role="alert"
                            aria-live="assertive"
                            aria-atomic="true"
                        >
                            <div className="d-flex">
                                <div className="toast-body">{toast.message}</div>
                                <button
                                    type="button"
                                    className="btn-close me-2 m-auto"
                                    aria-label="Close"
                                    onClick={() => removeToast(toast.id)}
                                />
                            </div>
                        </div>
                    ))}
                </div>,
                document.body
            )}
        </ToastContext.Provider>
    );
}

export function useToast(): ToastContextType {
    const context = useContext(ToastContext);
    if (!context) throw new Error("useToast must be used within a ToastProvider");
    return context;
}