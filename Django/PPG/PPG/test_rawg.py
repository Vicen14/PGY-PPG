import os
import django
from dotenv import load_dotenv

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PPG.settings')
django.setup()

from myPPG.services.rawg_service import RAWGService

load_dotenv()

def test_rawg_connection():
    print("🔍 Probando conexión con RAWG API...")
    
    # Verificar API Key
    from django.conf import settings
    if hasattr(settings, 'RAWG_API_KEY') and settings.RAWG_API_KEY:
        print(f"✅ API Key encontrada: {settings.RAWG_API_KEY[:10]}...")
    else:
        print("❌ API Key no configurada")
        return
    
    # Probar búsqueda de juegos populares
    print("📡 Buscando juegos populares...")
    try:
        result = RAWGService.get_popular_games()
        if result and 'results' in result:
            games = result['results'][:3]  # Mostrar solo 3
            print(f"✅ ¡Conexión exitosa! Encontrados {len(result['results'])} juegos")
            print("🎮 Primeros 3 juegos:")
            for game in games:
                print(f"   - {game['name']} (Rating: {game.get('rating', 'N/A')})")
        else:
            print("❌ No se pudieron obtener juegos")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_rawg_connection()