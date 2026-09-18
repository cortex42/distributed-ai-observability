# ntop observability stack

Checked: **2026-09-10**

Status: **Implementation evidence / production network-observability tooling**

## Why it matters

The ntop stack is relevant to distributed AI observability because it demonstrates that useful network evidence can already be collected, normalised, enriched, retained at relatively high time resolution, and exported in production systems. It does **not** solve cross-domain AI-task correlation by itself; its value is as a mature source of network-side evidence that could feed a participant gateway or other correlation layer.

## Components

### nProbe

nProbe is a flow probe and collector. Official ntop documentation describes support for NetFlow v5/v9, IPFIX, and sFlow collection, as well as generation of flow records from packet capture. It can normalise flow information and export or forward it to downstream systems.

Relevant evidence includes:

- flow endpoints and timing;
- byte and packet volumes;
- flow duration;
- exporter and interface context;
- protocol/application enrichment when used with nDPI.

For FOX-style use, nProbe is interesting because it can sit close to a participant's network edge and act as a source for selected, policy-filtered network evidence rather than requiring direct access to routers.

### ntopng

ntopng provides traffic analytics, flow visibility, application/protocol views, alerts, and time-series analysis. In 2026 ntop documented high-resolution time-series support intended to preserve short-lived traffic variation that can disappear in coarser five-minute aggregates.

That is directly relevant to distributed inference troubleshooting: a short congestion event may affect a handful of latency-sensitive AI tasks while remaining nearly invisible in coarse operational averages.

### nDPI

nDPI is ntop's deep-packet-inspection and traffic-classification library. It can enrich network observations with application/protocol classification rather than leaving the evidence as only addresses, ports, and counters.

This can improve correlation quality, but application classification also raises privacy, commercial-sensitivity, and disclosure-policy questions. A cross-domain exchange should therefore share only explicitly authorised derived evidence, not unrestricted DPI output.

## Production readiness

**Status: GREEN for network-local collection and analytics; AMBER for use in a cross-domain AI observability chain.**

The ntop stack is mature, deployed implementation technology for its network-observability scope. Its limitations are not basic collection capability but cross-domain semantics and correlation:

- a flow record does not identify the AI task or agent operation that caused it;
- application classification does not establish causal linkage to a model, queue, tool call, retry, or user-visible outcome;
- aggregation and sampling choices can still hide short incidents;
- high-detail flow and DPI evidence may be sensitive and should not be shared without explicit policy;
- there is no provider-neutral mapping from an ntop flow observation to W3C/OpenTelemetry trace context, inference-runtime identifiers, or FOX evidence objects.

## Potential FOX transport role

A practical participant-side pipeline could look like:

```text
router / packet capture
        |
        v
      nProbe ---- nDPI enrichment
        |
        v
      ntopng / local analytics
        |
        v
participant gateway
  normalise
  minimise
  redact
  attach policy + provenance
        |
        v
       FOX
```

The important architectural point is that raw packet capture, unrestricted flow records, and DPI classifications do not need to leave the participant domain. A gateway could derive and publish only evidence such as:

- flow/path health for a specific authorised time window;
- loss, retransmission, latency, or traffic-volume anomaly flags;
- service/application class where policy permits;
- ingress/egress timestamps and exporter provenance;
- aggregate health or incident summaries.

## What remains missing

ntop reinforces a central project conclusion: **the observability tools already exist in pieces**. The missing capability is consistent, privacy-safe correlation across application, agent, inference, network, and interconnection evidence.

For production cross-domain use, further work is still needed around:

1. task-to-flow correlation identifiers or mappings;
2. common evidence semantics;
3. timestamp quality and uncertainty;
4. per-recipient disclosure policy;
5. provenance and integrity of derived observations;
6. a transport/envelope for selected evidence reaching a FOX participant or broker;
7. privacy-safe handling of DPI/application classification.

## Authoritative sources

- ntop nProbe product and documentation: https://www.ntop.org/products/netflow-probes/nprobe/
- ntopng documentation on nProbe/flow collection: https://www.ntop.org/guides/ntopng/flows/nprobe.html
- ntop high-resolution time-series article: https://www.ntop.org/observability-enabling-high-resolution-timeseries-in-ntopng/
- nDPI project information: https://www.ntop.org/products/deep-packet-inspection/ndpi/

These sources demonstrate implementation capability in ntop products/projects. They do not establish industry-wide interoperability or a cross-domain standard.
