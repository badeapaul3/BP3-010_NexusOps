# Module 10: Production Observability, SRE & Cloud Operations

## Objectives
Implement enterprise-grade observability and Site Reliability Engineering (SRE) practices. Instrument Python microservices with OpenTelemetry distributed tracing, Prometheus RED metrics, high-performance structured JSON logging with `structlog`, and automated incident response alerting.

---

## Observability Architecture

```text
┌────────────────────────────────────────────────────────┐
│               FastAPI / AI Microservice                │
│                                                        │
│  ┌────────────────┐ ┌────────────────┐ ┌─────────────┐ │
│  │ OpenTelemetry  │ │ Prometheus     │ │ structlog   │ │
│  │ Tracing Spans  │ │ RED Metrics    │ │ JSON Logs   │ │
│  └───────┬────────┘ └───────┬────────┘ └──────┬──────┘ │
└──────────┼──────────────────┼─────────────────┼────────┘
           │ W3C Context      │ /metrics pull   │ stdout
           ▼                  ▼                 ▼
┌────────────────────────────────────────────────────────┐
│             OpenTelemetry Collector / Agent            │
└──────────────────────────┬─────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
┌─────────────────┐┌─────────────────┐┌──────────────────┐
│ Traces: Jaeger  ││ Metrics:        ││ Logs: CloudWatch │
│ / Cloud Trace   ││ Prometheus/     ││ / Cloud Logging  │
│ / Datadog       ││ Grafana         ││ / Loki           │
└─────────────────┘└─────────────────┘└──────────────────┘
```

---

## Core Topics
1. **Distributed Tracing with OpenTelemetry (OTel):**
   - W3C Trace Context propagation (`traceparent` header) across service boundaries.
   - Instrumenting FastAPI, SQLAlchemy, HTTPX clients, and custom LangChain/LangGraph execution runs.
   - Custom spans, attributes, semantic conventions, and exception recording.
   - Exporting traces via OTLP (OpenTelemetry Protocol) to collectors (Jaeger, AWS X-Ray, GCP Cloud Trace).
2. **High-Performance Structured Logging with `structlog`:**
   - Why plain text logs fail at scale in cloud log aggregators.
   - Building a zero-allocation, JSON-formatted structured logging pipeline.
   - Automatic contextual binding: injecting `request_id`, `tenant_id`, `trace_id`, and `span_id` into every log entry.
   - PII and sensitive data scrubbing filters (masking API keys, authorization tokens, credit cards).
3. **Application Metrics & The RED Method:**
   - Implementing the RED method: Rate (req/sec), Errors (5xx rate), and Duration (latency histograms: p50, p95, p99).
   - Custom business metrics: LLM token consumption counters, cache hit/miss gauges, and database connection pool saturation.
   - Prometheus `/metrics` scraping endpoints with secure internal networking.
4. **Site Reliability Engineering (SRE) Practices:**
   - Defining Service Level Indicators (SLIs) and Service Level Objectives (SLOs) (e.g. 99.9% of requests < 200ms).
   - Error Budget depletion alerting with Prometheus Alertmanager.
   - Graceful degradation: Fallbacks, load shedding, and circuit opening under sustained overload.

---

## Planned Directory Structure
```text
Module_10_Observability_SRE_Cloud_Operations/
├── README.md
├── src/
│   └── observability/
│       ├── __init__.py
│       ├── telemetry.py         # OpenTelemetry tracer provider & OTLP exporter
│       ├── logging.py           # structlog processors & JSON formatter
│       ├── metrics.py           # Prometheus meters & RED middleware
│       └── context.py           # ContextVar correlation & trace binding
├── monitoring/
│   ├── prometheus.yml           # Prometheus scrape configuration
│   ├── alertmanager.yml         # SLO breach alert rules
│   └── grafana/
│       └── dashboards/          # Pre-built Grafana dashboard JSON (RED & JVM/Python runtime)
└── tests/
    └── test_telemetry.py        # Automated trace and log verification tests
```

---

## Verification Criteria
- [ ] End-to-end trace context propagates across simulated multi-service HTTP calls.
- [ ] Log outputs are valid JSON with injected `trace_id` and `span_id` correlating to OTel spans.
- [ ] Prometheus scrapes `/metrics` and records p95/p99 latency histograms accurately.
- [ ] Alert rules trigger as expected when simulated synthetic error rates exceed error budgets.
