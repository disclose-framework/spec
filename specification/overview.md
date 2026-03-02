<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Disclose Framework — Official Specification v0.2</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 15px; line-height: 1.6; color: #1a1a1a; max-width: 960px; margin: 0 auto; padding: 2rem; background: #fff; }
  h1 { font-size: 2rem; font-weight: 700; margin-bottom: 0.25rem; }
  h2 { font-size: 1.4rem; font-weight: 700; margin-top: 3rem; margin-bottom: 0.5rem; border-bottom: 2px solid #e5e5e5; padding-bottom: 0.4rem; }
  h3 { font-size: 1.1rem; font-weight: 600; margin-top: 2rem; margin-bottom: 0.5rem; color: #111; }
  p { margin: 0.6rem 0 1rem; }
  table { width: 100%; border-collapse: collapse; margin: 1rem 0 1.5rem; font-size: 0.9rem; }
  th { background: #f5f5f5; text-align: left; padding: 0.5rem 0.75rem; border: 1px solid #ddd; font-weight: 600; }
  td { padding: 0.5rem 0.75rem; border: 1px solid #ddd; vertical-align: top; }
  td code, th code { background: #f0f0f0; padding: 0.1rem 0.3rem; border-radius: 3px; font-size: 0.85rem; font-family: 'SF Mono', 'Fira Code', monospace; }
  code { background: #f0f0f0; padding: 0.1rem 0.3rem; border-radius: 3px; font-size: 0.85rem; font-family: 'SF Mono', 'Fira Code', monospace; }
  pre { background: #f5f5f5; border: 1px solid #e0e0e0; border-radius: 6px; padding: 1rem 1.25rem; overflow-x: auto; font-size: 0.85rem; line-height: 1.5; }
  blockquote { border-left: 3px solid #ccc; margin: 1rem 0; padding: 0.5rem 1rem; color: #555; background: #fafafa; }
  .new-badge { display: inline-block; background: #e8f5e9; color: #2e7d32; font-size: 0.7rem; font-weight: 700; padding: 0.1rem 0.4rem; border-radius: 3px; margin-left: 0.4rem; vertical-align: middle; letter-spacing: 0.05em; }
  .category-intro { color: #444; margin-bottom: 1rem; font-size: 0.95rem; }
  .toc { background: #f9f9f9; border: 1px solid #e5e5e5; border-radius: 6px; padding: 1rem 1.5rem; margin: 1.5rem 0 2rem; }
  .toc h4 { margin: 0 0 0.5rem; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.08em; color: #666; }
  .toc ol { margin: 0; padding-left: 1.25rem; }
  .toc li { margin: 0.2rem 0; font-size: 0.9rem; }
  .toc a { color: #0066cc; text-decoration: none; }
  .toc a:hover { text-decoration: underline; }
  .note { background: #fffbea; border-left: 3px solid #f0c040; padding: 0.6rem 1rem; margin: 0.75rem 0 1rem; font-size: 0.9rem; color: #555; }
  hr { border: none; border-top: 1px solid #e5e5e5; margin: 2.5rem 0; }
  ul { margin: 0.5rem 0 1rem; padding-left: 1.5rem; }
  li { margin: 0.3rem 0; }
  ol { margin: 0.5rem 0 1rem; padding-left: 1.5rem; }
</style>
</head>
<body>

<h1>Disclose Framework</h1>
<p style="color:#666; margin-top:0.25rem;">Official Specification — v0.2</p>

<h2>Overview</h2>
<p>The Disclose Framework is an open standard for merchant disclosure attestations designed for the emerging era of agentic commerce. As AI agents increasingly act as intermediaries between buyers and merchants — researching products, comparing options, and making or informing purchasing recommendations — they require structured, machine-readable, and verifiable information about merchant practices before they can responsibly recommend where to buy.</p>
<p>Disclose provides that infrastructure layer. It enables AI agents, platforms, and automated systems to access verified, machine-readable information about merchant practices — including return policies, fulfillment performance, review authenticity, and other behavioural signals — when making or informing purchasing decisions on behalf of buyers.</p>
<p>Disclose operates as a disclosure layer that sits above the transaction. Before an agent decides where to buy, Disclose provides the structured signal data needed to make a trustworthy recommendation. It does not process payments, manage checkout sessions, or execute transactions. Its sole function is to standardize how merchants publish verified disclosures and how agents consume them.</p>

<hr>

<h2>Overarching Guidelines</h2>
<p>The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in RFC 2119 and RFC 8174.</p>
<p>Schema notes:</p>
<ul>
  <li><strong>Date format:</strong> Always specified as RFC 3339 unless otherwise specified.</li>
  <li><strong>Numeric values:</strong> Expressed as decimals unless otherwise noted (e.g., 0.92 for 92%).</li>
  <li><strong>Rates and ratios:</strong> Always expressed as a decimal between 0 and 1 (e.g., 0.06 for 6%).</li>
  <li><strong>Time-bounded metrics:</strong> MUST include a <code>_period_days</code> companion field declaring the observation window. The default observation window is 90 days unless otherwise specified.</li>
  <li><strong>Measurement methodology:</strong> Where a metric's value depends on how it is computed, the attesting Verifier's methodology governs. Agents SHOULD consider the Verifier's stated methodology when interpreting attested values, particularly for attributes where platform definitions vary.</li>
</ul>

<hr>

<h2>Design Philosophy</h2>

<h3>Trust Is Emergent, Not Engineered</h3>
<p>The Disclose Framework does not produce trust scores, badges, tiers, or rankings. It produces structured, verifiable facts about merchant behaviour. Trust emerges from those facts as agents and buyers draw their own conclusions.</p>
<p>This is a deliberate architectural choice with three consequences:</p>
<p><strong>Merchants disclose behaviour, not claims.</strong> Every attribute in the Disclose schema is grounded in operational outcomes — repeat purchases, return rates, fulfillment accuracy, chargeback rates. These are things that happened, not assertions about quality or intent.</p>
<p><strong>The framework enforces structure, not interpretation.</strong> Disclose defines what attributes mean, how they are measured, and how they are verified. It does not define how agents should weight them, combine them, or surface them to buyers. That discretion belongs to the platform.</p>
<p><strong>No centralized authority renders verdicts.</strong> There is no "Disclose Score." There is no tier that grants a badge. A merchant that publishes a low return rate, high on-time shipment rate, and fast refund processing becomes intuitively trustworthy — not because a framework said so, but because the evidence is visible and verifiable.</p>
<p>This philosophy also protects against gaming. Scores and badges create targets. Raw, time-bounded, verifier-attested metrics are far harder to manipulate without changing actual operations.</p>

<h3>Self-Reported Attribute Integrity</h3>
<p>Merchants MAY publish disclosures without attestations. Self-reported attributes carry no third-party verification and agents SHOULD treat them accordingly. The framework does not currently define a formal dispute process for false self-reported disclosures; however, platforms consuming Disclose data MAY implement their own policies for flagging or deprioritizing merchants whose self-reported attributes are demonstrably inconsistent with other observable signals. A future extension to this specification will define a community-based flagging and review process.</p>

<hr>

<h2>Core Concepts</h2>

<h3>The Three-Party Model</h3>
<p>Disclose defines three participants:</p>
<table>
  <thead><tr><th>Participant</th><th>Role</th></tr></thead>
  <tbody>
    <tr><td>Merchant</td><td>Publishes disclosure data about their own practices under their own domain</td></tr>
    <tr><td>Verifier</td><td>An authorized third party that attests to the accuracy of specific merchant disclosures using cryptographic signatures</td></tr>
    <tr><td>Agent</td><td>A platform, AI assistant, or automated system that queries and consumes disclosure data on behalf of a buyer</td></tr>
  </tbody>
</table>
<p>Unlike transaction protocols, Disclose does not require real-time negotiation between parties. Merchants publish; verifiers attest; agents consume. The flow is asynchronous and cacheable.</p>

<h3>Merchant Sovereignty</h3>
<p>A core principle of the Disclose Framework is that merchants retain full sovereignty over their disclosures. Participation is voluntary. Merchants choose which attributes to disclose, which verifiers to authorize, and when disclosures are updated or removed. The framework standardizes the format and verification mechanism — not the content or extent of disclosure.</p>

<h3>Selective Disclosure</h3>
<p>There is no all-or-nothing requirement. A merchant may publish a single attribute and add additional attributes over time as their business matures or as competitive incentives emerge. This progressive enhancement model lowers the barrier to participation while preserving the integrity of the standard.</p>

<h3>Commerce Risk Coverage</h3>
<p>The standard attribute set is designed to address the core risks an agent must evaluate before recommending a purchase:</p>
<table>
  <thead><tr><th>Risk Dimension</th><th>Covered By</th></tr></thead>
  <tbody>
    <tr><td>Product Quality</td><td>Repeat purchase rate, product return rate, defect rate</td></tr>
    <tr><td>Inventory Reliability</td><td>In-stock rate, inventory accuracy rate, backorder rate</td></tr>
    <tr><td>Delivery Reliability</td><td>On-time shipment rate, delivered on time rate, order accuracy rate</td></tr>
    <tr><td>Financial Risk</td><td>Refund processing time, chargeback rate, dispute win rate</td></tr>
    <tr><td>Service Reliability</td><td>Customer support resolution time, first contact resolution rate</td></tr>
    <tr><td>Pricing Integrity</td><td>Average discount rate, price stability rate, promotional frequency</td></tr>
    <tr><td>Long-term Value</td><td>Subscription churn rate</td></tr>
    <tr><td>Merchant Legitimacy</td><td>Business registration, domain age, platform seller tenure</td></tr>
  </tbody>
</table>
<p>No single dimension dominates. Agents weight these signals according to their own risk models and buyer context.</p>

<hr>

<h2>Discovery</h2>

<h3>Publication Endpoint</h3>
<p>Merchants publish their disclosure document at a well-known URI:</p>
<pre>/.well-known/disclose</pre>
<p>This endpoint MUST return a valid JSON document conforming to the Disclose schema. The endpoint SHOULD support HTTP caching via standard <code>Cache-Control</code> headers.</p>
<p>Example request:</p>
<pre>GET /.well-known/disclose HTTP/1.1
Host: merchant.example.com
Accept: application/json</pre>

<h3>Discovery by Agents</h3>
<p>Agents MAY fetch the disclosure document before, during, or after capability negotiation with a merchant's commerce infrastructure. Agents SHOULD cache disclosure documents according to HTTP cache-control directives.</p>
<p>Agents MUST NOT require a disclosure document to be present in order to complete a transaction. The absence of a disclosure document is itself a signal; agents MAY surface this to buyers or use it in ranking logic.</p>

<hr>

<h2>Disclosure Document Structure</h2>

<h3>Top-Level Fields</h3>
<table>
  <thead><tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr></thead>
  <tbody>
    <tr><td><code>disclose_version</code></td><td>string</td><td>Yes</td><td>Specification version (e.g., <code>"0.2"</code>)</td></tr>
    <tr><td><code>merchant_domain</code></td><td>string</td><td>Yes</td><td>The canonical domain of the merchant (e.g., <code>"merchant.example.com"</code>)</td></tr>
    <tr><td><code>issued_at</code></td><td>string</td><td>Yes</td><td>RFC 3339 timestamp of when this document was generated</td></tr>
    <tr><td><code>expires_at</code></td><td>string</td><td>No</td><td>RFC 3339 timestamp after which agents SHOULD re-fetch</td></tr>
    <tr><td><code>attributes</code></td><td>object</td><td>Yes</td><td>Flat key-value map of disclosed merchant attributes</td></tr>
    <tr><td><code>attestations</code></td><td>array</td><td>No</td><td>Array of verifier attestation objects</td></tr>
  </tbody>
</table>

<h3>Attribute Namespace</h3>
<p>All disclosure attributes exist in the <code>disclose:</code> namespace as flat properties. There are no nested categories or composite objects. This design prioritizes agent parsability over human organizational preference, and is consistent with the framework's principle that each metric stand alone.</p>
<p>Each time-bounded metric MUST be accompanied by a corresponding <code>_period_days</code> attribute declaring the observation window used to compute it.</p>
<p>Agents MUST ignore unknown attributes without error. Merchants MAY include attributes not yet defined in the core specification using their own <code>disclose:{merchant-domain}:</code> prefix.</p>

<hr>

<h2>Standard Attributes</h2>

<p>The following attributes are defined in this version of the specification. All are optional unless noted. Time-bounded metrics default to a 90-day observation window unless the corresponding <code>_period_days</code> attribute specifies otherwise.</p>
<p>Attributes marked <span class="new-badge">NEW</span> were added in v0.2.</p>

<div class="toc">
  <h4>Categories</h4>
  <ol>
    <li><a href="#product-quality">Product Quality</a></li>
    <li><a href="#returns-refunds">Returns &amp; Refunds</a></li>
    <li><a href="#fulfillment">Fulfillment</a></li>
    <li><a href="#inventory">Inventory &amp; Availability</a> <span class="new-badge">NEW</span></li>
    <li><a href="#shipping-delivery">Shipping &amp; Delivery Experience</a> <span class="new-badge">NEW</span></li>
    <li><a href="#financial-risk">Financial Risk</a></li>
    <li><a href="#customer-support">Customer Support</a></li>
    <li><a href="#pricing-conversion">Pricing &amp; Conversion</a></li>
    <li><a href="#subscriptions">Subscriptions</a></li>
    <li><a href="#sustainability-ethics">Sustainability &amp; Ethics</a></li>
    <li><a href="#identity-legitimacy">Identity &amp; Legitimacy</a> <span class="new-badge">NEW</span></li>
    <li><a href="#review-signals">Review Signals</a></li>
  </ol>
</div>

<hr>

<h2 id="product-quality">1. Product Quality</h2>
<p class="category-intro">Operational signals about product performance derived from post-purchase behaviour. These reflect what buyers actually did — returned, repurchased, reported defective — rather than what they said.</p>
<table>
  <thead><tr><th>Attribute</th><th>Type</th><th>Description</th></tr></thead>
  <tbody>
    <tr><td><code>disclose:repeat_purchase_rate</code></td><td>decimal</td><td>Rate of buyers who make a second purchase within the observation window (0–1)</td></tr>
    <tr><td><code>disclose:repeat_purchase_rate_period_days</code></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:product_return_rate</code></td><td>decimal</td><td>Rate of units returned across all orders (0–1). Measured as returned units divided by shipped units. May be disclosed at SKU or category level.</td></tr>
    <tr><td><code>disclose:product_return_rate_period_days</code></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:product_defect_rate</code> <span class="new-badge">NEW</span></td><td>decimal</td><td>Rate of units reported defective or dead-on-arrival at delivery (0–1). Distinct from return rate: captures manufacturing and quality control failures before buyer decision.</td></tr>
    <tr><td><code>disclose:product_defect_rate_period_days</code> <span class="new-badge">NEW</span></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:size_accuracy_rate</code> <span class="new-badge">NEW</span></td><td>decimal</td><td>Rate of orders where the delivered item matched the size or fit specified at purchase (0–1). Primarily relevant for apparel, footwear, and sized goods. Derived from return reason codes where available.</td></tr>
    <tr><td><code>disclose:size_accuracy_rate_period_days</code> <span class="new-badge">NEW</span></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
  </tbody>
</table>
<div class="note"><strong>Measurement note — return rate:</strong> Measured as returned units divided by total shipped units within the observation window. Exchanges (where the buyer selects a replacement item) are NOT counted as returns. Returnless refunds where no item is physically returned ARE counted. Where a Verifier attests this attribute, the Verifier's methodology governs.</div>

<hr>

<h2 id="returns-refunds">2. Returns &amp; Refunds</h2>
<p class="category-intro">Policy and performance signals covering the full returns lifecycle: what the merchant promises (policy), what they deliver (processing time), and how buyers respond (exchange vs. refund).</p>
<table>
  <thead><tr><th>Attribute</th><th>Type</th><th>Description</th></tr></thead>
  <tbody>
    <tr><td><code>disclose:return_policy_type</code></td><td>string</td><td>One of: <code>free</code>, <code>label_fee</code>, <code>buyer_pays</code>, <code>no_returns</code></td></tr>
    <tr><td><code>disclose:return_window_days</code></td><td>integer</td><td>Number of days a buyer has to initiate a return</td></tr>
    <tr><td><code>disclose:return_label_cost</code> <span class="new-badge">NEW</span></td><td>decimal</td><td>Cost of the return label in the merchant's primary currency, where <code>return_policy_type</code> is <code>label_fee</code>. Agents SHOULD surface this value alongside return policy type.</td></tr>
    <tr><td><code>disclose:refund_processing_time_median_days</code></td><td>decimal</td><td>Median business days from warehouse receipt of returned item to refund completion. Clock starts at receipt at merchant's return facility, not at return initiation or carrier pickup.</td></tr>
    <tr><td><code>disclose:refund_processing_time_p90_days</code></td><td>decimal</td><td>90th percentile business days from warehouse receipt to refund completion (same clock-start as median)</td></tr>
    <tr><td><code>disclose:exchange_rate</code></td><td>decimal</td><td>Rate of return transactions where the buyer selected a replacement item rather than a refund (0–1). A higher exchange rate signals product confidence and buyer intent to remain a customer.</td></tr>
    <tr><td><code>disclose:exchange_rate_period_days</code></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:returnless_refund_rate</code> <span class="new-badge">NEW</span></td><td>decimal</td><td>Rate of refunds issued without requiring the buyer to return the item (0–1). A higher rate signals merchant confidence in product quality and low unit economics on returns.</td></tr>
    <tr><td><code>disclose:returnless_refund_rate_period_days</code> <span class="new-badge">NEW</span></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:return_reason_top_category</code> <span class="new-badge">NEW</span></td><td>string</td><td>The most frequently cited return reason category within the observation window. Recommended values: <code>sizing</code>, <code>defective</code>, <code>not_as_described</code>, <code>changed_mind</code>, <code>arrived_late</code>, <code>other</code>.</td></tr>
    <tr><td><code>disclose:international_return_supported</code> <span class="new-badge">NEW</span></td><td>boolean</td><td>Whether the merchant supports returns from buyers outside the merchant's primary operating country.</td></tr>
  </tbody>
</table>

<hr>

<h2 id="fulfillment">3. Fulfillment</h2>
<p class="category-intro">Operational signals covering the merchant's warehouse-side fulfillment performance: whether orders leave correctly and on time. For signals covering what happens after carrier handoff, see <a href="#shipping-delivery">Shipping &amp; Delivery Experience</a>.</p>

<h3>Shipment Reliability</h3>
<table>
  <thead><tr><th>Attribute</th><th>Type</th><th>Description</th></tr></thead>
  <tbody>
    <tr><td><code>disclose:on_time_shipment_rate</code></td><td>decimal</td><td>Rate of orders shipped within the merchant's stated fulfillment window (0–1)</td></tr>
    <tr><td><code>disclose:on_time_shipment_rate_period_days</code></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:shipment_delay_median_hours</code></td><td>decimal</td><td>Median hours by which late shipments missed the promised fulfillment window</td></tr>
    <tr><td><code>disclose:shipment_delay_p90_hours</code></td><td>decimal</td><td>90th percentile hours by which late shipments missed the promised fulfillment window</td></tr>
    <tr><td><code>disclose:same_day_fulfillment_rate</code> <span class="new-badge">NEW</span></td><td>decimal</td><td>Rate of orders shipped on the same calendar day as placement, for orders placed before the merchant's same-day cutoff time (0–1).</td></tr>
    <tr><td><code>disclose:same_day_fulfillment_rate_period_days</code> <span class="new-badge">NEW</span></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:fulfillment_location_count</code> <span class="new-badge">NEW</span></td><td>integer</td><td>Number of distinct warehouse or fulfillment locations the merchant ships from. A higher count signals distributed inventory and reduced average transit distance.</td></tr>
  </tbody>
</table>

<h3>Order Accuracy</h3>
<table>
  <thead><tr><th>Attribute</th><th>Type</th><th>Description</th></tr></thead>
  <tbody>
    <tr><td><code>disclose:order_accuracy_rate</code></td><td>decimal</td><td>Rate of orders fulfilled without incorrect or damaged items (0–1)</td></tr>
    <tr><td><code>disclose:order_accuracy_rate_period_days</code></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:incorrect_item_rate</code></td><td>decimal</td><td>Rate of orders containing a wrong item (0–1)</td></tr>
    <tr><td><code>disclose:damaged_item_rate</code></td><td>decimal</td><td>Rate of orders containing a damaged item at delivery (0–1)</td></tr>
    <tr><td><code>disclose:carrier_on_time_delivery_rate</code> <span class="new-badge">NEW</span></td><td>decimal</td><td>Rate of shipments delivered on time per the carrier's own estimated delivery date (0–1). Distinguishes merchant-side fulfillment delays from carrier-side delivery delays.</td></tr>
    <tr><td><code>disclose:carrier_on_time_delivery_rate_period_days</code> <span class="new-badge">NEW</span></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
  </tbody>
</table>

<hr>

<h2 id="inventory">4. Inventory &amp; Availability <span class="new-badge">NEW</span></h2>
<p class="category-intro">Signals about whether products are actually available when an agent attempts to purchase. Inventory failures are a critical agentic commerce failure mode — an agent that recommends an out-of-stock product, or places an order against inaccurate inventory, has failed the buyer regardless of all other merchant quality signals.</p>
<table>
  <thead><tr><th>Attribute</th><th>Type</th><th>Description</th></tr></thead>
  <tbody>
    <tr><td><code>disclose:in_stock_rate</code></td><td>decimal</td><td>Rate at which listed products are in stock at the time of order placement (0–1), measured across all active SKUs within the observation window.</td></tr>
    <tr><td><code>disclose:in_stock_rate_period_days</code></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:stockout_frequency_rate</code></td><td>decimal</td><td>Rate of active SKUs that experienced at least one stockout during the observation window (0–1).</td></tr>
    <tr><td><code>disclose:stockout_frequency_rate_period_days</code></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:backorder_rate</code></td><td>decimal</td><td>Proportion of orders placed against backordered inventory (0–1). Agents SHOULD surface this to buyers who have expressed time-sensitivity.</td></tr>
    <tr><td><code>disclose:backorder_rate_period_days</code></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:inventory_accuracy_rate</code></td><td>decimal</td><td>Rate at which displayed inventory levels match actual warehouse counts at the time of order (0–1). Mismatches result in post-order cancellations — a significant buyer trust failure.</td></tr>
    <tr><td><code>disclose:inventory_accuracy_rate_period_days</code></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:pre_order_fulfillment_rate</code></td><td>decimal</td><td>For merchants who accept pre-orders: rate of pre-orders fulfilled on or before the stated availability date (0–1). Omit if the merchant does not offer pre-orders.</td></tr>
    <tr><td><code>disclose:pre_order_fulfillment_rate_period_days</code></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
  </tbody>
</table>

<hr>

<h2 id="shipping-delivery">5. Shipping &amp; Delivery Experience <span class="new-badge">NEW</span></h2>
<p class="category-intro">Post-handoff signals covering what the buyer actually experiences after an order leaves the merchant's facility. Distinct from Fulfillment, which measures warehouse-side operations. These signals require carrier tracking data and are natural attestation targets for post-purchase platforms such as Narvar and AfterShip.</p>
<table>
  <thead><tr><th>Attribute</th><th>Type</th><th>Description</th></tr></thead>
  <tbody>
    <tr><td><code>disclose:delivered_on_time_rate</code></td><td>decimal</td><td>Rate of orders delivered by the date promised to the buyer at checkout (0–1). Distinct from <code>disclose:on_time_shipment_rate</code>, which measures warehouse departure. This is the signal buyers actually experience.</td></tr>
    <tr><td><code>disclose:delivered_on_time_rate_period_days</code></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:tracking_provided_rate</code></td><td>decimal</td><td>Rate of orders for which tracking information was provided to the buyer (0–1).</td></tr>
    <tr><td><code>disclose:tracking_provided_rate_period_days</code></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:delivery_attempt_success_rate</code></td><td>decimal</td><td>Rate of shipments successfully delivered on the first carrier attempt (0–1).</td></tr>
    <tr><td><code>disclose:delivery_attempt_success_rate_period_days</code></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:average_transit_days</code></td><td>decimal</td><td>Median calendar days from ship date to confirmed delivery within the observation window.</td></tr>
    <tr><td><code>disclose:average_transit_days_period_days</code></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:carrier_selection_count</code></td><td>integer</td><td>Number of distinct carriers used by the merchant. A higher count signals redundancy and rate optimization capacity.</td></tr>
  </tbody>
</table>

<hr>

<h2 id="financial-risk">6. Financial Risk</h2>
<p class="category-intro">Signals about transaction integrity and payment reliability. Agents handling autonomous purchases on behalf of buyers have an elevated duty to assess financial risk before recommending a transaction.</p>
<table>
  <thead><tr><th>Attribute</th><th>Type</th><th>Description</th></tr></thead>
  <tbody>
    <tr><td><code>disclose:chargeback_rate</code></td><td>decimal</td><td>Chargebacks as a proportion of total transactions (0–1)</td></tr>
    <tr><td><code>disclose:chargeback_rate_period_days</code></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:dispute_win_rate</code> <span class="new-badge">NEW</span></td><td>decimal</td><td>Rate of disputed transactions resolved in the merchant's favour (0–1). Provides context for chargeback rate: a merchant with low chargebacks and a high dispute win rate has a materially stronger financial risk profile.</td></tr>
    <tr><td><code>disclose:dispute_win_rate_period_days</code> <span class="new-badge">NEW</span></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:fraud_order_rate</code> <span class="new-badge">NEW</span></td><td>decimal</td><td>Rate of orders identified as fraudulent and cancelled prior to fulfillment (0–1). Signals the merchant's fraud detection maturity and platform security posture.</td></tr>
    <tr><td><code>disclose:fraud_order_rate_period_days</code> <span class="new-badge">NEW</span></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:payment_method_coverage</code> <span class="new-badge">NEW</span></td><td>array of strings</td><td>Payment methods accepted by the merchant. Recommended values: <code>card</code>, <code>paypal</code>, <code>apple_pay</code>, <code>google_pay</code>, <code>shop_pay</code>, <code>buy_now_pay_later</code>, <code>crypto</code>, <code>bank_transfer</code>.</td></tr>
  </tbody>
</table>

<hr>

<h2 id="customer-support">7. Customer Support</h2>
<p class="category-intro">Signals about the quality, speed, and accessibility of the merchant's customer support. For agentic purchases, post-purchase support access is a material risk factor — an agent that cannot escalate a buyer issue has limited recourse.</p>
<table>
  <thead><tr><th>Attribute</th><th>Type</th><th>Description</th></tr></thead>
  <tbody>
    <tr><td><code>disclose:support_resolution_time_median_hours</code></td><td>decimal</td><td>Median hours from support contact initiation to issue resolution</td></tr>
    <tr><td><code>disclose:support_resolution_time_p90_hours</code></td><td>decimal</td><td>90th percentile hours from support contact to resolution</td></tr>
    <tr><td><code>disclose:support_channel_availability</code> <span class="new-badge">NEW</span></td><td>array of strings</td><td>Support channels available to buyers. Recommended values: <code>live_chat</code>, <code>email</code>, <code>phone</code>, <code>sms</code>, <code>social</code>, <code>self_serve</code>.</td></tr>
    <tr><td><code>disclose:support_hours_coverage</code> <span class="new-badge">NEW</span></td><td>string</td><td>Hours during which live support is available. Recommended values: <code>24_7</code>, <code>business_hours</code>, <code>extended_hours</code>, <code>async_only</code>.</td></tr>
    <tr><td><code>disclose:first_contact_resolution_rate</code> <span class="new-badge">NEW</span></td><td>decimal</td><td>Rate of support contacts resolved without requiring a follow-up interaction (0–1). A strong signal of support quality and operational maturity.</td></tr>
    <tr><td><code>disclose:first_contact_resolution_rate_period_days</code> <span class="new-badge">NEW</span></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
  </tbody>
</table>

<hr>

<h2 id="pricing-conversion">8. Pricing &amp; Conversion</h2>
<p class="category-intro">Signals about pricing integrity and buyer behaviour. These attributes help agents distinguish merchants with stable, honest pricing from those engaged in discount theater — artificial inflation followed by manufactured discounts.</p>
<table>
  <thead><tr><th>Attribute</th><th>Type</th><th>Description</th></tr></thead>
  <tbody>
    <tr><td><code>disclose:average_discount_rate</code></td><td>decimal</td><td>Average discount applied across completed transactions as a proportion of list price (0–1)</td></tr>
    <tr><td><code>disclose:average_discount_rate_period_days</code></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:search_to_conversion_rate</code></td><td>decimal</td><td>Rate of product page visits that result in a completed purchase (0–1). Signals demand authenticity and product-market fit.</td></tr>
    <tr><td><code>disclose:price_stability_rate</code> <span class="new-badge">NEW</span></td><td>decimal</td><td>Rate of active SKUs whose listed price did not change during the observation window (0–1). A low rate may indicate dynamic or promotional pricing practices that affect the reliability of displayed prices.</td></tr>
    <tr><td><code>disclose:price_stability_rate_period_days</code> <span class="new-badge">NEW</span></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:dynamic_pricing_used</code> <span class="new-badge">NEW</span></td><td>boolean</td><td>Whether the merchant uses algorithmic or demand-based dynamic pricing. Agents SHOULD surface this to buyers when the purchase context is price-sensitive.</td></tr>
    <tr><td><code>disclose:promotional_frequency_rate</code> <span class="new-badge">NEW</span></td><td>decimal</td><td>Proportion of days within the observation window on which at least one active site-wide or category-level promotion was running (0–1). A rate approaching 1.0 is a discount theater signal.</td></tr>
    <tr><td><code>disclose:promotional_frequency_rate_period_days</code> <span class="new-badge">NEW</span></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
  </tbody>
</table>

<hr>

<h2 id="subscriptions">9. Subscriptions</h2>
<p class="category-intro">Signals relevant to subscription products. These attributes apply only to merchants offering recurring purchase programmes. Agents evaluating subscription purchases face asymmetric risk: the buyer commits to ongoing charges while cancellation friction varies widely across merchants.</p>
<table>
  <thead><tr><th>Attribute</th><th>Type</th><th>Description</th></tr></thead>
  <tbody>
    <tr><td><code>disclose:subscription_churn_rate</code></td><td>decimal</td><td>Rate of active subscriptions cancelled within the observation window (0–1)</td></tr>
    <tr><td><code>disclose:subscription_churn_rate_period_days</code></td><td>integer</td><td>Observation window in days (default: 30)</td></tr>
    <tr><td><code>disclose:subscription_cancel_online</code></td><td>boolean</td><td>Whether subscriptions can be cancelled without contacting support</td></tr>
    <tr><td><code>disclose:subscription_pause_available</code></td><td>boolean</td><td>Whether subscriptions can be paused without cancelling</td></tr>
    <tr><td><code>disclose:subscription_trial_days</code></td><td>integer</td><td>Free trial duration in days, if offered. Omit if no trial is available.</td></tr>
    <tr><td><code>disclose:subscription_price_change_notice_days</code> <span class="new-badge">NEW</span></td><td>integer</td><td>Minimum number of days notice the merchant provides to subscribers before a price increase takes effect.</td></tr>
    <tr><td><code>disclose:subscription_skip_available</code> <span class="new-badge">NEW</span></td><td>boolean</td><td>Whether subscribers can skip an individual delivery without pausing or cancelling the subscription.</td></tr>
  </tbody>
</table>

<hr>

<h2 id="sustainability-ethics">10. Sustainability &amp; Ethics</h2>
<p class="category-intro">Certification-based signals about the merchant's environmental and ethical practices. These are naturally suited to third-party attestation: certifying bodies are ideal Verifier candidates for this category.</p>
<table>
  <thead><tr><th>Attribute</th><th>Type</th><th>Description</th></tr></thead>
  <tbody>
    <tr><td><code>disclose:sustainability_certified</code></td><td>boolean</td><td>Whether the merchant holds a recognized sustainability certification</td></tr>
    <tr><td><code>disclose:sustainability_certifier</code></td><td>string</td><td>Name of the certifying body (e.g., <code>B Corp</code>, <code>1% for the Planet</code>)</td></tr>
    <tr><td><code>disclose:ethical_sourcing_certified</code></td><td>boolean</td><td>Whether the merchant holds a recognized ethical sourcing certification</td></tr>
    <tr><td><code>disclose:carbon_neutral_certified</code> <span class="new-badge">NEW</span></td><td>boolean</td><td>Whether the merchant holds a recognized carbon neutral certification, distinct from general sustainability accreditation.</td></tr>
    <tr><td><code>disclose:carbon_neutral_certifier</code> <span class="new-badge">NEW</span></td><td>string</td><td>Name of the carbon neutral certifying body (e.g., <code>Climate Neutral</code>, <code>Carbon Trust</code>)</td></tr>
    <tr><td><code>disclose:living_wage_certified</code> <span class="new-badge">NEW</span></td><td>boolean</td><td>Whether the merchant holds a recognized living wage certification for their workforce.</td></tr>
    <tr><td><code>disclose:country_of_manufacture</code> <span class="new-badge">NEW</span></td><td>string or array of strings</td><td>ISO 3166-1 alpha-2 country code(s) where the merchant's products are manufactured. Relevant for ethical sourcing context and geopolitical supply chain risk assessment.</td></tr>
  </tbody>
</table>

<hr>

<h2 id="identity-legitimacy">11. Identity &amp; Legitimacy <span class="new-badge">NEW</span></h2>
<p class="category-intro">Signals that help agents distinguish legitimate merchants from fraudulent storefronts, impersonation attempts, and fly-by-night operators. This is the category most resistant to gaming: the signals are grounded in external registries — business registration databases, domain history, trademark records — rather than behavioral data the merchant controls.</p>
<div class="note"><strong>Verification note:</strong> Attributes in this category are particularly well-suited to third-party attestation. Business registry verifiers, WHOIS data providers, and trademark database services are natural Verifier candidates. Self-reported values in this category carry meaningfully less evidential weight than attested values and SHOULD be weighted accordingly by agents.</div>
<table>
  <thead><tr><th>Attribute</th><th>Type</th><th>Description</th></tr></thead>
  <tbody>
    <tr><td><code>disclose:business_registration_verified</code></td><td>boolean</td><td>Whether the merchant's legal business registration has been verified by a third party against a government business registry.</td></tr>
    <tr><td><code>disclose:domain_age_days</code></td><td>integer</td><td>Age of the merchant's primary domain in days as of the disclosure document's <code>issued_at</code> date. Derived from WHOIS registration data.</td></tr>
    <tr><td><code>disclose:trademark_registered</code></td><td>boolean</td><td>Whether the merchant's brand name is registered as a trademark in at least one major jurisdiction.</td></tr>
    <tr><td><code>disclose:platform_seller_tenure_days</code></td><td>integer</td><td>Number of days the merchant has been an active seller on their primary commerce platform as of <code>issued_at</code>. Attested by the platform.</td></tr>
    <tr><td><code>disclose:platform_seller_tenure_platform</code></td><td>string</td><td>The platform to which <code>disclose:platform_seller_tenure_days</code> refers (e.g., <code>shopify</code>, <code>amazon</code>, <code>etsy</code>).</td></tr>
  </tbody>
</table>

<hr>

<h2 id="review-signals">12. Review Signals</h2>
<p class="category-intro">Signals derived from buyer reviews and ratings. These differ from operational metrics: they are human-assessed rather than operationally derived, and more susceptible to manipulation. Agents SHOULD weight review signals in combination with operational metrics rather than in isolation.</p>
<div class="note"><strong>Recency matters:</strong> A merchant with 10,000 lifetime reviews but minimal recent activity has a materially different trust profile than a merchant with comparable volume and active ongoing engagement. Agents SHOULD weight <code>disclose:review_recency_90d_rate</code> and <code>disclose:review_recency_365d_rate</code> when interpreting <code>disclose:review_rating</code>.</div>
<table>
  <thead><tr><th>Attribute</th><th>Type</th><th>Description</th></tr></thead>
  <tbody>
    <tr><td><code>disclose:review_rating</code></td><td>decimal</td><td>Aggregate review score on a 0–5 scale</td></tr>
    <tr><td><code>disclose:review_count</code></td><td>integer</td><td>Total number of reviews included in the aggregate rating</td></tr>
    <tr><td><code>disclose:review_verified_purchase_rate</code></td><td>decimal</td><td>Proportion of reviews attributed to verified purchases (0–1). The most manipulation-resistant of the review signals.</td></tr>
    <tr><td><code>disclose:review_recency_90d_rate</code></td><td>decimal</td><td>Proportion of total reviews submitted within the last 90 days (0–1). Signals active and ongoing customer engagement.</td></tr>
    <tr><td><code>disclose:review_recency_365d_rate</code></td><td>decimal</td><td>Proportion of total reviews submitted within the last 365 days (0–1). Provides a longer-horizon view of review activity relative to lifetime review volume.</td></tr>
    <tr><td><code>disclose:review_platform</code> <span class="new-badge">NEW</span></td><td>string</td><td>The platform from which review data is derived. Recommended values: <code>own_site</code>, <code>google</code>, <code>trustpilot</code>, <code>yotpo</code>, <code>okendo</code>, <code>judge_me</code>, <code>other</code>. Agents SHOULD weight reviews from independent platforms higher than merchant-hosted reviews.</td></tr>
    <tr><td><code>disclose:review_response_rate</code> <span class="new-badge">NEW</span></td><td>decimal</td><td>Rate of reviews to which the merchant has posted a public response (0–1).</td></tr>
    <tr><td><code>disclose:review_response_rate_period_days</code> <span class="new-badge">NEW</span></td><td>integer</td><td>Observation window in days (default: 365)</td></tr>
    <tr><td><code>disclose:negative_review_rate</code> <span class="new-badge">NEW</span></td><td>decimal</td><td>Proportion of total reviews rated 2 stars or below (0–1). More granular than aggregate rating alone.</td></tr>
  </tbody>
</table>

<hr>

<h2>Attestations</h2>

<h3>Purpose</h3>
<p>An attestation is a cryptographically signed statement from an authorized Verifier confirming that one or more disclosed attributes have been independently verified against source data. Attestations distinguish Disclose from self-reported trust signals that can be easily manipulated.</p>
<p>Merchants MAY publish disclosures without attestations. Unattested attributes are self-reported and agents SHOULD treat them accordingly. Attested attributes carry the reputational weight of the signing Verifier.</p>

<h3>Attestation Object</h3>
<table>
  <thead><tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr></thead>
  <tbody>
    <tr><td><code>verifier_id</code></td><td>string</td><td>Yes</td><td>Unique identifier for the Verifier (e.g., <code>"loop-returns.com"</code>)</td></tr>
    <tr><td><code>verifier_name</code></td><td>string</td><td>Yes</td><td>Human-readable name of the Verifier</td></tr>
    <tr><td><code>attested_attributes</code></td><td>array of strings</td><td>Yes</td><td>List of <code>disclose:</code> attribute keys this attestation covers</td></tr>
    <tr><td><code>attested_at</code></td><td>string</td><td>Yes</td><td>RFC 3339 timestamp of when the attestation was issued</td></tr>
    <tr><td><code>expires_at</code></td><td>string</td><td>No</td><td>RFC 3339 timestamp after which the attestation should no longer be trusted</td></tr>
    <tr><td><code>signature</code></td><td>string</td><td>Yes</td><td>Base64url-encoded cryptographic signature over the attestation payload</td></tr>
    <tr><td><code>signing_key_id</code></td><td>string</td><td>Yes</td><td>Key ID (<code>kid</code>) corresponding to the Verifier's published signing key</td></tr>
  </tbody>
</table>

<h3>Attestation Payload</h3>
<p>The payload signed by the Verifier is a canonical JSON object containing the merchant domain, verifier ID, attested attribute values at time of attestation, and timestamps. The <code>attested_attributes</code> object contains actual attribute values — not just keys — preventing merchants from changing values after attestation without invalidating the signature.</p>

<h3>Signature Algorithm</h3>
<p>Verifiers MUST sign attestation payloads using ES256 (ECDSA with P-256 and SHA-256). Verifiers MUST publish their signing keys as JWK (JSON Web Key) objects at:</p>
<pre>/.well-known/disclose-verifier</pre>

<hr>

<h2>Verifier Registry</h2>

<h3>Purpose</h3>
<p>The Verifier Registry is the canonical list of authorized Disclose Verifiers. Its existence ensures that an attested disclosure carries meaningful weight — any party claiming to be a Verifier must be publicly listed, with their signing keys published and auditable.</p>

<h3>Registry Discovery</h3>
<p>The Verifier Registry is published and maintained by the Disclose Framework governing body at:</p>
<pre>https://discloseframework.dev/registry/verifiers.json</pre>
<p>Agents SHOULD cache this registry and refresh it periodically. Agents MUST validate that the <code>verifier_id</code> in any attestation appears in the current registry before treating the attestation as trusted.</p>

<h3>Verifier Listing</h3>
<table>
  <thead><tr><th>Field</th><th>Type</th><th>Description</th></tr></thead>
  <tbody>
    <tr><td><code>verifier_id</code></td><td>string</td><td>Unique identifier (matches the verifier's domain)</td></tr>
    <tr><td><code>verifier_name</code></td><td>string</td><td>Human-readable name</td></tr>
    <tr><td><code>verifiable_attributes</code></td><td>array of strings</td><td>The <code>disclose:</code> attributes this Verifier is authorized to attest</td></tr>
    <tr><td><code>keys_url</code></td><td>string</td><td>URL to the Verifier's <code>/.well-known/disclose-verifier</code> endpoint</td></tr>
    <tr><td><code>status</code></td><td>string</td><td>One of: <code>active</code>, <code>suspended</code>, <code>revoked</code></td></tr>
    <tr><td><code>listed_at</code></td><td>string</td><td>RFC 3339 timestamp of when the Verifier was added to the registry</td></tr>
  </tbody>
</table>

<h3>Registry Governance</h3>
<p><strong>Application.</strong> Any organization seeking Verifier status MUST submit an application to the governing body via <a href="https://github.com/disclose-framework/spec/issues">GitHub Issues</a> until the formal application process is established at <code>https://discloseframework.dev/registry/apply</code>. Applications must include: the applicant's domain, the <code>disclose:</code> attributes they seek authorization to attest, a description of their data access and verification methodology for each attribute, and their proposed signing key endpoint.</p>
<p><strong>Review.</strong> The governing body will review applications for methodology soundness, data access credibility, and potential conflicts of interest. Review outcomes are published publicly.</p>
<p><strong>Listing.</strong> Approved Verifiers are added to the registry with <code>status: active</code>. Verifiers MAY NOT attest attributes outside their approved scope.</p>
<p><strong>Suspension and Revocation.</strong> The governing body MAY suspend a Verifier (<code>status: suspended</code>) pending investigation, or revoke a Verifier (<code>status: revoked</code>) for material misrepresentation or methodology failure. Agents MUST treat attestations from suspended or revoked Verifiers as unverified.</p>
<p><strong>Appeals.</strong> Verifiers subject to suspension or revocation MAY appeal to the governing body within 30 days. The appeal process and outcomes are published publicly.</p>

<h3>Verifier Benchmarks</h3>
<p>Verifiers accumulate aggregate data across their merchant base that gives individual merchant disclosures meaningful context. A return rate of 8% means something different in apparel than in consumer electronics. Verifier benchmarks are out of scope for v0.2 of this specification. However, the field <code>disclose:benchmark_ref</code> is reserved in the attribute namespace for future use.</p>

<hr>

<h2>Security</h2>

<h3>Transport Security</h3>
<p>All Disclose endpoints MUST be served over HTTPS. HTTP requests MUST be rejected or redirected.</p>

<h3>Signature Verification</h3>
<p>Agents MUST verify attestation signatures before treating any attested attribute as verified. The verification flow is:</p>
<ol>
  <li>Fetch the Verifier Registry and confirm the <code>verifier_id</code> is listed with <code>status: active</code>.</li>
  <li>Fetch the Verifier's signing keys from their <code>keys_url</code>.</li>
  <li>Locate the key matching <code>signing_key_id</code>.</li>
  <li>Reconstruct the canonical attestation payload.</li>
  <li>Verify the ES256 signature against the payload using the public key.</li>
  <li>Confirm <code>attested_at</code> is in the past and <code>expires_at</code> (if present) is in the future.</li>
</ol>
<p>Agents MUST reject attestations that fail any step of this verification flow.</p>

<h3>Domain Binding</h3>
<p>The <code>merchant_domain</code> field in the disclosure document MUST match the domain from which the document was served. Agents MUST reject documents where these do not match.</p>

<h3>Replay Prevention</h3>
<p>Attestations include <code>attested_at</code> and <code>expires_at</code> timestamps. Agents SHOULD treat expired attestations as unverified, equivalent to self-reported attributes.</p>

<hr>

<h2>Agent Consumption Guidelines</h2>
<p>Agents consuming Disclose data operate with significant discretion. The framework does not mandate how agents weight or surface disclosure signals — this is intentionally left to the platform and agent developer. The following are non-normative recommendations:</p>
<ul>
  <li>Unattested attributes should be surfaced as merchant-reported and weighted accordingly.</li>
  <li>Attested attributes should be surfaced as independently verified, with the Verifier named when relevant to the buyer.</li>
  <li>Review signals should be distinguished from operational metrics when surfaced to buyers. Agents SHOULD treat <code>disclose:review_rating</code> as contextual rather than authoritative, and SHOULD surface <code>disclose:review_verified_purchase_rate</code> and recency signals alongside it wherever possible.</li>
  <li>Missing disclosures may be surfaced as "disclosure unavailable" rather than assumed positive or negative.</li>
  <li>Agents SHOULD NOT produce composite scores or trust tiers derived from Disclose attributes. Such aggregations undermine the principle that trust is emergent from raw, verifiable signals.</li>
  <li>Agents SHOULD NOT penalize merchants for not disclosing specific attributes unless disclosure of that attribute is required by applicable law or platform policy.</li>
</ul>

<hr>

<h2>Reference Implementation</h2>
<p>To support adoption and validate the specification, the Disclose Framework provides the following reference resources at <a href="https://github.com/disclose-framework/spec">https://github.com/disclose-framework/spec</a>:</p>
<ul>
  <li><strong>JSON Schema:</strong> A machine-readable schema for validating disclosure documents against the specification.</li>
  <li><strong>Validator:</strong> A reference validator that checks a disclosure document for schema compliance, domain binding, and <code>_period_days</code> completeness.</li>
  <li><strong>Sample document:</strong> A complete, valid example disclosure document suitable for testing agent consumption logic.</li>
  <li><strong>Verifier mock:</strong> A lightweight mock Verifier endpoint for testing signature verification flows without a live Verifier integration.</li>
</ul>
<p>Implementations that conform to the specification and pass the reference validator MAY self-identify as Disclose-compatible.</p>

<hr>

<h2>Versioning</h2>
<p>Disclose uses semantic versioning in the format <code>MAJOR.MINOR</code> (e.g., <code>0.2</code>, <code>1.0</code>). The version is declared in the disclosure document via the <code>disclose_version</code> field.</p>
<p>The following changes MAY be introduced without a version increment: adding new optional attributes, adding new optional attestation fields, adding new Verifier entries to the registry.</p>
<p>The following changes MUST result in a new MAJOR version: removing or renaming existing attributes, changing the attestation payload structure or signature algorithm, modifying the discovery endpoint path.</p>

<hr>

<h2>Glossary</h2>
<table>
  <thead><tr><th>Term</th><th>Definition</th></tr></thead>
  <tbody>
    <tr><td>Agent</td><td>A platform, AI assistant, or automated system that queries Disclose data on behalf of a buyer</td></tr>
    <tr><td>Attestation</td><td>A cryptographically signed statement from a Verifier confirming that specific disclosed attributes have been independently verified</td></tr>
    <tr><td>Benchmark Reference</td><td>An optional pointer to a Verifier-published document providing vertical or category-level distributions for disclosed attributes. Reserved for a future extension; see <code>disclose:benchmark_ref</code>.</td></tr>
    <tr><td>Disclosure Document</td><td>The JSON document published by a merchant at <code>/.well-known/disclose</code></td></tr>
    <tr><td>Emergent Trust</td><td>The principle that trustworthiness arises from visible, verifiable behaviour rather than from framework-assigned scores or badges</td></tr>
    <tr><td>Exchange Rate</td><td>The proportion of return transactions where the buyer selected a replacement item rather than a refund; a signal of product confidence distinct from the return rate</td></tr>
    <tr><td>Merchant</td><td>The entity selling goods or services, who publishes disclosure data under their own domain</td></tr>
    <tr><td>Merchant Sovereignty</td><td>The principle that merchants retain full control over what they disclose, to whom, and when</td></tr>
    <tr><td>Observation Window</td><td>The time period over which a metric is computed, declared via a companion <code>_period_days</code> attribute</td></tr>
    <tr><td>Progressive Enhancement</td><td>The ability to begin participation with a single attribute and expand disclosures over time</td></tr>
    <tr><td>Review Recency</td><td>The proportion of a merchant's total reviews submitted within a recent time window (90 or 365 days), used to assess the freshness of aggregate review ratings</td></tr>
    <tr><td>Selective Disclosure</td><td>The ability to disclose specific attributes without an all-or-nothing requirement</td></tr>
    <tr><td>Verifier</td><td>An authorized third party that cryptographically attests to the accuracy of specific merchant disclosures</td></tr>
    <tr><td>Verifier Registry</td><td>The canonical, publicly accessible list of authorized Disclose Verifiers maintained by the framework governing body</td></tr>
  </tbody>
</table>

</body>
</html>
