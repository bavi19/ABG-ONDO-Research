# ONDO research methodology

## Scope and evidence status

This repository reproduces the numerical exhibits in ABG's supplied draft report, including Appendices A and B. The research cutoff is November 8, 2026 Pacific; the source set labels November 9 reads of historical information separately. Current website checks help locate primary documentation but do not replace the frozen cutoff inputs.

Observed export fields, inferred attribution and modeled outcomes are kept distinct. The source decision memo reports 203 rows matched historical Blockscout records through block 26,375,966. That full response set is absent from the attachments. Local verification establishes exact reconciliation of the supplied data, not a repeated independent blockchain audit.

## Wallet attribution and funding

| Safe | Ethereum address | Status |
| --- | --- | --- |
| A | `0x677fd4ed8ae623f2f625deb2d64f2070e46ca1a1` | Officially attributed in the source set |
| B | `0x524083970c7a1e62fbaa61d38781f87a4f191fd0` | Foundation-linked, inferred |
| C | `0xea5785e1727de2ba2cefd102cb2dd91e018675e1` | Foundation-linked, inferred |

The official disclosure identifies A's locked holdings. Funding from A and related activity support a B/C link, without proving legal ownership or beneficial control. The source set reports no signer overlap with A. Funding subtotals recomputed from the supplied selected large-transfer CSV are 1,548,558,412 ONDO A-to-B and 725,000,000 A-to-C. The B subtotal is **100 ONDO below** the report/memo's 1,548,558,512. The source README describes this CSV as transfers of at least 1M ONDO, so it cannot establish a complete funding total. Missing small-transfer coverage is a plausible explanation, but the missing 100-ONDO record was not supplied and is not invented here. That selection does not establish complete inflows or reconcile end balances; the memo's net-balance claims are not certified by this repository.

## Transfer definition and precision

The authoritative token is Ethereum ONDO, `0xfAbA6f8e4a5E8Ab82F62fe7C39859FA577269BE3`, 18 decimals. The source export contains decimal ONDO amounts rounded to six places. Python `Decimal` sums their strings without binary floating-point drift. It cannot recover the missing 18-decimal raw units.

A transfer row is one supplied outgoing B/C record. The published 203-row definition retains four zero-amount records. Unique recipients are lowercased addresses. Unique transaction hashes count transactions rather than events. Hash `0x5d689f93586164fe2c3323df9f089fdf9bce864ad2c5eb7cf431e7b4a8453bdd` contains two C payouts of 15,040,950 and 22,594,114.45 ONDO to different recipients. Deduplication by hash alone is incorrect.

The export lacks block numbers, log indices, raw integer amounts, an explicit sender address column and a token-contract column. Safe letters map to documented addresses. Canonical event uniqueness and exact token filtering cannot be independently verified from these fields; the composite uniqueness check detects identical supplied rows only.

The published transaction export's SHA-256 is `af11b1bec6b1aa04241ed68420bfdd9a23cbe0dc99123e967cebcf654544ed7b`. The repository projects seven core columns and preserves every field string and row order. It consequently has a different file hash, recorded alongside the original in `data/provenance.json`. Downstream estimates are removed rather than redistributed as verified records.

## Calendar aggregation

Group `timestamp_utc` by YYYY-MM and Safe. Validate the existing month column against the timestamp. Initialize January 2025 through October 2026 inclusive before summing: 22 months, 20 with payouts, two zero months. Combined gross payouts divided by 22 gives the calendar average; division by 20 gives the active-month average. Twenty-two nonempty month/Safe combinations are not 22 active months.

All monthly totals and bars derive from transaction amounts, not rounded monthly source columns. Chart unit conversion to millions occurs after aggregation; floating-point conversion is restricted to plotting. Gross movement may reflect previously circulating or recycled tokens. It is not net free float or selling. January–October 2026 payouts are lower than the same 2025 period.

## Working January 2027 schedule

