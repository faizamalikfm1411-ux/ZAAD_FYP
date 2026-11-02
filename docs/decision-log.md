# ZAAD Decision Log

**Project:** ZAAD, an agentic AI-powered AR smart menu PWA (SRS v1.2, Merged Development Plan v2.0)
**Task:** S1-KF-01 | **Prepared by:** Khansa Farooq (Team Lead) | **Reviewer:** Faiza Malik
**Decision date:** 2 Nov 2026 | **Freeze deadline:** Fri 6 Nov 2026

**Status meaning.** *Final* = selected, subject to the stated constraints. *Provisional* = preferred, to be confirmed or changed after the named spike. No test result is claimed unless it is recorded here.

## Summary

| # | Decision | Owner | Status | Date | Evidence |
|---|---|---|---|---|---|
| 1 | React + TypeScript + Vite + Tailwind, installable PWA | Hamna Mushtaq | Final | 2 Nov 2026 | Scaffold S1-HM-01; iOS test S1-HM-06 only sets the iOS support path |
| 2 | React Router, TanStack Query, Zustand (IndexedDB), i18next, MSW, Vitest, Playwright | Hamna Mushtaq | Final | 2 Nov 2026 | MSW layer S1-HM-05 |
| 3 | model-viewer (Mode 1) + MindAR.js/Three.js (Mode 2), WebXR only if Mode 3 is a go | Sara Amin | Provisional | 2 Nov 2026 | PENDING S1-SA-02 (4 Nov) |
| 4 | Web Speech API behind one `useVoice` hook | Hamna Mushtaq | Provisional | 2 Nov 2026 | PENDING S1-HM-07 (6 Nov) |
| 5 | Python FastAPI (Node/Express dropped) | Faiza Malik | Final | 2 Nov 2026 | Skeleton S1-FM-02 |
| 6 | MongoDB | Faiza Malik | Final | 2 Nov 2026 | Connection and schema in S1-FM-02 |
| 7 | ChromaDB, filtered by customer ID | Khansa Farooq | Final | 2 Nov 2026 | Retrieval and isolation tests pending (Week 12) |
| 8 | Gemini free tier, Flash-Lite class, behind the abstraction layer | Khansa Farooq | Provisional | 2 Nov 2026 | PENDING S1-KF-02 (4 Nov) |
| 9 | One model URL per dish; AWS S3 or static files on the web host | Faiza Malik | Provisional | 2 Nov 2026 | PENDING S1-SA-03 (6 Nov), S2-FM-08 (18 Nov) |
| 10 | No cache, no Redis | Khansa Farooq | Final | 2 Nov 2026 | Confirmed in S2-KF-11 (26 Nov) |
| 11 | Sign-in required for every feature; login returns a token | Faiza Malik | Final | 2 Nov 2026 | Implemented in S2-FM-07 (17 Nov) |

## 1. Frontend platform
- **Decision:** React + TypeScript + Vite + Tailwind CSS (logical properties `ms-`, `me-`, `ps-`, `pe-`), installable PWA with `vite-plugin-pwa`.
- **Owner / date / status:** Hamna Mushtaq, 2 Nov 2026, Final.
- **Alternatives:** Vue.js (SRS Table 2.2); Next.js; React without PWA support.
- **Criteria:** Team familiarity, maintainability, PWA support, responsive and RTL layout, 3D/AR library integration (SRS 2.5.1).
- **Test evidence:** The scaffold from S1-HM-01 is the prototype; add the PR link when merged. PENDING: iOS installed-PWA camera and microphone test, S1-HM-06, due 6 Nov. Its result decides whether the supported iOS path is the installed PWA or a Safari tab. It does not change the framework choice.
- **Reason:** Vite keeps the build fast for a four-person team. Types protect the allergen and calorie logic. Tailwind logical properties let English (LTR) and Urdu (RTL) share components.
- **Cost to reverse:** Medium (routing, components, tests, PWA config).
- **Constraints:** The host must serve HTTPS, or camera and microphone will not work. The service worker caches the app shell and thumbnails only, never `.glb` files. Check the host's free-tier limits before choosing it.

## 2. Frontend libraries and state
- **Decision:** React Router (auth and onboarding guard), TanStack Query, Zustand persisted to IndexedDB, i18next, MSW, Vitest, Playwright.
- **Owner / date / status:** Hamna Mushtaq, 2 Nov 2026, Final.
- **Alternatives:** Redux Toolkit with RTK Query; React Context with custom hooks; Jest and Cypress.
- **Criteria:** Separation of server and client state, persistence across PWA restarts, testability without a live backend, localization and RTL support.
- **Test evidence:** None yet. The MSW mock layer (S1-HM-05, due 5 Nov) is the first proof that the app runs on mocks.
- **Reason:** Each library has one job, so the team does not build custom routing, caching, persistence or test tooling. Cached profile and dish data also feed the rule-based fallback.
- **Cost to reverse:** Medium to high (routing, state and tests).

