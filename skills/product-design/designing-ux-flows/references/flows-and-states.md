# Flows and states

## A useful flow answers five questions

1. What brings the person here, and what information do they already have?
2. What do they need to understand or decide on this screen?
3. Which action advances the task, and what feedback follows?
4. What happens when the expected content, permission, or result is absent?
5. How do they return, revise, cancel, or recover without losing useful work?

Separate the structure of the information from its visual arrangement. “Guide title, topic, reading length, summary, and open action” is a screen responsibility. “Three rounded cards” is a design option.

## Include states that have a cause

| Situation | Questions worth resolving |
|---|---|
| First use or no content | What explains the absence and offers a useful next action? |
| No matches | Can the user clear or change the condition that caused it? |
| Waiting for remote work | Is progress needed, can the user cancel, and what remains usable? |
| Invalid input | Where is the error explained, what is retained, and how can it be corrected? |
| Success | Is the result evident without an extra confirmation screen? |
| Access denied or unavailable content | What can the user do next within scope? |

An offline filter does not need a fake loading spinner or invented network failures. A prototype of an asynchronous task may simulate those states to explore the future behavior; record that distinction.

## Interaction notes

Write trigger → visible effect → focus/announcement → recovery when the sequence matters. For example: selecting a topic updates results in place, keeps focus on the select, announces the result count politely, and exposes a clear-filter action when useful. Do not move focus to every changed result.

Use native elements with the needed semantics and keyboard behavior. Custom roles do not provide interaction behavior automatically; use the relevant [WAI-ARIA authoring guidance](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/) for a custom widget that the task actually requires.

Define headings, landmarks, and reading order before relying on position or color to communicate relationships. The [W3C page structure tutorial](https://www.w3.org/WAI/tutorials/page-structure/) explains why these structures support navigation.

## Content pressure

Use meaningful sample labels and plausible text lengths instead of lorem ipsum. Check unusually long titles, missing optional fields, and localized text when relevant to the audience. Label invented content in the notes, without stuffing implementation commentary into the product interface.

Responsive behavior is about priority and task continuity: say what rearranges, wraps, or becomes sequential. Do not assume desktop controls can simply be made smaller. A touch user must not need hover to reveal an essential action.

## Placements on a native surface

A native platform surface, such as a menu-bar panel, a desktop window, a phone widget or a watch face, doesn't reflow to a narrow screen. It appears in placements: the displays and states it meets, each at the device's real scale. Take them from the brief and the project, and add the ones a surface of its kind always meets:

- **A menu-bar panel:** a built-in display with a hardware cut-out such as a camera housing; an external display without one; and a full-screen app, where the menu bar stays hidden until the pointer reaches it.
- **A phone widget:** each widget size it offers, on the home screen and on the lock screen.
- **A desktop window:** its smallest size, its default size, and side by side with another window.
- **A watch face:** each case size, and the always-on state.

For each placement, say what changes: what the surface loses to system UI such as the menu bar, a cut-out or system bars, where it opens, and what it shows first when space runs short. Keep reading order and the essential actions the same in every placement.
