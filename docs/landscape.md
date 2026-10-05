# Distributed AI Observability Landscape

Baseline: **2026-08-13**

Status: **Working document v0.1**

Companion talk: **Beyond the GPU Cluster: Building Networks for Distributed AI Inference**

## 1. Why this document exists

A user may experience a single five-second delay while the underlying task contains several overlapping delays:

- endpoint and provider selection;
- network transit and interconnection;
- inference admission and queueing;
- model prefill and time to first token;
- token generation;
- enterprise data or external tool calls;
- retries, fallback, and delegated agent work.

Each participant normally sees a useful but incomplete slice. A route change and GPU queue spike can occur at the same time. A retry can hide the original failure. Sampling can discard the incident trace. Trace context can stop at an organisational boundary. The observability problem is therefore not merely collecting more metrics; it is assembling enough authorised evidence to reconstruct the critical path.

## 2. Evidence domains

| Domain | Question it can answer | Typical evidence | Main limitation |
| --- | --- | --- | --- |
| Task and application | What workflow ran, and which dependency was critical? | spans, task/agent IDs, errors, retries, tool calls | context may not cross providers |
| Inference service | Was delay caused by admission, queueing, cache, prefill, or decode? | queue time, TTFT, inter-token latency, token rate, cache and batch metrics | provider internals and semantics vary |
| Network device | Did an interface, queue, buffer, or forwarding element degrade? | counters, drops, errors, queue depth, streaming telemetry | topology and customer/task mapping are local |
| Flow and routing | Who communicated, and did reachability or path selection change? | flow records, route views, peer events | usually lacks application causality |
| Active and on-path measurement | What delay, loss, variation, or path evidence was observed? | probes, timestamps, per-hop/on-path data | domain scope, overhead, time quality, deployment |
| Interconnection | What happened at a shared administrative boundary? | port/service health, route and traffic changes, active measurements | must avoid exposing participant-sensitive data |
| Tool and enterprise data | Did an API, datastore, or policy decision delay the task? | request traces, response time, policy/audit events | privacy and organisational boundaries |

## 3. Current toolbox

### Task context and semantic correlation

