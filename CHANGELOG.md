# Changelog

Material changes to the landscape and catalogue are recorded here. Routine scans that find no substantive change do not create commits.

## Unreleased

- Added CC BY 4.0 licensing for original documentation and catalogue content, and MIT licensing for software, configuration and source-code examples.
- Added full licence texts, scope and attribution guidance, and matching contribution terms.

## 0.9.0 — 2026-10-05

- Recorded unreleased OpenTelemetry GenAI additions for agent-skill lifecycle spans and the stable-ID `gen_ai.main_agent` entity; maturity remains experimental and the new fields are development status.
- Updated MCP implementation evidence to Python SDK v2.3.0, which records peer JSON-RPC errors on client spans; MCP project-specification maturity remains unchanged.
- Updated vLLM to v0.31.0, where Responses API per-request timing is now tagged, and recorded additional cache, connector, offload, residency, and logging signals.
- Promoted STAMP reflected headers from `draft` to `candidate` after revision `-15` entered IETF Last Call for Proposed Standard; it is not yet an RFC.
- Recorded the OPSAWG Data Manifest's transition to Waiting for AD Go-Ahead::Revised I-D Needed while its candidate maturity remains unchanged.
- Updated the individual agent-audit-record entry with the published 47-vector corpus, Go/Python reference verifiers, signed digests, and the v0.16.0 indeterminate-verdict compatibility change.
- Added the individual OpenTelemetry correlation extension for Agent Action Capsules as a draft gap-filler for joining trace context to sealed action evidence, with explicit same-producer, disclosure, base-profile, and implementation caveats.
- Added three monitoring sources and refined the correlation, disclosure, cache-state, vocabulary, and audit gaps. FOX remains an unchanged working hypothesis.

## 0.8.0 — 2026-09-28

- Recorded OpenTelemetry GenAI's unreleased 22 September breaking replacement of the token-usage histogram with aggregate usage counters and separate per-operation token distributions; maturity remains experimental.
- Updated vLLM to the 22 September v0.30.0 release, including shipped latency semantics and HiSparse cache/transfer counters, while retaining the Responses API timing change as main-only implementation work.
- Added the CATS working-group YANG data-model `-00` for service-instance mapping, operational counters and notifications; it is a draft, not an RFC or cross-domain task-correlation mechanism.
- Recorded the OPSAWG Data Manifest's 26 September transition from IETF Last Call to Waiting for AD Go-Ahead, with IANA expert review still outstanding; candidate maturity is unchanged.
- Updated the individual AI Audit Reference Architecture from `-00` to the substantively expanded `-01`, including new audience, liveness, producer-failure, effect-observation and verification semantics plus explicit unresolved completeness/security gaps.
- Added the individual agent-authorization audit-record `-01` as a concrete canonical signed decision/effect format. It has no formal IETF standing, published implementation, or published conformance corpus.
- Expanded the topology, vocabulary, cache-state and audit gaps, and added three authoritative monitoring sources. FOX remains an unchanged working hypothesis.

## 0.7.0 — 2026-09-21

- Recorded unreleased OpenTelemetry GenAI changes to tool-conversation correlation, sampling-relevant agent names, token/cache usage, and finish reasons, including breaking changes since its stored baseline.
- Added vLLM Responses API per-request timing support merged on 16 September, explicitly distinguished from stable v0.29.0, and clarified streamed-event latency versus per-request TPOT.
- Corrected MCP's release-candidate maturity to the published 2026-07-28 project specification using its July release announcement and current-version guidance; this is a baseline correction, not a September release or IETF/W3C standard.
- Added GROW BMP statistics `-01` (11 September) and IPPM STAMP reflected-header `-14` (18 September), with wire/measurement semantics and implementation caveats kept separate from the base RFCs.
- Added individual Agent Operation Continuity and AI Audit Reference Architecture drafts for failover evidence and scoped post-hoc audit. Neither has formal IETF standing or established cross-provider interoperability.
- Refined the vocabulary, sampling, retry, cache, and audit gaps and added seven authoritative monitoring sources. FOX remains an unchanged working hypothesis.

## 0.6.0 — 2026-09-10

- Added an implementation note covering the ntop observability stack: nProbe for flow collection/normalisation, ntopng for traffic analytics and higher-resolution time series, and nDPI for application/protocol enrichment.
- Recorded ntop as mature production evidence for network-local observability while explicitly retaining the cross-domain gap: flow/application evidence does not by itself correlate to AI tasks, model queues, agent operations, retries, or user-visible outcomes.
- Added `www.ntop.org` to the authoritative-source allowlist so future ntop documentation can be tracked through the repository validation process.
- Documented a possible FOX participant-gateway pattern in which raw packet/flow/DPI data remains local and only authorised derived evidence is exported.
## 0.6.0 — 2026-09-14

- Added the IETF OPSAWG Data Manifest `-15`, which entered IETF Last Call for Proposed Standard and preserves platform, schema, subscription, and actual collection-period context for YANG telemetry.
- Added individual `draft-arsentev-agent-run-metrics-00` for agent-run resource accounting, delegation lineage, and W3C trace/span bindings; it has no formal IETF standing and no known implementation.
- Refined the common-vocabulary, topology-mapping, and retry/delegation gaps to distinguish these proposals from end-to-end cross-domain correlation, verified evidence, privacy policy, and implementation.
- Added both authoritative Datatracker sources to the watchlist.

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