The Foundation proposal supplies allocations of 5,210,869,545 ecosystem, 3,300,000,000 protocol-development and 1,290,246,044 private-sale ONDO. It describes 24% of ecosystem released initially and annual steps at months 12/24/36/48/60. Implement the working convention as:

1. Use exact published category allocations.
2. Retain 76% of ecosystem after the initial 24%.
3. Divide that ecosystem remainder by five: 792,052,170.84.
4. Divide protocol development and private sales by five: 660,000,000 and 258,049,208.80.
5. Sum the components: 1,710,101,379.64 ONDO.

Alternative division of development/private over four gives 1,939,613,681.84 ONDO. It is an alternative interpretation of the same schedule. Public one-year-lock/48-month-release wording and beneficiary-specific documents are not fully reconciled. The source package's reported aggregate supply jump is supporting context, not a signed vesting contract. Exact January 17/18 timing remains unresolved; use the January 2027 release window.

Scheduled transferability is distinct from actual wallet transfers, vendor circulation, economic float, exchange deposits and executed sales. The schedule is not mechanically multiplied by a historical distribution average.

## Reference and valuation formula

`data/assumptions.json` records the report's package-reported November 8, 2026 23:36:53 PST working reference: cap C = $1,695,052,960; circulation S = 4,869,330,647; quoted price $0.348318. The later response body was not included. The older archive's CoinGecko response is a different observation and cannot authenticate the reference. This repository does not substitute a current live price.

C / S = $0.3481080015, whereas quote × S = $1,696,075,512.30, about 0.0603% above C. All scenario returns use the internally consistent cap-implied price.

For working release U, realization r and cap change g:

`P(r,g) = C × (1 + g) / (S + U × r)`

Evaluate r = 0%, 50%, 100% and g = −25%, 0%, +25%, +50%, +100% to reproduce all 15 Appendix B cells. The sensitivity curve evaluates the same formula at 201 fractions. Full realization gives modeled circulation 6,579,432,026.64 ONDO. Constant price would require cap growth of U / S ≈ 35.12%; that market-value change is not a dollar-for-dollar cash-inflow estimate.

Do not add gross historical or forecast Foundation distributions to U: distributions can draw from existing circulation or the same tranche. No effective-float denominator is mixed with vendor circulating capitalization. No scenario probabilities or intrinsic-value claim are made.

Reverse valuation at a 20× annual holder-cash-flow multiple gives C / 20 ≈ $84.753M reaching holders. A 40% capture assumption requires approximately $211.882M of defined net source earnings. Revenue, earnings and cash distributions are different; expenses, taxes, ownership and enforceability matter. These are assumption sensitivities rather than measured investor expectations.

## Historical comparison

Saved Coinbase daily candles use `[time, low, high, open, close, volume]`. Compute each asset's close-to-close return from January 17 to February 17 for the January 18 anniversary, i.e. offsets [−1,+30] and 31 intervals. Subtract BTC's simple return from ONDO's simple return. The results are about +2.011 and +0.344 percentage points in 2025 and 2026. They are not beta-adjusted alpha or proof of a causal unlock effect. No additional event-window selection is used to favor the thesis.

## Exclusions and reproducibility boundary

The source monthly script depends on missing `B_transfers_rows.json`, `blockscout_0xea57_tokentx.json`, `hop1_recipient_tokentx.json` and `etherscan_labels.json`, as well as absolute `/workspace` paths. Our replacement aggregates the included core CSV offline and does not execute that script. Its destination allocation also lacks a complete opening-balance/all-inflow fungible-token ledger.

Exchange-routing percentages, insider DEX-selling allegations, private research summaries, AI conversations and entire archives are excluded. No live blockchain verification is implemented. Repeating the chain audit would require bounded historical transfer logs with canonical event identifiers and archived responses. Reconstructing destinations additionally requires dated labels, recipient histories and an explicitly defined observation horizon.
