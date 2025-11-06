# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-06

### Added
- Initial release of WordPress MCP Server
- Complete MCP server implementation for WordPress REST API
- 8 core tools for WordPress management:
  - `create_post` - Create new posts with full metadata
  - `update_post` - Update existing posts
  - `get_post` - Get post details by ID
  - `list_posts` - List posts with filtering
  - `delete_post` - Delete or trash posts
  - `list_categories` - List all categories
  - `list_tags` - List all tags
  - `upload_media` - Upload media files
- Docker containerization with Dockerfile and docker-compose.yml
- Complete documentation (README, CONTRIBUTING, PROJECT_STRUCTURE)
- GitHub Actions CI/CD workflow
- MIT License
- Example configuration files
- Support for Claude Desktop integration

### Features
- WordPress Application Password authentication
- Full post metadata support (categories, tags, featured images, excerpts)
- Draft and publish post statuses
- Post search and filtering
- Error handling and user-friendly messages
- Environment variable configuration

### Documentation
- Comprehensive README with setup instructions
- Usage examples for common workflows
- Troubleshooting guide
- Contributing guidelines
- Project structure documentation
- Claude Desktop integration guide

[1.0.0]: https://github.com/SixFiveMil/wp-mcp-server/releases/tag/v1.0.0