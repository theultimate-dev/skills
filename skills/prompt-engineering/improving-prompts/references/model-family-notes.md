# Model family notes

Reviewed 2026-09-16, except sections that give their own review date. Model behaviour changes between releases; verify against the provider's current model page before relying on any line here. Apply these adjustments only when the user named the target model or family. Otherwise the enhanced prompt stays neutral and the report says so. Name the model in the report, never inside the prompt.

## Contents

- Claude, current generation
- Claude Opus 5
- Claude Fable 5.1 and Mythos 5.1
- Other current Claude models
- GPT-5.x
- Gemini 3.x
- Grok 4.7
- Unknown or other

## Claude, current generation

Observed at review on Claude Fable 5.1, Fable 5, Opus 5, Opus 4.8, Sonnet 5, Sonnet 4.6, and Haiku 4.5.

- Explicit instructions with motivation and modifiers work best. The models follow instructions literally, so say exactly what to do and, when "above and beyond" is wanted, ask for it.
- Dial aggressive language back. Prompts written to stop earlier models under-triggering ("CRITICAL: you MUST use this tool when…") now over-trigger; "Use this tool when…" is enough.
- A prefilled last assistant turn is rejected on Claude 4.6 and later. Use direct instructions, output tags, or structured outputs instead.
- Thinking is adaptive or always on, and its depth is an effort setting. Skip "think step by step", put no thinking budget wording in the prompt, and list the depth choice under Outside the prompt. Manual `<thinking>` tags only where thinking is off, and then prefer thinking on at a low effort level.
- "Before you finish, verify against [criteria]" helps on most of these models; see Opus 5 for the exception.
- Long inputs first, question last. Three to five examples in `<example>` tags.
- Independent tool calls run in parallel by default; a one-line nudge raises the rate further.
- Subagents are used readily; where that is excessive, say when delegation is and is not warranted.

## Claude Opus 5

- Responses run long, and effort controls thinking rather than length. Ask for conciseness explicitly and repeat a short reminder near the end of a long system prompt.
- It narrates readily during agentic work; describe the update cadence you want.
- Files it writes run long; add a length calibration for written deliverables.
- It verifies and self-corrects without being told. Remove verification and re-check instructions carried over from older prompts; they cause over-verification.
- It may widen a task; constrain scope explicitly for narrow tasks.
- It delegates to subagents readily; give explicit delegation rules or cap delegation in the harness.
- It narrates corrections to its own earlier statements; limit that to corrections that change the reader's decisions.
- With thinking disabled it can write a tool call as text or leak internal tags. Keep thinking on at low effort, or add one general instruction that permits a sentence before a tool call and bans internal tags, without naming the tags.
- Review prompts that say "only high-severity issues" are followed literally; ask for everything and filter afterwards.

## Claude Fable 5.1 and Mythos 5.1

- Fewer user-facing updates during long tool-calling turns. Remove any line that suppresses narration, then add a cadence line stating when to speak and what each update contains.
- In coding and computer-use loops it may issue one tool call per turn; a one-sentence batching nudge at the end of each tool-result turn fixes it.
- Keep the conversation history append-only; edits before a preserved thinking block fail or drop the block. Per-turn reminders go at the end of the newest turn.
- Prose can run dense; an instruction to drop mannered phrasing, or simply "remove all mannered prose", helps.
- It formats less than earlier models; replace anti-formatting blocks with a rule that says when lists and headings are appropriate.
- Summaries may reproduce source wording unmarked; one complete example with a rationale line fixes it better than a rule.
- On long autonomous work it may end the turn early or ask permission for requested work; use the autonomy block and the scope block from the agent tasks reference, together.
- Tell a client-side compaction summarizer what to preserve.
- It sometimes fixes nearby code or commits extra test files; the keep-changes-to-the-task instruction removes most of it.
- At low effort it answers from memory more often; add the search-before-answering line or raise effort for that turn.
- Safeguard false positives: ask "are there bugs in this program" rather than "does it compile", give context for obscure languages, and remove base64 from tool output.
- It may rewrite whole files for small changes; ask for targeted edits.
- At the two highest effort levels a long deliverable can be drafted twice, in reasoning and again in the reply; append the note that reasoning and output share one token limit and that drafting twice is wasted.
- An effort sweep on your own evaluations is the primary cost control; level names do not mean the same depth across models.

