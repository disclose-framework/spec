<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Disclose Framework — Standard Attributes v0.2</title>
<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 15px;
    line-height: 1.6;
    color: #1a1a1a;
    max-width: 960px;
    margin: 0 auto;
    padding: 2rem;
    background: #fff;
  }
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
</style>
</head>
<body>

<h1>Disclose Framework</h1>
<p style="color:#666; margin-top:0.25rem;">Standard Attributes — Specification v0.2</p>

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

<h2>Standard Attributes</h2>
<p>The following attributes are defined in this version of the specification. All are optional unless noted. Time-bounded metrics default to a 90-day observation window unless the corresponding <code>_period_days</code> attribute specifies otherwise.</p>
<p>Attributes marked <span class="new-badge">NEW</span> were added in v0.2.</p>

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
    <tr><td><code>disclose:same_day_fulfillment_rate</code> <span class="new-badge">NEW</span></td><td>decimal</td><td>Rate of orders shipped on the same calendar day as placement, for orders placed before the merchant's same-day cutoff time (0–1). Agents SHOULD surface this for time-sensitive purchases.</td></tr>
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
    <tr><td><code>disclose:stockout_frequency_rate</code></td><td>decimal</td><td>Rate of active SKUs that experienced at least one stockout during the observation window (0–1). A higher rate signals inventory planning weaknesses.</td></tr>
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
    <tr><td><code>disclose:delivery_attempt_success_rate</code></td><td>decimal</td><td>Rate of shipments successfully delivered on the first carrier attempt (0–1). Failed first attempts result in buyer inconvenience and delay.</td></tr>
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
    <tr><td><code>disclose:dispute_win_rate</code> <span class="new-badge">NEW</span></td><td>decimal</td><td>Rate of disputed transactions resolved in the merchant's favour (0–1). Provides context for chargeback rate: a merchant with low chargebacks and a high dispute win rate has a materially stronger financial risk profile than chargeback rate alone would indicate.</td></tr>
    <tr><td><code>disclose:dispute_win_rate_period_days</code> <span class="new-badge">NEW</span></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:fraud_order_rate</code> <span class="new-badge">NEW</span></td><td>decimal</td><td>Rate of orders identified as fraudulent and cancelled prior to fulfillment (0–1). Signals the merchant's fraud detection maturity and platform security posture.</td></tr>
    <tr><td><code>disclose:fraud_order_rate_period_days</code> <span class="new-badge">NEW</span></td><td>integer</td><td>Observation window in days (default: 90)</td></tr>
    <tr><td><code>disclose:payment_method_coverage</code> <span class="new-badge">NEW</span></td><td>array of strings</td><td>Payment methods accepted by the merchant. Recommended values: <code>card</code>, <code>paypal</code>, <code>apple_pay</code>, <code>google_pay</code>, <code>shop_pay</code>, <code>buy_now_pay_later</code>, <code>crypto</code>, <code>bank_transfer</code>. Agents SHOULD verify payment method compatibility before initiating checkout.</td></tr>
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
    <tr><td><code>disclose:support_channel_availability</code> <span class="new-badge">NEW</span></td><td>array of strings</td><td>Support channels available to buyers. Recommended values: <code>live_chat</code>, <code>email</code>, <code>phone</code>, <code>sms</code>, <code>social</code>, <code>self_serve</code>. Agents SHOULD surface available channels when escalation may be needed.</td></tr>
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
    <tr><td><code>disclose:promotional_frequency_rate</code> <span class="new-badge">NEW</span></td><td>decimal</td><td>Proportion of days within the observation window on which at least one active site-wide or category-level promotion was running (0–1). A rate approaching 1.0 suggests the merchant's list price does not reflect the price at which goods typically transact — a discount theater signal.</td></tr>
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
    <tr><td><code>disclose:subscription_price_change_notice_days</code> <span class="new-badge">NEW</span></td><td>integer</td><td>Minimum number of days notice the merchant provides to subscribers before a price increase takes effect. A higher value signals buyer-friendly pricing governance.</td></tr>
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
<p class="category-intro">Signals that help agents distinguish legitimate merchants from fraudulent storefronts, impersonation attempts, and fly-by-night operators. This is the category most resistant to gaming: the signals are grounded in external registries — business registration databases, domain history, trademark records — rather than behavioral data the merchant controls. As agentic commerce scales, counterfeit merchant risk becomes a material threat vector that no existing trust signal framework addresses.</p>
<div class="note"><strong>Verification note:</strong> Attributes in this category are particularly well-suited to third-party attestation. Business registry verifiers, WHOIS data providers, and trademark database services are natural Verifier candidates. Self-reported values in this category carry meaningfully less evidential weight than attested values and SHOULD be weighted accordingly by agents.</div>
<table>
  <thead><tr><th>Attribute</th><th>Type</th><th>Description</th></tr></thead>
  <tbody>
    <tr><td><code>disclose:business_registration_verified</code></td><td>boolean</td><td>Whether the merchant's legal business registration has been verified by a third party against a government business registry. Agents SHOULD weight attested values materially higher than self-reported values for this attribute.</td></tr>
    <tr><td><code>disclose:domain_age_days</code></td><td>integer</td><td>Age of the merchant's primary domain in days as of the disclosure document's <code>issued_at</code> date. Derived from WHOIS registration data. Older domains carry meaningfully higher legitimacy signal for first-time buyer interactions.</td></tr>
    <tr><td><code>disclose:trademark_registered</code></td><td>boolean</td><td>Whether the merchant's brand name is registered as a trademark in at least one major jurisdiction.</td></tr>
    <tr><td><code>disclose:platform_seller_tenure_days</code></td><td>integer</td><td>Number of days the merchant has been an active seller on their primary commerce platform as of <code>issued_at</code>. Attested by the platform. Longer tenure is a strong signal against fraudulent storefronts.</td></tr>
    <tr><td><code>disclose:platform_seller_tenure_platform</code></td><td>string</td><td>The platform to which <code>disclose:platform_seller_tenure_days</code> refers (e.g., <code>shopify</code>, <code>amazon</code>, <code>etsy</code>).</td></tr>
  </tbody>
