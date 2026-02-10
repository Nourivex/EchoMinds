# Contributing to EchoMinds 🤝

Thank you for your interest in contributing to EchoMinds! This document provides guidelines for contributing to the project.

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing Requirements](#testing-requirements)

---

## 🤝 Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior
- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior
- Harassment or discriminatory language
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

---

## 🚀 Getting Started

### Prerequisites
- Node.js 20+ & npm
- Python 3.11+
- Git
- Ollama (for LLM testing)

### Setup Development Environment

```bash
# Fork and clone repository
git clone https://github.com/YOUR_USERNAME/EchoMinds.git
cd EchoMinds

# Install dependencies
npm install
cd backend && pip install -r requirements.txt && cd ..

# Create feature branch
git checkout -b feature/your-feature-name
```

---

## 🔄 Development Process

### 1. Find or Create an Issue
- Check [existing issues](https://github.com/Nourivex/EchoMinds/issues)
- Create new issue if needed with clear description
- Wait for maintainer approval before starting work

### 2. Branch Naming Convention
```
feature/description    # New features
fix/description        # Bug fixes
docs/description       # Documentation updates
refactor/description   # Code refactoring
test/description       # Test additions
chore/description      # Build/config changes
```

### 3. Make Changes
- Write clean, readable code
- Follow coding standards (see below)
- Add tests for new features
- Update documentation as needed

### 4. Test Your Changes
```bash
# Frontend tests
npm run test
npm run type-check

# Backend tests
cd backend
pytest
mypy .
```

---

## 📝 Coding Standards

### Frontend (TypeScript/Svelte)

**Style Guide:**
- Use TypeScript strict mode
- Prefer `const` over `let`
- Use Svelte 5 Runes (`$state`, `$derived`, `$effect`)
- Component naming: PascalCase (e.g., `ChatInterface.svelte`)
- File naming: kebab-case for utilities (e.g., `api-client.ts`)

**Example:**
```typescript
// ✅ Good
interface Props {
  message: string;
  onSend: (text: string) => void;
}

let { message, onSend }: Props = $props();
let inputValue = $state('');

// ❌ Bad
let message: any;
var inputValue = '';
```

**ESLint & Prettier:**
```bash
npm run lint        # Check issues
npm run lint:fix    # Auto-fix
npm run format      # Format code
```

---

### Backend (Python/FastAPI)

**Style Guide:**
- Follow PEP 8
- Use type hints everywhere
- Docstrings for all public functions
- Async/await for I/O operations
- Pydantic models for validation

**Example:**
```python
# ✅ Good
async def generate_response(
    message: str,
    character_id: str,
    user_id: str
) -> ChatResponse:
    """Generate AI response with RAG context.
    
    Args:
        message: User input message
        character_id: Character identifier
        user_id: User identifier
        
    Returns:
        ChatResponse with AI reply and context
    """
    # Implementation...

# ❌ Bad
def generate_response(message, character_id, user_id):
    # No types, no docstring
    pass
```

**Code Formatting:**
```bash
# Format with black
black backend/

# Sort imports
isort backend/

# Type checking
mypy backend/
```

---

## 📜 Commit Guidelines

### Conventional Commits Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style (formatting, no logic change)
- `refactor`: Code restructuring
- `test`: Adding/updating tests
- `chore`: Build/config changes

### Examples
```bash
# Feature
feat(chat): add typing indicator to chat interface

Implement real-time typing indicator that shows when
AI is generating a response.

# Bug fix
fix(theme): resolve theme persistence issue on page reload

Theme was not loading from localStorage correctly due to
timing issue. Now initializes in main.ts before app mount.

# Documentation
docs(api): add endpoint documentation for chat API
```

### Commit Message Rules
- Use imperative mood ("add" not "added")
- First line max 72 characters
- Reference issue numbers when applicable
- Explain **why** not just **what**

---

## 🔀 Pull Request Process

### 1. Before Creating PR

```bash
# Update your branch with latest main
git checkout main
git pull upstream main
git checkout your-feature-branch
git rebase main

# Run all tests
npm run test
cd backend && pytest && cd ..

# Check for linting issues
npm run lint
black backend/ --check
```

### 2. Create Pull Request

**PR Title Format:**
```
<type>: <short description>

Example: feat: implement RAG-based character memory
```

**PR Description Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] No console errors

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
```

### 3. Review Process
- At least 1 maintainer approval required
- All CI checks must pass
- Address review comments promptly
- Keep PR focused and reasonably sized

### 4. After Merge
```bash
# Update your local main
git checkout main
git pull upstream main

# Delete feature branch
git branch -d your-feature-branch
git push origin --delete your-feature-branch
```

---

## 🧪 Testing Requirements

### Frontend Tests
```bash
# Run all tests
npm run test

# Watch mode
npm run test:watch

# Coverage
npm run test:coverage
```

**Required Coverage:**
- Components: > 80%
- Utilities: > 90%
- Services: > 85%

### Backend Tests
```bash
# Run all tests
pytest

# With coverage
pytest --cov=backend --cov-report=html

# Specific test file
pytest tests/test_chat_service.py -v
```

**Required Coverage:**
- Services: > 90%
- API routes: > 85%
- Models: > 95%

### Manual Testing Checklist
- [ ] Theme toggle works (light ↔ dark)
- [ ] Sidebar collapsible on mobile
- [ ] Chat interface responsive
- [ ] All navigation links work
- [ ] No console errors
- [ ] Backend health endpoint returns 200

---

## 🐛 Reporting Bugs

### Bug Report Template
```markdown
**Describe the bug**
Clear description of the issue

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What should happen

**Screenshots**
If applicable

**Environment:**
- OS: [e.g., Windows 11]
- Browser: [e.g., Chrome 120]
- Node version: [e.g., 20.10]
- Python version: [e.g., 3.11.5]

**Additional context**
Any other relevant information
```

---

## 💡 Feature Requests

### Feature Request Template
```markdown
**Is your feature request related to a problem?**
Clear description of the problem

**Describe the solution**
What you'd like to happen

**Describe alternatives**
Alternative solutions you've considered

**Additional context**
Mockups, examples, or references
```

---

## 📞 Questions & Support

- **General Questions:** [GitHub Discussions](https://github.com/Nourivex/EchoMinds/discussions)
- **Bug Reports:** [GitHub Issues](https://github.com/Nourivex/EchoMinds/issues)
- **Feature Requests:** [GitHub Issues](https://github.com/Nourivex/EchoMinds/issues) with `enhancement` label

---

## 🎉 Recognition

Contributors will be recognized in:
- [CONTRIBUTORS.md](CONTRIBUTORS.md) file
- Release notes for significant contributions
- Special mentions in project updates

---

## 📝 License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

**Thank you for contributing to EchoMinds! 💜**
