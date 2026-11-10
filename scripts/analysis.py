"""Offline ONDO research calculations. Token arithmetic uses Decimal."""
import csv
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal as D
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
WALLETS = {
    'A': '0x677fd4ed8ae623f2f625deb2d64f2070e46ca1a1',
    'B': '0x524083970c7a1e62fbaa61d38781f87a4f191fd0',
    'C': '0xea5785e1727de2ba2cefd102cb2dd91e018675e1',
}
TOKEN = '0xfAbA6f8e4a5E8Ab82F62fe7C39859FA577269BE3'

def assumptions():
    return json.loads((ROOT / 'data/assumptions.json').read_text(encoding='utf-8'))

def verify_files():
    manifest = json.loads((ROOT / 'data/provenance.json').read_text(encoding='utf-8'))
    for name, meta in manifest['files'].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != meta['sha256']:
            raise ValueError(f'Evidence checksum mismatch: {name}')
    return len(manifest['files'])

def load_transfers():
    with (ROOT / 'data/safe_outflows_tx.csv').open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row['amount_ondo'] = D(row['amount_ondo'])
        row['to'] = row['to'].lower()
        row['tx_hash'] = row['tx_hash'].lower()
        timestamp = datetime.fromisoformat(row['timestamp_utc']).replace(tzinfo=timezone.utc)
        if row['safe'] not in ('B', 'C') or row['amount_ondo'] < 0:
            raise ValueError('Invalid Safe or amount')
        if not row['amount_ondo'].is_finite():
            raise ValueError('Nonfinite token amount')
        if timestamp.strftime('%Y-%m') != row['month']:
            raise ValueError('Timestamp/month mismatch')
        if not re.fullmatch(r'0x[0-9a-f]{40}', row['to']):
            raise ValueError('Invalid recipient address')
        if not re.fullmatch(r'0x[0-9a-f]{64}', row['tx_hash']):
            raise ValueError('Invalid transaction hash')
        if row['etherscan_url'] != 'https://etherscan.io/tx/' + row['tx_hash']:
            raise ValueError('Transaction link mismatch')
    return rows

def monthly_totals(rows):
    a = assumptions()
    start, end = a['analysis_start_month'], a['analysis_end_month']
    months = []
    year, month = map(int, start.split('-'))
    while f'{year:04d}-{month:02d}' <= end:
        months.append({'month': f'{year:04d}-{month:02d}', 'B': D(0), 'C': D(0)})
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)
    lookup = {r['month']: r for r in months}
    for row in rows:
        if row['month'] not in lookup:
            raise ValueError('Transfer outside analysis window')
        lookup[row['month']][row['safe']] += row['amount_ondo']
    for row in months:
        row['combined'] = row['B'] + row['C']
    return months

def transfer_summary(rows):
    months = monthly_totals(rows)
    total = sum((r['amount_ondo'] for r in rows), D(0))
    active = sum(r['combined'] > 0 for r in months)
    return {
        'rows': len(rows), 'unique_hashes': len({r['tx_hash'] for r in rows}),
        'unique_recipients': len({r['to'] for r in rows}), 'gross_ondo': total,
        'zero_amount_rows': sum(r['amount_ondo'] == 0 for r in rows),
        'safe_B_ondo': sum((r['amount_ondo'] for r in rows if r['safe'] == 'B'), D(0)),
        'safe_C_ondo': sum((r['amount_ondo'] for r in rows if r['safe'] == 'C'), D(0)),
        'calendar_months': len(months), 'active_months': active,
        'calendar_average_ondo': total / len(months), 'active_average_ondo': total / active,
        '2025_ondo': sum((r['combined'] for r in months if r['month'].startswith('2025')), D(0)),
        '2026_through_october_ondo': sum((r['combined'] for r in months if r['month'].startswith('2026')), D(0)),
        '2025_january_october_ondo': sum((r['combined'] for r in months if '2025-01' <= r['month'] <= '2025-10'), D(0)),
    }

