# The `disclose.json` Convention
### A Standard File Location for Merchant Signals
**Disclose Framework — Convention Specification v0.1**

---

## Overview

`disclose.json` is a standardized file that merchants publish at a predictable location on their domain. Any AI agent, MCP server, or automated system can retrieve it without prior knowledge of the merchant's platform, tech stack, or API.

It is to AI agents what `robots.txt` is to web crawlers — a known address, a standard format, a voluntary signal.

---

## File Location

Merchants publish the file at the root of their domain:

```
https://www.merchantname.com/disclose.json
```

This location is canonical and non-negotiable. Agents check this path. No configuration, discovery, or registration is required.

---

## Full Example

```json
{
  "@context": "https://discloseframework.dev/schema/v1",
  "@type": "MerchantDisclosure",
  "schema_version": "1.0",
  "issued_at": "2026-03-01T00:00:00Z",
  "expires_at": "2026-06-01T00:00:00Z",
  "merchant": {
    "name": "Example Store",
    "domain": "examplestore.com",
    "jurisdiction": "CA"
  },
  "signals": {
    "fulfillment_time_days_median": 2.1,
    "return_rate_percent": 4.3,
    "refund_rate_percent": 1.8,
    "on_time_delivery_rate_percent": 97.2,
    "customer_satisfaction_score": 4.6,
    "inventory_accuracy_percent": 99.1
  },
  "verifications": [
    {
      "signal": "return_rate_percent",
      "verifier": "Loop Returns",
      "verifier_url": "https://loopreturns.com",
      "verified_at": "2026-02-15T00:00:00Z",
      "method": "platform_data"
    },
    {
      "signal": "fulfillment_time_days_median",
      "verifier": "Narvar",
      "verifier_url": "https://narvar.com",
      "verified_at": "2026-02-15T00:00:00Z",
      "method": "platform_data"
    }
  ],
  "permitted_use": {
    "agent_query": true,
    "real_time_recommendation": true,
    "aggregation": false,
    "benchmarking": false,
    "third_party_republication": false,
    "commercial_resale": false,
    "attribution_required": true,
    "attribution_text": "Data self-disclosed by examplestore.com via Disclose Framework"
  }
}
```

---

## Field Reference

### Root Fields

| Field | Required | Description |
|---|---|---|
| `@context` | Yes | Points to the Disclose Framework schema |
| `@type` | Yes | Always `MerchantDisclosure` |
| `schema_version` | Yes | Version of the spec used |
| `issued_at` | Yes | When this file was last generated (ISO 8601) |
| `expires_at` | Recommended | When agents should re-fetch. Prevents stale data use |
| `merchant` | Yes | Identifying information about the merchant |
| `signals` | Yes | The performance data being disclosed |
| `verifications` | Optional | Third-party attestations for specific signals |
| `permitted_use` | Yes | How agents and platforms may use this data |

---

### The `signals` Object

Merchants publish only the signals they choose. All fields are optional. Publishing a subset is valid and encouraged over publishing inaccurate data.

| Signal | Type | Description |
|---|---|---|
| `fulfillment_time_days_median` | Float | Median days from order to shipment |
| `return_rate_percent` | Float | Returns as % of orders over trailing 90 days |
| `refund_rate_percent` | Float | Refunds as % of orders over trailing 90 days |
| `on_time_delivery_rate_percent` | Float | % of orders delivered within estimated window |
| `customer_satisfaction_score` | Float | Verified CSAT score (0–5 scale) |
| `inventory_accuracy_percent` | Float | % of listed SKUs in stock at time of disclosure |

---

### The `permitted_use` Object

This is the merchant's explicit permission layer. Legitimate agents and platforms that implement the Disclose Framework **must** respect these flags. Scrapers may not — but published permissions establish norms, create accountability, and give merchants meaningful control.

| Flag | Type | Description |
|---|---|---|
| `agent_query` | Boolean | Agent may query this data for a single purchasing decision |
| `real_time_recommendation` | Boolean | Agent may use this data to recommend the merchant to a user |
| `aggregation` | Boolean | Platform may aggregate this data across merchants |
| `benchmarking` | Boolean | Platform may use this data in vertical benchmarks |
| `third_party_republication` | Boolean | Third parties may republish this data |
| `commercial_resale` | Boolean | Third parties may sell this data commercially |
| `attribution_required` | Boolean | Any use must credit the merchant as the source |
| `attribution_text` | String | Preferred attribution string if `attribution_required` is true |

**Default stance:** If `permitted_use` is omitted entirely, agents should treat the data as `agent_query: true` only and nothing else.

---

## Caching and Freshness

Agents should:
- Respect the `expires_at` field and re-fetch when stale
- Not cache beyond 24 hours if `expires_at` is absent
- Treat a missing or unreachable `disclose.json` as no disclosure, not as failure

---

## Minimal Valid Example

A merchant who only wants to disclose one signal, with no verifications:

```json
{
  "@context": "https://discloseframework.dev/schema/v1",
  "@type": "MerchantDisclosure",
  "schema_version": "1.0",
  "issued_at": "2026-03-01T00:00:00Z",
  "merchant": {
    "name": "Small Shop Co",
    "domain": "smallshop.co"
  },
  "signals": {
    "fulfillment_time_days_median": 1.5
  },
  "permitted_use": {
    "agent_query": true,
    "aggregation": false,
    "commercial_resale": false,
    "attribution_required": true,
    "attribution_text": "Data self-disclosed by smallshop.co via Disclose Framework"
  }
}
```

---

## Relationship to JSON-LD Schema Markup

`disclose.json` is the **standalone file convention**. Merchants may also embed Disclose signals as JSON-LD in their page `<head>` for agents that parse HTML. The two approaches are complementary:

- **`disclose.json`** — for agents that query the file directly (MCP servers, GPT Actions, LangChain tools)
- **JSON-LD in `<head>`** — for agents that browse and parse pages (browser agents, crawlers)

Both use the same schema. Merchants implementing both get maximum coverage.

---

## Implementation Checklist for Merchants

- [ ] Create `disclose.json` using the schema above
- [ ] Choose which signals to publish (start with one if needed)
- [ ] Set `permitted_use` flags explicitly
- [ ] Host the file at `yourdomain.com/disclose.json`
- [ ] Set `expires_at` 90 days out and update on a regular cadence
- [ ] Optionally add JSON-LD to your homepage `<head>` for browser agents

---

## For Agent Developers

To query a merchant's disclosure:

```
GET https://{merchant_domain}/disclose.json
Accept: application/json
```

Check `permitted_use` before acting. If `agent_query` is false or absent, do not use the data. If `attribution_required` is true, surface the `attribution_text` to the user when presenting recommendations based on this data.

---

*Disclose Framework is an open standard. Contribute at github.com/disclose-framework*
