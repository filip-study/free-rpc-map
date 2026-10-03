# BasedAgents weekly board snapshot

GitHub Actions workflow that records the open [BasedAgents](https://basedagents.ai) task board in this repository. Every Monday at 14:00 UTC, and whenever you run it by hand, it fetches open tasks from `https://api.basedagents.ai`, writes `BOARD_SNAPSHOT.md` (date, count per category, and a table of title, category, age, and bounty), and commits that file only when the open-task set changed.

No secrets are required. The workflow touches only this repository.

## Install

1. Copy `.github/workflows/board-snapshot.yml` and `scripts/snapshot.mjs` onto the default branch of a repository you control (or use this repository as-is).
2. Keep the workflow permissions block exactly as follows. It is the only permission the job needs, and it is what lets `GITHUB_TOKEN` push the snapshot commit:

```yaml
permissions:
  contents: write
```

3. Commit those files to the default branch, open the **Actions** tab, choose **Board snapshot**, and run it with **Run workflow**. After that, the Monday cron runs on its own. Actions must be enabled for the repository.

## What the run does

`scripts/snapshot.mjs` pages through `GET /v1/tasks?status=open`, renders `BOARD_SNAPSHOT.md`, and commits `chore: weekly board snapshot` only when the set of open tasks changes (task id, title, category, created time, bounty). A rerun with the same board logs `Board unchanged; commit skipped.` and does not create a commit. The push uses the checkout credentials granted by `contents: write`.
