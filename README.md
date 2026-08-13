# Distributed AI Observability Landscape

> A living, source-backed map of the protocols, systems, gaps, and emerging standards that may make distributed AI inference observable across organisational boundaries.

This repository is the evolving technical companion to Kaj Kjellgren's conference talk, **Beyond the GPU Cluster: Building Networks for Distributed AI Inference**.

The central question is deliberately practical:

> When one AI task crosses an application, agents, inference providers, tools, data sources, networks, and interconnection points, what evidence is needed to explain its performance and failure modes?

The current answer is incomplete. Useful observability already exists inside most domains; the larger gap is correlation, semantics, disclosure policy, and trust between them.

## Start here

- [Observability landscape](docs/landscape.md) — the human-readable backing document.
- [FOX working concept](docs/fox.md) — a possible Federated Observability Exchange.
- [Research and update methodology](docs/methodology.md) — evidence rules and maturity labels.
- [Machine-readable catalogue](catalog/protocols.json) — the tracked protocols and systems.
- [Authoritative watchlist](catalog/watchlist.json) — sources checked by the weekly review.

## Project principles

1. **Working hypotheses are not forecasts.** Plausible architectural ideas must be labelled separately from measured evidence and published standards.
2. **Primary sources win.** Standards bodies, official specifications, release notes, and project documentation are preferred over commentary.
3. **No silent automation.** The weekly agent may open a draft pull request, but it must never merge or push directly to `main`.
4. **No indiscriminate telemetry sharing.** Cross-domain observability must respect privacy, sovereignty, commercial sensitivity, and per-recipient disclosure policy.
5. **Useful evidence beats one giant dashboard.** The objective is a defensible causal timeline, not central ownership of every participant's telemetry.

## Pilot status

This is a 2–3 week pilot. The initial source baseline was checked on **2026-08-13**. During the pilot, weekly scans should produce a draft pull request only when there is a material change.

The project is maintained through KajTech by Kaj Kjellgren. It is an independent working project and **not an official DE-CIX standard, product, or commitment**.

## Contributing

Corrections and additions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or pull request. Every factual change must include an authoritative source and an explicit maturity classification.

## License during the pilot

No reuse licence has been selected yet. See [LICENSE.md](LICENSE.md). A public content and code licence should be chosen before the repository is promoted through a conference QR code.
