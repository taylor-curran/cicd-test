# AI-Powered Code Review CI/CD

Automated code review using Claude Code CLI and slash commands in GitHub Actions.

## What it does

- **Reviews code changes** against guidelines in `best_practices/security_rules.md`
- **Runs automatically** on every push/PR
- **Provides feedback** with specific recommendations
- **Uses slash commands** for consistent review workflow

## Files

- `code_checker_command.py` - Command wrapper for GitHub Actions
- `.claude/commands/code-review.md` - Slash command definition
- `best_practices/security_rules.md` - Security guidelines to enforce
- `badly_written_app.py` - Test Flask app with intentional security issues
- `.github/workflows/code-review-command.yml` - CI pipeline using CLI

## Try it yourself

### Local testing
```bash
# Setup
git clone <this-repo>
uv venv
source .venv/bin/activate
uv pip install claude-code-sdk anyio

# Set API key
export ANTHROPIC_API_KEY="your-key-here"

# Run code review locally
python code_checker.py
```

### GitHub Actions
1. Fork this repo
2. Add `ANTHROPIC_API_KEY` secret: Settings → Secrets and variables → Actions
3. Push code changes
4. Check Actions tab for automated review

[Example run](https://github.com/taylor-curran/cicd-test/actions/runs/16243842346/job/45863830367)

<img width="1051" height="781" alt="image" src="https://github.com/user-attachments/assets/ef328ba7-e096-46b8-92b6-a8191a6d53da" />

## Cost
~$0.05-0.15 per review depending on code complexity.

## Technical Notes

### Approach: CLI vs SDK
We tried 2 experimental approaches:

1. **Claude Code SDK** - Initially tried using `claude-code-sdk` to invoke slash commands from Python, but encountered errors when passing `/code-review` as a prompt
2. **Claude Code CLI** ✅ - Successfully used `claude -p "/code-review"` directly in GitHub Actions

**Current solution:** Uses Claude Code CLI directly rather than SDK wrapper. Still undecided if it's possible to invoke slash commands from SDK prompts - we gave up quickly after the first error.

### Slash Commands as Workflows
The `/code-review` slash command acts like a reusable workflow:
- Defined in `.claude/commands/code-review.md`
- Contains the review logic, git context gathering, and file references
- Can be invoked consistently from CLI or interactively

## Areas for improvement
- **SDK + Commands**: Investigate if slash commands can work with SDK (we hit errors and moved on)
- **More efficient prompting**: Could reduce API costs by focusing only on modified lines
- **Advanced workflows**: Future experiments with complex automation patterns
