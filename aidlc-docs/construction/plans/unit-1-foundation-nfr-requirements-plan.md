# NFR Requirements Plan — Unit 1: Foundation

## Questions

## Question 1: JWT Signing Algorithm
Which JWT algorithm should be used?

A) HS256 — symmetric, single secret key, simpler deployment

B) RS256 — asymmetric, public/private key pair, more secure for distributed systems

C) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 2: Password Hashing
How many bcrypt rounds for password hashing?

A) 12 rounds (standard balance of security vs speed)

B) 10 rounds (faster, suitable for high-traffic login)

C) 14 rounds (more secure, slower)

D) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 3: Connection Pool Size
What database connection pool configuration?

A) pool_size=10, max_overflow=20 (moderate, good for expected load)

B) pool_size=5, max_overflow=10 (smaller, for dev/light use)

C) pool_size=20, max_overflow=40 (larger, for high concurrency)

D) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Artifacts Checklist

- [ ] Create `nfr-requirements.md` — Scalability, performance, security, reliability requirements
- [ ] Create `tech-stack-decisions.md` — Pinned library versions and rationale