## 3. AR rendering
- **Decision:** model-viewer for Mode 1 (screen-locked 3D). MindAR.js with Three.js for Mode 2 (marker AR), lazy-loaded on the dish route only. WebXR only if Mode 3 is a go.
- **Owner / date / status:** Sara Amin, 2 Nov 2026, Provisional.
- **Alternatives:** Three.js alone for both modes; WebXR as the primary path; MindAR with A-Frame.
- **Criteria:** Fit with the two required modes, mobile browser compatibility, marker tracking feasibility, bundle size, 3D performance.
- **Test evidence:** PENDING: MindAR feasibility on 2 to 3 phones, S1-SA-02, due 4 Nov.
- **Reason:** model-viewer is a focused path for Mode 1, which is the guaranteed fallback. MindAR is the marker-tracking layer for the hero Mode 2 demo.
- **If the spike fails:** Mode 1 stays as the guaranteed path (SRS 4.3, UC-03 A1). Cutting Mode 2 needs supervisor approval (cut order item 6).
- **Cost to reverse:** Medium before dish assets are integrated; high after.

## 4. Voice
- **Decision:** Web Speech API behind one `useVoice` hook. Components never call the browser speech API directly.
- **Owner / date / status:** Hamna Mushtaq, 2 Nov 2026, Provisional.
- **Alternatives:** A hosted speech-to-text and text-to-speech provider; a third-party browser speech SDK; text-only.
- **Criteria:** Browser availability, English and Urdu coverage, permission handling, cost, graceful behavior when a language is unsupported.
- **Test evidence:** PENDING: Urdu voice test, S1-HM-07, due 6 Nov (scored in S1-KF-06, also 6 Nov).
- **Reason:** One hook is the single place to detect missing support and handle the Urdu fallback.
- **If Urdu is unsupported:** Urdu text and touch plus English voice, with a one-time notice to the customer (FR-VCE-08).
- **Cost to reverse:** Medium. Changing the hook's public contract costs more than changing what is behind it.

## 5. Backend framework
- **Decision:** Python FastAPI. Node.js/Express is dropped.
- **Owner / date / status:** Faiza Malik, 2 Nov 2026, Final.
- **Alternatives:** Node.js/Express (SRS Table 2.2); NestJS; Django REST Framework.
- **Criteria:** Fit with AI/LLM libraries, API validation, testing, deployment, team proficiency.
- **Test evidence:** The FastAPI skeleton with `/health` returning 200 (S1-FM-02, due 4 Nov) is the proof of concept; add the PR link when done. No benchmark is claimed.
- **Reason:** LangChain, ChromaDB and the Gemini SDK are Python-native, so there is no second backend stack.
- **Cost to reverse:** Low now; high once routes, schemas and deployment exist.

## 6. Primary database
- **Decision:** MongoDB for dishes, profiles, nutrition and allergen data.
- **Owner / date / status:** Faiza Malik, 2 Nov 2026, Final.
- **Alternatives:** PostgreSQL (SRS Table 2.2); Firebase Firestore; SQLite.
- **Criteria:** Document fit for dishes and profiles, schema evolution, hosting options, backups, free-tier limits.
- **Test evidence:** The database connection and dish schema draft in S1-FM-02. Check the free-tier limits of the chosen host and record them here.
- **Reason:** Dishes, profiles and nutrition fit documents (SRS 6.3). MongoDB is the authoritative store for these; it is not the vector store.
- **Cost to reverse:** High after repositories and indexes depend on it.

## 7. Vector memory
- **Decision:** ChromaDB for taste memory, filtered by customer ID.
- **Owner / date / status:** Khansa Farooq, 2 Nov 2026, Final.
- **Alternatives:** FAISS (SRS Table 2.2); MongoDB Atlas Vector Search; PostgreSQL with pgvector.
- **Criteria:** Persistence, metadata filtering, customer isolation, retrieval quality, deployment effort.
- **Test evidence:** PENDING: retrieval test on the pre-seeded five-session profile (Week 12). Also required: a test proving one customer cannot retrieve another's vectors.
- **Reason:** Low cost and a simple setup. Customer isolation is a security boundary, so the customer ID must come from the authenticated session on the server, never from a request field.
- **Cost to reverse:** Medium to high (embeddings, metadata and IDs must be exported and revalidated).

