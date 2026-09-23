# homebrew-merge-dependabot

Homebrew formula for `merge-dependabot` - a command-line tool to automatically merge green Dependabot PRs and sync all local repositories in `~/Documents/Github`.

## Installation

```bash
brew tap SiavoshZarrasvand/merge-dependabot
brew install merge-dependabot
```

## Usage

```bash
# Automatically merge green Dependabot PRs and pull/rebase all repos in ~/Documents/Github:
merge-dependabot

# Preview Dependabot merges without modifying GitHub PRs or pulling:
merge-dependabot --dry-run

# Only merge Dependabot PRs without pulling local repositories:
merge-dependabot --skip-sync

# Check version:
merge-dependabot --version
```

## Requirements

- macOS
- [GitHub CLI](https://cli.github.com/) (`gh`), authenticated with `gh auth login`
- Python 3

## Release

To cut a new release:
```bash
./release.sh
```
