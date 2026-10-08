# Security Architecture & LexConnect

Parselex is positioned as a **Secure Legal Enclave**: a private AI workspace for
legal professionals that is only reachable through **LexConnect**, our Zero-Trust
network client. This page documents the architecture for a technical audience
(CIO / CISO / IT director). The marketing-facing summary lives on the
[`/security/`](../security/index.html) page of the main site.

> **The problem this solves.** Law firms are reluctant to use public AI tools
> because uploading case files to a shared cloud risks waiving attorney-client
> privilege. Parselex addresses this with two reinforcing mechanisms: a
> Zero-Trust network layer (LexConnect) and edge-side PII redaction (the
> "Ethics Firewall").

## What is LexConnect?

LexConnect is the repurposing of a custom mesh-VPN / tunneling client
(codename `nullvpn`) into a Zero-Trust Network Access (ZTNA) product for the
legal industry. The client establishes an encrypted, device-to-workspace mesh
tunnel. Workspaces and inference nodes carry **no public IP addresses** — they
are invisible to internet-wide scanning, and there are no shared entry points
to attack.

**Feature mapping (old VPN capability → LexConnect capability):**

| Old VPN feature | LexConnect capability | Value for a law firm |
|-----------------|----------------------|----------------------|
| Multi-hop / exit nodes | Private AI ingress gateway | Inference nodes have no public IPs; immune to scanning and DDoS |
| Kill switch | Automatic session tear-down + jurisdiction policy | Tunnel drops instantly on untrusted networks or out-of-policy locations |
| DNS filtering | DLP & malware DNS shield | Blocks outbound calls to unauthorized third-party APIs (data loss prevention) |
| No-logs privacy | Access auditing without content logging | Who/when is logged (security, billing); the payload never is |
| Token-based auth | SSO + device posture checks | Entra ID / Okta sign-in; client connects only on healthy, managed devices |

## The Ethics Firewall: edge-side PII redaction

The redaction engine runs **on the lawyer's device**, before traffic enters the
tunnel — a capability cloud-only competitors cannot easily replicate:

```
Raw text
  → Presidio Analyzer (PII detection)
  → Presidio Anonymizer (deterministic tokenization)
  → encrypted LexConnect tunnel
  → private inference (vLLM)
  → encrypted tunnel (return path)
  → de-anonymization (local re-identification)
  → finished document in the UI
```

- `John Doe` → `[PERSON_1]`, `Acme Corp` → `[ENTITY_A]`, `SSN 123-45-6789` →
  `[REDACTED_SSN]`.
- Inference engines reason over the **structure and logic** of a matter; the
  confidential identities never leave the laptop.
- A **custom entity dictionary** (Pro tier) lets the lawyer tag parties —
  e.g. `[CLIENT]` vs `[OPPOSING_COUNSEL]` — so the AI keeps distinctions that
  matter for work product.
- Planned stack: Microsoft **Presidio** (spaCy + regex) plus custom regex
  patterns for legal identifiers (court case numbers, tax IDs, license
  formats); optional lightweight local NER for jurisdiction-specific entities.

Because identities are stripped at the edge, the server side processes
sanitized tokens rather than personal data — the basis for marketing the
pipeline as **zero-knowledge PII processing** and for the "reasonable efforts"
framing under professional-conduct rules (ABA Model Rule 1.6 analogues), with a
material reduction of GDPR/CCPA exposure for the firm.

## Threat model (published, not promised)

**Protected against:**

- Man-in-the-middle interception between client and workspace.
- Passive network / ISP observation of document content.
- Internet-wide scanning and DDoS against inference infrastructure (no public endpoints).
- Public-cloud data scraping (workspace content is not hosted on shared public cloud services).
- Unauthorized outbound calls from the AI client to third-party APIs (DNS-layer DLP).

**Outside our control (user responsibility):**

- A device left unlocked and unattended.
- A compromised endpoint operating system or endpoint malware.
- Phishing of firm SSO credentials (mitigated, not eliminated, by MFA).
- Authorized insiders acting within their permissions.
- Screen capture by a person with lawful access to the display.

## Processing & logging posture

- **Ephemeral sessions** — the working context exists in memory for the session
  and is discarded when it closes.
- **No content logging** — prompts and payloads are never written to logs;
  connection metadata (who, when, device class) is cryptographically separated
  from session content.
- **No training on firm data** — case files never train public models.
- **Data sovereignty options** — for solo practitioners and small firms a
  bring-your-own-infrastructure deployment is on the roadmap: the workspace
  container runs in the firm's own cloud account, LexConnect provides the
  secure overlay.

## Compliance vocabulary (approved vs banned)

Approved for all public copy: **Zero-Trust Architecture**, **cryptographically
isolated**, **ephemeral sessions**, **data sovereignty**, **least-privilege
access**, **attorney-client privilege enforced**.

Never used on Parselex properties: "100% secure", "unhackable",
"military-grade encryption", "we take security seriously", "anonymous" /
"hide your IP", "bulletproof".

## Where this lives

| Asset | Location |
|-------|----------|
| Public security page (5 languages) | `/security/`, `/ru/security/`, `/es/security/`, `/fr/security/`, `/hi/security/` |
| Landing section | `index.html` → "Security by Architecture, Not by Promise" |
| Technology stack list | `index.html` → System Architecture → Technology Stack |
| Generator | `scripts/s80_security_pages.py` + `scripts/s80_security_{ru,es,fr,hi}.py` |
| Landing i18n additions | `scripts/s80_tr_{ru,es,fr,hi}_add.py` (merged by `scripts/s72_build_i18n.py`) |
