# Test: create-data-audit-prompt-block

input:
  The prompt block in procedures/create-data-audit-prompt-block.md, pasted
  verbatim, followed by the sample messy data in tests/sample-messy-data.csv
  (13 data rows, all synthetic and fictional: mixed date formats, duplicate
  customer and region spellings, mixed currency formats, one missing date,
  one missing amount, one negative amount).

run:
  Start a conversation, paste the block exactly as written, then paste the
  sample data after the DATA marker. For the recorded run below, the executor
  was Claude (an LLM agent) on 2026-09-07, using the exact block text and the
  exact sample file. Live re-runs should use free Copilot as the procedure
  intends; any capable chat model should be checked the same way.

expect:
  The output contains exactly the five declared headings, in order, with no
  extra sections; every problem quoted exists verbatim in the sample; no row,
  column, or value appears in the output that is absent from the sample.

last_run: 2026-09-07
last_result: pass
notes:
  The recorded run was executed by an LLM agent, not a person and not a
  deterministic script — reruns may vary in which problems get flagged and in
  wording, because the model is nondeterministic. The pass is scoped to the
  two things the expect line states: format conformance and no invention.
  Fragility: if the block text is later edited, this record no longer
  describes the current block; re-run the test and update this file.

## Recorded output (2026-09-07)

```text
## Column inventory
- Date — 13 rows; one blank (row 10); three formats present (2026-01-05; 05/02/2026; 2026.01.12).
- Customer — 13 rows; case and spacing variants (" acme corp " vs "Acme Corp"; "GAMMA INC" vs "Gamma Inc"; "Delta Co." vs "Delta Co").
- Region — 13 rows; case variants (North/north/WEST) and spelling variants (north-east/northeast).
- Amount — 13 rows; one blank (row 5); one negative (-500); mixed formats (1200; "$1,300"; "1 100"; "1,050"; "USD 900"; leading space in " 750").

## Problems found
1. Date, row 3: "05/02/2026" — day/month order ambiguous against the ISO format used elsewhere.
2. Date, row 4: "2026.01.12" — dot-separated, inconsistent with the ISO format used elsewhere.
3. Date, row 10: blank — no date present.
4. Customer, row 3: " acme corp " — leading and trailing spaces, lowercase; duplicate of "Acme Corp" (rows 2 and 10).
5. Customer, row 7: "GAMMA INC" — uppercase duplicate of "Gamma Inc" (row 6).
6. Customer, row 9: "Delta Co." — trailing period; duplicate of "Delta Co" (row 8).
7. Region, rows 3, 10, 11: "north" — lowercase duplicate of "North".
8. Region, row 9: "WEST" — uppercase duplicate of "West" (row 8).
9. Region, rows 11 and 12: "north-east" and "northeast" — the same region spelled two ways.
10. Amount, row 3: "$1,300" — currency symbol and comma separator inside the value.
11. Amount, row 7: " 750" — leading space.
12. Amount, row 8: "1 100" — space used as a thousands separator.
13. Amount, row 13: "1,050" — comma separator, inconsistent with the plain numbers elsewhere.
14. Amount, row 14: "USD 900" — text prefix inside a numeric field.
15. Amount, row 6: "-500" — the only negative value; possibly a legitimate credit, flagged rather than assumed.

## Clean columns
- No column is fully clean; every column has at least one problem listed above.

## Suggested manual fixes
- Normalize all dates to YYYY-MM-DD; confirm row 3 with the data owner first.
- Trim spaces on Customer (row 3) and Amount (row 7); standardize Customer case and merge the duplicates (rows 3, 7, 9).
- Standardize Region casing (rows 3, 9) and choose one spelling for north-east/northeast (rows 11, 12).
- Convert Amount to plain numbers: strip "$" (row 3), separators (rows 8, 13), and "USD" (row 14); keep -500 only if confirmed as a credit.
- Complete or exclude the missing Date (row 10) and missing Amount (row 5).

## Questions for the data owner
1. Is "05/02/2026" the fifth of February or the second of May?
2. Should "-500" stay negative (a credit), or is it a sign error?
3. Are "north-east" and "northeast" the same region?
4. Should rows with a missing Date or Amount be completed, excluded, or kept as-is?
```

Format check against expect: exactly the five declared headings, in order, no
extra sections — conformant. Every quoted value was checked against
tests/sample-messy-data.csv; all exist verbatim, and no row, column, or value
in the output is absent from the sample — conformant. PASS.
