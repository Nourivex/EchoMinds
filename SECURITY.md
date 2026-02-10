# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please follow these steps:

### 1. **Do NOT** create a public issue

Please do not report security vulnerabilities through public GitHub issues.

### 2. Report privately

Send an email to: **security@echominds.dev**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if available)

### 3. Response Timeline

- **Initial Response:** Within 48 hours
- **Status Update:** Within 7 days
- **Fix Timeline:** Depends on severity

### 4. Disclosure Policy

- We will acknowledge receipt of your vulnerability report
- We will confirm the vulnerability and determine its impact
- We will release a fix as soon as possible
- We will publicly disclose the vulnerability after a fix is released

## Security Best Practices

### For Users

1. **Keep Dependencies Updated**
   ```bash
   npm update
   pip install --upgrade -r backend/requirements.txt
   ```

2. **Use Environment Variables**
   - Never commit `.env` files
   - Use strong API keys
   - Rotate credentials regularly

3. **Network Security**
   - Run backend on localhost for local development
   - Use HTTPS in production
   - Configure CORS properly

4. **Model Safety**
   - Only use trusted LLM models
   - Review model outputs
   - Implement content filtering if needed

### For Developers

1. **Input Validation**
   - Always validate user input
   - Use Pydantic models for API validation
   - Sanitize strings before storage

2. **Authentication**
   - Implement proper authentication before production
   - Use secure session management
   - Hash passwords with bcrypt

3. **Dependencies**
   - Regularly update dependencies
   - Use `npm audit` and `pip-audit`
   - Pin versions in production

4. **Code Review**
   - Review all PRs for security issues
   - Check for exposed secrets
   - Validate error handling

## Known Security Considerations

### Local LLM Privacy
- All data stays local by default
- No external API calls (unless configured)
- User conversations are not transmitted

### Vector Database
- ChromaDB stores embeddings locally
- No data leaves your machine
- Clear data with `clear_conversation()` API

### API Security
- FastAPI backend runs locally
- CORS configured for localhost
- Add authentication before exposing publicly

## Security Updates

Security updates will be released as:
- Patch versions (1.0.x) for minor security fixes
- Minor versions (1.x.0) for moderate security fixes
- Major versions (x.0.0) for critical security fixes

## Attribution

We appreciate security researchers who help keep EchoMinds safe. With your permission, we will acknowledge your contribution in our release notes.

---

**Last Updated:** February 10, 2026
