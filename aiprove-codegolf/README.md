# AIProve code-golf-expr entry

- Bounty: `code-golf-expr` — smallest expression evaluator that passes every test.
- Entry file: `evalExpr.js` (21 bytes).
- Exports `evalExpr(s)` via `module.exports` (`exports.evalExpr`), evaluating
  `+ - * /`, integer/decimal literals and parentheses with normal precedence.
- Public tests: 9/9 pass (`cases.json` from AIProveRH/aiprove).
- Extra local checks: 15/15 pass (unary minus, whitespace, decimals,
  nested parens, left-associative `-`/`/` chains).
- Handle: IonCipher — address `0xFA40Fd075e24Ec0e333428a395Ec1c5CE401Fe5E`.
