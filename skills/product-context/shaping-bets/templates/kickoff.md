# Bet [NN]: [title]

<!-- An issue in the code repository, for an implementation agent that cannot read the product context repository. Paste the bet's own fields and every file below as they read at the pinned commit, never at a later one; fill the four bookkeeping fields with their values at the latest commit. Creating the issue is the user's action, or needs their words. Delete this comment. -->

This work item is bet [NN], `[path of the bet in the context repository]`, from the product context repository [context repository name] ([remote URL]), pinned at commit `[full sha]`. The bet and the files it names are pasted below as they read at that commit. They were pasted, not read at the pin: report drift as not checked.

To build it, run the implementation loop on this issue:

```
Use running-implementation-loops on issue #[number] as work item [NN-slug]
```

The bet's requirements and acceptance criteria are agreed upstream; ask only about what they leave open. The context repository is read-only from here: anything that would change a requirement, an acceptance criterion, a no-go, a contract or a decision goes back to the user as a context change.

## The bet

<!-- The bet's own fields at the pinned commit: every header line except Status and Context pinned, and every section except Handoff and Outcome log. The bookkeeping fields carry their values at the latest commit, as below. -->

# Bet [NN]: [title]

Status: in delivery
[Version, Milestone, Appetite and Depends on line, at the pinned commit]
Code repository: [name] · Context pinned: [full sha]

[Every section from Outcome to Context pack, at the pinned commit.]

## Handoff

- Code repository: [name]
- Work item: [NN-slug]

## Requirements

<!-- The catalogue text for each requirement ID the bet names, at the pinned commit. -->

[ABC-01: text]

## Contracts and decisions

<!-- Each contract and decision record the bet names, at the pinned commit. -->

### [path]

[The file at the pinned commit.]

## Context pack

### [1. path]

[The file at the pinned commit.]

### [2. path]

[The file at the pinned commit.]
