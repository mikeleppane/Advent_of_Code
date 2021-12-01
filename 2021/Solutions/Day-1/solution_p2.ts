import { readFileSync } from "fs";
import _ from "lodash";

const inputFile = __dirname + "/input.txt";

let depths: number[] = [];

const createThreeSumMeasurement = (data: number[]) => {
  const threeSumMeasurements: number[] = [];
  let j = 0;
  for (let i = 2; i < data.length; i += 1) {
    if (data.length - 1 - j < 2) {
      break;
    }
    threeSumMeasurements.push(_.sum(data.slice(j, i + 1)));
    j += 1;
  }
  return threeSumMeasurements;
};

try {
  const data = readFileSync(inputFile, "utf8");
  depths = data.split("\n").map((depth) => Number(depth));
} catch (error) {
  console.error(error);
}

const threeSumMeasurements = createThreeSumMeasurement(depths);

let numOfIncreases = 0;

for (let i = 1; i < threeSumMeasurements.length; i++) {
  if (threeSumMeasurements[i] > threeSumMeasurements[i - 1]) {
    numOfIncreases += 1;
  }
}

console.log(numOfIncreases);
