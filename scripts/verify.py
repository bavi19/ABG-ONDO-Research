"""Regression checks against report values; expected answers never drive calculations."""
import json
from decimal import Decimal as D
from analysis import (ROOT, verify_files, load_transfers, transfer_summary, monthly_totals,
                      repeated_hash_rows, unlock, price, funding, historical_counterevidence, sensitivity)

def verify():
    checks = []
    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        checks.append(name)
    check('Evidence checksums', verify_files() == 6)
    rows = load_transfers()
    s = transfer_summary(rows)
    for key, expected in {'rows': 203, 'unique_hashes': 202, 'unique_recipients': 166,
                          'gross_ondo': D('2357719599.756896'), 'safe_B_ondo': D('1668727502.067002'),
                          'safe_C_ondo': D('688992097.689894'), '2025_ondo': D('1359038783.067002'),
                          '2026_through_october_ondo': D('998680816.689894'), 'calendar_months': 22,
                          'active_months': 20, 'zero_amount_rows': 4}.items():
        check(key, s[key] == expected)
    check('Calendar average', abs(s['calendar_average_ondo'] / 1000000 - D('107.169073')) < D('.000001'))
    keys = [(r['safe'], r['timestamp_utc'], r['tx_hash'], r['to'], r['amount_ondo']) for r in rows]
    check('No repeated composite transfer rows', len(keys) == len(set(keys)))
    repeated = repeated_hash_rows(rows)
    check('Repeated hash represents two distinct C recipients', len(repeated) == 2 and
          all(r['safe'] == 'C' for r in repeated) and len({r['to'] for r in repeated}) == 2)
    monthly = monthly_totals(rows)
    check('Zero months preserved', [r['month'] for r in monthly if r['combined'] == 0] == ['2025-11', '2025-12'])
    check('Monthly bars reconcile exactly', sum((r['B'] + r['C'] for r in monthly), D(0)) == s['gross_ondo'])
    check('Comparable payout counterevidence', s['2026_through_october_ondo'] < s['2025_january_october_ondo'])
    check('Selected A large-transfer subtotals (documented 100 ONDO B gap)',
          funding() == {'B': D('1548558412'), 'C': D('725000000')})
    u = unlock()
    for key, expected in {'ecosystem': '792052170.84', 'protocol': '660000000', 'private': '258049208.8',
                          'total': '1710101379.64', 'alternative_total': '1939613681.84'}.items():
        check('Unlock ' + key, u[key] == D(expected))
    # Appendix B's published four-decimal cells provide independent regression targets.
    targets = [('.2611', '.2221', '.1932'), ('.3481', '.2961', '.2576'),
               ('.4351', '.3701', '.3220'), ('.5222', '.4442', '.3864'), ('.6962', '.5922', '.5153')]
    for row, expected in zip(sensitivity(), targets):
        check('Appendix B cap change ' + row['capitalization_change'],
              tuple(row[x].quantize(D('.0001')) for x in ('0', '0.5', '1')) == tuple(map(D, expected)))
    check('Nonlinear decreasing price curve', price(0) > price('.5') > price(1) and
          price('.5') != (price(0) + price(1)) / 2)
    for row, expected in zip(historical_counterevidence(), ('2.011', '.344')):
        check('Historical counterevidence ' + str(row['year']), row['intervals'] == 31 and
              abs(row['ONDO_minus_BTC_pp'] - D(expected)) < D('.001'))
    return checks

if __name__ == '__main__':
    checks = verify()
    print(f'PASS: {len(checks)} checks')
    print('\n'.join(checks))
