# Verification and unresolved evidence

## Result

The notebook executed from first to last cell under Python 3.13.6 with the documented dependencies. All eight code cells completed without errors, displayed both figures inline, and regenerated the monthly CSV, calculated-results JSON and PNG/SVG figures. Thirty-two automated checks pass. This confirms arithmetic and internal consistency of included evidence; it does not certify the complete source archive or repeat a missing upstream chain audit.

## Reconciliation

| Check | Result |
| --- | --- |
| Original reconciliation manifest | All 23 listed entries passed byte-count and SHA-256 verification before import |
| Included numeric evidence | Six files pass repository SHA-256 checks |
| Transfer rows / transaction hashes / recipients | 203 / 202 / 166 |
| Gross payouts | 2,357,719,599.756896 ONDO |
| Safe B / Safe C payouts | 1,668,727,502.067002 / 688,992,097.689894 ONDO |
| 2025 / 2026 through October | 1,359,038,783.067002 / 998,680,816.689894 ONDO |
| Calendar / active months | 22 / 20; November and December 2025 retained as zeros |
| Calendar average | 107.169072716223M ONDO, rounded to 107.169073M |
| Repeated transaction hash | Two C payouts to different recipients; both retained |
| Zero amounts | Four source rows retained in reported row count |
| Working / alternative release | 1,710,101,379.64 / 1,939,613,681.84 ONDO |
| Flat-cap 0% / 50% / 100% prices | $0.3481 / $0.2961 / $0.2576 |
| Appendix B | All 15 prices reconcile at four decimals |
| Historical ONDO-minus-BTC | About +2.011 / +0.344 percentage points, 2025 / 2026 |
| A-to-C selected funding | 725,000,000 ONDO, matches report |
| A-to-B selected funding | 1,548,558,412 ONDO; **100 below report/memo** |

Monthly chart bars reconcile exactly to the transfer sum before plotting conversion. The sensitivity curve evaluates the shared valuation formula at 201 points. Both PNGs were visually inspected for readable labels, correct units and consistent crimson/navy report styling. Expected totals are confined to regression checks; the calculation functions do not read them.

## Installation and execution

The local `.venv` was created for this task; direct dependencies were installed at the versions in `requirements.txt`. `requirements-lock.txt` records the tested transitive environment. `pip check` reports no broken requirements. A second fresh virtual environment was installed using `pip install -r requirements.txt`; all 32 checks and the entire notebook also passed from an isolated copy containing only the 25 candidate repository files, without the original attachments or local review helpers. The execution script starts the current interpreter's kernel without global registration. On this managed host, local Jupyter socket creation requires execution outside the sandbox; this is an execution-environment restriction, not a live-data dependency.

## Discrepancy investigation

An initial funding regression exposed the 100-ONDO A-to-B difference. Re-reading every supplied large-transfer row confirmed that its exact sum is 1,548,558,412, while the report and memo state 1,548,558,512. The source README labels the export as transfers of at least 1M ONDO. A missing smaller transfer may explain this coverage difference, but a 100-ONDO record is not available to test that explanation. The export remains unmodified. The selected-export subtotal is the tested value, and the report-level total remains unresolved. Core B/C payout totals are unaffected.

The market snapshot also contains a documented inconsistency: reported quote times supply is about $1,696,075,512.30 versus $1,695,052,960 reported capitalization. Using capitalization divided by circulation consistently reproduces the report's scenarios without altering either input. The missing later API response prevents authentication of that vendor observation.

## Unresolved items

1. Obtain the original later CoinGecko response and retrieval metadata to authenticate the working reference.
2. Obtain complete historical direct-transfer responses, token filtering, raw units, block numbers and log indices to repeat the source-reported chain match and account for the 100-ONDO funding gap.
3. Resolve beneficiary-specific vesting and exact January release time. Keep the five-step estimate conditional.
4. Treat B/C attribution as inferred unless independent ownership evidence is supplied. Selected funding data cannot reproduce end balances.
5. Keep destination estimates excluded until recipient histories, labels, observation windows and allocation methods can be reconstructed.
6. Review third-party numeric-data service terms and ABG's authority to redistribute the assembled exports before publication; no unrestricted license is asserted.
7. No economic realization probabilities, independently established intrinsic target, measured net free float, borrow/funding costs or executed-sale attribution are provided.

## Publication state

The repository targets the requested GitHub origin. The owner authorized publication after delivery of the local review build. The README includes explicit review, staging, commit and push instructions. Original DOCX/ZIP files, internal review notes, proprietary outputs, credentials and environments are excluded from the publication file set.