</table>

<hr>

<h2 id="review-signals">12. Review Signals</h2>
<p class="category-intro">Signals derived from buyer reviews and ratings. These differ from operational metrics: they are human-assessed rather than operationally derived, and more susceptible to manipulation. They are included because they carry recognized signal value for agents and buyers. Agents SHOULD weight review signals in combination with operational metrics rather than in isolation.</p>
<div class="note"><strong>Recency matters:</strong> A merchant with 10,000 lifetime reviews but minimal recent activity has a materially different trust profile than a merchant with comparable volume and active ongoing engagement. Agents SHOULD weight <code>disclose:review_recency_90d_rate</code> and <code>disclose:review_recency_365d_rate</code> when interpreting <code>disclose:review_rating</code>.</div>
<table>
  <thead><tr><th>Attribute</th><th>Type</th><th>Description</th></tr></thead>
  <tbody>
    <tr><td><code>disclose:review_rating</code></td><td>decimal</td><td>Aggregate review score on a 0–5 scale</td></tr>
    <tr><td><code>disclose:review_count</code></td><td>integer</td><td>Total number of reviews included in the aggregate rating</td></tr>
    <tr><td><code>disclose:review_verified_purchase_rate</code></td><td>decimal</td><td>Proportion of reviews attributed to verified purchases (0–1). The most manipulation-resistant of the review signals.</td></tr>
    <tr><td><code>disclose:review_recency_90d_rate</code></td><td>decimal</td><td>Proportion of total reviews submitted within the last 90 days (0–1). Signals active and ongoing customer engagement.</td></tr>
    <tr><td><code>disclose:review_recency_365d_rate</code></td><td>decimal</td><td>Proportion of total reviews submitted within the last 365 days (0–1). Provides a longer-horizon view of review activity relative to lifetime review volume.</td></tr>
    <tr><td><code>disclose:review_platform</code> <span class="new-badge">NEW</span></td><td>string</td><td>The platform or source from which review data is derived. Recommended values: <code>own_site</code>, <code>google</code>, <code>trustpilot</code>, <code>yotpo</code>, <code>okendo</code>, <code>judge_me</code>, <code>other</code>. Agents SHOULD weight reviews from independent platforms higher than merchant-hosted reviews.</td></tr>
    <tr><td><code>disclose:review_response_rate</code> <span class="new-badge">NEW</span></td><td>decimal</td><td>Rate of reviews to which the merchant has posted a public response (0–1). Signals active merchant engagement with buyer feedback.</td></tr>
    <tr><td><code>disclose:review_response_rate_period_days</code> <span class="new-badge">NEW</span></td><td>integer</td><td>Observation window in days (default: 365)</td></tr>
    <tr><td><code>disclose:negative_review_rate</code> <span class="new-badge">NEW</span></td><td>decimal</td><td>Proportion of total reviews rated 2 stars or below (0–1). More granular than aggregate rating: a merchant with a 4.2 average but an 18% negative review rate has a materially different risk profile than one with a 4.2 average and a 4% negative review rate.</td></tr>
  </tbody>
</table>

<hr>

<h2>Attribute Count Summary</h2>
<table>
  <thead><tr><th>Category</th><th>v0.1</th><th>Added in v0.2</th><th>v0.2 Total</th></tr></thead>
  <tbody>
    <tr><td>1. Product Quality</td><td>4</td><td>+4</td><td>8</td></tr>
    <tr><td>2. Returns &amp; Refunds</td><td>6</td><td>+5</td><td>11</td></tr>
    <tr><td>3. Fulfillment</td><td>8</td><td>+4</td><td>12</td></tr>
    <tr><td>4. Inventory &amp; Availability</td><td>—</td><td>+10</td><td>10</td></tr>
    <tr><td>5. Shipping &amp; Delivery Experience</td><td>—</td><td>+9</td><td>9</td></tr>
    <tr><td>6. Financial Risk</td><td>2</td><td>+5</td><td>7</td></tr>
    <tr><td>7. Customer Support</td><td>2</td><td>+5</td><td>7</td></tr>
    <tr><td>8. Pricing &amp; Conversion</td><td>2</td><td>+6</td><td>8</td></tr>
    <tr><td>9. Subscriptions</td><td>5</td><td>+2</td><td>7</td></tr>
    <tr><td>10. Sustainability &amp; Ethics</td><td>3</td><td>+5</td><td>8</td></tr>
    <tr><td>11. Identity &amp; Legitimacy</td><td>—</td><td>+5</td><td>5</td></tr>
    <tr><td>12. Review Signals</td><td>5</td><td>+4</td><td>9</td></tr>
    <tr style="font-weight:bold; background:#f5f5f5;"><td>Total (inc. _period_days)</td><td>37</td><td>+64</td><td>101</td></tr>
    <tr style="font-weight:bold; background:#f0f0f0;"><td>Substantive signals only</td><td>~24</td><td>+~37</td><td>~61</td></tr>
  </tbody>
</table>
<p style="color:#555; font-size:0.9rem;">Substantive signal count excludes <code>_period_days</code> companion fields. "60+ signals across 12 categories" is an accurate characterisation of v0.2.</p>

</body>
</html>
