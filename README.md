# WordPress MCP Server 📝

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

A Model Context Protocol (MCP) server for WordPress that enables Claude AI to create, update, and manage WordPress blog posts via the WordPress REST API.

## ✨ Features

- 📄 Create new posts (draft or published)
- ✏️ Update existing posts
- 📋 List posts with filtering
- 🔍 Get post details
- 🗑️ Delete posts
- 🏷️ List categories and tags
- 🖼️ Upload media files
- 🎯 Full support for post metadata (categories, tags, featured images, excerpts)

## 🚀 Quick Start

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed
- WordPress site with REST API enabled (default in WordPress 4.7+)
- WordPress Application Password
- [Claude Desktop](https://claude.ai/download) (optional, for integration)

### 1. Generate WordPress Application Password

1. Log into your WordPress admin dashboard
2. Navigate to **Users → Profile**
3. Scroll to **Application Passwords** section
4. Enter a name (e.g., "MCP Server")
5. Click **Add New Application Password**
6. **Copy the generated password** (you won't see it again!)

### 2. Clone and Build

```bash
# Clone the repository
git clone https://github.com/SixFiveMil/wp-mcp-server.git
cd wp-mcp-server

# Build the Docker image
docker build -t wordpress-mcp-server .
```

### 3. Configure Environment

Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
WORDPRESS_URL=https://your-site.com
WORDPRESS_USERNAME=your-username
WORDPRESS_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx-xxxx-xxxx
```

### 4. Test the Server

```bash
docker run -i --rm \
  -e WORDPRESS_URL=https://your-site.com \
  -e WORDPRESS_USERNAME=your-username \
  -e WORDPRESS_APP_PASSWORD=your-app-password \
  wordpress-mcp-server
```

Or use docker-compose:

```bash
# Edit docker-compose.yml with your credentials first
docker-compose up
```

## 🔧 Claude Desktop Integration

### Installation

1. Locate your Claude Desktop config file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. Add the WordPress MCP server configuration:

```json
{
  "mcpServers": {
    "wordpress": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e", "WORDPRESS_URL=https://your-site.com",
        "-e", "WORDPRESS_USERNAME=your-username",
        "-e", "WORDPRESS_APP_PASSWORD=your-app-password",
        "wordpress-mcp-server"
      ]
    }
  }
}
```

3. Restart Claude Desktop

## 📚 Usage Examples

Once configured, you can use Claude to interact with your WordPress site:

### Create a Draft Post
```
Create a draft blog post titled "My First Post" with the content "Hello World!"
```

### Publish a Post
```
Create a published post titled "Announcing Our New Product" with this content: [your content]
```

### List Recent Posts
```
Show me the 5 most recent posts from my WordPress site
```

### Update a Post
```
Update post ID 123 to change the status to published
```

### Work with Categories
```
List all categories on my WordPress site
```

### Upload an Image
```
Upload the image at /path/to/image.jpg to WordPress
```

## 🛠️ Available Tools

| Tool | Description |
|------|-------------|
| `create_post` | Create new WordPress posts with full metadata support |
| `update_post` | Update existing posts |
| `get_post` | Get details of a specific post by ID |
| `list_posts` | List posts with filtering options (status, search, pagination) |
| `delete_post` | Delete or trash posts |
| `list_categories` | List all available categories |
| `list_tags` | List all available tags |
| `upload_media` | Upload media files to WordPress |

## 📖 API Documentation

### create_post

```json
{
  "title": "Post Title",
  "content": "Post content in HTML or plain text",
  "status": "draft|publish|pending|private",
  "excerpt": "Optional excerpt",
  "categories": [1, 2, 3],
  "tags": [4, 5, 6],
  "featured_media": 123
}
```

### update_post

```json
{
  "post_id": 123,
  "title": "Updated Title",
  "content": "Updated content",
  "status": "publish"
}
```

### list_posts

```json
{
  "per_page": 10,
  "page": 1,
  "status": "any|publish|draft|pending|private",
  "search": "search term"
}
```

## 🔒 Security Notes

- ⚠️ **Never commit your Application Password** to version control
- ✅ Use environment variables or secrets management
- 🔑 Application Passwords can be revoked anytime from WordPress profile
- 🛡️ The REST API respects your WordPress user permissions
- 🔐 Use HTTPS for your WordPress site in production

## 🐛 Troubleshooting

### Authentication Errors
- Verify your Application Password is correct (spaces are automatically removed)
- Ensure your WordPress user has permission to create/edit posts
- Check that REST API is enabled on your WordPress site

### Connection Errors
- Verify the WordPress URL is correct and accessible
- Ensure your WordPress site uses HTTPS
- Check if there's a firewall blocking the connection
- Confirm the WordPress REST API endpoint is accessible at `/wp-json/wp/v2/`

### Docker Issues
- Ensure Docker is running: `docker ps`
- Verify the image built successfully: `docker images | grep wordpress-mcp`
- Check Docker logs: `docker logs wordpress-mcp-server`
- Try rebuilding: `docker build --no-cache -t wordpress-mcp-server .`

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit pull requests

### Development Setup

```bash
# Clone the repo
git clone https://github.com/SixFiveMil/wp-mcp-server.git
cd wp-mcp-server

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests (if available)
pytest
```

## 🗺️ Roadmap

Future features under consideration:

- [ ] Support for custom post types
- [ ] Custom fields management
- [ ] Comments management
- [ ] User management
- [ ] Bulk operations
- [ ] Media gallery management
- [ ] SEO metadata support (Yoast, RankMath)
- [ ] Multisite support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- Powered by [WordPress REST API](https://developer.wordpress.org/rest-api/)
- Made for [Claude by Anthropic](https://claude.ai/)

## 📞 Support

- 📧 Issues: [GitHub Issues](https://github.com/SixFiveMil/wp-mcp-server/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/SixFiveMil/wp-mcp-server/discussions)
- 📖 Documentation: [Wiki](https://github.com/SixFiveMil/wp-mcp-server/wiki)

---

**Made with ❤️ for the WordPress and AI community**