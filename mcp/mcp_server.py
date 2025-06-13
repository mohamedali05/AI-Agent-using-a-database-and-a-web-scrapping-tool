import logging
import os
from typing import Dict, Any
from dataclasses import dataclass
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

import httpx
from mcp.server.fastmcp import FastMCP, Context
import time

time.sleep(6)

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration depuis les variables d'environnement
API_PORT = os.getenv("API_PORT", "5000")
print(f"API_PORT: {API_PORT}")
MCP_PORT = int(os.getenv("MCP_PORT", "5001"))
print(f"MCP_PORT: {MCP_PORT}")
API_BASE_URL = f"http://api:{API_PORT}"

@dataclass
class AppContext:
    """Contexte de l'application MCP"""
    session: httpx.AsyncClient

@asynccontextmanager
async def app_lifespan(_: FastMCP) -> AsyncIterator[AppContext]:
    """Initialise et nettoie les ressources au démarrage/arrêt."""
    logger.info("Démarrage du client HTTP pour l'appel d'API externe...")
    async with httpx.AsyncClient() as session:
        yield AppContext(session=session)
    logger.info("Client HTTP fermé.")

# Création du serveur MCP simple
mcp = FastMCP(
    "MCP Produits Beauté",
    description="Expose un outil de récupération de produits via une API Flask",
    version="0.1.0",
    lifespan=app_lifespan,
    port=MCP_PORT,
    host="0.0.0.0", 
)

@mcp.tool()
async def get_products(ctx: Context = None) -> Dict[str, Any]:
    """
    Récupère la liste des produits depuis l'API Flask locale.

    Returns:
        Un dictionnaire contenant les produits ou une erreur.
    """
    session = ctx.request_context.lifespan_context.session
    try:
        response = await session.get(f"{API_BASE_URL}/products")
        response.raise_for_status()
        data = response.json()
        return {"products": data, "count": len(data)}
    except Exception as e:
        logger.error(f"Erreur lors de l'appel à l'API Flask: {str(e)}")
        return {"error": str(e), "products": [], "count": 0}

@mcp.tool()
async def search_product_by_name(name: str, ctx: Context = None) -> Dict[str, Any]:
    """Recherche les produits dont le nom contient la chaîne donnée (insensible à la casse)."""
    session = ctx.request_context.lifespan_context.session
    try:
        response = await session.get(f"{API_BASE_URL}/product/{name}")
        response.raise_for_status()
        data = response.json()
        return {"results": data, "count": len(data)}
    except Exception as e:
        logger.error(f"Erreur lors de la recherche de produit: {str(e)}")
        return {"error": str(e), "results": [], "count": 0}

@mcp.tool()
async def get_stores(ctx: Context = None) -> Dict[str, Any]:
    """Récupère la liste des magasins."""
    session = ctx.request_context.lifespan_context.session
    try:
        response = await session.get(f"{API_BASE_URL}/stores")
        response.raise_for_status()
        data = response.json()
        return {"stores": data, "count": len(data)}
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des magasins: {str(e)}")
        return {"error": str(e), "stores": [], "count": 0}

@mcp.tool()
async def search_store_by_name(name: str, ctx: Context = None) -> Dict[str, Any]:
    """Recherche les magasins dont le nom contient la chaîne donnée (insensible à la casse)."""
    session = ctx.request_context.lifespan_context.session
    try:
        response = await session.get(f"{API_BASE_URL}/store/{name}")
        response.raise_for_status()
        data = response.json()
        return {"results": data, "count": len(data)}
    except Exception as e:
        logger.error(f"Erreur lors de la recherche de magasin: {str(e)}")
        return {"error": str(e), "results": [], "count": 0}

@mcp.tool()
async def get_store_products(ctx: Context = None) -> Dict[str, Any]:
    """Récupère tous les produits en stock dans tous les magasins."""
    session = ctx.request_context.lifespan_context.session
    try:
        response = await session.get(f"{API_BASE_URL}/store-products")
        response.raise_for_status()
        data = response.json()
        return {"stocks": data, "count": len(data)}
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des stocks: {str(e)}")
        return {"error": str(e), "stocks": [], "count": 0}

@mcp.tool()
async def search_store_products(store_name: str, ctx: Context = None) -> Dict[str, Any]:
    """Récupère les produits disponibles dans un magasin donné (nom partiel accepté, insensible à la casse)."""
    session = ctx.request_context.lifespan_context.session
    try:
        response = await session.get(f"{API_BASE_URL}/store-products/{store_name}")
        response.raise_for_status()
        data = response.json()
        return {"products": data, "count": len(data)}
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des produits pour le magasin '{store_name}': {str(e)}")
        return {"error": str(e), "products": [], "count": 0}

def run_server(transport: str = "sse") -> None:
    """Point d'entrée pour exécuter le serveur MCP."""
    try:
        mcp.run(transport=transport)
    except KeyboardInterrupt:
        logger.info("Arrêt manuel du serveur MCP")
    except Exception as e:
        logger.error(f"Erreur au démarrage du serveur: {str(e)}")

if __name__ == "__main__":
    run_server()