---
allowed-tools: Read, Grep, Glob, Bash(git*)
description: Review code changes against best practices guidelines
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Best practices guidelines: @best_practices/

## Your task

Check if new code changes adhere to the guidelines in the `/best_practices` directory.

Focus on: $ARGUMENTS

ONLY assess against `/best_practices` guidelines. Do not suggest improvements outside of those guidelines.

Provide a concise assessment of:
1. **Compliance** - What guidelines are being followed correctly
2. **Violations** - Specific violations found with file/line references
3. **Summary** - Overall compliance status

Be specific about which files and lines have issues.