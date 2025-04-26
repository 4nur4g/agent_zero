export function parseBackendData(rawStr) {
    const prefix = "data: ";
    if (!rawStr.startsWith(prefix)) {
        console.log("Raw string: ", rawStr)
        console.log("Returned: ",  JSON.parse(rawStr))
        return JSON.parse(rawStr);
    }
    ;

    try {
        const jsonString = rawStr.slice(prefix.length).trim();
        const parsed = JSON.parse(jsonString);
        return parsed;
    } catch (e) {
        console.error("Failed to parse backend data:", e);
        return null;
    }
}
