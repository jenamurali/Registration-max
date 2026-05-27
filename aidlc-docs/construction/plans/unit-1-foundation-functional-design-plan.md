# Functional Design Plan — Unit 1: Foundation

## Questions

## Question 1: User Model Scope
What user fields are needed for auth?

A) Minimal — username, password_hash only (no roles, simple auth)

B) Standard — username, email, password_hash, role (Admin, Operator), is_active

C) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 2: JWT Token Configuration
What JWT token lifetimes should be used?

A) Access token 30 min + Refresh token 7 days

B) Access token 1 hour + Refresh token 30 days

C) Access token 15 min + Refresh token 24 hours

D) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 3: Base Repository
Should the base repository include soft delete support?

A) Yes — all entities use soft delete (is_deleted flag)

B) No — hard deletes only

C) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 4: Database Session Scope
How should the SQLAlchemy async session be scoped?

A) Per-request via FastAPI dependency (yield session per request)

B) Per-transaction (create new session for each UOW commit)

C) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Design Artifacts Checklist

- [ ] Create `business-logic-model.md` — Base repository, UOW, auth flow
- [ ] Create `business-rules.md` — Auth rules, token validation, middleware logic
- [ ] Create `domain-entities.md` — User entity, base model, relationships
