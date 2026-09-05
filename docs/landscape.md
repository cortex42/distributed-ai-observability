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
| [OpenTelemetry GenAI Semantic Conventions](https://github.com/open-telemetry/semantic-conventions-genai) | Separate pre-release repository; no release at baseline | GenAI client, model, tool, MCP, metrics, event, and provider-specific conventions | fast-moving and not yet a released, stable cross-provider contract |
| [Model Context Protocol trace propagation](https://modelcontextprotocol.io/seps/414-request-meta) | 2026-07-28 specification release candidate; SEP-414 Final in the MCP process | Carries W3C `traceparent`, `tracestate`, and `baggage` in JSON-RPC `_meta`; official SDK documentation describes request spans and propagation | the specification is a release candidate rather than an IETF or W3C standard; propagation and SDK coverage vary, and metadata crossing trust boundaries needs strict policy |

### Inference and metric evidence

| Protocol or system | Current baseline | What it contributes | Remaining cross-domain gap |
| --- | --- | --- | --- |
| [vLLM observability](https://docs.vllm.ai/en/stable/design/metrics/) | Rolling stable implementation documentation | Prometheus metrics and OpenTelemetry traces; model forward/execute timing | provider deployment and enabled signals vary |
| [vLLM per-request metrics](https://docs.vllm.ai/en/latest/features/per_request_metrics/) | Request timing introduced July 2026; experimental speculative-decoding acceptance fields documented 20 August 2026 | Request-level queue time, TTFT, generation time, inter-token latency, and token rate, plus opt-in speculative-decoding acceptance length, rate, and distribution | acceptance fields may change, collection is disabled by default and limited to single-sequence requests, and neither feature solves provider-to-network correlation |
| [NVIDIA Triton metrics](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/metrics.html) and [tracing](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/trace.html) | Rolling product documentation | Prometheus request/GPU/cache metrics and per-request Triton or OpenTelemetry traces | signal names, retention, sampling, and disclosure remain deployment-specific |
| [OpenMetrics 1.0](https://prometheus.io/docs/specs/om/open_metrics_spec/) | Stable specification | Widely adopted metric exposition format | aggregates are often insufficient for causal attribution to one task |
| [OpenMetrics 2.0](https://prometheus.io/docs/specs/om/open_metrics_spec_2_0/) | Experimental release candidate | Evolves the metric format and improves alignment with the OpenTelemetry data model | not yet stable; adoption and compatibility must be tracked |

### Network state, flows, routing, and paths

| Protocol or system | Current baseline | What it contributes | Remaining cross-domain gap |
| --- | --- | --- | --- |
| [OpenConfig gNMI](https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-specification.md) | Revision history lists v0.11.0, March 2026; document header still states v0.10.0 | Configuration, operational state retrieval, and streaming telemetry | device data lacks a standard task-to-topology correlation model; the version-text mismatch is itself worth monitoring |
| [YANG-Push](https://datatracker.ietf.org/doc/rfc8641/) | RFC 8639/8640/8641 family | Periodic and on-change publication of YANG-modelled operational data | schema, access policy, and correlation identifiers vary |
| [IPFIX](https://datatracker.ietf.org/doc/rfc7011/) | RFC 7011 / STD 77 | Standard export of traffic-flow information | flow records generally identify conversations, not application critical paths |
| [BGP Monitoring Protocol](https://datatracker.ietf.org/doc/rfc7854/) | RFC 7854 plus active extensions | Route views and BGP session/change evidence | a route event can coincide with, but not prove, application or inference delay |
| [STAMP](https://datatracker.ietf.org/doc/rfc8762/) and TWAMP | RFC 8762 and RFC 5357 | Active one-way and round-trip delay, variation, and loss measurement | probes provide indirect evidence and depend on placement and time quality |
| [IOAM](https://datatracker.ietf.org/doc/rfc9197/) | RFC 9197 family, including direct export and YANG work | In-domain on-path operational and telemetry data | designed for limited domains; cross-domain policy and exposure are unresolved |
| [Network Telemetry Framework](https://datatracker.ietf.org/doc/rfc9232/) | RFC 9232 | A useful taxonomy spanning push, pull, active, passive, and hybrid techniques | framework rather than a transaction-correlation mechanism |
| [On-Path Telemetry YANG](https://datatracker.ietf.org/doc/draft-ietf-ippm-on-path-telemetry-yang/) | IETF working-group draft `-06`, 26 August 2026 | Augments the AltMark and IOAM YANG models with loss/delay evidence, timestamp type, IOAM data, and IPFIX-aligned path-delay summaries for YANG-Push | work in progress; limited to specific on-path methods and does not define cross-domain identifier scope, task correlation, or disclosure policy |

## 4. Particularly relevant emerging work

The following work is not proof that distributed AI observability will develop in one direction. It is important because it approaches the boundary between application outcome, compute selection, and network evidence.

| Work | Baseline status | Why it matters here |
| --- | --- | --- |
| [Computing-Aware Traffic Steering framework](https://datatracker.ietf.org/doc/draft-ietf-cats-framework/) | IETF draft `-24`; RFC Editor Queue at baseline | combines network and computing-resource information for service-instance selection, although the framework currently covers one service provider |
| [CATS OAM framework](https://datatracker.ietf.org/doc/draft-ietf-cats-oam-fw/) | IETF draft `-01`, July 2026 | explicitly spans clients, network paths, and service instances for fault and performance management |
| [CATS OAM use cases](https://datatracker.ietf.org/doc/draft-dikshit-cats-oam-usecases/) | Individual draft `-00`, July 2026 | grounds CATS OAM in use cases including multi-domain failure detection and metric-driven steering |
| [Quality of Outcome](https://datatracker.ietf.org/doc/draft-ietf-ippm-qoo/) | IETF draft `-11`, May 2026 | attempts to express application-specific network performance outcomes in a form useful to applications, users, and operators |
| [Transport Considerations for Large-Scale Distributed Inference Networks](https://datatracker.ietf.org/doc/draft-li-tsvwg-inference-transport/) | Individual draft `-00`, July 2026; no formal IETF standing | describes distributed-inference traffic such as prefill/decode KV-cache transfer and expert-parallel flows; it should be tracked, not treated as consensus |
| [Proxy Modes for Agent-Tool Protocols](https://datatracker.ietf.org/doc/draft-gaikwad-agent-proxy-modes/) | Individual draft `-00`, 13 August 2026; no formal IETF standing | proposes W3C trace propagation, append-only gateway-hop metadata, and intermediary metrics for MCP-like traffic, while also defining retry and partial-failure behaviour |
| [Temporal Integrity Metadata for Infrastructure Telemetry](https://datatracker.ietf.org/doc/draft-ackerman-temporal-integrity-metadata/) | Individual draft `-01`, 8 August 2026; no formal IETF standing | proposes source, synchronisation-state, uncertainty-bound, temporal-domain, and sequence metadata needed to judge whether heterogeneous timestamps can support causal reconstruction |
| [Telemetry identifier scoping and comparability](https://datatracker.ietf.org/doc/draft-dikshit-nmop-telemetry-identifier-scoping/) | Individual draft `-00`, 26 August 2026; no formal IETF standing | identifies recurring ambiguity in exported identifiers and proposes explicit uniqueness scopes, cross-node comparability rules, and safe handling of omitted identifiers; it defines no wire format or implementation |

## 5. What is missing

No single protocol currently supplies the minimum ingredients needed for a defensible cross-domain causal timeline:

MCP SEP-414 is a concrete improvement for the application side of that timeline: it standardises the carrier keys needed to continue a trace through agent-to-tool calls, and official SDK work makes the signal deployable. It does not connect those spans to network paths, inference queues, provider evidence, time-quality metadata, or cross-domain disclosure policy.

1. **Shared but privacy-safe correlation identifiers.** The individual telemetry-identifier-scoping draft makes a narrower but important contribution: exported network identifiers should state whether they are node-local, domain-local, controller-scoped, or globally unique, and should define cross-node comparability. It has no formal IETF standing and defines neither a task-level identifier nor a wire format, privacy policy, authentication, or mapping between application, inference, flow, route, and measurement evidence.
2. **Time quality and uncertainty.** The individual TIM draft proposes provenance, synchronisation-state, temporal-domain, and bounded-uncertainty metadata, but it has no formal IETF standing, implementation evidence, transport binding, or guarantee that declared quality is correct.
3. **A common evidence vocabulary.** Queue time, provider ingress, TTFT, tool timeout, route change, and packet loss must have stable semantics.
4. **Topology and service mapping.** Evidence must be mapped from local interfaces, paths, and service instances to the transaction without exposing unrestricted topology.
5. **Per-recipient disclosure policy.** A participant may share health or causal evidence without sharing prompts, customer identities, internal topology, or raw telemetry.
6. **Sampling and incident retention.** Rare failures are easily lost when every domain samples independently.
7. **Retry and delegation lineage.** A retry or child agent must remain attributable to the original task without creating an unlimited tracking token.
8. **State and cache affinity evidence.** Failover quality depends on context, session, KV-cache, and warm-capacity state—not only path availability.
9. **Trust, integrity, and audit.** Consumers need to know who produced evidence, under which policy, and whether it was altered.
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
