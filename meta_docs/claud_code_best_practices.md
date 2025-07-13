# Claude Code: Best practices for agentic coding

**Published Apr 18, 2025**

Claude Code is a command line tool for agentic coding. This post covers tips and tricks that have proven effective for using Claude Code across various codebases, languages, and environments.

We recently released Claude Code, a command line tool for agentic coding. Developed as a research project, Claude Code gives Anthropic engineers and researchers a more native way to integrate Claude into their coding workflows.

Claude Code is intentionally low-level and unopinionated, providing close to raw model access without forcing specific workflows. This design philosophy creates a flexible, customizable, scriptable, and safe power tool. While powerful, this flexibility presents a learning curve for engineers new to agentic coding tools—at least until they develop their own best practices.

This post outlines general patterns that have proven effective, both for Anthropic’s internal teams and for external engineers using Claude Code across various codebases, languages, and environments. Nothing in this list is set in stone nor universally applicable; consider these suggestions as starting points. We encourage you to experiment and find what works best for you!

Looking for more detailed information? Our comprehensive documentation at [claude.ai/code](https://claude.ai/code) covers all the features mentioned in this post and provides additional examples, implementation details, and advanced techniques.

---

## 1. Customize your setup

Claude Code is an agentic coding assistant that automatically pulls context into prompts. This context gathering consumes time and tokens, but you can optimize it through environment tuning.

### a. Create CLAUDE.md files

`CLAUDE.md` is a special file that Claude automatically pulls into context when starting a conversation. This makes it an ideal place for documenting:

- **Common bash commands**
- **Core files and utility functions**
- **Code style guidelines**
- **Testing instructions**
- **Repository etiquette** (e.g., branch naming, merge vs. rebase)
- **Developer environment setup** (e.g., pyenv use, which compilers work)
- **Any unexpected behaviors or warnings** particular to the project
- **Other information** you want Claude to remember

There’s no required format for `CLAUDE.md` files. We recommend keeping them concise and human-readable. For example:

```markdown
# Bash commands
- npm run build: Build the project
- npm run typecheck: Run the typechecker

# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible (e.g., import { foo } from 'bar')

# Workflow
- Be sure to typecheck when you’re done making a series of code changes
- Prefer running single tests, and not the whole test suite, for performance
```

You can place `CLAUDE.md` files in several locations:

- The root of your repo, or wherever you run `claude` from (the most common usage). Name it `CLAUDE.md` and check it into git so that you can share it across sessions and with your team (recommended), or name it `CLAUDE.local.md` and add it to `.gitignore`.
- Any parent of the directory where you run `claude` (useful for monorepos). Claude will pull in both parent and child `CLAUDE.md` files automatically.
- Any child of the directory where you run `claude`. Claude will pull in these files on demand when you work with files in child directories.
- Your home folder (`~/.claude/CLAUDE.md`), which applies it to all your Claude sessions.

When you run the `/init` command, Claude will automatically generate a `CLAUDE.md` for you.

### b. Tune your CLAUDE.md files

Your `CLAUDE.md` files become part of Claude’s prompts, so they should be refined like any frequently used prompt. A common mistake is adding extensive content without iterating on its effectiveness. Take time to experiment and determine what produces the best instruction following from the model.

You can add content to your `CLAUDE.md` manually or press the `#` key to give Claude an instruction that it will automatically incorporate into the relevant `CLAUDE.md`. Many engineers use `#` frequently to document commands, files, and style guidelines while coding, then include `CLAUDE.md` changes in commits so team members benefit as well.

At Anthropic, we occasionally run `CLAUDE.md` files through the prompt improver and often tune instructions (e.g., adding emphasis with "IMPORTANT" or "YOU MUST") to improve adherence.

### c. Curate Claude’s list of allowed tools

By default, Claude Code requests permission for any action that might modify your system: file writes, many bash commands, MCP tools, etc. We designed Claude Code with this deliberately conservative approach to prioritize safety. You can customize the allowlist to permit additional tools that you know are safe, or to allow potentially unsafe tools that are easy to undo (e.g., file editing, git commit).

There are four ways to manage allowed tools:

1. Select **Always allow** when prompted during a session.
2. Use the `/permissions` command after starting Claude Code to add or remove tools from the allowlist. For example:
   - `Edit` to always allow file edits
   - `Bash(git commit:*)` to allow git commits
   - `mcp__puppeteer__puppeteer_navigate` to allow Puppeteer navigation
3. Manually edit your `.claude/settings.json` or `~/.claude.json` (we recommend checking the former into source control to share with your team).
4. Use the `--allowedTools` CLI flag for session-specific permissions.

### d. If using GitHub, install the `gh` CLI

Claude knows how to use the `gh` CLI to interact with GitHub for creating issues, opening pull requests, reading comments, and more. Without `gh` installed, Claude can still use the GitHub API or MCP server (if you have it installed).

---

## 2. Give Claude more tools

Claude has access to your shell environment, where you can build up sets of convenience scripts and functions for it just like you would for yourself. It can also leverage more complex tools through MCP and REST APIs.

### a. Use Claude with bash tools

Claude Code inherits your bash environment, giving it access to all your tools. While Claude knows common utilities like Unix tools and `gh`, it won’t know about your custom bash tools without instructions:

- Tell Claude the tool name with usage examples
- Tell Claude to run `--help` to see tool documentation
- Document frequently used tools in `CLAUDE.md`

### b. Use Claude with MCP

Claude Code functions as both an MCP server and client. As a client, it can connect to any number of MCP servers to access their tools in three ways:

- In project config (available when running Claude Code in that directory)
- In global config (available in all projects)
- In a checked-in `.mcp.json` file (available to anyone working in your codebase)

For example, you can add Puppeteer and Sentry servers to your `.mcp.json`, so that every engineer working on your repo can use these out of the box.

When working with MCP, you can also launch Claude with the `--mcp-debug` flag to help identify configuration issues.

### c. Use custom slash commands

For repeated workflows—debugging loops, log analysis, etc.—store prompt templates in Markdown files within the `.claude/commands` folder. These become available through the slash commands menu when you type `/`. You can check these commands into git to make them available for the rest of your team.

Custom slash commands can include the special keyword `$ARGUMENTS` to pass parameters from the command invocation.

For example, here’s a slash command that you could use to automatically pull and fix a GitHub issue:

```markdown
Please analyze and fix the GitHub issue: $ARGUMENTS.

Follow these steps:

1. Use `gh issue view` to get the issue details
2. Understand the problem described in the issue
3. Search the codebase for relevant files
4. Implement the necessary changes to fix the issue
5. Write and run tests to verify the fix
6. Ensure code passes linting and type checking
7. Create a descriptive commit message
8. Push and create a PR
```

Putting the above content into `.claude/commands/fix-github-issue.md` makes it available as the `/project:fix-github-issue` command in Claude Code. You could then, for example, use `/project:fix-github-issue 1234` to have Claude fix issue #1234. Similarly, you can add your own personal commands to the `~/.claude/commands` folder for commands you want available in all of your sessions.

---

## 3. Try common workflows

Claude Code doesn’t impose a specific workflow, giving you the flexibility to use it how you want. Within the space this flexibility affords, several successful patterns for effectively using Claude Code have emerged across our community of users:

### a. Explore, plan, code, commit

This versatile workflow suits many problems:

1. Ask Claude to read relevant files, images, or URLs, providing either general pointers ("read the file that handles logging") or specific filenames ("read logging.py"), but explicitly tell it not to write any code just yet.
2. Use subagents for complex problems: telling Claude to use subagents to verify details or investigate particular questions tends to preserve context without sacrificing efficiency.
3. Ask Claude to make a plan for how to approach a specific problem. Use the word **think** to trigger extended thinking modes:
   - `think`  
   - `think hard`  
   - `think harder`  
   - `ultrathink`  

   Each level allocates progressively more thinking budget.
4. If the plan looks good, ask Claude to create a document or GitHub issue with its plan so you can reset to this spot if the implementation isn’t what you want.
5. Ask Claude to implement its solution in code, verifying reasonableness as it goes.
6. Ask Claude to commit the result and create a pull request. Update READMEs or changelogs if relevant.

> **Why?** Steps 1–2 prevent Claude from jumping straight to code, improving results for deeper problems.

### b. Write tests, commit; code, iterate, commit

This Anthropic-favorite workflow leverages test-driven development (TDD):

1. Ask Claude to write tests based on expected input/output pairs. Be explicit that you’re doing TDD to avoid mock implementations.
2. Tell Claude to run the tests and confirm they fail—do not write implementation code yet.
3. Commit the tests.
4. Ask Claude to write code to pass the tests, instructing it not to modify the tests. Iterate until all tests pass.
5. (Optional) Use independent subagents to ensure the implementation isn’t overfitting.
6. Commit the code when satisfied.

> **Why?** Providing clear targets (tests) lets Claude evaluate and improve until success.

### c. Write code, screenshot result, iterate

Similar to TDD but for visual targets:

1. Provide browser screenshots (via Puppeteer MCP, iOS simulator MCP, or manual copy/paste).
2. Provide visual mocks by dragging/dropping images or specifying file paths.
3. Ask Claude to implement the design, take screenshots, and iterate until the result matches the mock.
4. Commit when satisfied.

> **Why?** Iteration on visual feedback yields better UI results.

### d. Safe YOLO mode

Use `claude --dangerously-skip-permissions` to bypass permission checks. Ideal for bulk fixes like lint errors or boilerplate generation.

> **Warning:** This is risky. Use in a contained environment (e.g., Docker Dev Containers without internet).

### e. Codebase Q&A

For onboarding or exploration, ask Claude the same questions you would a human engineer:

- How does logging work?
- How do I make a new API endpoint?
- What does `async move { ... }` do on line 134 of `foo.rs`?
- What edge cases does `CustomerOnboardingFlowImpl` handle?
- Why are we calling `foo()` instead of `bar()` on line 333?
- What’s the equivalent of line 334 of `baz.py` in Java?

> **Impact:** This has become our core onboarding workflow, reducing ramp time and support load.

### f. Use Claude to interact with git

Claude handles many git operations:

- Searching history: “What changes made it into v1.2.3?”, “Who owns this feature?”
- Writing commit messages based on diffs
- Complex ops: reverting, resolving rebase conflicts, grafting patches

### g. Use Claude to interact with GitHub

- Creating pull requests via `pr` shorthand
- Fixing review comments
- Resolving build or linter failures
- Categorizing and triaging issues

> **Benefit:** Automates routine GitHub tasks without memorizing `gh` syntax.

### h. Use Claude to work with Jupyter notebooks

Claude can read/write `.ipynb` files, interpret outputs and images. To optimize:

- Open notebook side-by-side with Claude in VS Code
- Ask Claude to clean up or prettify visualizations for human review

---

## 4. Optimize your workflow

These suggestions apply across workflows:

### a. Be specific in your instructions

Specificity improves first-pass success. Examples:

| Poor | Good |
|---|---|
| add tests for foo.py | write a new test case for `foo.py` covering the logged-out edge case; avoid mocks |
| why does ExecutionFactory have such a weird api? | look through `ExecutionFactory`’s git history and summarize how its API evolved |
| add a calendar widget | examine existing widgets on the home page; follow patterns in `HotDogWidget.php`; implement a calendar widget from scratch with pagination |

> **Tip:** Claude infers intent but can’t read minds.

### b. Give Claude images

Claude excels with images:

- Paste screenshots (macOS: `Cmd`+`Ctrl`+`Shift`+`4`, then `Ctrl`+`V`)
- Drag-and-drop images
- Provide file paths

> **Use case:** Design mocks and visual debugging.

### c. Mention files you want Claude to look at

Use tab-completion to reference files or folders, ensuring Claude edits the right resources.

### d. Give Claude URLs

Paste specific URLs for Claude to fetch and read. Use `/permissions` to allow repeated access.

### e. Course correct early and often

While `--dangerously-skip-permissions` offers autonomy, active collaboration yields better outcomes:

1. Ask Claude to make a plan before coding.
2. Press `Esc` to interrupt and redirect.
3. Double-tap `Esc` to edit previous prompts.
4. Ask Claude to undo changes and try a new approach.

### f. Use `/clear` to keep context focused

Reset context between tasks to avoid distracting Claude with irrelevant history.

### g. Use checklists and scratchpads for complex workflows

For large tasks (e.g., lint migrations):

1. Run lint, write errors to a Markdown checklist
2. Instruct Claude to fix each issue and verify before checking off

### h. Pass data into Claude

- Copy/paste data
- Pipe into Claude (e.g., `cat foo.txt | claude`)
- Use bash, MCP, or slash commands to fetch logs, CSVs, images

---

## 5. Use headless mode to automate your infra

Headless mode (`-p` + `--output-format stream-json`) is ideal for CI, pre-commit hooks, and automation:

### a. Use Claude for issue triage

Trigger automations on GitHub events (e.g., label new issues automatically).

### b. Use Claude as a linter

Subjective code reviews for typos, stale comments, misleading names, and more.

---

## 6. Uplevel with multi-Claude workflows

### a. Have one Claude write code; another verify

1. Claude A writes code
2. `/clear` or open Claude B in another terminal
3. Claude B reviews the code
4. Claude C merges feedback and edits

> **Benefit:** Separate context yields better peer review.

### b. Have multiple checkouts of your repo

- Create 3–4 clones in separate directories
- Run Claude in each folder with different tasks
- Cycle through for permission prompts and approvals

### c. Use git worktrees

A lightweight alternative to multiple clones:

- `git worktree add ../project-feature-a feature-a`
- `cd ../project-feature-a && claude`
- Repeat as needed

> **Tip:** Use consistent naming and separate IDE windows.

### d. Use headless mode with a custom harness

- **Fanning out:** Generate scripts to handle thousands of tasks (e.g., code migrations)
- **Pipelining:** Integrate `claude -p` JSON output into processing pipelines

> **Pro tip:** Use `--verbose` for debugging; disable in production.

---

### What are your tips and best practices for working with Claude Code? Tag @AnthropicAI so we can see what you’re building!

---

## Acknowledgements

Written by **Boris Cherny**. Special thanks to **Daisy Hollman**, **Ashwin Bhat**, **Cat Wu**, **Sid Bidasaria**, **Cal Rueb**, **Nodir Turakulov**, **Barry Zhang**, **Drew Hodun**, and many other Anthropic engineers whose insights shaped these recommendations.

