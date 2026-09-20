"""Аудит: облигации, акции, выплаты."""
from database import db


def main():
    print("=" * 70)
    print(f"  БАЗА ДАННЫХ ПОРТФЕЛЯ")
    print("=" * 70)

    bonds = db.get_bonds()
    stocks = db.get_stocks()
    payments = db.get_payments()

    print(f"\nОблигаций: {len(bonds)}")
    print(f"Акций:     {len(stocks)}")
    print(f"Выплат:    {len(payments)}")

    # ─────── Выплаты по годам ───────
    if payments:
        print("\n" + "=" * 70)
        print("  ВЫПЛАТЫ ПО ГОДАМ")
        print("=" * 70)
        from collections import defaultdict
        by_year = defaultdict(lambda: {'count': 0, 'total': 0.0, 'after_tax': 0.0})
        for p in payments:
            year = p['payment_date'][:4]
            by_year[year]['count'] += 1
            by_year[year]['total'] += p['amount']
            by_year[year]['after_tax'] += p['amount_after_tax']

        for year in sorted(by_year.keys()):
            d = by_year[year]
            print(f"  {year}: {d['count']:>4} выплат, "
                  f"сумма: {d['total']:>12,.2f} ₽, "
                  f"после налога: {d['after_tax']:>12,.2f} ₽".replace(',', ' '))

    # ─────── Топ-10 эмитентов по сумме выплат ───────
    if payments:
        print("\n" + "=" * 70)
        print("  ТОП-10 ЭМИТЕНТОВ ПО СУММЕ ВЫПЛАТ")
        print("=" * 70)
        from collections import defaultdict
        by_issuer = defaultdict(lambda: {'count': 0, 'total': 0.0})
        for p in payments:
            name = p.get('issuer_name') or '???'
            by_issuer[name]['count'] += 1
            by_issuer[name]['total'] += p['amount']

        top = sorted(by_issuer.items(), key=lambda x: -x[1]['total'])[:10]
        print(f"  {'#':<3} {'Эмитент':<42} {'Выплат':>7} {'Сумма':>14}")
        print(f"  {'-'*3} {'-'*42} {'-'*7} {'-'*14}")
        for i, (name, d) in enumerate(top, 1):
            print(f"  {i:<3} {name[:42]:<42} {d['count']:>7} "
                  f"{d['total']:>14,.2f}".replace(',', ' '))

    # ─────── Проверка тикеров ───────
    import unicodedata
    print("\n" + "=" * 70)
    print("  ПРОВЕРКА ТИКЕРОВ")
    print("=" * 70)
    problems = 0
    for b in bonds:
        ticker = b['ticker'] or ''
        # Проверяем кириллицу
        has_cyr = any('CYRILLIC' in unicodedata.name(ch, '') for ch in ticker)
        if has_cyr:
            print(f"  ⚠️  {ticker} — содержит кириллицу")
            problems += 1
    if problems == 0:
        print("  ✅ Все тикеры чистые")


if __name__ == "__main__":
    main()