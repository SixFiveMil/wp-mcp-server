# Contributing to WordPress MCP Server

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/SixFiveMil/wp-mcp-server/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Docker version, WordPress version)
   - Any relevant logs or screenshots

### Suggesting Features

1. Check [Issues](https://github.com/SixFiveMil/wp-mcp-server/issues) for existing feature requests
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach (optional)

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test thoroughly
5. Commit with clear messages: `git commit -m 'Add amazing feature'`
6. Push to your fork: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Development Guidelines

- Follow existing code style and conventions
- Add comments for complex logic
- Update documentation as needed
- Test your changes with a real WordPress site
- Ensure no sensitive data is committed

### Testing

Before submitting a PR:

```bash
# Test the Docker build
docker build -t wordpress-mcp-server-test .

# Test with your WordPress site
docker run -i --rm \
  -e WORDPRESS_URL=https://your-test-site.com \
  -e WORDPRESS_USERNAME=test-user \
  -e WORDPRESS_APP_PASSWORD=test-password \
  wordpress-mcp-server-test
```

## Questions?

Feel free to open a [Discussion](https://github.com/SixFiveMil/wp-mcp-server/discussions) if you have questions!