#!/usr/bin/env python3
"""
Script de test pour l'extension iSMART Modbus.
À exécuter avant l'installation dans Home Assistant pour vérifier la communication Modbus.
"""

import sys
import os

# Ajouter le chemin de l'extension
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'custom_components', 'ismart_modbus'))

from modbus_interface import ModbusInterface
import asyncio
import logging

logging.basicConfig(level=logging.DEBUG)

async def test_modbus():
    """Test de la communication Modbus."""
    print("🔌 Test de l'extension iSMART Modbus")
    print("=" * 50)
    
    # Configuration
    port = "/dev/ttyUSB0"
    baudrate = 38400
    timeout = 0.03
    
    print(f"\n📋 Configuration:")
    print(f"   Port série : {port}")
    print(f"   Vitesse    : {baudrate} bauds")
    print(f"   Timeout    : {timeout}s")
    
    # Création de l'interface
    print(f"\n🔧 Création de ModbusInterface...")
    modbus = ModbusInterface(port=port, baudrate=baudrate, timeout=timeout)
    
    # Connexion
    print(f"🔗 Connexion au port série...")
    if not await modbus.async_connect():
        print("❌ ERREUR : Impossible de se connecter au port série")
        print("\n💡 Vérifications :")
        print("   1. Le port existe : ls -l /dev/ttyUSB*")
        print("   2. Permissions : sudo usermod -a -G dialout $USER")
        print("   3. Aucun autre programme n'utilise le port")
        return False
    
    print("✅ Connexion réussie !")
    
    # Test de lecture d'état
    print(f"\n📖 Test de lecture d'état des automates...")
    try:
        outvalid, outstate, memstate = modbus.readstate()
        print(f"   Automates valides : {outvalid}")
        print(f"   États sorties     : {outstate}")
        print(f"   États mémoire     : {memstate}")
        
        if sum(outvalid) > 0:
            print(f"✅ Lecture d'état réussie ({sum(outvalid)} automate(s) actif(s))")
        else:
            print("⚠️  Aucun automate ne répond")
    except Exception as e:
        print(f"❌ Erreur lors de la lecture : {e}")
    
    # Test d'écriture (Lumière Gabriel)
    print(f"\n💡 Test d'écriture (Lumière Gabriel - slave 1, coil 0x2C02)...")
    try:
        print(f"   → Allumage...")
        result = modbus.writecoil_device(slave=1, coil=0x2C02, value=1)
        if result == 0:
            print(f"   ✅ Allumage réussi")
        else:
            print(f"   ❌ Erreur d'allumage")
        
        await asyncio.sleep(2)
        
        print(f"   → Extinction...")
        result = modbus.writecoil_device(slave=1, coil=0x2C02, value=0)
        if result == 0:
            print(f"   ✅ Extinction réussie")
        else:
            print(f"   ❌ Erreur d'extinction")
    except Exception as e:
        print(f"❌ Erreur lors de l'écriture : {e}")
    
    # Déconnexion
    print(f"\n🔌 Déconnexion...")
    modbus.disconnect()
    print("✅ Test terminé !")
    
    print("\n" + "=" * 50)
    print("📝 Résumé :")
    print("   Si tous les tests sont ✅, l'extension est prête !")
    print("   Vous pouvez l'installer dans Home Assistant.")
    print("\n📚 Voir INSTALLATION.md pour les étapes suivantes.")
    
    return True

if __name__ == "__main__":
    print("🚀 Démarrage du test...\n")
    try:
        result = asyncio.run(test_modbus())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ ERREUR FATALE : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
