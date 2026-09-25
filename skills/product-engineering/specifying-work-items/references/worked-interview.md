# Worked interview

One compact, fictional example. Pantrybox is an invented online-shop builder for small food producers, and every name and path below is invented. The example runs from the request, through grounding and two rounds, to the G1 summary and the spec that results.

## Contents

- The request
- Grounding: what the code answered
- Ranked unknowns
- Round 1: the cancellation rule
- Round 2: what happens around a cancellation
- The G1 summary
- The resulting spec
- What to notice

## The request

The user writes: "Spec out #214. I want to review anything that touches refunds myself."

Issue #214, fetched with `gh issue view 214`:

> Customers should be able to cancel their own orders. Today they email the shop and staff cancel in the admin, which takes about a day. Three shops asked for it this month.

Track: feature. It has several criteria and touches payments.

## Grounding: what the code answered

Read, not asked:

| Fact | Where |
|---|---|
| Order statuses are `pending`, `packed`, `shipped`, `delivered`, `cancelled` | `src/orders/status.ts` |
| Staff can cancel any order before `shipped`: a full refund through `refundPayment`, then `releaseStock` | `src/admin/orders/cancel.ts` |
| When the refund call fails, the staff cancellation aborts and the order is unchanged | the same file and `cancel.test.ts` |
| Guests open their order through an emailed link that carries a token | `src/storefront/orders/by-token.tsx` |
| Shops get order emails from a template set, and the dashboard has an activity feed | `src/notify/templates/`, `src/dashboard/feed.ts` |
| All payments go through one provider wrapper, which has a test mode | `src/payments/provider.ts` |

The staff cancellation is the prior art. Most recommended defaults below come from it. The request already said the user reviews refund changes, so that goes straight into Constraints and is never asked.

## Ranked unknowns

| Unknown | Impact | Treatment |
|---|---|---|
| Until which status can a customer cancel? | High: the core rule | Round 1 |
| Is the refund automatic, or approved by the shop? | High: money | Round 1 |
| Whole order only, or single items? | High: doubles the scope | Round 1 |
| Can guests cancel from the order link? | High: a new actor and an auth path | Round 1 |
| The shop packs the order while the customer is confirming | Medium: edge behavior | Round 2 |
| The refund call fails | Medium: error behavior on money | Round 2 |
| How the shop learns about the cancellation | Medium: behavior within one slice | Round 2 |
| Is stock released? | Inferred from the code: the staff flow releases it, and a cancelled order's items are unsold | Not asked; stated in R3 and in the G1 summary, where the user sees it |
| Is a cancellation reason collected? | Low: reversible, not requested | Assumption |
| Button placement and copy | Low: follows the order page, seen at review | Assumption |

## Round 1: the cancellation rule

Sent as one call to the host's structured-question tool. Shown here as text:

```text
Round 1 of 2: the cancellation rule.

1. Until when can a customer cancel? Staff can cancel until the order ships.
   a) While it is pending, before packing starts (recommended: packing commits the shop's stock and time)
   b) Until it ships, like staff
   c) Within 30 minutes of ordering, whatever the status

2. How is the money returned?
   a) An automatic full refund, like the staff flow (recommended: no new payment path)
   b) The shop approves each refund first
   c) Store credit instead of a refund

3. Orders with several items:
   a) Whole order only (recommended: the smallest scope; single items become a non-goal)
   b) Customers can cancel single items

4. Guests see their order through the emailed link. Can they cancel there?
   a) Yes, from the link (recommended: otherwise guests keep emailing the shop)
   b) No, signed-in customers only
```

The user answers: "1a, 2a, 3a. 4a, but make guests type the email address on the order first."

The condition on 4 is a new requirement, not a nuance. It becomes R2 and two criteria.

## Round 2: what happens around a cancellation

```text
Round 2 of 2: what happens around a cancellation.

1. The shop marks the order packed while the customer is on the confirm screen. What happens when they confirm?
   a) The cancellation is refused: "This order is already being packed. Contact the shop to cancel." (recommended: keeps the pending-only rule strict)
   b) The cancellation goes through and the shop is told to unpack

2. The refund call fails.
   a) Nothing changes; the customer sees an error and can try again (recommended: matches the staff flow, and no half-cancelled orders)
   b) The order cancels and the refund is flagged for the shop to issue by hand

3. How does the shop learn about it?
   a) An email from the existing order templates (recommended: shops already read these)
   b) The dashboard feed only
   c) Both
```