## Other current Claude models

- Sonnet 5, Opus 4.8, Sonnet 4.6: literal instruction following; plain "use this tool when…" triggers tools appropriately; context awareness pairs well with a compaction-awareness line in compacting harnesses.
- Opus 4.6: more upfront exploration; replace blanket defaults with targeted tool instructions; a commit-to-an-approach line curbs re-deliberation; damp subagent use explicitly.
- Haiku 4.5: benefits from more guidance and examples than the larger models; test the prompt on it separately.

## GPT-5.x

From the GPT-5, 5.1, and 5.2 prompting guides at review.

- Reasoning effort is a request parameter; keep it out of the prompt text.
- Agentic eagerness is tunable. For less, set explicit context-gathering budgets and tool-call limits and say when to stop searching; for more, add persistence instructions.
- Ask for brief tool preambles: a short plan before calls and one-line updates at phase changes, not narration of routine calls.
- Give concrete length constraints; explicitly forbid unrequested features and styling.
- On long inputs, ask for key sections to be summarized and claims re-anchored to document regions.
- Ask for labelled assumptions and plausible interpretations instead of fabricated detail.
- For extraction, supply a JSON schema with required and optional fields and `null` for missing values.
- Ask for citations on web-derived claims and explicit resolution of contradictions.
- Keep prompts functionally identical when resuming a compacted workflow.
- Instructions are followed closely, so contradictory instructions cost more than on older models; remove conflicts before adding rules.

## Gemini 3.x

- System instructions and role first, then context, then the specific task.
- Keep sampling parameters at their defaults.
- Thinking is built in; drop redundant "plan first" requests.
- Keep formatting consistent across few-shot examples.
- Use the grounding tools for current facts and code execution for calculation rather than asking the model to compute in text.
- Request the output format explicitly (table, list, JSON).

## Grok 4.7

Reviewed 2026-09-29. xAI publishes no text-prompting guide for Grok 4.7 or any Grok 4.x model, so these lines record what its model page, API documentation, and launch post state. Apply the portable core and test on the model.

- Reasoning is always on and cannot be disabled. Its depth is the `reasoning_effort` setting: `low`, `medium`, `high` (the default), or `xhigh`. List the depth under Outside the prompt. xAI does not say whether step-by-step wording in the prompt helps or hurts.
- Stop sequences and presence and frequency penalties return an error on xAI's reasoning models, Grok 4.7 included. A draft that relies on a stop sequence needs output tags or a structured output instead.
- xAI says it works longer on difficult tasks and checks its own work more carefully than Grok 4.6. Whether an explicit verification instruction still helps is unconfirmed.
- Parallel function calling is on by default.
- With structured outputs, a response is guaranteed to match the supported schema features, so the prompt can describe the task without restating the required fields.
- Inline citations are on by default in the Responses API, but the model decides when to cite; they do not guarantee a citation on every answer.
- For cache hits, keep system prompt, few-shot examples, and reference documents at the start as a stable prefix and only append to the history. The cache key, passing reasoning items back unchanged, and context compaction for long agent loops are harness settings for Outside the prompt.
- For Grok Build rule files such as AGENTS.md (Grok 4.7 is Grok Build's default model), xAI says short, specific instructions are followed more reliably than long ones.

Unconfirmed for Grok 4.7: response to instruction style and emphasis, verbosity and length (no verbosity setting is documented), formatting defaults, persistence and progress updates on agentic work, delegation, few-shot examples, prefill, question placement in long inputs, and changes needed when migrating prompts from Grok 4.6.

## Unknown or other

Apply the portable core only and say so in the report. A prompt tuned for one family's quirks can underperform on another.
