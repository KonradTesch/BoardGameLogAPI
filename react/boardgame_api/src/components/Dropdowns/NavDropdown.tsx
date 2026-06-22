import type { User } from "../../types/User.ts"
import type {ReactNode} from "react";

interface NavDropdownProps {
    user: User;
    dropdownOptions: ReactNode[];
}

function NavDropdown(props: NavDropdownProps) {
    return (
        <li className="nav-item dropdown">
            <button className="nav-link dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                {props.user.name}
            </button>
            <ul className="dropdown-menu dropdown-menu-lg-end">
                {props.dropdownOptions.map((option, index) => (
                    <li key = {index}>{option}</li>
                ))}
            </ul>
        </li>
    );
}

export default NavDropdown;