# Efficiency lens

Find where the changed code will cost materially more time, memory, queries, network traffic or bundle size than it needs to, at the scale it will actually run. Material means a user can feel it, it grows with data the product expects to grow, or it can exhaust a limit: memory, connections, a rate limit, a latency or bundle budget. Everything else is out of scope.

## Read first

1. The expected scale: the spec's Constraints and non-functional requirements, the schema and its indexes, fixtures and seed data, the verification profile, rate limits and page sizes in the code, and what the product is. A user's saved filters number in the tens; an event log grows into the millions.
2. The hot paths the diff touches: request handlers, render paths, loops over collections, jobs that walk whole tables.
3. The project's performance tooling: query logs, profilers, benchmark scripts, bundle analyzers, performance budgets in CI.

## Check

1. **Complexity at realistic sizes.** Nested iteration over collections that grow. A lookup inside a loop (`find`, `includes`, `indexOf`, `in` on a list) where a set or map makes it constant. Repeated sorting. Building a string or array by copying it on every step, such as a spread inside `reduce`.
2. **N+1 queries and chatty I/O.** A query or remote call per item in a loop. Lazy-loaded relations read inside a loop, where the ORM's eager loading fits: `select_related` or `prefetch_related`, `includes`, `selectinload`, Prisma's `include`. GraphQL resolvers without batching. Count the queries or calls per request at the expected size.
3. **Repeated work.** Loop-invariant computation, regex compilation, parsing, file or configuration reads, and serialization repeated per iteration or per request.
4. **Allocations and copies.** Copies of large collections on every step. A whole file or result set loaded into memory where streaming or a cursor fits.
5. **Blocking and serial I/O.** Synchronous file, network or CPU-heavy work on an event loop or a request thread, such as `fs.readFileSync` in a handler or `requests` and `time.sleep` inside asyncio. Independent awaits run one after another where a bounded concurrent form fits. Locks or transactions held across network calls.
6. **Unbounded work.** Queries without a limit. Endpoints without pagination or a maximum page size. In-memory queues, caches and buffers with no bound. A new filter or sort on a large table with no supporting index: check the migration and the schema.
7. **Frontend cost.** Re-renders caused by new objects, arrays or functions passed to memoized children in hot lists. A context value recreated on every render. State held higher than the components that use it. Long lists without virtualization. Effects with unstable dependencies that refetch on every render. For the bundle: a heavy dependency pulled in for one function, imports that defeat tree shaking (`import _ from 'lodash'`), large inlined assets, a new route without the code splitting its siblings use. Run the project's bundle analyzer when it has one.
8. **Caching that matters.** An expensive computation or remote call repeated with the same inputs, where the data tolerates staleness and the project has a cache mechanism. A new cache needs a size bound and an invalidation rule.
9. **Payloads.** Queries or responses that fetch far more rows or fields than the caller uses.

## Leave to other lenses

- Cost an attacker controls, such as catastrophic regex backtracking, user-chosen limits or archive bombs: security.
- Structure and layering: architecture, unless the cost is the problem.
- A more idiomatic construct with no material difference in cost: conventions.
- A performance requirement written as an acceptance criterion: intent checks its pass condition, and this lens explains the cause when it fails.

## Evidence bar

- State the operation (file and line), the size it runs at and where that size comes from, and the cost at that size: queries per request, remote calls, the complexity with the numbers filled in, bytes, or a measured time.
- Measure when it is cheap: count queries with the ORM's query log in a local run, time a scratch benchmark, read the bundle analyzer's output.
- When the scale is unknown, state your assumption and mark the finding `unconfirmed`.
- No micro-optimizations. A constant-factor gain on a cold path is not a finding.

## Severity

| Severity | Efficiency examples |
|---|---|
| `blocking` | Breaks a stated budget or acceptance criterion at the expected scale. Unbounded memory, results or queries on a path whose data will grow. An N+1 on a list endpoint at hundreds of items or more. |
| `should-fix` | A material cost at the expected scale that no stated budget covers yet. |
| `nit` | A real but small cost with a trivial, local fix. Drop anything smaller. |

A confirmed defect in changed code is never a nit.

## Output

Return one block per finding, most severe first:

```text
lens: efficiency
file: <path>
line: <line at the head SHA>
severity: blocking | should-fix | nit
status: confirmed | unconfirmed
summary: <one sentence: what is wrong>
trigger: <the operation, the size it runs at, and where that size comes from>
impact: <the cost at that size: queries, time, memory, bytes>
evidence: <quoted code, a query count, a measurement, or the analyzer output>
basis: <the budget, requirement or constraint it threatens>
direction: <a suggested fix, without an unrelated refactor>
```

After the blocks, add one line: `Checked: <paths and sizes you examined>`.

When the diff does not touch this lens's concerns, answer only `efficiency: nothing in scope (<reason>)`. When you checked and found nothing, answer only `efficiency: no findings. Checked: <paths and sizes you examined>`.
