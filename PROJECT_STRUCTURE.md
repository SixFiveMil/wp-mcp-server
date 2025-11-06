# WordPress MCP Server - Project Structure

## 📁 Complete File Structure

```
wp-mcp-server/
├── .github/
│   └── workflows/
│       └── docker-build.yml            # GitHub Actions CI/CD
├── server.py                           # Main MCP server implementation
├── Dockerfile                          # Docker container configuration
├── docker-compose.yml                  # Docker Compose setup
├── requirements.txt                    # Python dependencies
├── .gitignore                          # Git ignore rules
├── .env.example                        # Environment variables template
├── LICENSE                             # MIT License
├── README.md                           # Main documentation
├── CONTRIBUTING.md                     # Contribution guidelines
├── PROJECT_STRUCTURE.md                # This file
└── claude_desktop_config.example.json  # Claude Desktop config template
```

## 📄 File Descriptions

### Core Files

- **server.py**: The main MCP server that handles communication with WordPress REST API
- **Dockerfile**: Defines the Docker image for the MCP server
- **docker-compose.yml**: Simplifies running the server with Docker Compose
- **requirements.txt**: Lists Python package dependencies

### Configuration Files

- **.env.example**: Template for environment variables (copy to .env)
- **claude_desktop_config.example.json**: Example Claude Desktop configuration
- **.gitignore**: Prevents sensitive files from being committed

### Documentation

- **README.md**: Main project documentation with setup instructions
- **CONTRIBUTING.md**: Guidelines for contributors
- **PROJECT_STRUCTURE.md**: This file - explains the project organization
- **LICENSE**: MIT License text

### Automation

- **.github/workflows/docker-build.yml**: GitHub Actions workflow for automated testing

## 🚀 Setup Order

1. Clone/download all files into a directory
2. Copy `.env.example` to `.env` and configure
3. Build Docker image: `docker build -t wordpress-mcp-server .`
4. Test the server
5. Configure Claude Desktop (optional)

## 🔧 Customization

### Adding New Tools

Edit `server.py` and add to the `handle_list_tools()` and `handle_call_tool()` functions.

### Modifying Docker Configuration

Edit `Dockerfile` or `docker-compose.yml` to change container settings.

### Updating Dependencies

Add packages to `requirements.txt` and rebuild the Docker image.

## 📦 Distribution

When sharing this project:
1. Ensure no sensitive data in any files
2. All example files should have `.example` extension
3. README should be clear and comprehensive
4. Include proper attribution in LICENSE