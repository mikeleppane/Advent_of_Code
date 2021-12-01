import { readFileSync } from "fs";

const inputFile = __dirname + "/input.txt";

let depths: number[] = [];

try {
  const data = readFileSync(inputFile, "utf8");
  depths = data.split("\n").map((depth) => Number(depth));
} catch (error) {
  console.error(error);
}

let numOfIncreases = 0;

for (let i = 1; i < depths.length; i++) {
  if (depths[i] > depths[i - 1]) {
    numOfIncreases += 1;
  }
}

console.log(numOfIncreases);
