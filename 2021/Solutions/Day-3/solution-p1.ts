import { readFileSync } from "fs";

const inputFile = __dirname + "/input.txt";

let diagnosticReport: number[][] = [];

const readInputs = () => {
  try {
    const data = readFileSync(inputFile, "utf8");
    return data.split("\n").map((line) => {
      return line
        .trim()
        .split("")
        .map((bit) => Number(bit));
    });
  } catch (error) {
    console.error(error);
    if (error instanceof Error) {
      throw new Error(error.message);
    }
    throw new Error("Unknown error occurred");
  }
};

const generateBinaryNumbers = (diagnosticReport: number[][]) => {
  let i = 0;
  let mostCommonBit = "";
  let leastCommonBit = "";
  let commonBit = { zeros: 0, ones: 0 };
  for (i; i < diagnosticReport[0].length; i += 1) {
    commonBit = { zeros: 0, ones: 0 };
    for (let j = 0; j < diagnosticReport.length; j += 1) {
      if (diagnosticReport[j][i] === 1) {
        commonBit.ones += 1;
      } else {
        commonBit.zeros += 1;
      }
    }
    mostCommonBit += commonBit.ones > commonBit.zeros ? "1" : "0";
    leastCommonBit += commonBit.ones > commonBit.zeros ? "0" : "1";
  }
  return [parseInt(mostCommonBit, 2), parseInt(leastCommonBit, 2)];
};

const solve = () => {
  diagnosticReport = readInputs();
  const [gammaRate, epsilonRate] = generateBinaryNumbers(diagnosticReport);
  console.log(`Result: ${gammaRate * epsilonRate}`);
};

solve();
