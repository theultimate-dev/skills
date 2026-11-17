---
name: reclaiming-docker-disk-space
description: "Frees space on a full Docker disk by removing unused data older than an age the user picks, 24 hours by default: stopped containers, unused networks, unused images, build cache and anonymous volumes. Runs a bundled shell script that has a dry run, keeps everything a container uses, lists unused named volumes for the user to decide instead of removing them, and on Colima trims the disk so the host gets the space back. Use when the Docker disk is full or nearly full, a build or pull fails with no space left on device, the user asks to clean up or prune Docker, or the Colima or Docker Desktop disk image keeps growing."
license: MIT
---

# Reclaiming Docker disk space

Remove the Docker data nothing uses any more and that is older than an age limit, then report how much space came back. The work is done by one script, [scripts/docker-cleanup.sh](scripts/docker-cleanup.sh), so the cleanup is the same every time. Your part is to agree the scope, show the user what will go, and settle what the script leaves to a person.

The script needs bash 3.2 or newer, the `docker` CLI and a reachable Docker daemon. Run it with `bash`, by its path inside this skill's directory:

```bash
bash <this skill's directory>/scripts/docker-cleanup.sh --dry-run
```

## What is removed and what is kept

| Data | Removed when | Kept when |
|---|---|---|
| Containers | Stopped, and created before the age limit | Running, however old |
| Networks | Unused, and created before the age limit | A container is attached |
| Images | No container uses them, and they were built before the age limit | Any container uses them, running or stopped |
| Build cache | Not used since the age limit | Used more recently |
| Anonymous volumes | No container uses them, and they were created before the age limit | Attached to a container, or newer |
| Named volumes | Never by the script | Always. Unused ones are listed |

Three things about this table surprise people. Tell the user the ones that apply before the real run:

- An image's age is its build date, not the day it was pulled. An unused image pulled today but built last month is removed. Docker pulls it again on next use.
- A running container protects itself, its image and its volumes at any age. Old stacks that are still up keep their space until someone stops them.
- Docker cannot filter volumes by age, so the script reads each volume's creation date itself. A volume whose date it cannot read is kept.

## Steps

1. **Agree the age limit.** The default is 24 hours. Use the age the user named, as a whole number of hours or days: `--older-than 48h`, `--older-than 7d`. If the user asked for a cleanup without naming an age, say that the default is 24 hours and go on.

2. **Dry run.** Run the script with `--dry-run` and the age limit. It removes nothing. It prints disk usage by type, the prune commands a real run would execute, every anonymous volume it would remove, and the unused named volumes. Usage by type can take minutes when there are hundreds of volumes; let it finish.

3. **Show the user what will go.** Give a short summary: where the space is (the `RECLAIMABLE` column), how many anonymous volumes the run removes, and which of the surprises above apply. If old stacks are still running and hold most of the space, say so, because the cleanup will not touch them.

4. **Get a yes, then run.** Removal cannot be undone. Run the script without `--dry-run` only when the user has asked for the cleanup itself in this conversation, or says yes after the summary. A request such as "check why the disk is full" is not a yes.

5. **Settle the named volumes.** The script lists unused named volumes and never removes them, because a named volume is usually data someone chose to keep, such as a database or uploaded files. Show the list with each volume's creation date and ask which to remove. Remove only the ones the user names, with `docker volume rm <name>`.

6. **Report.** State the disk usage before and after, what was removed, what was kept and why, and anything that failed. Exit code 2 means some volumes could not be removed, usually because a container started using them during the run; the output names each one.

## Handing the space back to the host

On macOS and Windows, Docker runs in a virtual machine and keeps its data in a disk image. Deleting data frees space inside that image, but the image file on the host does not shrink until the disk is trimmed.

When the current Docker context belongs to Colima, the script trims the disk itself after the cleanup and prints the data disk's usage before and after. Pass `--no-trim` to skip that. With any other setup the script does not trim: report the space freed inside Docker, and tell the user that the host may show the difference only after their Docker tool compacts its disk image.

## When the disk is still full afterwards

Read the usage by type that the script prints at the end.

- **Images or volumes with little reclaimable space**: running containers hold them. List the stacks with `docker ps`, ask which the user no longer needs, stop those, and run the script again.
- **Volumes with a lot of reclaimable space**: either the unused volumes are newer than the age limit, or they are named. Offer a shorter age limit, or go through the named volumes with the user.
- **Build cache**: it was used inside the age limit. A shorter age limit clears it; the next build is slower once.

## Keeping it from filling up again

If the dry run showed dozens of anonymous volumes of similar size, something creates one on every run and never removes it. The usual cause is a Compose service with an anonymous volume, often for a dependency directory, that is brought down without its volumes. Tell the user what you saw and that `docker compose down -v` removes a stack's volumes with it. Do not change their Compose files or scripts unless they ask.
