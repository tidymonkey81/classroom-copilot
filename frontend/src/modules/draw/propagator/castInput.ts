function castInput(input: string): any {
  // Try to parse input as JSON
  try {
    const parsedInput: any = JSON.parse(input);

    if (Array.isArray(parsedInput)) {
      return parsedInput; // array
    }

    if (parsedInput === null) {
      return null; // null
    }

    if (typeof parsedInput === "object") {
      return parsedInput; // object
    }

    if (typeof parsedInput === "boolean") {
      return parsedInput; // boolean
    }

    if (typeof parsedInput === "number") {
      return parsedInput; // integer or float
    }
  } catch (e) {
    // Not JSON parsable
  }

  // Check for boolean strings
  if (input.toLowerCase() === "true") {
    return true; // boolean
  }
  if (input.toLowerCase() === "false") {
    return false; // boolean
  }

  // Check for null string
  if (input.toLowerCase() === "null") {
    return null; // null
  }

  // Check for number
  const num: number = parseFloat(input);
  if (!isNaN(num)) {
    return num; // integer or float
  }

  // Default to string
  return input; // string
}

export default castInput;