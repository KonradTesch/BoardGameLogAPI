export function getDetailStringOrDefault(detail: any, defaultValue: string): string {
    if (typeof(detail) === "string" && detail !== "") {
        return detail;
    }
    else {
        console.log(detail)
        return defaultValue;
    }
}