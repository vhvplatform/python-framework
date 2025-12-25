# Contributing to SaaS Framework Python

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/saas-framework-python.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests: `pytest`
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

```bash
# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run linting
ruff check src/ tests/

# Run type checking
mypy src/
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Write Google-style docstrings
- Maximum line length: 100 characters
- Use `ruff` for formatting and linting
- Pass `mypy` strict mode checks

## Testing Requirements

- Write tests for all new features
- Maintain >90% test coverage
- Include both unit and integration tests
- Use meaningful test names that describe what is being tested
- Mock external dependencies appropriately

## Commit Message Guidelines

Use conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```
feat(core): add service discovery mechanism

Implements a service registry pattern for microservice discovery.
Includes health checking and metadata tracking.

Closes #123
```

## Pull Request Process

1. Update documentation for any changed functionality
2. Add tests for new features
3. Ensure all tests pass
4. Update the README.md if needed
5. Request review from maintainers
6. Address review feedback
7. Wait for approval and merge

## Code Review Guidelines

Reviewers will check for:

- Code quality and style
- Test coverage
- Documentation completeness
- Type safety
- Performance implications
- Security considerations
- Breaking changes

## Reporting Issues

When reporting issues, please include:

- Python version
- Framework version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages or logs

## Feature Requests

For feature requests:

- Check if the feature already exists
- Explain the use case
- Describe the proposed solution
- Discuss alternatives considered
- Provide examples if possible

## Questions?

- Open a GitHub Discussion
- Create an issue with the "question" label
- Check existing documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to SaaS Framework Python! 🚀
