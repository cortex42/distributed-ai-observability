# Contributing

Thank you for helping improve the Distributed AI Observability Landscape.

## Licensing of contributions

By submitting a contribution, you agree to license your original contribution under the licence applicable to that part of the repository, as described in [LICENSE.md](LICENSE.md): [CC BY 4.0](LICENSES/CC-BY-4.0.txt) for documentation and catalogue content, and [MIT](LICENSES/MIT.txt) for software, configuration and source-code examples. You retain copyright in your contribution.

Submit only material you have the right to contribute under those terms. Identify any third-party material, its source and its applicable licence so reviewers can assess compatibility.

## Before proposing a change

1. Check whether the item already exists in `catalog/protocols.json`.
2. Read `docs/methodology.md` and select the correct maturity label.
3. Locate an authoritative primary source.
4. Explain the relevance to cross-domain distributed inference, not merely to observability in general.

## Pull requests

A pull request should update all affected representations together:

- `catalog/protocols.json` for structured facts;
- `catalog/watchlist.json` when a new authoritative source must be monitored;
- `docs/landscape.md` when the human-readable analysis changes;
- `CHANGELOG.md` for a material change.

Run:

```bash
python3 scripts/validate_catalog.py
```

The pull request must remain a draft until a human reviewer confirms the evidence and interpretation.

## Good additions

- a new standards revision that changes interoperability or semantics;
- a documented inference metric that improves causal attribution;
- a cross-domain identity, timing, topology, disclosure, or integrity mechanism;
- measurements showing which delay dominates a real workflow;
- evidence that challenges one of the project's working hypotheses.

## Out of scope

- generic AI news with no observability or network consequence;
- unsourced product marketing;
- GPU-cluster fabric details that do not affect distributed inference outside the cluster;
- claims that an individual draft represents IETF consensus;
- raw prompts, customer data, credentials, or sensitive topology.