| Protocol or system | Current baseline | What it contributes | Remaining cross-domain gap |
| --- | --- | --- | --- |
| [W3C Trace Context](https://www.w3.org/TR/trace-context/) | W3C Recommendation, 2021 | Standard `traceparent` and `tracestate` propagation for distributed traces | a provider may reject, regenerate, sample, or stop propagating context |
| [W3C Trace Context Level 2](https://www.w3.org/TR/trace-context-2/) | Candidate Recommendation Draft | Adds trace/span ID generation considerations and a random trace-ID flag | still work in progress; adoption and trust-policy questions remain |
| [W3C Baggage](https://www.w3.org/TR/baggage/) | Candidate Recommendation Snapshot, 2024 | Propagates application-defined properties associated with a workflow | baggage can expose sensitive data and requires strict allow-listing |
| [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/) | v1.44.0 | Common names and meanings for spans, metrics, events, logs, and resources | common vocabulary does not itself authorise exchange or guarantee end-to-end propagation |
| [OpenTelemetry GenAI Semantic Conventions](https://github.com/open-telemetry/semantic-conventions-genai) | Experimental, unreleased main; semantic changes through 30 September 2026 | Adds conversation correlation, skill-lifecycle attributes, sampling inputs, a stable-ID main-agent entity, and aggregate/per-operation token evidence | breaking changes remain possible; entity and skill fields are development status, source URIs may be sensitive, and neither a stable schema nor coordinated cross-provider sampling is established |
| [Model Context Protocol trace propagation](https://modelcontextprotocol.io/seps/414-request-meta) | Published 2026-07-28 project specification; SEP-414 Final; Python SDK v2.3.0 | Carries W3C context in JSON-RPC `_meta`; the tagged Python SDK records JSON-RPC error replies as client-span errors with protocol status codes | not an IETF or W3C standard; optional conventions and SDK-specific behavior do not guarantee propagation, consistent error semantics, or safe disclosure |

The MCP maturity correction is retrospective: the [official release announcement](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/7c046ffbbce305afb84842439f5694f46da797c6/blog/content/posts/2026-07-28-spec-ga/index.md) was published on **28 July 2026**, and [versioning guidance](https://modelcontextprotocol.io/specification/versioning) identifies that version as current and ready for use. This is not a newly released September specification. The catalogue's `standard` label denotes the published project specification, not standards-body endorsement.

The [Python SDK v2.3.0 release](https://github.com/modelcontextprotocol/python-sdk/releases/tag/v2.3.0), published **2 October 2026**, records peer JSON-RPC errors on the client span with OpenTelemetry `ERROR` status, `error.type`, and `rpc.response.status_code`. This is deployable SDK behavior, not a protocol maturity change. In automatic compatibility mode, a legacy server that lacks `server/discover` intentionally produces one error probe span, so operators must distinguish discovery fallback from a failed user operation.

GenAI changes since its stored baseline are still **unreleased**, with important migration and interpretation consequences:

- **20 and 27 August 2026:** [cache-write naming and per-modality usage](https://github.com/open-telemetry/semantic-conventions-genai/commit/8a3767d6c5d09bc0917722720973c0c44182d960) replace cache-creation naming; [cache-read/write fields were removed from internal `invoke_agent` spans](https://github.com/open-telemetry/semantic-conventions-genai/commit/5f5ae69e52464c56eea4389fb793c2690caaea78) to avoid misleading cross-model aggregation. Use inference client spans for those fields.
- **1 September 2026:** [per-message `finish_reason` was deprecated](https://github.com/open-telemetry/semantic-conventions-genai/commit/5ca9052bc796ef1e497200b1d558fd87a201f335) in favour of `gen_ai.response.finish_reasons`.
- **10 and 16 September 2026:** [agent names became sampling-relevant on tool and plan spans](https://github.com/open-telemetry/semantic-conventions-genai/commit/b06f7a2c840ceeacd8478acd3443e697ce390f96), so a reported name should be supplied at span creation. [Tool spans now require conversation ID when available](https://github.com/open-telemetry/semantic-conventions-genai/commit/be23fcc250f72e6f740c96d05fa6f12fbee3d71a); the conventions say `SHOULD NOT` synthesize a UUID, trace ID, or content hash when no real conversation identifier is available. Persistent conversation identifiers need bounded disclosure and retention.
- **22 September 2026:** a [breaking token-metric redesign](https://github.com/open-telemetry/semantic-conventions-genai/commit/8ffdf568e1b4391a99adb081db16e8102e36918e) removed `gen_ai.client.token.usage` and `gen_ai.token.type`. New `gen_ai.client.inference.usage.*` monotonic counters support aggregate spend/rate and cost approximation, split by modality and by input, output, cache-read, cache-write, or reasoning category. Separate per-operation input/output histograms support percentile and outlier analysis; they deliberately omit modality because modality percentiles do not add, and they must not be used for total usage or cost. Cache and reasoning counters are subsets of the input/output totals, and instrumentation reports billable rather than used tokens when both are available.
- **29 September 2026:** [`gen_ai.skill.*` attributes and execute-tool refinements](https://github.com/open-telemetry/semantic-conventions-genai/commit/771e3210f7518694666834f7243573b8018c7a4f) describe loading skill instructions, reading bundled resources, and running bundled scripts on the existing tool span. Names, descriptions, paths, and source URIs improve agent-step reconstruction but can expose internal structure or credentials and require scrubbing.
- **30 September 2026:** the new development [`gen_ai.main_agent` entity](https://github.com/open-telemetry/semantic-conventions-genai/commit/b9ecbaef4ac462cc2b6f7f7763b2cff1d15d5400) associates one persistent top-level agent with internal agent, tool, workflow, and plan spans. Its identity must be provider-assigned and stable across invocations; instrumentation must not substitute an in-memory or process-local ID.

### Inference and metric evidence

| Protocol or system | Current baseline | What it contributes | Remaining cross-domain gap |
| --- | --- | --- | --- |
| [vLLM observability](https://docs.vllm.ai/en/stable/design/metrics/) | v0.31.0 released 5 October 2026 | Prometheus metrics and OpenTelemetry traces; tagged Responses timing; logging controls; additional KV transfer, offload, residency, and encoder-connector metrics | provider deployment and enabled signals vary; implementation-specific cache and connector metrics do not describe transferable state |
| [vLLM per-request metrics](https://docs.vllm.ai/en/latest/features/per_request_metrics/) | Responses API timing is included in v0.31.0; speculative acceptance fields remain experimental | Queue, TTFT, generation, and streaming timing on chat, completions, and Responses; optional per-request speculative acceptance statistics | timing is opt-in and needs statistics enabled; multi-sequence and multi-generation Responses calls omit metrics; acceptance fields remain experimental and single-sequence |
| [NVIDIA Triton metrics](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/metrics.html) and [tracing](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/trace.html) | Rolling product documentation | Prometheus request/GPU/cache metrics and per-request Triton or OpenTelemetry traces | signal names, retention, sampling, and disclosure remain deployment-specific |
| [OpenMetrics 1.0](https://prometheus.io/docs/specs/om/open_metrics_spec/) | Stable specification | Widely adopted metric exposition format | aggregates are often insufficient for causal attribution to one task |
| [OpenMetrics 2.0](https://prometheus.io/docs/specs/om/open_metrics_spec_2_0/) | Experimental release candidate | Evolves the metric format and improves alignment with the OpenTelemetry data model | not yet stable; adoption and compatibility must be tracked |

The [v0.31.0 release](https://github.com/vllm-project/vllm/releases/tag/v0.31.0), published **5 October 2026**, includes the Responses API per-request timing that was main-only at the previous baseline and adds `cache_write_tokens` to Responses. Timing still needs `--enable-per-request-metrics`, cannot be combined with disabled statistics, and can add non-negligible CPU overhead. Metrics are omitted for multiple sequences and multi-generation tool turns because one generation's timing cannot be attributed to the aggregate response; streaming clients receive timing only in the final usage-bearing event.

The [15 September latency clarification](https://github.com/vllm-project/vllm/commit/79e205e8cdf7864b8b9f2d23c908b887f2f5badb), now included in v0.30.0, also matters when comparing systems: `vllm:inter_token_latency_seconds` samples each streamed output event, which can contain several tokens; `vllm:request_time_per_output_token_seconds` samples each completed request as `(end-to-end latency - TTFT) / (output tokens - 1)`. Their histogram weightings differ. The server records zero TPOT for at most one output token, while the serving benchmark excludes those requests from TPOT.

v0.30.0 also ships a HiSparse host-resident tier for sparse-MLA decode. Its [Prometheus counters](https://github.com/vllm-project/vllm/pull/56061) report device hot-buffer hits, misses, and bytes transferred from host KV storage to the device. The implementation collects them asynchronously through the KV-connector statistics path every 2,000 steps. v0.31.0 adds HiSparse residency, simple CPU-offload, encoder-connector, and distinct KV transport-failure versus expiry metrics. These make cache and transfer failure modes more observable inside vLLM, but they neither identify compatible state at an alternate provider nor define provider-neutral cache semantics. Timing and cache-related metrics can reveal workload characteristics even without prompts or completions.

### Network state, flows, routing, and paths

| Protocol or system | Current baseline | What it contributes | Remaining cross-domain gap |
| --- | --- | --- | --- |
| [OpenConfig gNMI](https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-specification.md) | Revision history lists v0.11.0, March 2026; document header still states v0.10.0 | Configuration, operational state retrieval, and streaming telemetry | device data lacks a standard task-to-topology correlation model; the version-text mismatch is itself worth monitoring |
| [YANG-Push](https://datatracker.ietf.org/doc/rfc8641/) | RFC 8639/8640/8641 family | Periodic and on-change publication of YANG-modelled operational data | schema, access policy, and correlation identifiers vary |
| [Data Manifest for Contextualized Telemetry Data](https://datatracker.ietf.org/doc/draft-ietf-opsawg-collected-data-manifest/) | IETF OPSAWG draft `-15`; Waiting for AD Go-Ahead::Revised I-D Needed since 2 October 2026 | Associates collected telemetry with platform, software, YANG schema, subscription, collection mode, and actual collection-period context | not yet approved or an RFC; one GENART item and IANA expert review remain, the collection-manifest model is non-normative, and it does not map network evidence to an AI task |
| [IPFIX](https://datatracker.ietf.org/doc/rfc7011/) | RFC 7011 / STD 77 | Standard export of traffic-flow information | flow records generally identify conversations, not application critical paths |
| [BGP Monitoring Protocol](https://datatracker.ietf.org/doc/rfc7854/) | RFC 7854 plus active extensions | Route views and BGP session/change evidence | a route event can coincide with, but not prove, application or inference delay |
| [BMP Statistics Information TLV](https://datatracker.ietf.org/doc/draft-ietf-grow-bmp-stats-informational-tlv/) | GROW working-group draft `-01`, 11 September 2026; not an RFC | Gauge extrema, timestamps, percentiles, measurement window, and sample count can preserve excursions between exports | changed draft wire layout; comparison depends on collection settings, and no implementation evidence was found |
| [STAMP](https://datatracker.ietf.org/doc/rfc8762/) and TWAMP | RFC 8762 and RFC 5357 | Active one-way and round-trip delay, variation, and loss measurement | probes provide indirect evidence and depend on placement and time quality |
| [STAMP reflected headers](https://datatracker.ietf.org/doc/draft-ietf-ippm-stamp-ext-hdr/) | IPPM working-group draft `-15`; in IETF Last Call for Proposed Standard through 15 October 2026 | Reflects selected IP/IPv6 extension headers, potentially including IOAM, alongside probes; clarifies matching, conformance, reverse headers, MTU, and received TTL/Hop-Limit handling | not yet an RFC; three IPR disclosures, limited-domain and disclosure constraints, and cited implementation targets `-04`, not verified `-15` conformance |
| [IOAM](https://datatracker.ietf.org/doc/rfc9197/) | RFC 9197 family, including direct export and YANG work | In-domain on-path operational and telemetry data | designed for limited domains; cross-domain policy and exposure are unresolved |
| [Network Telemetry Framework](https://datatracker.ietf.org/doc/rfc9232/) | RFC 9232 | A useful taxonomy spanning push, pull, active, passive, and hybrid techniques | framework rather than a transaction-correlation mechanism |
| [On-Path Telemetry YANG](https://datatracker.ietf.org/doc/draft-ietf-ippm-on-path-telemetry-yang/) | IETF working-group draft `-06`, 26 August 2026 | Augments the AltMark and IOAM YANG models with loss/delay evidence, timestamp type, IOAM data, and IPFIX-aligned path-delay summaries for YANG-Push | work in progress; limited to specific on-path methods and does not define cross-domain identifier scope, task correlation, or disclosure policy |

These extensions do not change the maturity of base BMP or STAMP. BMP statistics `-01` adds window/sample-count fields and expands extrema timestamps to seconds plus microseconds; collectors cannot assume its earlier draft layout remains compatible. It neither exports the collection methodology nor fixes the percentile algorithm. STAMP reflected headers `-15` entered IETF Last Call on **1 October 2026**, promoting the extension entry from `draft` to `candidate` under this catalogue's late-review rule. Revision `-15` addressed Area Director review, including received TTL/Hop-Limit discard wording. Its cited [Teaparty commit](https://github.com/cerfcast/teaparty/commit/393abf9357a6c2439877d9bcf2dc426dd89c7158), dated **9 June 2025**, explicitly targets `-04`. Reflected headers and routing statistics can reveal internal network details, and neither authenticates application causality.

## 4. Particularly relevant emerging work

The following work is not proof that distributed AI observability will develop in one direction. It is important because it approaches the boundary between application outcome, compute selection, and network evidence.

| Work | Baseline status | Why it matters here |
| --- | --- | --- |
| [Computing-Aware Traffic Steering framework](https://datatracker.ietf.org/doc/draft-ietf-cats-framework/) | IETF draft `-24`; RFC Editor Queue at baseline | combines network and computing-resource information for service-instance selection, although the framework currently covers one service provider |
| [CATS YANG data model](https://datatracker.ietf.org/doc/draft-ietf-cats-data-model/) | CATS working-group draft `-00`, approved and posted 23 September 2026 | maps CATS service and service-contact-instance identifiers to location, extensible service metrics, matched/forwarded traffic counters, and limit notifications; it narrows local service/topology mapping but supplies no cross-domain task binding or disclosure policy |
| [CATS OAM framework](https://datatracker.ietf.org/doc/draft-ietf-cats-oam-fw/) | IETF draft `-01`, July 2026 | explicitly spans clients, network paths, and service instances for fault and performance management |
| [CATS OAM use cases](https://datatracker.ietf.org/doc/draft-dikshit-cats-oam-usecases/) | Individual draft `-00`, July 2026 | grounds CATS OAM in use cases including multi-domain failure detection and metric-driven steering |
| [Quality of Outcome](https://datatracker.ietf.org/doc/draft-ietf-ippm-qoo/) | IETF draft `-11`, May 2026 | attempts to express application-specific network performance outcomes in a form useful to applications, users, and operators |
| [Transport Considerations for Large-Scale Distributed Inference Networks](https://datatracker.ietf.org/doc/draft-li-tsvwg-inference-transport/) | Individual draft `-00`, July 2026; no formal IETF standing | describes distributed-inference traffic such as prefill/decode KV-cache transfer and expert-parallel flows; it should be tracked, not treated as consensus |
| [Proxy Modes for Agent-Tool Protocols](https://datatracker.ietf.org/doc/draft-gaikwad-agent-proxy-modes/) | Individual draft `-00`, 13 August 2026; no formal IETF standing | proposes W3C trace propagation, append-only gateway-hop metadata, and intermediary metrics for MCP-like traffic, while also defining retry and partial-failure behaviour |
| [Agent Run Metrics](https://datatracker.ietf.org/doc/draft-arsentev-agent-run-metrics/) | Individual draft `-00`, 10 September 2026; no formal IETF standing | proposes per-run JSON accounting with parent/root delegation lineage, model/tool/delegation steps, resource and cost fields, and W3C trace/span bindings; reports are unverified reporter assertions and no implementation is known |
| [Agent Operation Continuity](https://datatracker.ietf.org/doc/draft-schrock-agent-operation-continuity/) | Individual draft `-00`, 15 September 2026; no formal IETF standing | proposes preserving operation identity, provider bindings, attempt evidence, and unresolved outcomes across executor replacement within one coordination domain; reported tests are local/synthetic, not independent or live-provider interoperability |
| [AI Audit Reference Architecture](https://datatracker.ietf.org/doc/draft-sato-agent-accountability-refarch/) | Individual draft `-01`, 21 September 2026; no formal IETF standing | adds confirmation windows, credential revalidation, producer-failure policy, independent effect observation, audience binding, redactable content, and six verification checks; it also documents unresolved coverage, observer-compromise, denial-of-service, and formal-verification gaps |
| [Agent authorization audit record](https://datatracker.ietf.org/doc/draft-gilda-wimse-agent-audit-record/) | Individual draft `-01`; no formal IETF standing; companion vectors v0.16.0 | defines an RFC 8785-canonical in-toto/DSSE record joining decisions to observed effects; all 47 Appendix B vectors now ship with Go/Python verifiers and signed corpus digests, while signed coherence still does not prove completeness or external truth |
| [OpenTelemetry correlation for Agent Action Capsules](https://datatracker.ietf.org/doc/draft-palanisamy-scitt-aac-otel/) | Individual draft `-00`, 2 October 2026; no formal IETF standing | proposes a signed, allow-listed trace/span and GenAI-semconv block plus reverse `aac.capsule_id` lookup; same-producer spans are explicitly not independent corroboration and base-profile placement remains unsettled |
| [Temporal Integrity Metadata for Infrastructure Telemetry](https://datatracker.ietf.org/doc/draft-ackerman-temporal-integrity-metadata/) | Individual draft `-01`, 8 August 2026; no formal IETF standing | proposes source, synchronisation-state, uncertainty-bound, temporal-domain, and sequence metadata needed to judge whether heterogeneous timestamps can support causal reconstruction |
| [Telemetry identifier scoping and comparability](https://datatracker.ietf.org/doc/draft-dikshit-nmop-telemetry-identifier-scoping/) | Individual draft `-01`, 4 September 2026; no formal IETF standing | replaces the earlier four-scope vocabulary with broader requirements for uniqueness and meaningful scope, instance and observation domains, time scope, normalization, cross-context comparability, and equality-versus-identity semantics; it still defines no wire format or implementation |

## 5. What is missing

No single protocol currently supplies the minimum ingredients needed for a defensible cross-domain causal timeline:

MCP SEP-414 is a concrete improvement for the application side of that timeline: it standardises the carrier keys needed to continue a trace through agent-to-tool calls, and official SDK work makes the signal deployable. It does not connect those spans to network paths, inference queues, provider evidence, time-quality metadata, or cross-domain disclosure policy.

1. **Shared but privacy-safe correlation identifiers.** Revision `-01` of the individual telemetry-identifier-scoping draft defines useful scope and comparability requirements but no task-level wire format or cross-domain mapping. The new individual Agent Action Capsule OpenTelemetry extension proposes a concrete trace/span-to-signed-record join and reverse `aac.capsule_id`, with clear, digest-only, and never-enters rules. It still has no formal standing, depends on another individual profile, leaves its top-level placement unsettled, and binds two records from one producer rather than establishing independent truth.
2. **Time quality and uncertainty.** The individual TIM draft proposes provenance, synchronisation-state, temporal-domain, and bounded-uncertainty metadata, but it has no formal IETF standing, implementation evidence, transport binding, or guarantee that declared quality is correct.
3. **A common evidence vocabulary.** Queue time, provider ingress, TTFT, tool timeout, route change, and packet loss must have stable semantics. OpenTelemetry's aggregate-versus-per-operation token split and vLLM's event-versus-token distinction demonstrate why names alone are insufficient. The individual Agent Run Metrics draft proposes run/step accounting, while the individual agent-audit-record draft now has executable vectors for a canonical signed decision/effect schema; neither has formal IETF standing or established cross-provider interoperability.
4. **Topology and service mapping.** The OPSAWG Data Manifest preserves platform, schema, subscription, and collection context for network observations. The new CATS working-group YANG draft maps local service and service-contact-instance IDs to locations, metrics, counters, and notifications. Evidence still must be bound from those local objects to the transaction across domains without exposing unrestricted topology.
5. **Per-recipient disclosure policy.** A participant may share health or causal evidence without sharing prompts, customer identities, internal topology, or raw telemetry. The Agent Action Capsule OpenTelemetry draft's allow-list, digest-only option, and `never-enters` rules are a concrete proposal, but they are not an adopted cross-domain policy and trace identifiers can themselves unlock user-bearing systems.
6. **Sampling and incident retention.** Rare failures are easily lost when every domain samples independently. GenAI's early agent-name attributes can inform local sampling, while proposed BMP windowed extrema can preserve some excursions; neither coordinates retention across domains, guarantees incident coverage, or makes incompatible measurement windows comparable.
7. **Retry and delegation lineage.** Agent Run Metrics proposes parent/root lineage; the new individual Agent Operation Continuity draft adds preservation of uncertain attempt evidence during executor replacement, but only inside one authoritative coordination domain. Neither has established cross-provider interoperability or supplies a universal privacy-safe task identity.
8. **State and cache affinity evidence.** Failover quality depends on context, session, KV-cache, and warm-capacity state—not only path availability. GenAI cache-token accounting describes usage, and vLLM v0.31.0 expands implementation-specific offload, residency, and connector-failure metrics. None establishes transferable cache state, compatibility, or warm capacity at an alternative provider.
9. **Trust, integrity, and audit.** Consumers need evidence provenance, policy, and tamper detection. Revision `-01` of the individual AI Audit Reference Architecture expands scoped records and verification roles; the separate agent-audit-record draft now has a tagged 47-vector corpus and two reference verifiers; and the Agent Action Capsule extension proposes a signed trace join. None has formal IETF standing or verified cross-provider interoperability. Published vectors improve executable consistency but signatures, internal coherence, and same-producer spans still do not establish completeness, identity binding, observation vantage, or outcome truth.
10. **Cross-domain governance.** Retention, revocation, sovereignty, liability, and commercial policy require explicit control.

## 6. Minimum useful causal timeline

A useful reconstruction does not require every metric. It needs enough evidence to place the critical events:

1. task starts and correlation context is created;
2. endpoint/provider and service instance are selected;
3. provider ingress is observed;
4. inference admission and queue time are recorded;
5. model execution and first output are observed;
6. tool/data calls and delegated tasks are linked;
7. network or routing events are correlated with their uncertainty;
8. retries, fallback, and completion are linked to the original task;
9. every disclosed item retains source, time quality, policy, and maturity metadata.

## 7. FOX as a working hypothesis

[FOX](fox.md), a **Federated Observability Exchange**, is one possible neutral model for coordinating selected evidence. It is intentionally presented as a design question, not as a finished protocol or product.

The route-server analogy is useful but limited: FOX would not own every participant's data. It could provide identity, schema discovery, policy, subscriptions, audit, and correlation services while participants retain control of detailed evidence.

## 8. Research questions

- Which agentic and distributed-inference workflows actually cross administrative boundaries today?
- Which delays dominate by workload: network, queue, prefill, decode, tool, data, or retry?
- Which identifiers can safely propagate between organisations?
- What is the minimum evidence each participant would disclose during an incident?
- Can time uncertainty be represented consistently enough for causal ordering?
- When is aggregate health sufficient, and when is transaction-level evidence necessary?
- Which current standards can be combined without creating a new protocol?
- Which gaps genuinely require a neutral exchange layer?

## 9. Interpretation rule

Entries in this document are classified using the maturity rules in [methodology.md](methodology.md). An Internet-Draft is work in progress. A product feature demonstrates implementation, not interoperability. A working concept such as FOX is a hypothesis until independently implemented and evaluated.
