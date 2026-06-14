import { createPortal} from "react-dom";
import type {ReactNode} from "react";
import Button from "../Button/Button.tsx";
import type {BootstrapVariant} from "../../types/BootstrapVariant.ts";

interface ConfirmModalProps{
    id: string;
    header: ReactNode;
    body: ReactNode,
    onSubmit: () => void;
    confirmButtonVariant?: BootstrapVariant;
}

function ConfirmModal({id, header, body, onSubmit, confirmButtonVariant = "primary"}: ConfirmModalProps) {
    return createPortal(
        <div className="modal fade" id={id} data-bs-backdrop="static" data-bs-keyboard="false" tabIndex={-1} aria-labelledby={{id} + "-label"} aria-hidden="true">
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header">
                        <h1 className="modal-title fs-5" id={id + "-header"}>{header}</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div className="modal-body">
                        {body}
                    </div>
                    <div className="modal-footer">
                        <Button
                            variant="secondary"
                            label="Close"
                            data-bs-dismiss="modal"/>
                        <Button
                            variant={confirmButtonVariant}
                            label="Confirm"
                            onClick={onSubmit}
                            data-bs-dismiss="modal"
                        />
                    </div>
                </div>
            </div>
        </div>,
        document.body
    );
}

export default ConfirmModal;