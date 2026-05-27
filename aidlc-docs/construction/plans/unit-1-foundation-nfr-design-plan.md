# NFR Design Plan — Unit 1: Foundation

## Questions

## Question 1: Rate Limiting Storage
Where should rate limiting state be stored?

A) In-memory (dict) — simple, lost on restart, single instance only

B) Database table — persistent, shared across instances

C) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 2: Log Format
What log output format?

A) JSON structured logs (machine-parseable)

B) Human-readable text logs (easier local dev)

C) Both — JSON in production, text in development (configurable)

D) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## Artifacts Checklist

- [ ] Create `nfr-design-patterns.md` — Security, resilience, performance patterns
- [ ] Create `logical-components.md` — Middleware stack, DI chain, component wiring
