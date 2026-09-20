#!/usr/bin/env bash
# scripts/ci.sh — Local-only CI pipeline for homebrew-merge-dependabot
# Per agent-docs/conventions/local-ci.md

set -euo pipefail

BOLD='\033[1m'
GREEN='\033[0;32m'
RED='\033[0;31m'
RESET='\033[0m'

pass() { echo -e "  ${GREEN}PASS:${RESET} $1"; }
fail() { echo -e "  ${RED}FAIL:${RESET} $1"; exit 1; }

echo -e "\n${BOLD}=== Stage 0: Preconditions ===${RESET}"
command -v python3 >/dev/null 2>&1 && pass "python3 available" || fail "python3 not found"
command -v gh >/dev/null 2>&1 && pass "gh CLI available" || fail "gh CLI not found"
command -v ruby >/dev/null 2>&1 && pass "ruby available" || fail "ruby not found"

echo -e "\n${BOLD}=== Stage 1: Syntax & Version Verification ===${RESET}"
python3 -m py_compile merge-dependabot && pass "merge-dependabot Python syntax" || fail "merge-dependabot syntax error"
ruby -c Formula/merge-dependabot.rb >/dev/null && pass "Formula/merge-dependabot.rb Ruby syntax" || fail "Formula syntax error"

SCRIPT_VER=$(grep '^VERSION = ' merge-dependabot | cut -d'"' -f2)
FORMULA_VER=$(grep 'version "' Formula/merge-dependabot.rb | cut -d'"' -f2)
if [[ "$SCRIPT_VER" == "$FORMULA_VER" ]]; then
  pass "version parity ($SCRIPT_VER)"
else
  fail "version mismatch: script has $SCRIPT_VER but formula has $FORMULA_VER"
fi

echo -e "\n${BOLD}=== Stage 2: Unit Tests ===${RESET}"
python3 -m unittest discover -s test -v && pass "unit tests" || fail "unit tests failed"

echo -e "\n${GREEN}${BOLD}All CI stages passed!${RESET}\n"
