# Investment Banking Job Watcher

![Tests](https://github.com/JonathanLRoss/job-watcher/actions/workflows/tests.yml/badge.svg)

## Project Overview

This project automatically tracks job openings across financial services, investment banking, investment management, and financial technology companies.

The pipeline collects job postings daily, identifies new and removed postings, maintains historical data, and publishes the results to a website.

## Live Website

https://jonathanlross.github.io/job-watcher/

## Employer Sources

All sources use the Greenhouse public JSON API without login.

| Employer | ATS | Board ID |
|---|---|---|
| Stripe | Greenhouse | stripe |
| Brex | Greenhouse | brex |
| Ramp | Greenhouse | ramp |
| Robinhood | Greenhouse | robinhood |
| Coinbase | Greenhouse | coinbase |
| Affirm | Greenhouse | affirm |
| Chime | Greenhouse | chime |
| SoFi | Greenhouse | sofi |
| Betterment | Greenhouse | betterment |
| Clear Street | Greenhouse | clearstreet |
| Public | Greenhouse | public |
| IMC | Greenhouse | imc |
| Jane Street | Greenhouse | janestreet |
| Point72 | Greenhouse | point72 |
| Flow Traders | Greenhouse | flowtraders |
| iCapital | Greenhouse | icapitalnetwork |
| Andreessen Horowitz | Greenhouse | a16z |
| FT Partners | Greenhouse | financialtechnologypartners |

No search terms are currently required.

## Title Rule

The target role is investment banking analyst and related finance analyst positions.

A matching title must contain "analyst" and at least one of the following terms:

- Investment bank
- Capital markets
- Corporate finance
- Financial analyst
- Equity research
- Valuation
- Investment analyst
- Mergers
- Acquisitions

The rule is case-insensitive. All collected postings are retained regardless of whether they match the target role.

## Repository Files

- watcher.py: Data collection and historical processing.
- test_watcher.py: Automated pytest tests.
- .github/workflows/daily.yml: Daily pipeline and website deployment.
- .github/workflows/tests.yml: Automated testing.
- data/raw/: Compressed daily JSON snapshots.
- data/history.csv: Historical job posting records.
- data/status.json: Latest pipeline status.
- data/issue.md: Generated daily issue content.
- index.html: Today page.
- browse.html: Searchable job listings.
- market.html: Market analysis and charts.
- app.js: Browser calculations and interactive features.
- style.css: Website styling.
- manifest.json: Web application configuration.
- sw.js: Offline service worker.
- icon-192.png: Application icon.
- icon-512.png: Application icon.
- README.md: Project documentation.

## Commands

Run the daily pipeline:

    python watcher.py

Rebuild historical data from raw files:

    python watcher.py --build

Run automated tests:

    python -m pytest

## Automation

GitHub Actions runs the pipeline daily at 12:15 UTC. The pipeline collects job postings, updates historical records, creates daily GitHub Issues, commits data, and deploys the website.

## Website Features

The Today page displays daily collection results and source statuses.

The Browse page provides job searches, employer and location filters, sorting, application links, and a persistent shortlist.

The Market page provides six automatically calculated analyses of job market activity.

The website includes a manifest and service worker for installation and offline access.
