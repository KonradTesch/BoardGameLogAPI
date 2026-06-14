import type {ReactNode} from "react";

interface ContentModalProps {
    id: string;
    title: string;
    footer: ReactNode;
    children: ReactNode;
}

function ContentModal({id, title, footer, children}: ContentModalProps) {
    return (
        <div className="modal fade" id={id} tabIndex={-1} aria-labelledby={id + "-header"} aria-hidden="true">
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header">
                        <h1 className="modal-title fs-5" id={id + "-header"}>{title}</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div className="modal-body">
                        {children}
                    </div>
                    <div className="modal-footer">
                        {footer}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ContentModal;