## 8. LLM provider
- **Decision:** Gemini free tier, Flash-Lite class model, behind the abstraction layer. The provider is one config value.
- **Owner / date / status:** Khansa Farooq, 2 Nov 2026, Provisional.
- **Alternatives:** Another hosted provider (SRS Table 2.2); a local open-weight model.
- **Criteria:** Latency against the 3 s budget, free-tier quota and rate limits, English and Urdu quality, availability, cost.
- **Test evidence:** PENDING: LLM latency test, S1-KF-02, due 4 Nov (20+ calls, median and p95 against 3 s).
- **Reason:** A Flash-Lite class model is the low-latency, low-cost candidate for ARIA. The abstraction keeps a provider change to one config value.
- **Constraints:** Model names and free-tier limits change, so re-check them in Week 1. API keys never go in the PWA or the repository. The 3 s timeout is enforced regardless of provider. The Allergy Guardian never calls the LLM.
- **Cost to reverse:** Low to medium if the abstraction is kept; high if provider-specific logic leaks into business code.

## 9. 3D model storage
- **Decision:** One model URL per dish. The target is AWS S3 or static files on the web host, chosen after the pipeline spike.
- **Owner / date / status:** Faiza Malik, 2 Nov 2026, Provisional.
- **Alternatives:** Firebase Storage (SRS Table 2.2); AWS S3; static files on the web host.
- **Criteria:** Model load time, CORS and URL needs, cost, bandwidth limits, licensing, ease of delivery on target mobile browsers.
- **Test evidence:** PENDING: model pipeline on 2 dishes, S1-SA-03, due 6 Nov. Hosting and CORS test on a phone: S2-FM-08, due 18 Nov.
- **Reason:** One URL per dish keeps the app independent of the storage vendor; switching is a one-line change.
- **Constraints:** If S3 is chosen, set CORS early and a budget alert before uploading. Models go from storage straight to the phone, not through the API (NFR-ARCH-04). The service worker never caches `.glb` files.
- **Cost to reverse:** Low if URLs stay behind one configuration value.

## 10. Caching
- **Decision:** No Redis and no extra cache. Add one only if measurement shows a benefit.
- **Owner / date / status:** Khansa Farooq, 2 Nov 2026, Final.
- **Alternatives:** Redis; in-process FastAPI cache.
- **Criteria:** Measured latency benefit, invalidation complexity, risk of stale allergen or profile data, deployment effort.
- **Test evidence:** No measurement yet. The decision is recorded formally in S2-KF-11 (26 Nov); the SRS Appendix B target is 30 Nov.
- **Reason:** The SRS says to profile performance before adding a cache. A stale allergen or profile value is a safety risk.
- **Cost to reverse:** Low to medium.

## 11. Authentication scope
- **Decision:** Sign-in is required before any feature (SRS 2.2, FR-PROF-19, FR-PROF-21). `/auth/login` returns a token and a `profileComplete` flag (Plan 6.3).
- **Owner / date / status:** Faiza Malik, 2 Nov 2026, Final.
- **Alternatives:** Treat JWT as unnecessary (the open question in SRS Appendix B).
- **Criteria:** SRS 2.2 requires sign-in for every feature; the profile must link to an account.
- **Test evidence:** Implementation and 12+ tests in S2-FM-07 (due 17 Nov). Token type and expiry are recorded there.
- **Note:** NFR-SEC-03 and NFR-SEC-04 are not complete until access control is implemented and tested with authorised and unauthorised sessions.
- **Cost to reverse:** High once the frontend guard and API depend on it.

## Pending evidence

| Row | Spike | Owner | Due | Needed |
|---|---|---|---|---|
| 1 | S1-HM-06 iOS installed-PWA camera and mic | Hamna | 6 Nov | Result per iPhone and iOS version; supported path logged |
| 3 | S1-SA-02 MindAR feasibility | Sara | 4 Nov | Results matrix and go/no-go for Mode 2 |
| 4 | S1-HM-07 Urdu voice (scored in S1-KF-06) | Hamna, Khansa | 6 Nov | Per-phone recognition list and verdict |
| 8 | S1-KF-02 LLM latency | Khansa | 4 Nov | Table of 20+ calls, median and p95 against 3 s |
| 9 | S1-SA-03 model pipeline | Sara | 6 Nov | 2 `.glb` files of 3 MB or less, load times, budget proposal |
| 7 | ChromaDB retrieval and isolation | Khansa | Week 12 | Retrieval on the seeded profile; cross-customer test |

All provisional rows must be changed to Final, or explicitly re-scoped, by Fri 6 Nov 2026. Three spikes (S1-HM-06, S1-HM-07, S1-SA-03) are due on the freeze day itself. If a spike fails or is missing, record that fact. Never record it as passed.

## Change process

Update this file in the same pull request as any change. Record: the new decision and what it affects; one owner; the date; at least two alternatives, including the previous choice; criteria; real test evidence or a PENDING spike with its due date; the reason; and the cost to reverse. The team lead coordinates review. The decision owner prepares the rationale and evidence.
