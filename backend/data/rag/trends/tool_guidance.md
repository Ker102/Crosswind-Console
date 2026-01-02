# Trends Tool Guidance

Use this document to determine which tool to use for social trends queries.

## Social/Trends Tools

| User Query Pattern | Tool to Use | Key Parameters |
|-------------------|-------------|----------------|
| "Trending topics on X" | `get_twitter_trends` | location |
| "Popular hashtags" | `search_hashtags` | query, platform |
| "Social media analytics" | `get_analytics` | platform, handle |

## Intent Mapping

When the user says:
- **"Twitter" or "X"** → platform=twitter
- **"Instagram"** → platform=instagram
- **"LinkedIn"** → platform=linkedin
- **"viral"** → sort by engagement

## Placeholder

> **Note**: Add more social/trends API parameter guidance here as you integrate trends-related MCP tools.
