#!/usr/bin/env python3
"""
Setup script for CodeAlpha FAQ Chatbot
Installs dependencies and downloads required NLTK data
"""

import subprocess
import sys
import nltk

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    return True

def download_nltk_data():
    """Download required NLTK data"""
    print("📚 Downloading NLTK data...")
    try:
        nltk.download('punkt_tab', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✅ NLTK data downloaded successfully!")
    except Exception as e:
        print(f"❌ Error downloading NLTK data: {e}")
        return False
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up CodeAlpha FAQ Chatbot...")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed!")
        return
    
    # Download NLTK data
    if not download_nltk_data():
        print("❌ Setup failed!")
        return
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n🎉 You can now run the chatbot with:")
    print("   python app.py")
    print("\n🌐 Then open your browser to:")
    print("   http://localhost:5000")

if __name__ == "__main__":
    main()