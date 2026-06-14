interface IconButtonProps{
    icon: string;
    onClick?: () => void;
    title?: string;
    [key: string]: unknown;
}
function IconButton({icon, onClick, title, ...rest}: IconButtonProps) {
    return (<button
        type="button"
        className={"btn btn-link p-0 text-body"}
        onClick={onClick}
        title={title}
        {...rest}
    >
        <i className={`bi bi-${icon}`}></i>
    </button>
    );
}

export default IconButton;