def repeated_hash_rows(rows):
    counts = Counter(r['tx_hash'] for r in rows)
    return [r for r in rows if counts[r['tx_hash']] > 1]

def funding():
    with (ROOT / 'data/safeA_large_transfers.csv').open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    return {safe: sum((D(r['amount_ondo']) for r in rows
                       if r['from'].lower() == WALLETS['A'] and r['to'].lower() == WALLETS[safe]), D(0))
            for safe in ('B', 'C')}

def unlock():
    a = assumptions()
    ecosystem = D(a['ecosystem_allocation_ondo']) * (1 - D(a['ecosystem_initial_release_fraction'])) / a['working_steps']
    protocol = D(a['protocol_allocation_ondo']) / a['working_steps']
    private = D(a['private_allocation_ondo']) / a['working_steps']
    alternative = ecosystem + (D(a['protocol_allocation_ondo']) + D(a['private_allocation_ondo'])) / a['alternative_protocol_private_steps']
    total = ecosystem + protocol + private
    return {'ecosystem': ecosystem, 'protocol': protocol, 'private': private,
            'total': total, 'alternative_total': alternative,
            'pct_reference_circulation': total / D(a['reference_circulating_ondo']) * 100,
            'pct_total_supply': total / D(a['total_supply_ondo']) * 100}

def price(realization, cap_change=0):
    realization, cap_change = D(str(realization)), D(str(cap_change))
    if not 0 <= realization <= 1 or cap_change <= -1:
        raise ValueError('Realization must be in [0,1]; capitalization must remain positive')
    a = assumptions()
    return D(a['reference_cap_usd']) * (1 + cap_change) / (D(a['reference_circulating_ondo']) + unlock()['total'] * realization)

def sensitivity():
    a = assumptions()
    return [{'capitalization_change': change, **{fraction: price(fraction, change) for fraction in a['release_realizations']}}
            for change in a['capitalization_changes']]

def snapshot_reconciliation():
    a = assumptions()
    cap, circ, quote = (D(a[k]) for k in ('reference_cap_usd', 'reference_circulating_ondo', 'reported_quote_usd'))
    return {'cap_implied_price': cap / circ, 'quote_times_supply': quote * circ,
            'quote_cap_gap_pct': (quote * circ / cap - 1) * 100,
            'post_full_release_circulation': circ + unlock()['total'],
            'cap_to_preserve_reference_price': price(0) * (circ + unlock()['total']),
            'required_holder_cashflow_at_20x': cap / 20,
            'required_source_earnings_at_40pct_capture_20x': cap / (D('.4') * 20)}

def historical_counterevidence():
    results = []
    for year in (2025, 2026):
        event = date(year, 1, 18)
        start, end = event - timedelta(days=1), event + timedelta(days=30)
        returns = {}
        for asset in ('ONDO', 'BTC'):
            candles = json.loads((ROOT / 'data' / f'coinbase_{asset}_{year}-01-18.json').read_text())
            closes = {datetime.fromtimestamp(r[0], timezone.utc).date(): D(str(r[4])) for r in candles}
            returns[asset] = (closes[end] / closes[start] - 1) * 100
        results.append({'year': year, 'start_close_date_utc': str(start), 'end_close_date_utc': str(end),
                        'intervals': (end - start).days, **returns, 'ONDO_minus_BTC_pp': returns['ONDO'] - returns['BTC']})
    return results

def style():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.edgecolor': '#AAB1B8', 'text.color': '#233A50',
                         'axes.labelcolor': '#233A50', 'xtick.color': '#233A50', 'ytick.color': '#233A50',
                         'savefig.facecolor': 'white'})
    return plt

