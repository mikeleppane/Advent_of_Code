import { readFileSync } from "fs";

const inputFile = __dirname + "/input.txt";

enum Direction {
  Forward = "forward",
  Up = "up",
  Down = "down",
}

interface Command {
  direction: string;
  value: number;
}

let commands: Command[] = [];

const readInputs = () => {
  try {
    const data = readFileSync(inputFile, "utf8");
    return data.split("\n").map((command) => {
      const parsedCommand = command.trim().split(" ");
      return { direction: parsedCommand[0], value: Number(parsedCommand[1]) };
    });
  } catch (error) {
    console.error(error);
    if (error instanceof Error) {
      throw new Error(error.message);
    }
    throw new Error("Unknown error occurred");
  }
};

const calculatePosition = (commands: Command[]) => {
  let horizontal_pos = 0;
  let depth = 0;
  let aim = 0;
  for (const command of commands) {
    if (command.direction === Direction.Forward) {
      horizontal_pos += command.value;
      depth += aim * command.value;
    }
    if (command.direction === Direction.Down) {
      aim += command.value;
    }
    if (command.direction === Direction.Up) {
      aim -= command.value;
    }
  }
  return [horizontal_pos, depth];
};

const solve = () => {
  commands = readInputs();
  const [horizontal_pos, depth] = calculatePosition(commands);
  console.log(`Result: ${horizontal_pos * depth}`);
};

solve();
