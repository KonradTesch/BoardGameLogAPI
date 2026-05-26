import type {ReactNode} from "react";

interface PageContainerProps {
    children: ReactNode;
}

function PageContainer({ children } : PageContainerProps) {
    return (
        <div className="container py-5">
            <div className="row justify-content-center">
                <div className="col-12 col-lg-8">
                    {children}
                </div>
            </div>
        </div>
    );
}

export default PageContainer;