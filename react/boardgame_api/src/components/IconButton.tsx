interface IconButtonProps{
    icon: string;
    onClick?: () => void;
    title?: string;
}
function IconButton({icon, onClick, title}: IconButtonProps) {
    return (<button
        type="button"
        className={"btn btn-link p-0 text-body"}
        onClick={onClick}
        title={title}
    >
        <i className={`bi bi-${icon}`}></i>
    </button>
    );
}

export default IconButton;