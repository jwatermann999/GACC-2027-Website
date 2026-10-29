# GACC security launch checklist

This is a deployment checklist, not evidence that a control is enabled. Website source is public, but account security and DNS/provider settings are configured in separate dashboards.

## GitHub settings (owner action)
- [ ] Require multifactor authentication for every account with write or admin access.
- [ ] GitHub repository > Settings > Rules > Rulesets: add an **Active** branch ruleset targeting `main`.
- [ ] Block force pushes and deletion. Require changes through pull requests and the `public-source-guardrails` status check once it has run successfully. If there is only one maintainer, do **not** require a reviewer who cannot approve their own PR.
- [ ] Verify Settings > Pages > **Enforce HTTPS**. Confirm the configured domain is the intended GACC domain.
- [ ] Turn on GitHub secret scanning and Dependabot alerts where available. Review connected apps and collaborators.

## Hosting, DNS and Cloudflare (requires domain/Cloudflare admin)
- [ ] Record existing DNS records **before any nameserver changes**, especially mail, SPF, DKIM, DMARC, Brevo, and domain verification records.
- [ ] Confirm HTTPS, certificate validity, HTTP-to-HTTPS redirects and HSTS policies in production.
- [ ] If using Cloudflare, verify the DNS proxy is active for website records and set SSL/TLS according to the actual origin configuration. Prefer strict origin verification where supported.
- [ ] Verify the applicable Cloudflare WAF managed rules, bot/rate limits and security event monitoring. Do not challenge legitimate Stripe redirects or Brevo forms.
- [ ] Add response security headers at the hosting/proxy layer only after testing a Content Security Policy in report-only mode. This site uses Google Analytics, external signup links and some embedded content.
- [ ] Back up domain/DNS configuration and verify website rollback.

## Dealer applications and mailing lists
- [ ] Review whether FormSubmit processing and forwarding dealer personal data into email is appropriate. Limit access and email retention.
- [ ] Never request full card numbers, CVV/CVC, bank account numbers, passwords or Social Security numbers in the application.
- [ ] Confirm Brevo double opt-in and Turnstile/CAPTCHA are active and test with a new signup.
- [ ] Turn on account MFA for email, Brevo, Stripe and domain registrar; keep access to named trusted individuals.
- [ ] Review the public privacy notice for accuracy, legal requirements and actual processing practices before publishing.
- [ ] Authenticate outgoing domain mail with SPF, DKIM and DMARC after confirming legitimate senders.

## Stripe go-live gate
- [ ] Use Stripe-hosted Checkout, Payment Links or Invoices for the initial launch; do not put secret API keys in public HTML or JavaScript.
- [ ] For individual dealer credits/deposits, create and verify the amount within Stripe, not from editable browser totals.
- [ ] Enable Stripe MFA, restrict team roles, configure payouts and notifications, and review Radar fraud rules.
- [ ] If custom backend/webhooks are implemented, authenticate Stripe signatures, use idempotency, and verify payments server-side before marking records paid.
- [ ] Test successful, failed, duplicate, refunded and disputed payment cases in test mode.
- [ ] Review Stripe's PCI guidance for the final payment method. Set an incident response contact and a refund/dispute process.

**Current state:** this checklist must be performed by account administrators. A successful GitHub source check alone does not certify website or payment security.
