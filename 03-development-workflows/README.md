# Chapter 03: Development Workflows

In this chapter, GitHub Copilot CLI becomes your daily driver. You'll use it inside the workflows you rely on every day: code review, refactoring, debugging, testing, and Git.

## 🎯 Learning Objectives

By the end of this chapter, you'll be able to:

- Run comprehensive code reviews with Copilot CLI
- Refactor legacy code safely
- Debug issues with AI assistance
- Generate tests automatically
- Integrate Copilot CLI with your Git workflow

⏱️ **Estimated Time**: ~60 minutes (15 min reading + 45 min hands-on)

## 🧩 Real-World Analogy: A Carpenter's Workflow

A carpenter doesn't just know how to use tools — they have workflows for different jobs:

![Illustration of a carpenter's workflow with different tools for different jobs](images/caprenters-workflow.png)

Similarly, developers have workflows for different tasks. GitHub Copilot CLI enhances each of these workflows, making you more efficient and effective in your daily coding tasks.

## The Five Workflows

![Overview diagram of the five core developer workflows](images/workflows.png)

Each workflow below is self-contained. Pick the ones that match your current needs, or work through them all.

### Choose Your Own Adventure

This chapter covers five workflows that developers typically use. However, you don't need to read them all at once! Each workflow is self-contained in a section below. Pick the ones that match what you need and that fit best with your current project. You can always come back and explore the others later.

![Diagram showing the different types of developer workflows](images/different-type-of-workflows.png)

| I want to... | Jump to |
|--------------|---------|
| Review code before merging | Workflow 1: Code Review |
| Clean up messy or legacy code | Workflow 2: Refactoring |
| Track down and fix a bug | Workflow 3: Debugging |
| Generate tests for my code | Workflow 4: Test Generation |
| Write better commits and PRs | Workflow 5: Git Integration |
| Research before coding | Quick Tip: Research Before You Plan or Code |
| See a full bug-fix workflow end to end | Putting It All Together |

Select a workflow below to expand it and see how GitHub Copilot CLI can enhance your development process in that area.

---

## Workflow 1: Code Review

> Review files, use the `/review` agent, create severity checklists

![Illustration of a code review process](images/code-review.png)

### Basic Review

This example uses the `@` symbol to reference a file, giving Copilot CLI direct access to its contents for review.

```bash
copilot
> Review @samples/book-app-project/book_app.py for code quality
```

### Input Validation Review

Ask Copilot CLI to focus its review on a specific concern (here, input validation) by listing the categories you care about in the prompt.

```bash
copilot
> Review @samples/book-app-project/utils.py for input validation issues. Check for: missing validation, error handling gaps, and edge cases
```

### Cross-File Project Review

Reference an entire directory with `@` to let Copilot CLI scan every file in the project at once.

```bash
copilot
> @samples/book-app-project/ Review this entire project. Create a markdown checklist of issues found, categorized by severity
```

### Interactive Code Review

Use a multi-turn conversation to drill deeper. Start with a broad review, then ask follow-up questions without restarting.

```bash
copilot
> @samples/book-app-project/book_app.py Review this file for:
> - Input validation
> - Error handling
> - Code style and best practices

# Copilot CLI provides detailed review

> The user input handling - are there any edge cases I'm missing?

# Copilot CLI shows potential issues with empty strings, special characters

> Create a checklist of all issues found, prioritized by severity

# Copilot CLI generates prioritized action items
```

### Review Checklist Template

Ask Copilot CLI to structure its output in a specific format (here, a severity-categorized markdown checklist you can paste into an issue).

```bash
copilot
> Review @samples/book-app-project/ and create a markdown checklist of issues found, categorized by:
> - Critical (data loss risks, crashes)
> - High (bugs, incorrect behavior)
> - Medium (performance, maintainability)
> - Low (style, minor improvements)
```

### Understanding Git Changes (Important for `/review`)

Before using the `/review` command, you need to understand two types of changes in git:

| Change Type | What It Means | How to See |
|-------------|---------------|------------|
| Staged changes | Files you've marked for the next commit with `git add` | `git diff --staged` |
| Unstaged changes | Files you've modified but haven't added yet | `git diff` |

```bash
# Quick reference
git status           # Shows both staged and unstaged
git add file.py      # Stage a file for commit
git diff             # Shows unstaged changes
git diff --staged    # Shows staged changes
```

### Using the `/review` Command

The `/review` command invokes the built-in code-review agent, which is optimized for analyzing staged and unstaged changes with high signal-to-noise output. Use a slash command to trigger a specialized built-in agent instead of writing a free-form prompt.

```bash
copilot
> /review
# Invokes the code-review agent on staged/unstaged changes
# Provides focused, actionable feedback

> /review Check for security issues in authentication
# Run review with specific focus area
```

💡 **Tip**: The code-review agent works best when you have pending changes. Stage your files with `git add` for more focused reviews.

---

## Workflow 2: Refactoring

> Restructure code, separate concerns, improve error handling

![Illustration of code refactoring](images/refactoring.png)

### Simple Refactoring

Try this first:

```bash
copilot
> @samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.
```

Start with straightforward improvements. Try these on the book app. Each prompt uses an `@` file reference paired with a specific refactoring instruction so Copilot CLI knows exactly what to change.

```bash
copilot
> @samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.

> @samples/book-app-project/utils.py Add type hints to all functions

> @samples/book-app-project/book_app.py Extract the book display logic into utils.py for better separation of concerns
```

### Separate Concerns

Reference multiple files with `@` in a single prompt so Copilot CLI can move code between them as part of the refactor.

```bash
copilot
> @samples/book-app-project/utils.py @samples/book-app-project/book_app.py
> The utils.py file has print statements mixed with logic. Refactor to separate display functions from data processing.
```

### Improve Error Handling

Provide two related files and describe the cross-cutting concern so Copilot CLI can suggest a consistent fix across both.

```bash
copilot
> @samples/book-app-project/utils.py @samples/book-app-project/books.py
> These files have inconsistent error handling. Suggest a unified approach using custom exceptions.
```

### Add Documentation

Use a detailed bullet list to specify exactly what each docstring should contain.

```bash
copilot
> @samples/book-app-project/books.py Add comprehensive docstrings to all methods:
> - Include parameter types and descriptions
> - Document return values
> - Note any exceptions raised
> - Add usage examples
```

### Safe Refactoring with Tests

Chain two related requests in a multi-turn conversation. First generate tests, then refactor with those tests as a safety net.

```bash
copilot
> @samples/book-app-project/books.py Before refactoring, generate tests for current behavior

# Get tests first

> Now refactor the BookCollection class to use a context manager for file operations

# Refactor with confidence — tests verify behavior is preserved
```

---

## Workflow 3: Debugging

> Track down bugs, trace issues through code, understand errors

![Illustration of debugging workflow with Copilot CLI](images/debugging.png)

### Simple Debugging

Try this first:

```bash
copilot
> @samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.
```

```bash
copilot

# Pattern: "Expected X but got Y"
> @samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.

# Pattern: "Unexpected behavior"
> @samples/book-app-buggy/book_app_buggy.py When I remove a book that doesn't exist, the app says it was removed. Help me find why.

# Pattern: "Wrong results"
> @samples/book-app-buggy/books_buggy.py When I mark one book as read, ALL books get marked. What's the bug?
```

💡 **Debugging tip**: Describe the symptom (what you see) and the expectation (what should happen). Copilot CLI figures out the rest.

### The "Bug Detective" — AI Finds RELATED Bugs

This is where context-aware debugging shines. Try this scenario with the buggy book app. Provide the whole file via `@` and describe only the user-reported symptom. Copilot CLI will trace the root cause and may spot additional bugs nearby.

```bash
copilot
> @samples/book-app-buggy/books_buggy.py
> Users report: "Finding books by author name doesn't work for partial names"
> Debug why this happens
```

Example output:

> ● Found the bug! On line 95, the `find_by_author` method uses exact equality (`==`) instead of checking if the search term is contained within the author name. This means searching for "Tolkien" won't match "J.R.R. Tolkien" or any partial author name.
>
> **The Issue:**
> ```python
> return [b for b in self.books if b.author == author]
> ```
>
> **The Fix:**
> Should use case-insensitive partial matching like:
> ```python
> return [b for b in self.books if author.lower() in b.author.lower()]
> ```
>
> This will allow:
> - "Tolkien" to match "J.R.R. Tolkien"
> - "rowling" to match "J.K. Rowling"
> - "king" to match "Stephen King"

Why this matters: Copilot CLI reads the whole file, understands the context of your bug report, and gives you a specific fix with a clear explanation.

💡 **Bonus**: Because Copilot CLI analyzes the entire file, it often discovers other issues you didn't ask about. For example, while fixing the author search, Copilot CLI might also notice the case-sensitivity bug in `find_book_by_title`!

### Real-World Security Sidebar

While debugging your own code is important, understanding security vulnerabilities in production applications is critical. Try this example: Point Copilot CLI at an unfamiliar file and ask it to audit for security issues.

```bash
copilot
> @samples/buggy-code/python/user_service.py Find all security vulnerabilities in this Python user service
```

This file demonstrates real-world security patterns you'll encounter in production apps.

💡 **Common security terms you'll encounter:**

- **SQL Injection**: When user input is put directly into a database query, allowing attackers to run malicious commands
- **Parameterized queries**: The safe alternative — placeholders (`?`) separate user data from SQL commands
- **Race condition**: When two operations happen at the same time and interfere with each other
- **XSS (Cross-Site Scripting)**: When attackers inject malicious scripts into web pages

### Understanding an Error

Paste a stack trace directly into your prompt along with an `@` file reference so Copilot CLI can map the error to the source code.

```bash
copilot
> I'm getting this error:
> AttributeError: 'NoneType' object has no attribute 'title'
>     at show_books (book_app.py:19)
>
> @samples/book-app-project/book_app.py Explain why and how to fix it
```

### Debugging with Test Case

Describe the exact input and observed output to give Copilot CLI a concrete, reproducible test case to reason about.

```bash
copilot
> @samples/book-app-buggy/books_buggy.py The remove_book function has a bug. When I try to remove "Dune",
> it also removes "Dune Messiah". Debug this: explain the root cause and provide a fix.
```

### Trace an Issue Through Code

Reference multiple files and ask Copilot CLI to follow the data flow across them to locate where the issue originates.

```bash
copilot
> Users report that the book list numbering starts at 0 instead of 1.
> @samples/book-app-buggy/book_app_buggy.py @samples/book-app-buggy/books_buggy.py
> Trace through the list display flow and identify where the issue occurs
```

### Understanding Data Issues

Include a data file alongside the code that reads it so Copilot CLI understands the full picture when suggesting error-handling improvements.

```bash
copilot
> @samples/book-app-project/data.json @samples/book-app-project/books.py
> Sometimes the JSON file gets corrupted and the app crashes. How should we handle this gracefully?
```

---

## Workflow 4: Test Generation

> Generate comprehensive tests and edge cases automatically

![Illustration of test generation workflow](images/test-generation.png)

Try this first:

```bash
copilot
> @samples/book-app-project/books.py Generate pytest tests for all functions including edge cases
```

### The "Test Explosion" — 2 Tests vs 15+ Tests

Manually writing tests, developers typically create 2-3 basic tests:

- Test valid input
- Test invalid input
- Test an edge case

Watch what happens when you ask Copilot CLI to generate comprehensive tests! This prompt uses a structured bullet list with an `@` file reference to guide Copilot CLI toward thorough test coverage:

```bash
copilot
> @samples/book-app-project/books.py Generate comprehensive pytest tests. Include tests for:
> - Adding books
> - Removing books
> - Finding by title
> - Finding by author
> - Marking as read
> - Edge cases with empty data
```

### Unit Tests

Target a single function and enumerate the input categories you want tested so Copilot CLI generates focused, thorough unit tests.

```bash
copilot
> @samples/book-app-project/utils.py Generate comprehensive pytest tests for get_book_details covering:
> - Valid input
> - Empty strings
> - Invalid year formats
> - Very long titles
> - Special characters in author names
```

### Running Tests

Ask Copilot CLI a plain-English question about your toolchain. It can generate the right shell command for you.

```bash
copilot
> How do I run the tests? Show me the pytest command.

# Copilot CLI responds:
# cd samples/book-app-project && python -m pytest tests/
# Or for verbose output: python -m pytest tests/ -v
# To see print statements: python -m pytest tests/ -s
```

### Test for Specific Scenarios

List advanced or tricky scenarios you want covered so Copilot CLI goes beyond the happy path.

```bash
copilot
> @samples/book-app-project/books.py Generate tests for these scenarios:
> - Adding duplicate books (same title and author)
> - Removing a book by partial title match
> - Finding books when collection is empty
> - File permission errors during save
> - Concurrent access to the book collection
```

### Add Tests to Existing File

Ask for additional tests for a single function so Copilot CLI generates new cases that complement what you already have.

```bash
copilot
> @samples/book-app-project/books.py
> Generate additional tests for the find_by_author function with edge cases:
> - Author name with hyphens (e.g., "Jean-Paul Sartre")
> - Author with multiple first names
> - Empty string as author
> - Author name with accented characters
```

---

## Workflow 5: Git Integration

> Commit messages, PR descriptions, `/pr`, `/delegate`, and `/diff`

![Illustration of Git integration workflow](images/git-integration.png)

💡 **Note**: This workflow assumes basic git familiarity (staging, committing, branches). If git is new to you, try the other four workflows first.

### Generate Commit Messages

Try this first: `copilot -p "Generate a conventional commit message for: $(git diff --staged)"` — stage some changes, then run this to see Copilot CLI write your commit message.

```bash
# See what changed
git diff --staged

# Generate commit message using Conventional Commit format
# (structured messages like "feat(books): add search" or "fix(data): handle empty input")
copilot -p "Generate a conventional commit message for: $(git diff --staged)"

# Output: "feat(books): add partial author name search
#
# - Update find_by_author to support partial matches
# - Add case-insensitive comparison
# - Improve user experience when searching authors"
```

### Explain Changes

Pipe the output of `git show` into a `-p` prompt to get a plain-English summary of the last commit.

```bash
# What did this commit change?
copilot -p "Explain what this commit does: $(git show HEAD --stat)"
```

### PR Description

Combine `git log` output with a structured prompt template to auto-generate a complete pull request description.

```bash
# Generate PR description from branch changes
copilot -p "Generate a pull request description for these changes:
$(git log main..HEAD --oneline)

Include:
- Summary of changes
- Why these changes were made
- Testing done
- Breaking changes? (yes/no)"
```

### Using `/pr` in Interactive Mode

If you're working with a branch in Copilot CLI's interactive mode, you can use the `/pr` command to work with pull requests:

```bash
copilot

# View a PR:
> /pr view

# Create a PR:
> /pr create

# Fix an existing PR:
> /pr fix

# Let Copilot decide:
> /pr auto
```

### Review Before Push

Use `git diff main..HEAD` inside a `-p` prompt for a quick pre-push sanity check across all branch changes.

```bash
# Last check before pushing
copilot -p "Review these changes for issues before I push:
$(git diff main..HEAD)"
```

### Using `/delegate` for Background Tasks

The `/delegate` command hands off work to the GitHub Copilot cloud agent. Use the `/delegate` slash command (or the `&` shortcut) to offload a well-defined task to a background agent.

```bash
copilot
> /delegate Add input validation to the login form

# Or use the & prefix shortcut:
> & Fix the typo in the README header

# Copilot CLI:
# 1. Commits your changes to a new branch
# 2. Opens a draft pull request
# 3. Works in the background on GitHub
# 4. Requests your review when done
```

This is great for well-defined tasks you want completed while you focus on other work.

### Using `/diff` to Review Session Changes

The `/diff` command shows all changes made during your current session. Use this slash command to see a visual diff of everything Copilot CLI has modified before you commit.

```bash
copilot

# After making some changes...
> /diff

# Shows a visual diff of all files modified in this session
# Great for reviewing before committing
```

---

## Quick Tip: Research Before You Plan or Code

When you need to investigate a library, understand best practices, or explore an unfamiliar topic, use `/research` to run a deep research investigation before writing any code:

```bash
copilot
> /research What are the best Python libraries for validating user input in CLI apps?
```

Copilot searches GitHub repositories and web sources, then returns a summary with references. This is useful when you're about to start a new feature and want to make informed decisions first. You can share the results using `/share`.

💡 **Tip**: `/research` works well before `/plan`. Research the approach, then plan the implementation.

---

## Putting It All Together: Bug Fix Workflow

Here's a complete workflow for fixing a reported bug:

```bash
# 1. Understand the bug report
copilot
> Users report: 'Finding books by author name doesn't work for partial names'
> @samples/book-app-project/books.py Analyze and identify the likely cause

# 2. Debug the issue and fix (continuing in same session)
> Based on the analysis, show me the find_by_author function and explain the issue
> Fix the find_by_author function to handle partial name matches

# 3. Generate tests for the fix
> @samples/book-app-project/books.py Generate pytest tests specifically for:
> - Full author name match
> - Partial author name match
> - Case-insensitive matching
> - Author name not found

# Exit the interactive session
> /exit

# 4. Stage the changes so git diff --staged has something to work with
git add .

# 5. Generate commit message
copilot -p "Generate commit message for: $(git diff --staged)"
# Example Output: "fix(books): support partial author name search"

# 6. Commit changes (optional)
git commit -m "<paste generated message>"
```

### Bug Fix Workflow Summary

| Step | Action | Copilot Command |
|------|--------|-----------------|
| 1 | Understand the bug | `> [describe bug] @relevant-file.py Analyze the likely cause` |
| 2 | Analysis and fix | `> Show me the function and fix the issue` |
| 3 | Generate tests | `> Generate tests for [specific scenarios]` |
| 4 | Stage changes | `git add .` |
| 5 | Generate commit message | `copilot -p "Generate commit message for: $(git diff --staged)"` |
| 6 | Commit changes | `git commit -m "<paste generated message>"` |

---

## 🔑 Key Takeaways

- Code review becomes comprehensive with specific prompts
- Refactoring is safer when you generate tests first
- Debugging benefits from showing Copilot CLI the error AND the code
- Test generation should include edge cases and error scenarios
- Git integration automates commit messages and PR descriptions
