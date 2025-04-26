// export function parseBackendData(rawStr) {
//   const regex = /(\w+)=('(?:\\'|[^'])*'|\{.*?\}|\S+)/g;
//   const result = {};
//
//   let match;
//   while ((match = regex.exec(rawStr)) !== null) {
//     let [_, key, value] = match;
//
//     // Clean up value
//     if (value.startsWith("'") && value.endsWith("'")) {
//       value = value.slice(1, -1); // remove surrounding quotes
//     } else if (value.startsWith("{") && value.endsWith("}")) {
//       try {
//         // Try parsing object-like string
//         value = JSON.parse(
//           value.replace(/'/g, '"') // convert single quotes to double
//         );
//       } catch {
//         // If not parseable, keep as string
//       }
//     }
//
//     result[key] = value;
//   }
//
//   return result;
// }

export function parseBackendData(rawStr) {
  const prefix = "data: ";
  if (!rawStr.startsWith(prefix)) return null;

  try {
    const jsonString = rawStr.slice(prefix.length).trim();
    const parsed = JSON.parse(jsonString);
    return parsed;
  } catch (e) {
    console.error("Failed to parse backend data:", e);
    return null;
  }
}
