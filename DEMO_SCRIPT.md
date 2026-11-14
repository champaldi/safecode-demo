# Demo script (about 5 minutes)

## Before you go on stage
- Dashboard running and tunnel URL in the `SAFECODE_API_URL` secret (SETUP.md step 3 and 5). Open `/dashboard` in one tab, it refreshes every 5 s.
- A **backup PR**, identical to the live one, already opened, scanned and merged-ready: do SETUP.md step 7 on a branch `feature/user-search-backup` the day before and leave it open. Keep its tab open.
- Dry-run output saved in `demo/backup/dryrun-01.md` (regenerate: `python scripts/dryrun.py`). Take screenshots of the summary comment, one inline suggestion, the red check, the green check and the dashboard, and keep them in a slide at the end.
- Optionally delete `data/safecode.db` first so the dashboard starts at zero.

## 10 minutes before the defence (the tunnel link dies with the laptop)
1. Start the dashboard and `cloudflared tunnel --url http://localhost:8765`, copy the new `https://....trycloudflare.com` URL.
2. Update the secret: `gh secret set SAFECODE_API_URL --repo champaldi/safecode-demo --body "<new url>"`.
3. Sanity check: open the new URL + `/dashboard`.
4. Do NOT merge any demo PR before the defence. Merging puts the fix into `main`, and patch 01 would no longer apply. Branch protection keeps Merge blocked while the check is red.
5. Accepted-fix counter only increments if the dashboard already holds the first scan of the live PR, so keep the same dashboard database between the first scan and the live click.

## Links for the examiner
Public and always open: https://github.com/champaldi/safecode-ai, https://github.com/champaldi/safecode-demo, the demo PRs in `safecode-demo`, plus dashboard screenshots. The live dashboard link only works while the laptop and tunnel are on.

## Live steps
| Time | Do | Say / what appears |
|---|---|---|
| 0:00 | Show `/dashboard`: REAL block at zero, SIMULATED block with the six KPI cards | "Real numbers start at zero. The lower block is a plan simulation, labelled." |
| 0:30 | `git checkout -b feature/user-search && git apply patches/01-user-search.patch && git add -A && git commit -m "Add user search" && git push -u origin feature/user-search` | "A developer adds a search endpoint." |
| 1:00 | `gh pr create --fill`, open the PR page | Workflow starts. |
| 1:15 to 2:00 | Wait, talk about the problem: audits cost $10-30k, scanners flood small teams with false positives | Summary comment appears: **5 raw → 2 real, 3 filtered (60% noise removed)**; the check is red. |
| 2:00 | Open `<details>` in the comment | Three filtered findings with reasons: constant SQL, test-only token, md5 as cache key. "This is the noise we removed." |
| 2:30 | Open "Files changed": two inline comments in Russian with a Rule-based fix | SQL injection (critical) and weak password hash (high). |
| 3:00 | "Add suggestion to batch" on both, then "Commit suggestions" | A new commit; the workflow re-runs. |
| 3:45 | Refresh the PR | Same comment updated in place, findings struck through, check green. Merge. |
| 4:15 | Back to `/dashboard` (no reload needed) | 2 real findings, 60% filtered, 2 accepted fixes, avg scan time, cost per scan (0 KZT, rule-based). "updated Xs ago" ticks. |
| 4:45 | Scroll to SIMULATED | Revenue, paying teams, activation red; burn yellow; churn, uptime green. "Simulated for September 2027; the point is the plan has owners and actions." |

Pricing and roadmap are in the README table: Team 125,000 KZT per team per month (proposed, not purchasable); everything else is PLANNED.

## If something fails
- **Workflow does not start or takes over 2 minutes:** switch to the backup PR tab (already scanned, same comment, same red check). Do the Commit-suggestion step on it live if it works, otherwise just narrate.
- **No comment but a check exists:** the token lacked permission. Show the backup PR and say so honestly.
- **Check says "SafeCode AI: scan failed":** that is the designed behaviour, never a silent pass. Show the error in the summary, switch to the backup PR.
- **Dashboard shows nothing new:** the tunnel URL changed or the token differs; the check is unaffected by ingest failures. Show `demo/backup/dryrun-01.md` and the dashboard screenshots.
- **No internet at all:** run `python scripts/dryrun.py` in a terminal. It prints the exact comments, both runs, and (with `--api-url`) fills a local dashboard.
