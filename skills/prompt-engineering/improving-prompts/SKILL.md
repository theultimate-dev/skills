---
name: improving-prompts
description: "Rewrites a rough prompt into an engineered one. Classifies where the prompt will run (chat request, system prompt, coding or research agent task, agent operating instructions, long-document job, extraction or classification), diagnoses its gaps, applies the prompt and context engineering techniques that close them, and returns the techniques applied with reasons, the techniques rejected with reasons, placeholders for facts it could not infer, and a copy-paste-ready enhanced prompt inside an enhanced_prompt tag. Use when the user asks to improve, enhance, refine, optimize, rewrite, or engineer a prompt, system prompt, or agent task, or passes a prompt as the argument."
license: MIT
---

# Improving prompts

Take the prompt the user supplied, return a short report and an enhanced prompt, and never block on questions. A technique earns its place only by closing a diagnosed gap; the shortest prompt that reliably does the job wins. The enhanced prompt is the user's own request, engineered, not a document about the request.

## Take in the prompt

The prompt to improve is the text the user supplies with the request: inline, in a code block, or in a file to read. Everything else the user says, such as the target model, the harness, the audience, where the prompt will run, or what went wrong last time, is context for the diagnosis and does not go into the prompt.

A system prompt supplied together with a task prompt is two prompts with two destinations. Improve both and deliver two blocks.

Keep the prompt's language and register. Do not translate it, and do not turn first person into third person. Write the report in the language of the user's request.

If no prompt was supplied, ask for it. That is the only case in which this skill asks a question. If the prompt's purpose is to defeat a model's safeguards or to deceive people, say so in one sentence and stop.

## Classify the destination

| Destination | Signals in the draft | What changes |
|---|---|---|
| Chat request | An imperative one-liner or a question; a person reads the answer; no tools implied | Stay short: task, audience, form, and the facts the reader lacks |
| System prompt or app prompt | "You are…"; standing behaviour for many users or sessions; tools or policies described | Role, altitude, sections, tone, refusal and escalation, trust boundary, reusable prefix |
| Coding or research agent task | A repository, files, tests, an investigation; verbs like fix, implement, migrate, investigate | Scope, pointers to files and patterns, a verification target, autonomy and handback rules |
| Agent operating instructions | Rules meant for every session: conventions, commands, etiquette; files such as AGENTS.md or CLAUDE.md | Only what the agent cannot infer, short and calm; no tutorials |
| Long-document task | Pasted or attached documents, "based on the attached", inputs of tens of thousands of tokens | Inputs first with metadata, question last, quote-first grounding |
| Extraction or classification | A schema, labels, "return JSON", a batch of inputs | Schema shape, label set, no preamble, diverse examples |

Choose the most likely destination and record it in the report. When two readings would produce materially different prompts, deliver the most likely one and name the other under Assumptions. Read [diagnosis](references/diagnosis.md) for the full signal list, the gap checklist, and how to write success criteria.

## Diagnose

Walk the draft against this checklist: goal and definition of done; audience and destination; facts the reader lacks; constraints and scope; output form and length; a pattern the output must match; reasoning demand; risk, meaning untrusted content, side effects, hallucination stakes, or personal data; defects in the draft itself, meaning contradictions, duplicated rules, emphasis in capitals, prohibitions without an alternative, instructions the destination cannot honour, and bloat; runtime assumptions such as a prefilled response, a sampling setting, or a tool the destination lacks.

Rate each gap `blocks` (the model cannot do the job), `degrades` (it will do a worse job), or `cosmetic`. Only `blocks` and `degrades` justify a change. A draft with nothing above cosmetic is already good: say so, fix the cosmetics, and do not inflate it.

## Select techniques

Pick from the groups below. Read the reference for every group you apply and for every group you reject on a judgment call.

| Group | Apply when | Reject when | Read |
|---|---|---|---|
| Clarity and directness | The verb is ambiguous; goal, audience, or constraints are missing; a "don't" has no positive alternative; the draft shouts or contradicts itself | The vagueness is deliberate exploration ("what would you improve here?") | [clarity and structure](references/clarity-and-structure.md) |
| Structure and ordering | Instructions mix with data or examples; the prompt exceeds a screen; it will be reused | A short conversational request; the existing structure already works | [clarity and structure](references/clarity-and-structure.md) |
| Examples | A format, tone, or label set must match a pattern, and real examples exist or can stand as placeholders | Simple tasks; examples would have to be invented; creative work where copying is the risk | [examples](references/examples.md) |
| Roles and system prompts | The destination is a system prompt, or expertise changes the answer | A role line that changes nothing | [system prompts](references/system-prompts.md) |
| Reasoning | Multistep analysis where the destination's thinking is off or unknown; checkable criteria exist for a self-check | Lookups and transformations; models that already verify their work; latency-bound chat | [reasoning](references/reasoning.md) |
| Output control | Any deliverable; machine-consumed output; a length or format complaint | The user wants the model to choose the form | [output control](references/output-control.md) |
| Context packaging | The reader lacks facts; inputs are long; sources are retrievable; a prefix will be reused | Everything needed is already present and short | [context packaging](references/context-packaging.md) |
| Reliability and grounding | Factual, analytical, advisory, research, or code questions | Fiction; pure formatting or translation | [reliability and grounding](references/reliability-and-grounding.md) |
| Trust boundaries and safety | Third-party content, tools with side effects, public users, personal data | Closed inputs the user wrote, no tools, nobody else reads the output | [trust boundaries](references/trust-boundaries.md) |
| Agent task prompts | Coding, research, or operational work run by an agent with tools | Chat without tools | [agent tasks](references/agent-tasks.md) |
| Decomposition | One prompt carries several tasks; intermediate outputs need inspection; independent parts can run in parallel | A capable model handles it in one pass and nobody needs the intermediates | [decomposition](references/decomposition.md) |
| Model-family adjustments | The user named the target model or family | Target unknown: stay neutral and say so | [model family notes](references/model-family-notes.md) |

