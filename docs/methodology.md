# Research and Update Methodology

This project is intended to evolve without blurring standards, implementations, measurements, and hypotheses.

## Source hierarchy

Use sources in this order:

1. standards-body publication or official datatracker;
2. official specification repository and release notes;
3. official implementation documentation;
4. peer-reviewed paper or primary measurement dataset;
5. vendor engineering material that describes its own implementation;
6. secondary analysis only as a discovery lead, never as the sole evidence for a factual update.

Search snippets, generated summaries, social posts, and unattributed presentations are not sufficient evidence.

## Maturity labels

| Label | Meaning |
| --- | --- |
| `standard` | final or formally published standard/RFC/Recommendation |
| `candidate` | candidate recommendation, release candidate, or late formal review state |
| `draft` | Internet-Draft, working draft, or early specification work |
| `experimental` | explicitly experimental or pre-release work |
| `implementation` | shipping or documented system capability without implying interoperability |
| `framework` | published taxonomy or architecture rather than an exchange protocol |
| `working-hypothesis` | project concept that has not been independently validated |
| `deprecated` | officially deprecated, withdrawn, obsolete, or replaced |

## What counts as a material update

- a new release, RFC, Recommendation, or formal status transition;
- an Internet-Draft revision that materially changes scope, semantics, security, privacy, or interoperability;
- a new protocol/system that fills a documented gap;
- a documented implementation that makes a previously theoretical signal deployable;
- a deprecation, removal, incompatible change, or security issue;
- primary evidence that strengthens or contradicts a project hypothesis.

Editorial changes, date-only refreshes, search-result churn, and unsupported claims should not create pull requests.

## Required change record

Every factual pull request must state:

- what changed;
- why it is material to distributed AI observability;
- authoritative source URL and publication/release date;
- old and new maturity status;
- affected catalogue entries and document sections;
- uncertainty, contradictions, or implementation caveats.

## Review rules

- The weekly agent opens **draft pull requests only**.
- The agent never merges, enables auto-merge, rewrites history, changes repository visibility, or modifies branch protection.
- One source does not establish industry adoption.
- An individual Internet-Draft has no formal IETF standing and must be labelled accordingly.
- Product documentation establishes a capability in that product, not a universal standard.
- Conflicting primary sources are recorded explicitly instead of silently reconciled.
- Privacy, security, sovereignty, and commercial sensitivity must be considered for every proposed cross-domain signal.

## Baseline and scan cadence

The initial baseline date is **2026-08-13**. The watchlist is reviewed weekly. If the workflow produces noisy or weak proposals, refine the prompt and catalogue before continuing the schedule.
