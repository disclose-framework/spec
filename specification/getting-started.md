# Getting Started with Disclose

### Publishing Your First Disclosure Document
**Disclose Framework — Quick Start Guide**

---

## Overview

A Disclose disclosure document is a JSON file merchants publish at a predictable location on their domain. Any AI agent, MCP server, or automated system can retrieve it without prior knowledge of the merchant's platform, tech stack, or API.

It is to AI agents what `robots.txt` is to web crawlers — a known address, a standard format, a voluntary signal.

The full specification is in [`specification/overview.md`](overview.md). This guide covers what you need to publish a valid disclosure document and get discovered.

---

## File Location

Publish your disclosure document at:

```
https://www.merchantname.com/.well-known/disclose
```

This is the canonical path. Agents check here first. No registration or configuration required.

If your hosting platform does not support the `/.well-known/` directory (some hosted storefronts do not), agents will also check `/.well-known/disclose.json` before falling back to the domain root:

```
https://www.merchantname.com/disclose.json
```

Agents will fall back to the root path if both `/.well-known/` paths return a 404.

---

## Minimal Valid Example

A merchant disclosing a single signal — no attestations required to get started:

```json
{
  "disclose_version": "0.2",
  "merchant_domain": "merchantname.com",
  "issued_at": "2026-03-01T00:00:00Z",
  "expires_at": "2026-06-01T00:00:00Z",
  "attributes": {
    "disclose:on_time_shipment_rate": 0.97,
    "disclose:on_time_shipment_rate_period_days": 90
  }
}
```

That's a valid Disclose implementation. Publish it and any agent that knows the convention can find it.

---

## Full Example with Attestations

A merchant with verified signals from Loop Returns and Narvar:

```json
{
  "disclose_version": "0.2",
  "merchant_domain": "merchantname.com",
  "issued_at": "2026-03-01T00:00:00Z",
  "expires_at": "2026-06-01T00:00:00Z",
  "attributes": {
    "disclose:repeat_purchase_rate": 0.38,
    "disclose:repeat_purchase_rate_period_days": 90,
    "disclose:product_return_rate": 0.06,
    "disclose:product_return_rate_period_days": 90,
    "disclose:return_policy_type": "free",
    "disclose:return_window_days": 30,
    "disclose:on_time_shipment_rate": 0.97,
    "disclose:on_time_shipment_rate_period_days": 90,
    "disclose:delivered_on_time_rate": 0.94,
    "disclose:delivered_on_time_rate_period_days": 90,
    "disclose:chargeback_rate": 0.003,
    "disclose:chargeback_rate_period_days": 90,
    "disclose:review_rating": 4.7,
    "disclose:review_count": 14200,
    "disclose:review_verified_purchase_rate": 0.91
  },
  "attestations": [
    {
      "verifier_id": "loop-returns.com",
      "verifier_name": "Loop Returns",
      "attested_attributes": [
        "disclose:product_return_rate",
        "disclose:product_return_rate_period_days",
        "disclose:return_policy_type",
        "disclose:return_window_days"
      ],
      "attested_at": "2026-02-15T00:00:00Z",
      "expires_at": "2026-08-15T00:00:00Z",
      "signature": "eyJhbGciOiJFUzI1NiIsImtpZCI6Imxvb3AtMjAyNiJ9...",
      "signing_key_id": "loop-2026"
    },
    {
      "verifier_id": "narvar.com",
      "verifier_name": "Narvar",
      "attested_attributes": [
        "disclose:on_time_shipment_rate",
        "disclose:on_time_shipment_rate_period_days",
        "disclose:delivered_on_time_rate",
        "disclose:delivered_on_time_rate_period_days"
      ],
      "attested_at": "2026-02-15T00:00:00Z",
      "expires_at": "2026-08-15T00:00:00Z",
      "signature": "eyJhbGciOiJFUzI1NiIsImtpZCI6Im5hcnZhci0yMDI2In0...",
      "signing_key_id": "narvar-2026"
    }
  ]
}
```

---

## Top-Level Fields

