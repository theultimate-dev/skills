# 0020: Package the prototype loop as a `product-prototyping` category

- Status: accepted
- Date: 2026-11-06

## Context

A prototype is built to be tried and then kept or removed. Its discipline is the same as a product's: a requirement per behaviour, checks that prove it, decisions with reasons, a history. Its rhythm differs. There are no planned versions, so there is no roadmap and no milestone; work comes as small bets of half a day to two days, and the person judges each by trying it. [0013](0013-product-context-category.md) packages the context of a product that lives through several versions, and [0014](0014-product-engineering-implements-bets.md) lets `product-engineering` build its bets through pull requests. Both assume versions, a separate context repository and a review loop that a prototype does not need. Without a fitting profile, the agent either skips the discipline or imports ceremony the prototype cannot pay for.

## Options

1. **Prototype modes inside the ten existing skills of `product-context` and `product-engineering`.** One set of skills, but a conditional in nearly every step: versions, roadmap, pull requests and the context repository each become optional, and neither plugin's promise stays crisp.
2. **A prototype track in `product-engineering`.** It reuses the loop, but the loop is a pull-request loop and its context lives in a separate repository. A prototype wants the bet, the code and the history in one place and one gate to try it, not G1 to G4.
3. **A `product-prototyping` category of five skills with its own profile.** Costs a seventh plugin and some templates that overlap with `product-context`. Gives the prototype loop its own gates and statuses without touching the plugins that serve versioned products.

## Decision

Option 3. `product-prototyping` is a category and plugin, starting at `0.0.0`, with five skills: `structuring-prototype-context`, `framing-prototype-ideas`, `shaping-prototype-bets`, `building-prototype-bets` and `closing-prototype-bets`.

- One profile, kept as a single reference, `references/prototype-profile.md`. Its source is in `structuring-prototype-context`, and the other four skills carry byte-identical copies under [0019](0019-mirror-shared-templates-across-skills.md), listed in `scripts/validate.py`. The profile defines the `context/` tree, the house rules, the statuses, the IDs and the reading order by task.
- Two human gates. At Gate 1, in `shaping-prototype-bets`, the person approves the bet and its autonomy line. At Gate 2, in `closing-prototype-bets`, the person tries the result and decides to keep or remove it. Between them, `building-prototype-bets` runs a self-verifying loop within the appetite, with an independent review in a fresh context.
- A bet is approved at a pinned commit in the same repository as the code, and building reads it at that pin. `context/` sits at the root of the code repository by default, so the commit a bet is approved at and the commits that build it are in one log. Code commits and context commits stay separate, so removing a bet reverts exactly its code.
- The catalogue holds only `built` and `dropped` requirements. An open bet carries its requirement deltas and reserved IDs until it closes.
- History is the application's own Keep a Changelog file, beside its code. Building adds the bet's entry under `[Unreleased]`.
- Mirrors may cross plugins. Under [0019](0019-mirror-shared-templates-across-skills.md), a full-profile template with no version, `Since:` or `roadmap/` field is mirrored unchanged from `product-context`. Any other template gets a prototype variant written in this category. Each pair is listed in `scripts/validate.py`.
- Graduation to the full profile is a recorded trigger, recommended as a planned release or a second contributor. When it fires, `structuring-product-context` restructures the context, and a new record supersedes the profile record.
- The skills are project-agnostic and harness-neutral under [0002](0002-agent-skills-open-format.md). Each belongs to one category, and the plugin is the install unit, under [0003](0003-categories-as-directories.md).
- [0013](0013-product-context-category.md) stays unchanged. `product-context` keeps its six skills, its profile and its bet template; the only change there is a paragraph in `structuring-product-context` for the graduation path.

## Consequences

- A seventh plugin. Its first release, `product-prototyping--v0.1.0`, is a minor marketplace release under [0011](0011-marketplace-release-with-every-plugin-release.md).
- Some templates are mirrored from `product-context`, which ties those files across the two plugins. A change to a mirrored source changes every copy in the same commit.
- The prototype bet template differs from the one in `shaping-bets`, so graduation maps fields rather than moving files. The restructure in `structuring-product-context` has to carry that map.
- A person with a prototype now has two places to look: `product-prototyping` for something to try, `product-context` and `product-engineering` for a versioned product. The skill descriptions each name the other as the one to use instead, and the boundary needs watching.
- The skills have not run on a real adoption yet. The first release waits for one, and its workarounds are logged and fed back into the skills.
