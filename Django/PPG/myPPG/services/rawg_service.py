import requests
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class RAWGService:
    BASE_URL = "https://api.rawg.io/api"
    
    @staticmethod
    def _make_request(endpoint, params=None):
        """Método base para requests a RAWG"""
        if params is None:
            params = {}
        
        # Verificar que la API key esté configurada
        if not hasattr(settings, 'RAWG_API_KEY') or not settings.RAWG_API_KEY:
            logger.error("RAWG_API_KEY no configurada en settings.py")
            return None
        
        params['key'] = settings.RAWG_API_KEY
        url = f"{RAWGService.BASE_URL}/{endpoint}"
        
        cache_key = f"rawg_{endpoint}_{hash(frozenset(params.items()))}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            # Cachear por 1 hora
            cache.set(cache_key, data, 3600)
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling RAWG API: {e}")
            return None
    
    @staticmethod
    def search_games(query, page=1, page_size=20):
        """Buscar juegos por término"""
        return RAWGService._make_request("games", {
            'search': query,
            'page': page,
            'page_size': page_size,
            'ordering': '-rating'
        })
    
    @staticmethod
    def get_game_details(game_id):
        """Obtener detalles específicos de un juego"""
        return RAWGService._make_request(f"games/{game_id}")
    
    @staticmethod
    def get_popular_games():
        """Obtener juegos populares para la página principal"""
        return RAWGService._make_request("games", {
            'ordering': '-added',
            'page_size': 12
        })
    
    @staticmethod
    def get_games_by_genre(genre_slug, page=1, page_size=20):
        """Obtener juegos por género"""
        return RAWGService._make_request("games", {
            'genres': genre_slug,
            'page': page,
            'page_size': page_size,
            'ordering': '-rating'
        })