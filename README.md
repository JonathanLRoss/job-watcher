# Investment Banking Job Watcher

![Tests](https://github.com/JonathanLRoss/job-watcher/actions/workflows/tests.yml/badge.svg)

Target: investment banking and related finance analyst roles. Titles must contain analyst and one of investment bank, capital markets, corporate finance, financial analyst, equity research, valuation, investment analyst, mergers, acquisitions (case insensitive). All postings are retained. Sources below are candidate Greenhouse public JSON boards; verify first-run status and replace failed boards. No search terms currently used; oversized boards fail rather than silently truncate.

## Sources

- Stripe: Greenhouse (`stripe`)
- Brex: Greenhouse (`brex`)
- Ramp: Greenhouse (`ramp`)
- Robinhood: Greenhouse (`robinhood`)
- Coinbase: Greenhouse (`coinbase`)
- Affirm: Greenhouse (`affirm`)
- Chime: Greenhouse (`chime`)
- Plaid: Greenhouse (`plaid`)
- SoFi: Greenhouse (`sofi`)
- Betterment: Greenhouse (`betterment`)
- Wealthfront: Greenhouse (`wealthfront`)
- Clear Street: Greenhouse (`clearstreet`)
- Public: Greenhouse (`public`)
- IMC: Greenhouse (`imc`)
- Jane Street: Greenhouse (`janestreet`)
- Two Sigma: Greenhouse (`twosigma`)
- Point72: Greenhouse (`point72`)
- Acadian Asset Management: Greenhouse (`acadianassetmanagement`)
- Flow Traders: Greenhouse (`flowtraders`)
- Hudson River Trading: Greenhouse (`hudsonrivertrading`)

## Files
- `watcher.py`: collects snapshots, builds history, status and issue text.
- `tests/test_watcher.py`: conversion, title and history tests.
- `.github/workflows/daily.yml`: daily collection, commit, issue and Pages deployment.
- `.github/workflows/tests.yml`: pytest on push.
- `data/raw/<date>/<source>.json.gz`: raw JSON snapshots.
- `data/history.csv`: deterministic posting history.
- `data/status.json`: latest run status.
- `data/issue.md`: generated issue body.
- `index.html`, `browse.html`, `market.html`: Today, Browse and Market pages.
- `app.js`: browser calculations, filtering, shortlist and charts.
- `style.css`: shared styling.
- `manifest.json`, `sw.js`, `icon-192.png`, `icon-512.png`: installable offline app.
- `README.md`: documentation.

## Commands
`python watcher.py` collects data. `python watcher.py --build` rebuilds history from raw files alone. `python -m pytest` runs tests (install pytest first). Enable GitHub Pages with GitHub Actions as the source, then manually run Daily watcher. Verify at least 15 sources succeed. The schedule is 12:15 UTC daily.
