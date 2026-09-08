# Changelog

Material changes to the landscape and catalogue are recorded here. Routine scans that find no substantive change do not create commits.

## 0.5.0 — 2026-09-07

- Updated the individual telemetry-identifier-scoping draft from `-00` to the substantively rewritten `-01` revision published 4 September 2026; it still has no formal IETF standing.
- Replaced the retired four-value scope vocabulary and omitted-identifier default with the revision's broader semantics for uniqueness, context, observation domain, comparability, time scope, normalization, and equality versus identity.
- Recorded the draft's remaining uncertainty: no wire format, data model, implementation, interoperability evidence, or working-group adoption, plus inconsistent `MUST`/`SHOULD` strength between the abstract and requirements.

## 0.4.0 — 2026-08-31

- Updated the IPPM On-Path Telemetry YANG entry from `-05` to the substantively redesigned `-06` revision, including its augmentation of the existing AltMark and IOAM models, timestamp-type context, and IPFIX-aligned path-delay metrics.
- Added individual `draft-dikshit-nmop-telemetry-identifier-scoping-00`, which proposes explicit uniqueness scopes, cross-node comparability rules, and omitted-identifier handling; it has no formal IETF standing.
- Refined the correlation gap to distinguish network-telemetry identifier scope from task-level correlation, privacy policy, authentication, and cross-domain evidence mapping.
- Added the new identifier-scoping draft to the authoritative watchlist.

## 0.3.0 — 2026-08-24

- Added vLLM's experimental, opt-in per-request speculative-decoding acceptance metrics, including documented limitations and the relationship to aggregate Prometheus counters.
- Added individual `draft-ackerman-temporal-integrity-metadata-01`, which proposes timestamp provenance, synchronisation-state, uncertainty, temporal-domain, and sequence metadata; it has no formal IETF standing.
- Updated the time-quality gap to distinguish the new proposal from implementation, interoperability, or standards consensus.
- Expanded the authoritative watchlist for vLLM acceptance-metric and TIM status changes.

## 0.2.0 — 2026-08-17

- Added the Model Context Protocol 2026-07-28 release candidate and Final SEP-414 as a candidate task-correlation mechanism carrying W3C trace context through JSON-RPC `_meta`.
- Recorded official MCP SDK documentation showing deployable request spans and trace propagation, while keeping protocol maturity distinct from implementation support.
- Added the individual `draft-gaikwad-agent-proxy-modes-00` proposal for intermediary trace propagation, hop metadata, and metrics; it has no formal IETF standing.
- Expanded the authoritative watchlist for MCP specification, SEP, SDK, and agent-tool proxy changes.

## 0.1.0 — 2026-08-13

- Established the initial distributed AI observability landscape.
- Added the first machine-readable protocol and system catalogue.
- Separated standards, candidates, drafts, implementations, frameworks, and working hypotheses.
- Added FOX as a working Federated Observability Exchange concept with explicit non-goals.
- Added authoritative watch sources and a human-reviewed weekly update procedure.
- Noted fast-moving areas including OpenTelemetry GenAI conventions, vLLM per-request metrics, CATS OAM, Quality of Outcome, on-path telemetry YANG, and distributed-inference transport work.
