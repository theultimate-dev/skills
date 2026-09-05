---
name: shaping-product-briefs
description: "Turn a rough application, feature, or proof-of-concept idea into a product brief with audience, outcomes, scope, prioritized functional requirements, assumptions, and acceptance criteria. Use before design or implementation when the problem and intended behavior need clarification."
license: MIT
---

# Shaping product briefs

Produce the smallest brief that lets the user agree what should be designed and why. A brief can be a section of an existing document; it need not be a new PRD.

## Ground the brief

Read applicable project instructions, including `AGENTS.md` or `CLAUDE.md` when present, existing requirements, decisions, and relevant implementation. Work from supplied context when files are unavailable and say what was not inspected. Do not overwrite an agreed brief with a speculative replacement.

Identify who is trying to do what, in which situation, what currently obstructs them, and what useful change the idea promises. Separate the user's goal from a suggested feature: “find the right guide” may not require accounts, recommendations, or a search service.

Ask only questions that materially change scope or behavior and cannot be answered from available context. Offer a concrete smallest useful scope and its tradeoffs. Carry forward answers already given. Read [requirements and uncertainty](references/requirements-and-uncertainty.md) before converting the idea into requirements.

## Define the useful boundary

- State audience, problem, intended outcome, in-scope behavior, and explicit exclusions.
- Capture established stack and design constraints as project context. Leave absent technology undecided unless a requirement's feasibility depends on it; explain that dependency to the user.
- Distinguish functional requirements from constraints, design hypotheses, and implementation suggestions.
- Prioritize the requirements needed for the outcome. Add observable acceptance criteria and stable local IDs when later artifacts will refer to them.
- Include relevant content, data, accessibility, privacy, performance, or integration needs at the product level. Do not invent numerical targets or compliance claims.
- Mark assumptions and propose the smallest useful way to test consequential ones. A proof of concept needs a learning question and evaluation criteria, not a pretend launch specification.

Use the [product brief template](templates/product-brief.md), adapting existing conventions and removing irrelevant sections. For calibration, read the [annotated examples](references/examples.md).

## Review and deliver

Show the recommendation, consequential assumptions, and any alternatives that still need a decision. Record scope as agreed only when the user agreed or explicitly delegated the choice. A request to draft a brief authorizes drafting, not automatic approval of its contents.

Return the brief, unresolved questions with their implications, and the next useful design input. Preserve the distinction between a blocker to design and a question engineering can resolve later. If later UX or prototype work changes behavior, update the requirement and note which prior decision needs review.

This skill can run alone. It does not require the discovery coordinator or any other skill. Without file access, provide complete Markdown and a suggested filename and state that no file was written.
