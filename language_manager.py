"""
Multi-Language Manager for BuildSmartOS
Supports: English, Sinhala, Tamil
"""
import json
import os

class LanguageManager:
    def __init__(self, default_language="english"):
        self.current_language = default_language
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """Load all translation files"""
        languages = ["english", "sinhala", "tamil"]
        translations_dir = os.path.join(os.path.dirname(__file__), "translations")
        
        for lang in languages:
            file_path = os.path.join(translations_dir, f"{lang}.json")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.translations[lang] = json.load(f)
            except Exception as e:
                print(f"Error loading {lang} translations: {e}")
                self.translations[lang] = {}
    
    def set_language(self, language):
        """Change current language"""
        if language in self.translations:
            self.current_language = language
            return True
        return False
    
    def get(self, key, fallback=None):
        """Get translated text for a key"""
        try:
            return self.translations[self.current_language].get(key, fallback or key)
        except:
            return fallback or key
    
    def get_available_languages(self):
        """Return list of available languages"""
        return list(self.translations.keys())
    
    def translate_dict(self, keys):
        """Translate multiple keys at once"""
        return {key: self.get(key) for key in keys}

# Global instance
_language_manager = None

def get_language_manager():
    """Get or create global language manager instance"""
    global _language_manager
    if _language_manager is None:
        _language_manager = LanguageManager()
    return _language_manager

def translate(key, fallback=None):
    """Quick translation function"""
    return get_language_manager().get(key, fallback)
