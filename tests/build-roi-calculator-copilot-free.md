# Test: build-roi-calculator-copilot-free

input:
  The prompt block in procedures/build-roi-calculator-copilot-free.md, and the
  reference artifact it specifies: tests/build-roi-calculator-copilot-free.html
  (authored to that spec, since a live model session cannot be captured here).

run:
  Headless render plus computation check. The harness page
  tests/roi-calculator-test-harness.html loads the artifact in an iframe, sets
  the known-case inputs (one-time cost 6000; hours saved 300; hourly rate 50;
  recurring cost 3000), calls calculate(), and asserts the three outputs:

      "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" \
        --headless=new --disable-gpu --no-first-run --no-default-browser-check \
        --allow-file-access-from-files \
        --user-data-dir="<any temp dir>" \
        --virtual-time-budget=5000 --dump-dom \
        "file:///<repo>/tests/roi-calculator-test-harness.html"

  PASS when the dumped DOM contains data-test-result="PASS" and RESULT: PASS.
  If the installed Edge rejects --headless=new, use --headless.

expect:
  The harness reports PASS on all checks: the artifact loads in the iframe;
  the known case yields annual net benefit $12,000.00, payback 6.0 months, and
  year-one ROI 100.0%; the artifact exposes the global calculate() function
  named in the procedure's prompt; and the artifact contains no external src
  or href references.

last_run: 2026-09-07
last_result: pass
notes:
  Scope of method: script-verified — this test verifies the reference artifact, in
  other words the specification the procedure's prompt asks the model to meet.
  It does NOT verify that a live free-Copilot session emits an artifact
  meeting that spec; the model is nondeterministic, and that part of the
  procedure is verified the first time a person runs it end to end. Fragility:
  same-origin iframe access from file:// needs --allow-file-access-from-files;
  the harness ids are coupled to the ids the procedure's prompt mandates (they
  are mandated precisely so the test can attach); the Edge path shown is one
  machine's, adjust per machine.

## Recorded run (2026-09-07)

Executed with the command above (Edge 2.55-era headless, --headless=new).
Dumped DOM contained:

- data-test-result="PASS"
- RESULT: PASS
- PASS artifact loads in iframe with expected inputs
- PASS annual net benefit is $12,000.00
- PASS payback is 6.0 months
- PASS year-one ROI is 100.0%
- PASS artifact exposes global calculate()
- PASS artifact has no external src or href references
