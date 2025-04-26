export function parseBackendData(rawStr) {
  const regex = /(\w+)=('(?:\\'|[^'])*'|\{.*?\}|\S+)/g;
  const result = {};

  let match;
  while ((match = regex.exec(rawStr)) !== null) {
    let [_, key, value] = match;

    // Clean up value
    if (value.startsWith("'") && value.endsWith("'")) {
      value = value.slice(1, -1); // remove surrounding quotes
    } else if (value.startsWith("{") && value.endsWith("}")) {
      try {
        // Try parsing object-like string
        value = JSON.parse(
          value.replace(/'/g, '"') // convert single quotes to double
        );
      } catch {
        // If not parseable, keep as string
      }
    }

    result[key] = value;
  }

  return result;
}