The user answers: "1a, 2a, 3b. Our shops complain about too much email."

Every criterion is now observable and testable, so the interview stops. The two low-impact unknowns become assumptions.

## The G1 summary

```text
The spec for #214 is ready: docs/product-engineering/customer-order-cancellation/spec.md

Customers and guests cancel a whole pending order themselves. The full amount is refunded automatically, stock is released, and the shop sees it in the dashboard feed.
- 5 requirements, 10 acceptance criteria
- Not included: single items, cancelling after packing, store credit, a cancellation reason
- Please check: no reason is collected; the button sits under the order summary in the existing secondary style
- You review: every change that touches refunds

Is the spec agreed as written?
```

The user answers "Agreed", and the status becomes `Status: agreed (G1, 2026-09-25: "Agreed")`.

## The resulting spec

```markdown
# Spec: Customer order cancellation

Status: agreed (G1, 2026-09-25: "Agreed")
Track: feature
Source: issue #214

## Problem

Customers who want to cancel an order email the shop, and staff cancel it in the admin (`src/admin/orders/cancel.ts`), which takes about a day. Three shops asked for self-service this month. Customers should cancel pending orders themselves, without staff.

## Requirements

- R1: A signed-in customer can cancel their own order while it is pending.
- R2: A guest can cancel from the order link after entering the email address on the order.
- R3: A customer cancellation refunds the full amount automatically and releases the stock.
- R4: A customer cannot cancel an order that is no longer pending.
- R5: The shop sees each customer cancellation in its dashboard feed.

## Acceptance criteria

- AC1 (R1): Given a signed-in customer with a pending order, when they confirm cancellation, the order page shows "Cancelled" and the admin order list shows the order as cancelled.
- AC2 (R3): After AC1, the payment provider's test mode shows a refund of the full order amount.
- AC3 (R3): After AC1, the stock of each item in the order is back to its level before the order.
- AC4 (R2): Given a guest on the order link, when they enter the email address on the order and confirm, the order is cancelled, refunded, and restocked as in AC1 to AC3.
- AC5 (R2): Given a guest who enters a different email address, the order stays pending and the page says the address does not match.
- AC6 (R4): Given an order marked packed after the customer opened the confirm screen, when they confirm, the order stays packed and the page shows "This order is already being packed. Contact the shop to cancel."
- AC7 (R4): The order page shows no cancel action on packed, shipped, delivered, or cancelled orders.
- AC8 (R4): A direct request to cancel a packed order is rejected, and the order stays packed.
- AC9 (R3): When the refund call fails, the order stays pending, no stock changes, and the customer sees an error with a way to try again.
- AC10 (R5): After a customer cancellation, the shop's dashboard feed shows the order number with "Cancelled by customer", and no email goes to the shop.

## Non-goals

- Cancelling single items of an order.
- Cancelling after packing starts. Staff keep that in the admin.
- Store credit or partial refunds.
- Collecting a cancellation reason.

## Constraints

- Payments: the only payment integration is `src/payments/provider.ts`.
- Guest access is by the order token link (`src/storefront/orders/by-token.tsx`); guests have no accounts.
- Done and review: the user reviews every change that touches refunds before it merges (from the request).

## Assumptions and open questions

- Assumption: no cancellation reason is collected. Basis: not asked: low impact. If wrong: one optional field and a feed change.
- Assumption: the cancel button sits under the order summary in the existing secondary style. Basis: inferred from code (`src/storefront/orders/by-token.tsx`). If wrong: a layout change, visible at review.

## Approach

<!-- Written at G2 by brainstorming-solutions. -->

## Verification

<!-- Written at G3 by defining-verification. -->
```

## What to notice

- No question asked for a fact the code held: the statuses, the refund wrapper, guest links, and the notification channels. Restocking was inferred rather than asked, so the summary states it where the user confirms it.
- Round 1 holds four questions under one theme, the cancellation rule, although they span behavior, money, scope, and actors.
- Every recommended default cites prior art or a reason, and the user overrode one (email) with a reason worth keeping.
- A free-text condition ("type the email address first") became a requirement with a success and a failure criterion.
- The review expectation came from the request and was recorded without being asked again.
- The spec names no module to build and no library to use. The Approach and Verification sections wait for G2 and G3, and the Plan heading is gone because this is not a small change.
