# AI-Powered Code Review CI/CD

Automated code review using Claude Code SDK in GitHub Actions.

## What it does

- **Reviews code changes** against guidelines in `best_practices/CLAUDE.md`
- **Runs automatically** on every push/PR
- **Provides feedback** with specific recommendations

## Files

- `code_checker.py` - Claude Code SDK script that performs code review
- `best_practices/CLAUDE.md` - Guidelines to enforce
- `badly_written_app.py` - Test Flask app with intentional issues
- `.github/workflows/code-review.yml` - CI pipeline

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

[Example run](https://github.com/taylor-curran/cicd-test/actions/runs/16243209724/job/45862303481)

<img width="1051" height="781" alt="image" src="https://github.com/user-attachments/assets/ef328ba7-e096-46b8-92b6-a8191a6d53da" />

## Cost
~$0.05-0.15 per review depending on code complexity.

## Areas for improvement
- **Diff-only analysis**: Currently reviews entire files instead of just git diff changes
- **More efficient prompting**: Could reduce API costs by focusing only on modified lines
- **Claude Code workflows**: Future experiments with advanced automation (similar to Windsurf workflows)
