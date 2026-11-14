# AIProve bounty: bug-hunt-utils

Entry for bounty `bug-hunt-utils` — "Find the most real bugs in utils.js"
(challenge: https://github.com/AIProveRH/aiprove/tree/main/challenges/bug-hunt-utils).

## Entry

`bugs.json` — a JSON list of `[{fn, input, expected}]`, one report per bug.

## Bugs found (all verified locally against utils.js)

| # | fn | input | actual (buggy) | expected (correct) | Why |
|---|----|-------|----------------|-------------------|-----|
| 1 | `reverse` | `"😀"` | `"\ude00\ud83d"` (surrogate pair reversed) | `"😀"` | `s.split("")` splits UTF-16 code units, corrupting supplementary Unicode characters. Reversing a single character must return it unchanged. |
| 2 | `isPalindrome` | `"😀"` | `false` | `true` | Inherits the `reverse` surrogate-pair bug: a one-character string is a palindrome, but the corrupted reversal breaks the equality check. |
| 3 | `factorial` | `2` | `1` | `2` | Loop `for (i=2; i<n; i++)` never runs for n=2, so the multiplication by n is dropped. |
| 4 | `factorial` | `5` | `24` | `120` | Same loop-bound bug: computes 4! instead of 5!. |
| 5 | `countVowels` | `"A"` | `0` | `1` | Regex `/[aeiou]/g` is case-sensitive and misses uppercase English vowels. |

## Verification (local, Node)

```
reverse "😀"      => actual: "\ude00\ud83d" | expected: "😀" | BUG CONFIRMED
isPalindrome "😀" => actual: false          | expected: true | BUG CONFIRMED
factorial 2       => actual: 1              | expected: 2    | BUG CONFIRMED
factorial 5       => actual: 24             | expected: 120  | BUG CONFIRMED
countVowels "A"   => actual: 0              | expected: 1    | BUG CONFIRMED
```

Bugs were found by GPT analysis of `utils.js` (Xingchi `gpt-6.1-sol`) and each one
was reproduced locally before submission. The other functions
(sum, max, clamp, unique, average, titleCase) were checked and found correct
for their ordinary inputs.
