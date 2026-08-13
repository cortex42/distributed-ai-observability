# FOX: Federated Observability Exchange

Status: **Working hypothesis**

Baseline: **2026-08-13**

FOX is a possible policy-controlled framework for exchanging selected observability evidence across organisational boundaries. It is not currently a protocol, standard, DE-CIX product, or deployment commitment.

## Problem statement

Distributed inference can cross applications, enterprises, networks, interconnection points, inference providers, models, tools, and other agents. Each domain can monitor itself, but no participant can reliably explain the entire critical path.

The goal is not unrestricted access to every monitoring platform. The goal is to disclose the minimum evidence required to explain a transaction, service degradation, or failure.

## Possible functional components

| Component | Possible responsibility |
| --- | --- |
| Participant gateway | map local telemetry to shared schemas; redact and aggregate before disclosure |
| Identity and trust | authenticate organisations, services, evidence producers, and authorised consumers |
| Schema registry | publish evidence types, versions, semantics, and compatibility information |
| Policy broker | express consent, purpose, recipient, retention, granularity, and revocation rules |
| Subscription service | match authorised consumers to selected signals or incident evidence |
| Correlation service | associate task, request, flow, route, path, and provider evidence without exposing global raw identifiers |
| Audit trail | record who disclosed or accessed which evidence under which policy |

## Exchange patterns

### Brokered

Selected and redacted signals transit a neutral FOX service. This is operationally simple but increases concentration, retention, and trust concerns.

### Federated

FOX handles identity, policy, schema discovery, and authorisation while detailed evidence flows directly between participants. This reduces central data custody but is harder to coordinate.

### Hybrid

FOX carries limited health and discovery signals; transaction detail is exchanged directly after authorisation. This is currently the most plausible working model.

## Candidate evidence envelope

A future evidence item might need the following fields. This is a discussion model, not a proposed wire format:

- evidence type and schema version;
- pseudonymous transaction or correlation reference;
- producing organisation and service role;
- event or interval timestamp plus clock uncertainty;
- observation point or abstract topology role;
- value, unit, aggregation, and sampling method;
- confidence and maturity;
- disclosure policy, purpose, retention, and recipient constraints;
- integrity or provenance metadata;
- link to parent, child, retry, or delegated work.

## Non-goals

FOX should not:

- become a central lake for raw participant telemetry;
- expose prompts, completions, tool payloads, customer identities, or unrestricted topology by default;
- replace OpenTelemetry, Prometheus, gNMI, IPFIX, BMP, STAMP, IOAM, or participant monitoring platforms;
- control routing or inference placement merely because it carries observability evidence;
- claim causal certainty when timestamps, sampling, or topology mappings are incomplete;
- require every participant to disclose the same level of detail.

## Open design questions

1. Is a persistent cross-domain transaction ID safe, or should correlation use scoped and rotating references?
2. Which evidence is useful at an IXP without revealing bilateral or customer-sensitive information?
3. How is clock quality expressed and verified?
4. Should the exchange carry events, summaries, queries, or only authorisations for direct retrieval?
5. How are schema compatibility and semantic drift handled?
6. How are evidence integrity, repudiation, and retention disputes handled?
7. Can existing standards supply most of the envelope and transport?
8. What minimum viable experiment could validate the neutral-exchange hypothesis?

## Suggested first experiment

A deliberately narrow proof of concept could correlate four independently collected signals for one synthetic transaction:

1. W3C/OpenTelemetry application trace context;
2. inference queue and TTFT evidence from vLLM or Triton;
3. active path measurement using STAMP or an equivalent method;
4. route-change evidence from BMP.

Each participant would disclose only a timestamped, pseudonymous event with uncertainty and policy metadata. Success would mean reconstructing the correct critical path without central access to raw monitoring systems.
