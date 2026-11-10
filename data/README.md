# Data provenance and reuse review

## Included evidence

| File | Origin and treatment |
| --- | --- |
| `safe_outflows_tx.csv` | Supplied reconciliation `results/safe_outflows_tx.csv`; seven core numerical/identifier columns projected, all 203 rows retained |
| `safeA_large_transfers.csv` | Supplied selected A large-transfer export; timestamp/from/to/amount/hash only |
| `coinbase_ONDO_2025-01-18.json`, `coinbase_BTC_2025-01-18.json` | Unmodified public numerical daily candles from the nested original audit archive |
| `coinbase_ONDO_2026-01-18.json`, `coinbase_BTC_2026-01-18.json` | Same source and format for 2026 |
| `assumptions.json` | Transcribed explicit report/reference inputs; not an original vendor response |
| `provenance.json` | Source archive/member hashes, included-file hashes, transformations and record counts |
| `monthly_gross_payouts.csv`, `calculated_results.json` | Generated outputs; overwritten by notebook execution |

All 23 entries listed in the supplied reconciliation manifest passed byte-count and SHA-256 checks before import. Only the files above were selected. Source hashes establish identity, not authenticity of the underlying events or permission to redistribute unrelated material. Each included evidence file has a hash checked at runtime. Assumptions intentionally remain editable; the verification script detects changes that no longer reconcile with the report.

## Transfer schema

- `safe`: B or C, mapped to a full Ethereum address in `scripts/analysis.py`.
- `timestamp_utc`: source ISO timestamp interpreted as UTC.
- `month`: YYYY-MM; validated against timestamp.
- `to`: Ethereum recipient address; no proprietary address label.
- `amount_ondo`: source decimal token amount, exported at up to six places; four zero-amount rows retained.
- `tx_hash`: Ethereum transaction hash; not a unique transfer-event ID.
- `etherscan_url`: public transaction lookup link.

The source memo describes matching each record against historical Blockscout records. Complete underlying responses and canonical event identifiers were not supplied. Amounts are gross transfers, not executed sales. No synthetic records were created. The source CSV's downstream allocation and Etherscan-label columns were deliberately removed.

## Primary references

- [ONDO token](https://docs.ondo.foundation/ondo-token): governance, token address, initial supply and investor wording.
- [Foundation unlock proposal](https://blog.ondo.foundation/unlocking-ondo-a-proposal-from-the-ondo-foundation/): exact category allocations, initial ecosystem release and scheduled steps.
- [Official Foundation wallet disclosure](https://blog.ondo.foundation/ondo-foundation-group-wallet-address-disclosure/): official Safe A attribution; does not officially attribute B/C.
- [FIP 08](https://forum.fluxfinance.com/t/fip-08-release-of-the-ondo-token-lock-up/563): release proposal.
- [Blockscout ONDO](https://eth.blockscout.com/token/0xfAbA6f8e4a5E8Ab82F62fe7C39859FA577269BE3): public token lookup. Per-transaction links are included in the CSV.
- [Coinbase candles](https://docs.cdp.coinbase.com/exchange/reference/exchangerestapi_getproductcandles): daily OHLCV schema. Numerical bodies were saved in the original research audit archive, not freshly retrieved for this build.

Primary website checks during preparation were corroborative. Research calculations retain the supplied cutoff and do not use live prices or update source assertions silently.

## Redistribution review

The supplied archives were inspected for explicit license, copyright, redistribution and proprietary-data notices. No explicit redistribution license or dataset-specific restriction was found for these selected exports. This is not a blanket grant for other files in the archives.

Included material is limited to the user's supplied ABG research export of public chain facts, public numerical Coinbase candle responses and ABG's numerical assumptions/results. Proprietary Allium output, named destination labels, articles, legal PDFs, competitor reports, AI conversations and source-document bodies are excluded. The report DOCX, evidence memo and complete ZIP archives are not part of the public candidate.

No third-party content is relicensed. Public-source access does not establish an unrestricted redistribution license. Coinbase/explorer service terms and ABG's authority to release the assembled research export remain for the repository owner's publication review. This limitation does not prevent local reproduction. No open-source license was invented on ABG's behalf.
