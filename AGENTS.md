# Agent Instructions: homebrew-merge-dependabot

## House rules: read first

Read `../../agent-docs/AGENTS.md` before starting any work. It is the shared foundation across all repos: conventions (commit messages, how work lands, local CI) expected to be followed, plus templates for build plans, beads, and reviews.

Merge-Dependabot specific overrides & details:
- **Stack**: Standalone Python 3 CLI executable (zero external python dependencies) + Homebrew Ruby formula (`Formula/merge-dependabot.rb`).
- **Dependencies**: Depends only on Python 3 and the GitHub CLI (`gh`).
- **Local CI**: Run `sh scripts/ci.sh` before merging.
- **Releases**: Managed via `./release.sh`, which auto-increments version, tags git commit, fetches tarball SHA256, and updates `Formula/merge-dependabot.rb`.
- **Landing work**: Per `../../agent-docs/conventions/landing-work.md`, work on branches, verify `scripts/ci.sh` passes, then merge locally.
- **Issue tracking**: Beads only (`bd`).

---

## Quick Reference

```bash
bd ready                # Find available work
bd show <id>            # View issue details
bd update <id> --claim  # Claim work atomically
bd close <id>           # Complete work
bd dolt push            # Push beads data to remote
```

## Non-Interactive Shell Commands

**ALWAYS use non-interactive flags** with file operations to avoid hanging on confirmation prompts (`rm -rf`, `cp -f`, etc.).
