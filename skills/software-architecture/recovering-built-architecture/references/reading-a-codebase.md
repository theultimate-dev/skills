# Reading a codebase for its architecture

How to find what an application is made of from its repository alone: which processes run, which stores they use, what they call, and how sure you can be of each. The skill's steps say what to do; this file says where to look and how to judge what you find.

The examples use Larder, a fictional household pantry app with a web client, a mobile client, an API and one Postgres database, and occasionally other stacks where they hide structure differently.

## Contents

1. [Read outside in](#read-outside-in)
2. [Where structure hides, per stack](#where-structure-hides-per-stack)
3. [What becomes an element](#what-becomes-an-element)
4. [One image, several processes](#one-image-several-processes)
5. [Three kinds of evidence](#three-kinds-of-evidence)
6. [Names that mislead](#names-that-mislead)
7. [Documents that are out of date](#documents-that-are-out-of-date)
8. [Writing a blind spot](#writing-a-blind-spot)
9. [Large repositories](#large-repositories)
10. [Searching, where a shell is available](#searching-where-a-shell-is-available)

## Read outside in

Start from what runs in production and work inwards, because the folder tree describes how people organised the code, not what the system is. A deployment manifest names every process that is started, and nothing else does that as directly. Then:

1. **Deployment and container files**: which services, jobs and stores exist in each environment, how each is started, how many instances, on what schedule.
2. **Workspace and package manifests**: which units are built, and what each depends on.
3. **Entry points and process commands**: what each started process actually runs.
4. **Configuration and environment variables**: what each process connects to, and which external systems it knows about.
5. **CI**: what is built, tested and deployed, and which services the tests need.
6. **Schema and migrations**: what each store holds, and from the queries, which process reads and writes which tables.
7. **The call sites**: database queries, producers and consumers, outbound HTTP, inbound routes.

Keep a working list as you go: units, stores, externals, calls, each with the path and line that showed it. The views are written from this list, not from memory.

## Where structure hides, per stack

| Look for | Where it hides | What it tells you |
|---|---|---|
| Workspaces and packages | `package.json` with `workspaces`, `pnpm-workspace.yaml`, `turbo.json`, `nx.json`; `Cargo.toml` `[workspace]`; `go.work`, several `go.mod`; `pyproject.toml` with a uv or Poetry workspace; `settings.gradle`, Maven `<modules>`; `.sln` and `.csproj`; a Mix umbrella; `composer.json` | The units that are built. A package is a library until something starts it |
| Entry points | `main`, `bin` and `scripts` in `package.json`; `cmd/<name>/main.go`; `__main__.py`, `manage.py` commands, `[project.scripts]`; `src/main.rs`, `[[bin]]`; `Program.cs`; a class with `@SpringBootApplication`; `config.ru`, `bin/` in Rails; `mix.exs` releases | What each unit runs when started. Several entry points in one package mean several possible processes |
| Process commands | `Dockerfile` `CMD` and `ENTRYPOINT`; `command:` in compose; `Procfile` lines; Kubernetes `command` and `args`; `dockerCommand`, `startCommand` and similar in platform manifests; systemd units; `supervisord.conf` | Which entry point each deployed process actually starts. The command overrides the image's default |
| Deployment | `render.yaml`, `fly.toml`, `app.yaml`, `app.json`, `Procfile`, `vercel.json`, `netlify.toml`, `serverless.yml`, SAM and CloudFormation templates; Terraform, Pulumi, CDK; Helm charts, Kubernetes manifests, Kustomize overlays; ECS task definitions; Nomad jobs | What runs in production, as which kind (web, worker, cron, private service, static site), how many instances, in which region, with which managed stores and which variables |
| Development stack | `docker-compose.yml`, `compose.yaml`, devcontainers, `Tiltfile`, `skaffold.yaml` | What a developer runs. It often differs from production: extra tools, missing externals, different images. Read it, but let the production manifest decide what runs in production |
| CI and CD | `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/`, `azure-pipelines.yml`, `bitbucket-pipelines.yml` | Service containers the tests need (a hint at stores), deploy jobs and their targets, environments, scheduled workflows that are themselves jobs |
| Schema and migrations | `migrations/`, `db/migrate/`, `alembic/`, `prisma/schema.prisma`, `drizzle/`, Flyway `V1__*.sql`, Liquibase changelogs, Django `migrations/`, ORM models, seed files | What each store holds. Seeds and migrations also set defaults that behave like configuration, such as feature flags inserted switched off |
| Configuration | `.env.example`, `.env.*`, a `config` module, `settings.py`, `application.yml`, `appsettings.json`, ConfigMaps and Secrets, Helm `values.yaml`, parameter store paths | Which variables each process reads. Names ending in `_URL`, `_HOST`, `_DSN`, `_TOKEN`, `_API_KEY`, `_BUCKET`, `_QUEUE`, `_TOPIC` point at a store or an external system |
| Client build configuration | `VITE_*`, `NEXT_PUBLIC_*`, `EXPO_PUBLIC_*`, `REACT_APP_*` variables; `eas.json` profiles, `app.json`, Gradle `buildConfigField`, iOS `.xcconfig` | Which host each client calls, per build. Two clients often call different hosts |
| Scheduled jobs | Cron entries in platform manifests, Kubernetes `CronJob`, `schedule:` in CI, Celery beat, Sidekiq-cron, Quartz, `@Scheduled`, `node-cron` or `setInterval` inside a server, a `crontab` file | Work that nobody calls. A scheduler inside a server process is a responsibility of that process, not a separate unit |
| Queues and streams | Client libraries (`ioredis` stream commands, BullMQ, `amqplib`, `kafkajs`, SQS and SNS SDKs, Pub/Sub, NATS, Celery, Sidekiq, RQ); queue, topic and stream names as constants | Which process produces and which consumes. A producer with no consumer in the repository is a blind spot, not a missing arrow |
| Outbound HTTP | `fetch`, `axios`, `got`, `requests`, `httpx`, `net/http`, `HttpClient`, `RestTemplate`, `WebClient`; vendor SDK imports such as payment, mail or storage SDKs; hard-coded hosts | External systems. Find the host in the call site or in the variable it reads |
| Inbound calls | Route registrations, controllers, GraphQL schemas, gRPC protos, webhook handlers, proxy and rewrite rules | Who calls this unit. A webhook route means an external system calls in |
| Stores the platform runs | Managed databases, caches and buckets in the deployment manifest or infrastructure code | Stores you own even though you do not run them; draw them inside the system |

## What becomes an element

- **A container** is something that runs on its own: a process with its own start command and lifecycle (a web service, a worker, a scheduled job, a static site served to browsers, a mobile app on phones). Each separately started process is its own element, even when it shares code or an image with another, because it fails, scales and deploys on its own.
- **A store** is a database, stream, queue, cache or bucket that keeps data between calls. A managed database the platform runs for you is still your store.
- **An external system** is anything reached over the network that someone else runs: a mail provider, a payment API, a product database, an identity provider.
- **A person** is a role that uses the system, found in the README, the auth and role code, and the routes.
- **Not an element**: a library or shared package that nothing starts on its own (it is a module inside the units that import it); a migration or build step run before a deploy (mention it in prose); a development-only tool from the compose file (mention it when someone could mistake it for production); the hosting platform itself, which belongs in a deployment view.

The unit is decided by how it is started, not by how the code is arranged. One folder can hold three units; three folders can be one unit.

## One image, several processes

A single image or build is often started several ways. Signs:

- The same `Dockerfile` or build appears under several services in a deployment manifest or in compose, each with a different command.
- A `Procfile` with `web:`, `worker:` and `release:` lines.
- Kubernetes deployments or jobs that share an image and differ in `args`.
- A package with several entry scripts (`dev`, `worker`, `jobs`) in its manifest.
- One entry point that branches on a variable such as `ROLE` or `PROCESS_TYPE`.

Draw each started process as its own container, with an id from what it does (`api`, `mailer`, `search`). Say the shared image in the Technology cell ("same image as the API, started with `node dist/mailer.js`") and cite both the deployment entry with its command and the entry point the command runs.

The opposite also happens: one process with several roles. A web server that also runs a scheduler on a timer, or consumes a queue in a background loop, is one container whose Responsibility names both roles, with the line that starts each role as evidence. Drawing it as two containers would claim that the roles fail and scale apart, and they do not.

To tell the two apart, ask what the operating system or platform starts. Count the start commands in production, not the entry files in the tree: an entry file that no command starts is code that does not run in production, and is worth a blind spot or a disagreement.

## Three kinds of evidence

Every fact you draw rests on one of three kinds of evidence. Keep them apart, because each one can be wrong in its own way.

### Static: what the code shows

An import, a call site, a query against a table, a route registration, a producer writing to a named stream. It proves that the code can do this, wherever and whenever it runs.

Larder examples: `api/src/pantry/repo.ts` runs `SELECT` and `INSERT` against `pantry_items`, so `api` reads and writes `db`. The web client's API module calls `/v1/households`, so `web` calls `api`.

It cannot prove that the code runs in production, which instance it reaches, or that a branch is ever taken. An import alone proves less still: a client library imported in a file that nothing calls is not a relationship. Draw an arrow for a call site, and say in the row when it sits behind a condition.

### Configuration: what the deployment says

A service in the deployment manifest, an instance count, a schedule, a variable that names a host, a managed store, a client build profile that sets the API URL.

Larder examples: the production manifest declares a cron service that runs the mailer every ten minutes, so `mailer` is a scheduled job, not a long-running worker. A DSN variable for an error tracker is set only in the production manifest; the code reads it through a generic config helper, so without the manifest nobody would know the external exists.

Configuration proves what is declared to run and where it points. It cannot prove that the platform applied it, that a secret has a value, or which service a public domain reaches when the mapping lives in a dashboard. When an element or relationship rests on configuration alone, say so in its row ("named only in `render.yaml`"), and cite the code that reads the variable first and the configuration line that sets it second.

Development and production configuration often disagree. Compose may run a plain database image where production uses a managed one with different settings, or wire a client straight to the API where production puts a proxy between them. Draw production, and note in the view's prose any development difference that would surprise a reader.

### Runtime only: what no file can settle

Whether a feature flag stored in the database is on; whether a code path is ever exercised; how many instances run under autoscaling; which service a custom domain is mapped to; whether a setting changed in a hosting dashboard overrides the manifest; the value of a secret; the volume of data or traffic; whether a consumer that the code expects exists in another repository.

Larder examples: the flag that turns on household invitations by link lives in a `settings` table and is seeded off by a migration; whether production turned it on is runtime only. The manifest declares a read replica, and the code reads its URL in one report query; whether that query runs often enough to matter, or at all, is runtime only.

Draw a runtime-only fact only when code or configuration shows it can happen, write "unconfirmed at runtime" in its row, and add a blind spot that says what would confirm it. Never conclude from one absence that something cannot happen: an empty search result does not rule out a host built from parts, a plugin loaded by name, or a caller in another repository.

### When sources disagree

| Disagreement | Trust | Record |
|---|---|---|
| A name or a document against the code | The code | A disagreement row with both paths |
| The development stack against the production manifest | The production manifest, for what runs in production | A sentence in the view's prose when it would mislead a developer |
| The production manifest against the code (a service whose entry file does not exist, a variable nothing reads) | Neither, alone: draw what both support | A blind spot or a disagreement, with both paths |
| An accepted decision record against the code | The code, for what is built | A disagreement row; the record stays as it is, and the report names it so the person can decide whether the code or the decision is wrong |

## Names that mislead

Folder names, package names, service names, layout tables and comments are written once and drift. Typical cases:

- A `cache/` or `utils/` package that is the only writer of a table.
- A `shared/` or `common/` package that opens its own database connection or calls an external system, so every unit that imports it gains that relationship.
- A folder named for one purpose whose code does another: `legacy/` still on the login path, `admin/` that serves public pages, `jobs/` that holds a long-running server, `metrics/` that writes customer orders.
- A service called a gateway, an edge or a bff that only forwards requests, or one that does far more (authentication, rate limits, caching) than its name admits.
- A `worker` that also serves HTTP; an `api` that also runs scheduled work.
- A `mock`, `stub` or `fake` module that production configuration selects.

**How to catch them.** For each unit and each folder that might become an element, write one sentence from its behaviour before you look at its name: what it reads (tables, streams, files, requests), what it writes, what it calls (hosts, queues), what it sends (mail, pushes, webhooks), and who starts it. Read what its entry point imports and follow the calls one level down. Then compare the sentence with the name and with what the documents say about it. When they differ:

- Name the element and choose its id from the behaviour (`order_import`, not `metrics`).
- Keep the folder in the Technology or Responsibility cell, so a reader can find the code: "code in `metrics/`".
- Say in the row that the name misleads, in a few words: "the folder name says metrics; it imports orders".
- Add a row to the disagreements table with the folder or document as the source.

A misleading name often hides a relationship too: the folder that "exports reports" also uploads customer data to a partner's bucket. Follow every outbound call of such code, because that hidden arrow is usually the fact that matters most to the next reader.

## Documents that are out of date

Architecture documents, READMEs, layout tables in `AGENTS.md`, wiki exports and diagrams in pull requests describe the system on the day they were written. Treat each as a list of claims.

**Signs a document is out of date**: a date or a "last updated" line older than the newest migration or deployment change; units or stores in the deployment manifest that the document never mentions; technologies it names that no manifest lists; a diagram with fewer processes than the manifest starts; words like "only", "never" and "all" ("the API is the only writer"), which one new process makes false.

**What to do with each claim**: find the code or configuration that confirms or contradicts it. A confirmed claim needs no mention. A contradicted one becomes a disagreement row with the document's path and line, what it says, what the code does, and the evidence. A claim you cannot check becomes a blind spot.

**Never copy a diagram as truth.** Draw from your working list. An old diagram is useful for one thing: every box and arrow on it is a claim to check, and every unit in the manifest that it lacks is a sign of when it stopped being true.

**Leave the person's documents unchanged.** Write the recovered views beside them in the conventions' format, list the old file in the index as not verified, and propose in the report that the person replace it with a link to the new views or remove it. Decision records are different: they record why, which the code cannot tell you. Link them from the views they explain, never edit them, and report any record the code contradicts.

## Writing a blind spot

A blind spot is a fact that matters to the architecture and that the repository cannot settle. Write each one so that someone can close it with one action:

- **The fact**, as a question with a yes, no or number answer: "Is the invitation-link flag on in production?", not "flags unclear".
- **Why the repository cannot settle it**: the value lives in the database, in a dashboard, in DNS, in a secret store, in another repository, or only in traffic.
- **What would establish it**: a concrete action: a query to run and where (`SELECT enabled FROM settings WHERE key = 'invite_links'` on production), the dashboard page to read (the hosting platform's custom domains page for the web service), a log search over a named period, or the person who knows ("the person who set up the domains").
- **The ids it affects**, so a later review knows which boxes rest on it.

Good: "How many API instances run in production; the manifest allows one to four and the rate limiter counts in process memory. Would establish it: the hosting dashboard's instance history for the API service over the last week. Ids: `api`."

Not useful: "Scaling unknown." It names no fact, no reason and no next step.

Write blind spots for what matters to the views: an element that may not run, a relationship whose target is unknown, a guarantee that depends on a setting. Skip facts no view depends on. Questions a person could answer in a minute go in the report as one list; do not stop to ask them before the views are written.

## Large repositories

When the repository is too large to read whole, recover a scope instead of pretending to cover it all:

- Read every deployment manifest in full, because it is short and lists every unit. That gives the complete set of elements even when you read the code of only some.
- Read the entry point and outbound calls of every unit, and the internals only where a relationship needs them.
- State the scope in the Recovery section: which units and folders were read, which were not, and which elements therefore rest on configuration alone.

A recovery that says what it did not read is useful. One that implies full coverage it does not have misleads every review built on it.

## Searching, where a shell is available

Searches find candidates; reading the hit confirms them. Useful starting points, adapted to the stack:

```bash
git ls-files | grep -Ei '(dockerfile|compose|procfile|render\.yaml|fly\.toml|serverless|helm|k8s|terraform|\.tf$|workflows/)'
git ls-files | grep -Ei '(migrations?/|schema\.prisma|alembic|\.sql$)'
grep -rnE 'process\.env\.|os\.environ|os\.Getenv|ENV\[|getenv\(' --include='*.*' .
grep -rnE 'https?://[a-z0-9.-]+' --include='*.ts' --include='*.py' --include='*.go' --include='*.rb' .
grep -rnE '\b(fetch|axios|requests\.|httpx\.|http\.Get|HttpClient)\b' .
grep -rnE '\b(xadd|xreadgroup|publish|subscribe|sendMessage|enqueue|perform_async|delay\()' .
git rev-parse --short HEAD
git status --porcelain
```

Exclude dependency and build folders (`node_modules`, `vendor`, `dist`, `target`, `.venv`) from every search. The last two commands give the commit for the `Verified` part and show whether any file you cite has uncommitted changes, in which case the `Verified` part stays off.
