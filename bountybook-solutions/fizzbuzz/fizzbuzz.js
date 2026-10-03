/**
 * Build the FizzBuzz sequence from 1 through n.
 *
 * Each rule is a pair [divisor, word]. For every number, rules are checked
 * in the order given. Matching words are concatenated. If nothing matches,
 * the number itself is returned as a decimal string.
 *
 * @param {number} n
 * @param {Array<[number, string]>} rules
 * @returns {string[]}
 */
export default function fizzBuzz(n, rules) {
  if (!Number.isInteger(n) || n < 1) {
    throw new Error("n must be a positive integer");
  }
  if (!Array.isArray(rules)) {
    throw new Error("rules must be an array of [divisor, word] pairs");
  }

  const output = [];
  for (let value = 1; value <= n; value += 1) {
    let label = "";
    for (const rule of rules) {
      const divisor = rule[0];
      const word = rule[1];
      if (divisor !== 0 && value % divisor === 0) {
        label += word;
      }
    }
    output.push(label.length > 0 ? label : String(value));
  }
  return output;
}
