from typing import Any, List, Dict, Optional
import asyncio
import logging
from mcp.server.fastmcp import FastMCP
from search import AuthorSearchEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("authorProfile")

# Initialize search engine
search_engine = AuthorSearchEngine()

@mcp.tool()
async def get_coauthors(
    name: str,
    surname: str,
    institution: Optional[str] = None,
    field: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get all co-authors for a given author.
    
    Args:
        name: Author's first name
        surname: Author's last name
        institution: Optional institution affiliation
        field: Optional research field
    
    Returns:
        Dictionary containing co-authors list with their information
    """
    try:
        logger.info(f"Searching co-authors for {name} {surname}")
        
        # Search for author and get co-authors
        coauthors = await search_engine.get_coauthors(
            name=name,
            surname=surname,
            institution=institution,
            field=field
        )
        
        return {
            "success": True,
            "author": f"{name} {surname}",
            "institution": institution,
            "total_coauthors": len(coauthors),
            "coauthors": coauthors
        }
        
    except Exception as e:
        logger.error(f"Error getting co-authors: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "coauthors": []
        }

@mcp.tool()
async def get_author_keywords(
    name: str,
    surname: str,
    institution: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get research keywords/areas for a given author.
    
    Args:
        name: Author's first name
        surname: Author's last name
        institution: Optional institution affiliation
    
    Returns:
        Dictionary containing keywords with frequencies
    """
    try:
        logger.info(f"Searching keywords for {name} {surname}")
        
        keywords = await search_engine.get_author_keywords(
            name=name,
            surname=surname,
            institution=institution
        )
        
        return {
            "success": True,
            "author": f"{name} {surname}",
            "institution": institution,
            "total_keywords": len(keywords),
            "keywords": keywords
        }
        
    except Exception as e:
        logger.error(f"Error getting keywords: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "keywords": []
        }

@mcp.tool()
async def get_second_degree_network(
    name: str,
    surname: str,
    institution: Optional[str] = None,
    max_connections: int = 50
) -> Dict[str, Any]:
    """
    Get second-degree network (co-authors of co-authors) for a given author.
    
    Args:
        name: Author's first name
        surname: Author's last name
        institution: Optional institution affiliation
        max_connections: Maximum number of second-degree connections to return
    
    Returns:
        Dictionary containing second-degree network grouped by first-degree connections
    """
    try:
        logger.info(f"Searching second-degree network for {name} {surname}")
        
        network = await search_engine.get_second_degree_network(
            name=name,
            surname=surname,
            institution=institution,
            max_connections=max_connections
        )
        
        return {
            "success": True,
            "author": f"{name} {surname}",
            "institution": institution,
            "network_size": sum(len(connections["second_degree"]) for connections in network.values()),
            "first_degree_count": len(network),
            "network": network
        }
        
    except Exception as e:
        logger.error(f"Error getting second-degree network: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "network": {}
        }

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()