| Field | Required | Description |
|---|---|---|
| `disclose_version` | Yes | Spec version. Use `"0.2"` |
| `merchant_domain` | Yes | Your canonical domain. Must match the domain serving the file |
| `issued_at` | Yes | When this document was generated (RFC 3339) |
| `expires_at` | Recommended | When agents should re-fetch. Set 90 days out |
| `attributes` | Yes | Flat key-value map of your disclosed signals |
| `attestations` | Optional | Cryptographically signed verifications from authorized third parties |

---

## Choosing What to Disclose

All attributes are optional. Publish what you have clean data for. A single accurate signal is better than ten inaccurate ones.

Good starting signals for most merchants:

| Signal | What it tells agents |
|---|---|
| `disclose:on_time_shipment_rate` | Whether orders leave on time |
| `disclose:product_return_rate` | How often buyers return products |
| `disclose:delivered_on_time_rate` | Whether buyers receive orders when promised |
| `disclose:chargeback_rate` | Financial risk profile |
| `disclose:review_rating` + `disclose:review_verified_purchase_rate` | Review quality signal |

Every time-bounded metric requires a companion `_period_days` field declaring the observation window. The default is 90 days.

The full attribute reference — 61 signals across 12 categories — is in [`specification/overview.md`](overview.md).

---

## Attested vs. Self-Reported Signals

Agents treat attested and self-reported signals differently.

**Self-reported:** You publish the attribute with no attestation. Agents surface it as merchant-reported and weight it accordingly. Valid and useful — better than nothing.

**Attested:** An authorized Verifier with direct data access cryptographically signs the attribute. Agents surface it as independently verified. Significantly stronger signal.

Attestations come from Verifiers listed in the [Disclose Verifier Registry](https://discloseframework.dev/registry/verifiers.json). If you use Loop Returns, Narvar, AfterShip, or Recharge, ask them about Disclose attestation support.

---

## Permitted Use

The `permitted_use` object is an optional permission layer that tells agents and platforms how they may use your data.

```json
"permitted_use": {
  "agent_query": true,
  "real_time_recommendation": true,
  "aggregation": false,
  "benchmarking": false,
  "third_party_republication": false,
  "commercial_resale": false,
  "attribution_required": true,
  "attribution_text": "Data self-disclosed by merchantname.com via Disclose Framework"
}
```

If `permitted_use` is omitted, agents treat the data as `agent_query: true` only.

---

## Caching and Freshness

- Set `expires_at` 90 days from `issued_at` and regenerate on a regular cadence
- Agents will re-fetch when the document expires
- A missing or unreachable file is treated as no disclosure — not as an error

---

## JSON-LD in Storefront Head

For agents that browse pages rather than querying files directly, you can also embed Disclose signals as JSON-LD in your storefront `<head>`:

```html
<script type="application/ld+json">
{
  "@context": {
    "@vocab": "https://schema.org/",
    "disclose": "https://discloseframework.dev/vocab#"
  },
  "@type": "Organization",
  "disclose:product_return_rate": 0.06,
  "disclose:product_return_rate_period_days": 90,
  "disclose:on_time_shipment_rate": 0.97,
  "disclose:on_time_shipment_rate_period_days": 90
}
</script>
```

The two approaches use the same schema and are complementary. `/.well-known/disclose` for agents querying directly; JSON-LD for agents parsing pages.

---

## Implementation Checklist

- [ ] Create your disclosure document using the schema above
- [ ] Choose which signals to publish — start with one if needed
- [ ] Set `permitted_use` flags if you want explicit control over data use
- [ ] Publish at `/.well-known/disclose` on your domain
- [ ] Set `expires_at` 90 days out and schedule regular updates
- [ ] Optionally embed JSON-LD in your storefront `<head>` for browser agents

---

## For Agent Developers

To query a merchant's disclosure:

```
GET https://{merchant_domain}/.well-known/disclose
Accept: application/json
```

Fall back to `https://{merchant_domain}/.well-known/disclose.json`, then `https://{merchant_domain}/disclose.json` if the canonical path returns a 404.

Verify attestation signatures against the [Verifier Registry](https://discloseframework.dev/registry/verifiers.json) before treating attested attributes as verified. Full verification flow is in [`specification/overview.md`](overview.md).

---

*Disclose Framework is an open standard. Contribute at [github.com/disclose-framework](https://github.com/disclose-framework)*