def monthly_figure(months):
    plt = style()
    fig, ax = plt.subplots(figsize=(12, 5.6), layout='constrained')
    x = list(range(len(months)))
    b, c = ([float(r[s] / D(1000000)) for r in months] for s in ('B', 'C'))
    ax.bar(x, b, color='#A6192E', label='Safe B', width=.75)
    ax.bar(x, c, bottom=b, color='#233A50', label='Safe C', width=.75)
    ax.set_xticks(x, [datetime.strptime(r['month'], '%Y-%m').strftime('%b %y') for r in months], rotation=55, ha='right')
    ax.set_ylabel('Gross payouts (million ONDO)')
    ax.set_ylim(0, max(bi + ci for bi, ci in zip(b, c)) * 1.12)
    ax.set_title('Monthly gross payouts from Safes B and C', loc='left', fontsize=15, fontweight='bold', pad=36)
    ax.text(0, 1.035, 'Aztec Blockchain Group | January 2025–October 2026 | 22 calendar months', transform=ax.transAxes)
    ax.set_axisbelow(True)
    ax.grid(axis='y', color='#DFE3E8')
    ax.legend(frameon=False, loc='upper right')
    fig.supxlabel('Foundation link inferred for B/C. Gross transfers do not establish sales.', fontsize=9)
    return fig

def sensitivity_figure():
    plt = style()
    from matplotlib.ticker import PercentFormatter, StrMethodFormatter
    fig, ax = plt.subplots(figsize=(10, 5.6), layout='constrained')
    fractions = [D(i) / 200 for i in range(201)]
    ax.plot([float(x) for x in fractions], [float(price(x)) for x in fractions], color='#A6192E', linewidth=2.6)
    for fraction in (D(0), D('.5'), D(1)):
        value = price(fraction)
        ax.scatter(float(fraction), float(value), color='#233A50', s=40, zorder=3)
        ax.annotate(f'{fraction:.0%} release: ${value:.4f}', (float(fraction), float(value)),
                    xytext=(8 if fraction < 1 else -8, -24 if fraction == 1 else 13), textcoords='offset points',
                    ha='left' if fraction < 1 else 'right', va='top' if fraction == 1 else 'bottom', fontsize=10,
                    bbox={'facecolor': 'white', 'edgecolor': 'none', 'alpha': .9, 'pad': 2})
    ax.set(xlim=(-.02, 1.02), ylim=(.24, .375), xlabel='Fraction of working January release realized in modeled circulation', ylabel='Modeled USD per ONDO')
    ax.xaxis.set_major_formatter(PercentFormatter(1))
    ax.yaxis.set_major_formatter(StrMethodFormatter('${x:.2f}'))
    ax.grid(color='#DFE3E8')
    ax.set_title('Supply realization at unchanged capitalization', loc='left', fontsize=15, fontweight='bold', pad=36)
    ax.text(0, 1.035, 'Aztec Blockchain Group | Reference capitalization $1.695053B', transform=ax.transAxes)
    fig.supxlabel('Conditional accounting sensitivity. No probabilities or forecast of realized sales.', fontsize=9)
    return fig

def export_results(rows):
    months = monthly_totals(rows)
    with (ROOT / 'data/monthly_gross_payouts.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['month', 'B', 'C', 'combined'])
        w.writeheader(); w.writerows(months)
    result = {'transfers': transfer_summary(rows), 'funding_from_A': funding(), 'unlock': unlock(),
              'snapshot': snapshot_reconciliation(), 'appendix_B': sensitivity(),
              'historical_counterevidence': historical_counterevidence()}
    (ROOT / 'data/calculated_results.json').write_text(json.dumps(result, default=str, indent=2) + '\n', encoding='utf-8')
    plt = style()
    for name, fig in [('monthly_gross_payouts', monthly_figure(months)), ('supply_realization_sensitivity', sensitivity_figure())]:
        fig.savefig(ROOT / 'figures' / (name + '.png'), dpi=180)
        fig.savefig(ROOT / 'figures' / (name + '.svg'))
        plt.close(fig)
    return result

if __name__ == '__main__':
    verify_files()
    result = export_results(load_transfers())
    print(json.dumps(result, default=str, indent=2))
