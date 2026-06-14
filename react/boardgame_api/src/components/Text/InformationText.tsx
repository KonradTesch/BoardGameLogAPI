import type {InfoText} from "../../types/InfoText.ts";

interface InformationTextProps {
    infoText: InfoText;
}

function InformationText({ infoText: {variant = "primary", message}}: InformationTextProps) {
    return <p className={"text-" + variant}>{message}</p>;
}

export default InformationText;