Rejection reasons must be specific to this prompt: "no real transcripts to use as examples; invented ones would teach the wrong voice", never "not needed". Record every group you seriously weighed.

## Apply

- Preserve intent, scope, voice, terms, and language. A changed meaning is a defect. If the draft contradicts itself, keep the reading its wording supports and flag it.
- Never add a fact the user did not give: no product names, numbers, file paths, policies, dates, or audience claims. A missing fact becomes a placeholder in square brackets naming what goes there, such as `[paste the failing test output]` or `[audience, e.g. finance managers]`, and every placeholder is listed under Assumptions. Nothing the draft already says becomes a placeholder.
- Minimal sufficient structure. A one-line request usually becomes three to eight lines, not a page. Use tags or headings only when the prompt mixes kinds of content. Keep the user's structure where it works.
- Say what to do. Keep a prohibition only when it protects something, and pair it with the alternative.
- No emphasis in capitals, no "critical", no chains of "must". One plainly stated instruction each. Current models over-trigger on shouted rules.
- Give the reason behind a constraint that is not obvious, in a clause, so the model can generalize from it.
- Consistent terms and tag names throughout; descriptive tags, balanced and closed.
- No meta commentary inside the prompt: no "Improved prompt:", no technique labels, no notes to the user. The enhanced prompt reads as the user's own request and stands alone without the report.
- No instruction the destination cannot honour: no tests for a model without tools, no "search the web" without search.
- Runtime settings and architecture stay out of the prompt text: effort or reasoning level, schema enforcement, cache breakpoints, tool-result encoding, screening, sampling parameters. Report them under Outside the prompt.
- Model-neutral wording unless the user named the target. Then apply the dated adjustments and name the model in the report, never inside the prompt.
- Each added sentence traces to one diagnosed gap. Do not stack techniques.

Shape the result with the [prompt skeleton](templates/prompt-skeleton.md), dropping every section the diagnosis did not call for.

## Check before delivering

Someone with no context could follow the prompt. Every addition maps to a `blocks` or `degrades` gap. Nothing is invented and every placeholder is listed. No contradictions, duplicate rules, shouted emphasis, or prohibition without an alternative remain. The length is proportionate to the task. Tags are balanced. The first sentence states the task. Language and voice are unchanged. Nothing asks the destination for what it cannot do. Model-specific wording appears only when a model was named.

## Deliver

Fill the [improvement report](templates/improvement-report.md) in this order and put nothing after the enhanced prompt:

1. `## Diagnosis`: destination; target, either the model the user named or "not specified; neutral"; three to six gaps with severity.
2. `## Techniques applied`: a table of technique and why here, each row naming the gap it closes.
3. `## Techniques considered and not applied`: a table of technique and why not, specific to this prompt.
4. `## Assumptions and placeholders`: omit when empty. One line per placeholder (what to fill in and why it could not be inferred) and per assumption.
5. `## Outside the prompt`: omit when empty. Settings, architecture, and evaluation suggestions the prompt text cannot carry.
6. The enhanced prompt inside `<enhanced_prompt>` and `</enhanced_prompt>`, with the tagged block inside a fenced code block opened with more backticks than any run inside the prompt, at least four. The fence keeps markdown clients from rendering the prompt and lets code fences inside it survive. Two prompts use `<enhanced_prompt role="system">` and `<enhanced_prompt role="user">`, each in its own fence.

When the draft is already good, the report says so and the applied table may hold a single cosmetic row. For calibration, read the [worked examples](references/worked-examples.md). Without file access, deliver the same response as text and do not claim that a file was written.

## References

| Read | When |
|---|---|
| [diagnosis](references/diagnosis.md) | Classifying the destination, rating gaps, writing success criteria, choosing the default bundle |
| [clarity and structure](references/clarity-and-structure.md) | Ambiguous verbs, missing goal or audience, shouted or negative rules, sectioning and ordering |
| [examples](references/examples.md) | A pattern must be matched; deciding whether examples help or harm |
| [system prompts](references/system-prompts.md) | System prompts, app prompts, and agent operating instructions |
| [reasoning](references/reasoning.md) | Multistep analysis, self-checks, and when reasoning instructions backfire |
| [output control](references/output-control.md) | Format, length, structured data, prefill migration, formatting complaints |
| [context packaging](references/context-packaging.md) | What to include, point to, or leave out; ordering; caching; long tasks |
| [reliability and grounding](references/reliability-and-grounding.md) | Factual accuracy, quotes, citations, assumptions instead of invention |
| [trust boundaries](references/trust-boundaries.md) | Third-party content, tools with side effects, public users, personal data |
| [agent tasks](references/agent-tasks.md) | Prompts a coding, research, or operational agent executes |
| [decomposition](references/decomposition.md) | Splitting one prompt into a chain, a pipeline, or a system prompt plus a task |
| [model family notes](references/model-family-notes.md) | The user named the target model or family |
| [worked examples](references/worked-examples.md) | Calibrating length, placeholders, and the report |
| [sources](references/sources.md) | Where the catalog comes from and its limits |
| [improvement report](templates/improvement-report.md) | The output skeleton |
| [prompt skeleton](templates/prompt-skeleton.md) | Section order for task prompts and system prompts |
