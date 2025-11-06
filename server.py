import os
import asyncio
from typing import Any
import httpx
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from base64 import b64encode

# WordPress configuration from environment variables
WP_URL = os.getenv("WORDPRESS_URL", "")
WP_USERNAME = os.getenv("WORDPRESS_USERNAME", "")
WP_PASSWORD = os.getenv("WORDPRESS_APP_PASSWORD", "")

# Create auth header
def get_auth_header():
    credentials = f"{WP_USERNAME}:{WP_PASSWORD}"
    token = b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {token}"}

server = Server("wordpress-mcp")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available WordPress tools."""
    return [
        types.Tool(
            name="create_post",
            description="Create a new WordPress post. Can be published immediately or saved as draft.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Post title"
                    },
                    "content": {
                        "type": "string",
                        "description": "Post content (HTML or plain text)"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["publish", "draft", "pending", "private"],
                        "description": "Post status (default: draft)",
                        "default": "draft"
                    },
                    "excerpt": {
                        "type": "string",
                        "description": "Post excerpt (optional)"
                    },
                    "categories": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "Array of category IDs (optional)"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "Array of tag IDs (optional)"
                    },
                    "featured_media": {
                        "type": "integer",
                        "description": "Featured image ID (optional)"
                    }
                },
                "required": ["title", "content"]
            }
        ),
        types.Tool(
            name="update_post",
            description="Update an existing WordPress post.",
            inputSchema={
                "type": "object",
                "properties": {
                    "post_id": {
                        "type": "integer",
                        "description": "ID of the post to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New post title (optional)"
                    },
                    "content": {
                        "type": "string",
                        "description": "New post content (optional)"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["publish", "draft", "pending", "private"],
                        "description": "New post status (optional)"
                    },
                    "excerpt": {
                        "type": "string",
                        "description": "New post excerpt (optional)"
                    }
                },
                "required": ["post_id"]
            }
        ),
        types.Tool(
            name="get_post",
            description="Get details of a specific WordPress post by ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "post_id": {
                        "type": "integer",
                        "description": "ID of the post to retrieve"
                    }
                },
                "required": ["post_id"]
            }
        ),
        types.Tool(
            name="list_posts",
            description="List WordPress posts with optional filtering.",
            inputSchema={
                "type": "object",
                "properties": {
                    "per_page": {
                        "type": "integer",
                        "description": "Number of posts per page (default: 10, max: 100)",
                        "default": 10
                    },
                    "page": {
                        "type": "integer",
                        "description": "Page number (default: 1)",
                        "default": 1
                    },
                    "status": {
                        "type": "string",
                        "enum": ["publish", "draft", "pending", "private", "any"],
                        "description": "Filter by post status (default: any)"
                    },
                    "search": {
                        "type": "string",
                        "description": "Search term to filter posts"
                    }
                }
            }
        ),
        types.Tool(
            name="delete_post",
            description="Delete a WordPress post (moves to trash or permanently deletes).",
            inputSchema={
                "type": "object",
                "properties": {
                    "post_id": {
                        "type": "integer",
                        "description": "ID of the post to delete"
                    },
                    "force": {
                        "type": "boolean",
                        "description": "Whether to permanently delete (true) or move to trash (false)",
                        "default": False
                    }
                },
                "required": ["post_id"]
            }
        ),
        types.Tool(
            name="list_categories",
            description="List all WordPress categories.",
            inputSchema={
                "type": "object",
                "properties": {
                    "per_page": {
                        "type": "integer",
                        "description": "Number of categories per page (default: 100)",
                        "default": 100
                    }
                }
            }
        ),
        types.Tool(
            name="list_tags",
            description="List all WordPress tags.",
            inputSchema={
                "type": "object",
                "properties": {
                    "per_page": {
                        "type": "integer",
                        "description": "Number of tags per page (default: 100)",
                        "default": 100
                    }
                }
            }
        ),
        types.Tool(
            name="upload_media",
            description="Upload a media file to WordPress. Note: This expects a file path or URL.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Local file path to upload"
                    },
                    "title": {
                        "type": "string",
                        "description": "Media title (optional)"
                    },
                    "alt_text": {
                        "type": "string",
                        "description": "Alternative text for the image (optional)"
                    }
                },
                "required": ["file_path"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests."""
    
    if not WP_URL or not WP_USERNAME or not WP_PASSWORD:
        return [types.TextContent(
            type="text",
            text="Error: WordPress credentials not configured. Please set WORDPRESS_URL, WORDPRESS_USERNAME, and WORDPRESS_APP_PASSWORD environment variables."
        )]
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            headers = get_auth_header()
            base_url = WP_URL.rstrip("/") + "/wp-json/wp/v2"
            
            if name == "create_post":
                data = {
                    "title": arguments.get("title"),
                    "content": arguments.get("content"),
                    "status": arguments.get("status", "draft"),
                }
                
                if "excerpt" in arguments:
                    data["excerpt"] = arguments["excerpt"]
                if "categories" in arguments:
                    data["categories"] = arguments["categories"]
                if "tags" in arguments:
                    data["tags"] = arguments["tags"]
                if "featured_media" in arguments:
                    data["featured_media"] = arguments["featured_media"]
                
                response = await client.post(
                    f"{base_url}/posts",
                    json=data,
                    headers=headers
                )
                response.raise_for_status()
                result = response.json()
                
                return [types.TextContent(
                    type="text",
                    text=f"Post created successfully!\nID: {result['id']}\nTitle: {result['title']['rendered']}\nStatus: {result['status']}\nURL: {result['link']}"
                )]
            
            elif name == "update_post":
                post_id = arguments["post_id"]
                data = {}
                
                if "title" in arguments:
                    data["title"] = arguments["title"]
                if "content" in arguments:
                    data["content"] = arguments["content"]
                if "status" in arguments:
                    data["status"] = arguments["status"]
                if "excerpt" in arguments:
                    data["excerpt"] = arguments["excerpt"]
                
                response = await client.post(
                    f"{base_url}/posts/{post_id}",
                    json=data,
                    headers=headers
                )
                response.raise_for_status()
                result = response.json()
                
                return [types.TextContent(
                    type="text",
                    text=f"Post updated successfully!\nID: {result['id']}\nTitle: {result['title']['rendered']}\nStatus: {result['status']}\nURL: {result['link']}"
                )]
            
            elif name == "get_post":
                post_id = arguments["post_id"]
                response = await client.get(
                    f"{base_url}/posts/{post_id}",
                    headers=headers
                )
                response.raise_for_status()
                result = response.json()
                
                return [types.TextContent(
                    type="text",
                    text=f"Post Details:\nID: {result['id']}\nTitle: {result['title']['rendered']}\nStatus: {result['status']}\nDate: {result['date']}\nURL: {result['link']}\n\nContent Preview:\n{result['content']['rendered'][:500]}..."
                )]
            
            elif name == "list_posts":
                params = {
                    "per_page": arguments.get("per_page", 10),
                    "page": arguments.get("page", 1)
                }
                
                if "status" in arguments:
                    params["status"] = arguments["status"]
                if "search" in arguments:
                    params["search"] = arguments["search"]
                
                response = await client.get(
                    f"{base_url}/posts",
                    params=params,
                    headers=headers
                )
                response.raise_for_status()
                posts = response.json()
                
                posts_list = "\n\n".join([
                    f"ID: {post['id']}\nTitle: {post['title']['rendered']}\nStatus: {post['status']}\nDate: {post['date']}\nURL: {post['link']}"
                    for post in posts
                ])
                
                return [types.TextContent(
                    type="text",
                    text=f"Found {len(posts)} posts:\n\n{posts_list}"
                )]
            
            elif name == "delete_post":
                post_id = arguments["post_id"]
                force = arguments.get("force", False)
                
                response = await client.delete(
                    f"{base_url}/posts/{post_id}",
                    params={"force": force},
                    headers=headers
                )
                response.raise_for_status()
                
                action = "permanently deleted" if force else "moved to trash"
                return [types.TextContent(
                    type="text",
                    text=f"Post {post_id} has been {action} successfully."
                )]
            
            elif name == "list_categories":
                params = {"per_page": arguments.get("per_page", 100)}
                
                response = await client.get(
                    f"{base_url}/categories",
                    params=params,
                    headers=headers
                )
                response.raise_for_status()
                categories = response.json()
                
                cat_list = "\n".join([
                    f"ID: {cat['id']} - {cat['name']} (Slug: {cat['slug']}, Count: {cat['count']})"
                    for cat in categories
                ])
                
                return [types.TextContent(
                    type="text",
                    text=f"WordPress Categories:\n\n{cat_list}"
                )]
            
            elif name == "list_tags":
                params = {"per_page": arguments.get("per_page", 100)}
                
                response = await client.get(
                    f"{base_url}/tags",
                    params=params,
                    headers=headers
                )
                response.raise_for_status()
                tags = response.json()
                
                tag_list = "\n".join([
                    f"ID: {tag['id']} - {tag['name']} (Slug: {tag['slug']}, Count: {tag['count']})"
                    for tag in tags
                ])
                
                return [types.TextContent(
                    type="text",
                    text=f"WordPress Tags:\n\n{tag_list}"
                )]
            
            elif name == "upload_media":
                file_path = arguments["file_path"]
                
                # Read file
                with open(file_path, "rb") as f:
                    file_content = f.read()
                
                # Prepare headers
                filename = os.path.basename(file_path)
                upload_headers = {
                    **headers,
                    "Content-Disposition": f"attachment; filename={filename}"
                }
                
                response = await client.post(
                    f"{base_url}/media",
                    content=file_content,
                    headers=upload_headers
                )
                response.raise_for_status()
                result = response.json()
                
                # Update alt text if provided
                if "alt_text" in arguments:
                    await client.post(
                        f"{base_url}/media/{result['id']}",
                        json={"alt_text": arguments["alt_text"]},
                        headers=headers
                    )
                
                return [types.TextContent(
                    type="text",
                    text=f"Media uploaded successfully!\nID: {result['id']}\nTitle: {result['title']['rendered']}\nURL: {result['source_url']}"
                )]
            
            else:
                return [types.TextContent(
                    type="text",
                    text=f"Unknown tool: {name}"
                )]
                
    except httpx.HTTPStatusError as e:
        return [types.TextContent(
            type="text",
            text=f"HTTP Error: {e.response.status_code}\n{e.response.text}"
        )]
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="wordpress-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())