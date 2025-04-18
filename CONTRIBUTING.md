# Contributing to GIST

We're thrilled you're interested in contributing to GIST. Whether you're fixing a bug, adding a feature, or improving our docs, every contribution makes GIST better! To keep our community vibrant and welcoming, all members must adhere to our Code of Conduct.

## Setting Up Locally

There are two ways to set up GIST locally:

### Quick Setup

Use our automated setup script:
```bash
chmod -x start-local.sh
```

```bash
./start-local.sh
```

This script will set up the project with lightning speed, installing all dependencies and configuring your environment.

### Manual Setup

If you prefer setting up manually:

1. **Frontend (Web)**
   ```bash
   pnpm install
   pnpm dev
   ```

2. **Backend (Server)**
   ```bash
   uv venv
   source .venv/bin/activate
   uv sync
   fastapi dev
   ```

### Environment Variables

All required environment variables are documented in [Documentation/environment-variables.md](Documentation/environment-variables.md). Make sure to set these up before running the project.

<blockquote class='warning-note'>
     🔐 <b>Important:</b> Never commit sensitive environment variables to the repository.
</blockquote>

## Development Guidelines

### Code Quality
- Run linting tools before submitting your code
- Follow existing code style and patterns
- Write tests for new features
- Ensure all tests pass before submitting

### Pull Request Process

1. **Keep Pull Requests Focused**
   - Limit PRs to a single feature or bug fix
   - Split larger changes into smaller, related PRs

2. **Before Submitting**
   - Ensure your branch builds successfully
   - Make sure all tests are passing
   - Review your changes for any debugging code or console logs

3. **Pull Request Description**
   - Clearly describe what your changes do
   - Include steps to test the changes
   - Add screenshots for UI changes

## Reporting Bugs or Issues

Bug reports help make GIST better for everyone! When reporting issues, please include:
- Steps to reproduce the bug
- Expected behavior
- Actual behavior
- Environment details (browser, OS, etc.)
- Screenshots if applicable

## Contribution Agreement

By submitting a pull request, you agree that your contributions will be licensed under the same license as the project.

Remember: Contributing to GIST isn't just about writing code - it's about being part of a community that's shaping something meaningful. Let's build something amazing together! 🚀 