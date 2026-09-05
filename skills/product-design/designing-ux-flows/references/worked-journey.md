# Worked journey: recover from no matching guides

Fictional product: Fieldnotes. Requirement R1 filters a saved guide collection by topic; R2 clears the filter; R3 provides recovery when no guides match. The existing collection and its visual language remain in scope as constraints.

## Primary flow

Open collection → read available titles → choose Writing → inspect matching guides → open a guide.

The collection's responsibilities are to explain what is saved, expose a topic filter, show the result count, and make guide titles and summaries readable. A guide's full reading view is already defined elsewhere and does not need redesign for this feature.

## Recovery branch

| Event | Visible result | Focus and announcement |
|---|---|---|
| Choose a topic with matches | Matching guides remain; count updates | Focus stays on the select; result count is a polite status message |
| Choose a topic without matches | “No saved guides in this topic.” and “Clear filter” appear | Focus stays on the select; zero results is announced |
| Activate Clear filter | All guides return; selection becomes All topics | Focus moves to the topic select if the clear button is removed or hidden |
| Choose another topic | New matching set appears | No page navigation and no focus jump to the results |

Retain the filter while opening and returning from a guide only if that behavior is in scope and agreed; do not silently add persistence requirements.

## Content and responsiveness

Use three plausible guides for the sketch: “Keep a field journal,” “Observe before you interview,” and “Write a useful checklist.” Include a longer title to check wrapping. On a narrow viewport, place the filter above the result count and list without changing reading order. Filter labels remain visible.

## What this does not settle

The flow specifies no server, URL scheme, storage policy, or framework. The offline prototype uses local sample data. If production filtering later needs remote results, loading, failure, and request ordering become additional engineering/UX questions; they are not evidence that this local prototype implements them.
