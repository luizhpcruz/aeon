#!/usr/bin/env python3
"""
Launcher for AEONCOSMA Advanced Visualization Suite with AI Integration
======================================================================
"""

import subprocess
import sys
import os
import time

def launch_advanced_suite():
    """Lança o Advanced Visualization Suite com integração de IA"""
    
    print("🚀 Launching AEONCOSMA Advanced Visualization Suite with AI Integration...")
    print("="*70)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("aeoncosma/ui/advanced_visualization_suite.py"):
        print("❌ Error: Please run this from the Digital Twin root directory")
        return
    
    # Configurar ambiente
    env = os.environ.copy()
    
    try:
        # Comando para executar o Streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            "aeoncosma/ui/advanced_visualization_suite.py",
            "--server.port=8507",
            "--server.headless=true",
            "--server.fileWatcherType=none"
        ]
        
        print("📊 Starting Advanced Visualization Suite...")
        print(f"🌐 URL: http://localhost:8507")
        print("🤖 AI Analytics Integration: Enabled")
        print("="*70)
        
        # Executar comando
        process = subprocess.run(cmd, env=env)
        
    except KeyboardInterrupt:
        print("\n🛑 Visualization Suite stopped by user")
    except Exception as e:
        print(f"❌ Error launching suite: {e}")

if __name__ == "__main__":
    launch_advanced_suite()
