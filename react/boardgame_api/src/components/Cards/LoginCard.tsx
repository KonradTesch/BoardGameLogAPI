import type { ReactNode } from 'react';

interface LoginCardProps {
    isLogin: boolean;
    children: ReactNode;
}

function LoginCard(props: LoginCardProps) {
    return (
        <div className="container min-vh-100 d-flex align-items-center justify-content-center">
            <div className="col-12 col-sm-8 col-md-6 col-lg-4">
                <div className="card">
                    <div className="card-header text-center">
                        <h4><i className={props.isLogin ?  "bi bi-box-arrow-in-right" : "bi bi-person-square"} /> {props.isLogin ? "Login" : "Register"}</h4>
                    </div>
                    <div className="card-body">
                        {props.children}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default LoginCard;