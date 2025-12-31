from flask import Flask, request, jsonify
import os
import requests
import json
from urllib.parse import quote

# Language Translation Tool - CodeAlpha Internship Project
app = Flask(__name__)

# Language codes for translation API
LANGUAGE_CODES = {
    'auto': 'auto',
    'en': 'en',
    'hi': 'hi', 
    'fr': 'fr',
    'es': 'es',
    'de': 'de',
    'zh': 'zh',
    'ja': 'ja',
    'ko': 'ko',
    'ar': 'ar',
    'pt': 'pt',
    'ru': 'ru',
    'it': 'it',
    'nl': 'nl',
    'tr': 'tr'
}

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeAlpha Language Translation Tool</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }

        header {
            text-align: center;
            margin-bottom: 40px;
            color: white;
        }

        header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .translation-container {
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            gap: 20px;
            margin-bottom: 30px;
            align-items: start;
        }

        .input-section, .output-section {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .language-selector {
            margin-bottom: 15px;
        }

        .language-selector label {
            display: block;
            color: white;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .language-selector select {
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.9);
            font-size: 16px;
            cursor: pointer;
        }

        .text-area-container {
            position: relative;
        }

        textarea {
            width: 100%;
            height: 200px;
            padding: 15px;
            border: none;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.9);
            font-size: 16px;
            resize: vertical;
            font-family: inherit;
        }

        textarea:focus {
            outline: 2px solid #4ade80;
        }

        .char-count {
            position: absolute;
            bottom: 10px;
            right: 15px;
            color: #666;
            font-size: 12px;
        }

        .output-actions {
            position: absolute;
            bottom: 10px;
            right: 15px;
            display: flex;
            gap: 8px;
        }

        .action-btn {
            background: #667eea;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
        }

        .action-btn:hover:not(:disabled) {
            background: #5a67d8;
            transform: translateY(-2px);
        }

        .action-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .swap-container {
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .swap-btn {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            cursor: pointer;
            font-size: 18px;
            transition: all 0.3s ease;
        }

        .swap-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: rotate(180deg);
        }

        .controls {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 20px;
        }

        .translate-btn, .clear-btn {
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .translate-btn {
            background: linear-gradient(45deg, #4ade80, #22c55e);
            color: white;
        }

        .translate-btn:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(74, 222, 128, 0.4);
        }

        .translate-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .clear-btn {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        .clear-btn:hover {
            background: rgba(255, 255, 255, 0.3);
        }

        .loading {
            text-align: center;
            color: white;
            font-size: 18px;
            margin: 20px 0;
        }

        .loading i {
            margin-right: 10px;
        }

        .error-message {
            background: rgba(239, 68, 68, 0.9);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
        }

        .detected-language {
            background: rgba(59, 130, 246, 0.9);
            color: white;
            padding: 10px 15px;
            border-radius: 8px;
            margin: 10px 0;
            text-align: center;
        }

        .hidden {
            display: none;
        }

        .slide-in {
            animation: slideIn 0.5s ease-out;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @media (max-width: 768px) {
            .translation-container {
                grid-template-columns: 1fr;
                gap: 15px;
            }

            .swap-container {
                order: 2;
            }

            .swap-btn {
                transform: rotate(90deg);
            }

            .controls {
                flex-direction: column;
                align-items: center;
            }

            .translate-btn, .clear-btn {
                width: 100%;
                max-width: 300px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1><i class="fas fa-language"></i> CodeAlpha Language Translation Tool</h1>
            <p>Translate text between multiple languages instantly</p>
        </header>

        <main class="translation-container">
            <div class="input-section">
                <div class="language-selector">
                    <label for="source-lang">From:</label>
                    <select id="source-lang">
                        <option value="auto" selected>Auto Detect</option>
                        <option value="en">English</option>
                        <option value="hi">Hindi</option>
                        <option value="fr">French</option>
                        <option value="es">Spanish</option>
                        <option value="de">German</option>
                        <option value="zh">Chinese</option>
                        <option value="ja">Japanese</option>
                        <option value="ko">Korean</option>
                        <option value="ar">Arabic</option>
                        <option value="pt">Portuguese</option>
                        <option value="ru">Russian</option>
                        <option value="it">Italian</option>
                        <option value="nl">Dutch</option>
                        <option value="tr">Turkish</option>
                    </select>
                </div>

                <div class="text-area-container">
                    <textarea 
                        id="input-text" 
                        placeholder="Enter text to translate..."
                        maxlength="5000"
                    ></textarea>
                    <div class="char-count">
                        <span id="char-counter">0/5000</span>
                    </div>
                </div>
            </div>

            <div class="swap-container">
                <button id="swap-languages" class="swap-btn" title="Swap languages">
                    <i class="fas fa-exchange-alt"></i>
                </button>
            </div>

            <div class="output-section">
                <div class="language-selector">
                    <label for="target-lang">To:</label>
                    <select id="target-lang">
                        <option value="en">English</option>
                        <option value="hi">Hindi</option>
                        <option value="fr">French</option>
                        <option value="es" selected>Spanish</option>
                        <option value="de">German</option>
                        <option value="zh">Chinese</option>
                        <option value="ja">Japanese</option>
                        <option value="ko">Korean</option>
                        <option value="ar">Arabic</option>
                        <option value="pt">Portuguese</option>
                        <option value="ru">Russian</option>
                        <option value="it">Italian</option>
                        <option value="nl">Dutch</option>
                        <option value="tr">Turkish</option>
                    </select>
                </div>

                <div class="text-area-container">
                    <textarea 
                        id="output-text" 
                        placeholder="Translation will appear here..."
                        readonly
                    ></textarea>
                    <div class="output-actions">
                        <button id="copy-btn" class="action-btn" title="Copy to clipboard" disabled>
                            <i class="fas fa-copy"></i>
                        </button>
                        <button id="speak-btn" class="action-btn" title="Listen to translation" disabled>
                            <i class="fas fa-volume-up"></i>
                        </button>
                    </div>
                </div>
            </div>
        </main>

        <div class="controls">
            <button id="translate-btn" class="translate-btn" disabled>
                <i class="fas fa-language"></i>
                Translate
            </button>
            <button id="clear-btn" class="clear-btn">
                <i class="fas fa-trash"></i>
                Clear
            </button>
        </div>

        <div id="loading" class="loading hidden">
            <i class="fas fa-spinner fa-spin"></i>
            Translating...
        </div>

        <div id="error-message" class="error-message hidden"></div>

        <div id="detected-language" class="detected-language hidden">
            <i class="fas fa-info-circle"></i>
            <span id="detected-text"></span>
        </div>
    </div>

    <script>
        const inputText = document.getElementById('input-text');
        const outputText = document.getElementById('output-text');
        const sourceLang = document.getElementById('source-lang');
        const targetLang = document.getElementById('target-lang');
        const translateBtn = document.getElementById('translate-btn');
        const clearBtn = document.getElementById('clear-btn');
        const swapBtn = document.getElementById('swap-languages');
        const copyBtn = document.getElementById('copy-btn');
        const speakBtn = document.getElementById('speak-btn');
        const loading = document.getElementById('loading');
        const errorMessage = document.getElementById('error-message');
        const detectedLanguage = document.getElementById('detected-language');
        const detectedText = document.getElementById('detected-text');
        const charCounter = document.getElementById('char-counter');

        let currentAudio = null;

        document.addEventListener('DOMContentLoaded', function() {
            inputText.addEventListener('input', function() {
                const text = this.value.trim();
                const length = this.value.length;
                
                charCounter.textContent = `${length}/5000`;
                translateBtn.disabled = !text;
                
                if (!text) {
                    clearOutput();
                }
            });

            translateBtn.addEventListener('click', translateText);
            clearBtn.addEventListener('click', clearAll);
            swapBtn.addEventListener('click', swapLanguages);
            copyBtn.addEventListener('click', copyToClipboard);
            speakBtn.addEventListener('click', speakText);

            inputText.addEventListener('keydown', function(e) {
                if (e.ctrlKey && e.key === 'Enter') {
                    e.preventDefault();
                    if (!translateBtn.disabled) {
                        translateText();
                    }
                }
            });

            sourceLang.addEventListener('change', function() {
                if (inputText.value.trim()) {
                    clearOutput();
                }
            });

            targetLang.addEventListener('change', function() {
                if (inputText.value.trim()) {
                    clearOutput();
                }
            });
        });

        async function translateText() {
            const text = inputText.value.trim();
            const source = sourceLang.value;
            const target = targetLang.value;

            if (!text) {
                showError('Please enter text to translate');
                return;
            }

            if (source === target && source !== 'auto') {
                showError('Source and target languages cannot be the same');
                return;
            }

            showLoading(true);
            hideError();
            hideDetectedLanguage();

            try {
                console.log('Making translation request...', {text, source, target});
                
                const response = await fetch('/api/translate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        text: text,
                        source_lang: source,
                        target_lang: target
                    })
                });

                console.log('Response status:', response.status);
                
                const data = await response.json();
                console.log('Response data:', data);

                if (!response.ok) {
                    throw new Error(data.error || `HTTP ${response.status}: Translation failed`);
                }

                if (!data.translated_text) {
                    throw new Error('No translation received from server');
                }

                outputText.value = data.translated_text;
                outputText.classList.add('slide-in');
                outputText.style.backgroundColor = '#f0fff4';
                
                console.log('Translation successful:', data.translated_text);
                
                const successMsg = document.createElement('div');
                successMsg.textContent = '✅ Translation completed!';
                successMsg.style.cssText = 'position:fixed;top:20px;right:20px;background:#4ade80;color:white;padding:10px 20px;border-radius:8px;z-index:1000;font-weight:600;';
                document.body.appendChild(successMsg);
                setTimeout(() => successMsg.remove(), 3000);

                if (source === 'auto' && data.detected_language) {
                    showDetectedLanguage(data.detected_language);
                }

                copyBtn.disabled = false;
                speakBtn.disabled = false;

            } catch (error) {
                showError(error.message);
                clearOutput();
            } finally {
                showLoading(false);
            }
        }

        async function speakText() {
            const text = outputText.value.trim();
            const lang = targetLang.value;

            if (!text) {
                showError('No text to speak');
                return;
            }

            if (currentAudio) {
                currentAudio.pause();
                currentAudio = null;
            }

            speakBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            speakBtn.disabled = true;

            try {
                if ('speechSynthesis' in window) {
                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.lang = getVoiceLang(lang);
                    utterance.rate = 0.8;
                    utterance.pitch = 1;
                    
                    utterance.onend = function() {
                        speakBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
                        speakBtn.disabled = false;
                    };
                    
                    utterance.onerror = function() {
                        speakBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
                        speakBtn.disabled = false;
                        showError('Speech synthesis failed');
                    };
                    
                    speechSynthesis.speak(utterance);
                    return;
                }

            } catch (error) {
                showError(error.message);
            } finally {
                speakBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
                speakBtn.disabled = false;
            }
        }

        function getVoiceLang(langCode) {
            const voiceMap = {
                'en': 'en-US', 'hi': 'hi-IN', 'fr': 'fr-FR', 'es': 'es-ES', 'de': 'de-DE',
                'zh': 'zh-CN', 'ja': 'ja-JP', 'ko': 'ko-KR', 'ar': 'ar-SA', 'pt': 'pt-BR',
                'ru': 'ru-RU', 'it': 'it-IT', 'nl': 'nl-NL', 'tr': 'tr-TR'
            };
            return voiceMap[langCode] || 'en-US';
        }

        async function copyToClipboard() {
            const text = outputText.value.trim();
            
            if (!text) {
                showError('No text to copy');
                return;
            }

            try {
                await navigator.clipboard.writeText(text);
                
                const originalIcon = copyBtn.innerHTML;
                copyBtn.innerHTML = '<i class="fas fa-check"></i>';
                copyBtn.style.background = '#28a745';
                
                setTimeout(() => {
                    copyBtn.innerHTML = originalIcon;
                    copyBtn.style.background = '#667eea';
                }, 1500);

            } catch (error) {
                outputText.select();
                document.execCommand('copy');
                showError('Text copied to clipboard');
            }
        }

        function swapLanguages() {
            const sourceValue = sourceLang.value;
            const targetValue = targetLang.value;
            const inputValue = inputText.value.trim();
            const outputValue = outputText.value.trim();

            if (sourceValue === 'auto') {
                showError('Cannot swap when auto-detect is selected');
                return;
            }

            sourceLang.value = targetValue;
            targetLang.value = sourceValue;

            inputText.value = outputValue;
            outputText.value = inputValue;

            const hasInputText = inputText.value.trim();
            translateBtn.disabled = !hasInputText;
            copyBtn.disabled = !outputText.value.trim();
            speakBtn.disabled = !outputText.value.trim();

            charCounter.textContent = `${inputText.value.length}/5000`;

            hideError();
            hideDetectedLanguage();
        }

        function clearAll() {
            inputText.value = '';
            clearOutput();
            translateBtn.disabled = true;
            charCounter.textContent = '0/5000';
            hideError();
            hideDetectedLanguage();
            
            if (currentAudio) {
                currentAudio.pause();
                currentAudio = null;
            }
        }

        function clearOutput() {
            outputText.value = '';
            copyBtn.disabled = true;
            speakBtn.disabled = true;
            outputText.classList.remove('slide-in');
        }

        function showLoading(show) {
            if (show) {
                loading.classList.remove('hidden');
                translateBtn.disabled = true;
            } else {
                loading.classList.add('hidden');
                translateBtn.disabled = !inputText.value.trim();
            }
        }

        function showError(message) {
            errorMessage.textContent = message;
            errorMessage.classList.remove('hidden');
            
            setTimeout(() => {
                hideError();
            }, 5000);
        }

        function hideError() {
            errorMessage.classList.add('hidden');
        }

        function showDetectedLanguage(language) {
            detectedText.textContent = `Detected language: ${language}`;
            detectedLanguage.classList.remove('hidden');
        }

        function hideDetectedLanguage() {
            detectedLanguage.classList.add('hidden');
        }
    </script>
</body>
</html>'''

@app.route('/')
def home():
    return HTML

@app.route('/api/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        source_lang = data.get('source_lang', 'auto')
        target_lang = data.get('target_lang', 'es')
        
        if not text:
            return jsonify({'error': 'Please enter text to translate'}), 400
            
        if len(text) > 5000:
            return jsonify({'error': 'Text too long. Maximum 5000 characters allowed.'}), 400
        
        # Try Google Translate API first if available
        api_key = os.getenv('GOOGLE_TRANSLATE_API_KEY')
        if api_key:
            result = translate_with_google_api(text, source_lang, target_lang, api_key)
            if result:
                return jsonify(result)
        
        # Use Google Translate API for ALL translations
        result = translate_with_google_translate_free(text, source_lang, target_lang)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Translation failed: {str(e)}'}), 500

def translate_with_google_translate_free(text, source_lang, target_lang):
    """Use Google Translate via web scraping for free translations"""
    try:
        import urllib.parse
        import re
        
        # Clean text for URL encoding
        text_encoded = urllib.parse.quote(text)
        
        # Map language codes
        lang_map = {
            'auto': 'auto', 'en': 'en', 'hi': 'hi', 'es': 'es', 'fr': 'fr',
            'de': 'de', 'zh': 'zh', 'ja': 'ja', 'ko': 'ko', 'ar': 'ar',
            'pt': 'pt', 'ru': 'ru', 'it': 'it', 'nl': 'nl', 'tr': 'tr'
        }
        
        source_code = lang_map.get(source_lang, 'auto')
        target_code = lang_map.get(target_lang, 'hi')
        
        # Use Google Translate URL
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_code}&tl={target_code}&dt=t&q={text_encoded}"
        
        # Make request
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            # Parse JSON response
            result = response.json()
            
            if result and len(result) > 0 and result[0]:
                # Extract translated text
                translated_parts = []
                for part in result[0]:
                    if part and len(part) > 0:
                        translated_parts.append(part[0])
                
                translated_text = ''.join(translated_parts)
                
                if translated_text and translated_text.strip():
                    return {
                        'success': True,
                        'translated_text': translated_text.strip(),
                        'detected_language': result[2] if len(result) > 2 else 'unknown',
                        'confidence': 0.95,
                        'api_used': 'Google Translate Free API'
                    }
        
        # Fallback to simple translation
        return simple_translate(text, source_lang, target_lang)
        
    except Exception as e:
        print(f"Google Translate Free API error: {e}")
        # Fallback to simple translation
        return simple_translate(text, source_lang, target_lang)

def simple_translate(text, source_lang, target_lang):
    """Simple but effective translation system"""
    
    # Basic translations - COMPREHENSIVE DICTIONARY
    translations = {
        # Common words
        'hello': {'hi': 'नमस्ते', 'es': 'hola', 'fr': 'bonjour'},
        'world': {'hi': 'दुनिया', 'es': 'mundo', 'fr': 'monde'},
        'how': {'hi': 'कैसे', 'es': 'cómo', 'fr': 'comment'},
        'are': {'hi': 'हैं', 'es': 'estás', 'fr': 'êtes'},
        'you': {'hi': 'आप', 'es': 'tú', 'fr': 'vous'},
        'good': {'hi': 'अच्छा', 'es': 'bueno', 'fr': 'bon'},
        'morning': {'hi': 'सुबह', 'es': 'mañana', 'fr': 'matin'},
        'thank': {'hi': 'धन्यवाद', 'es': 'gracias', 'fr': 'merci'},
        'i': {'hi': 'मैं', 'es': 'yo', 'fr': 'je'},
        'love': {'hi': 'प्यार', 'es': 'amor', 'fr': 'amour'},
        'my': {'hi': 'मेरा', 'es': 'mi', 'fr': 'mon'},
        'name': {'hi': 'नाम', 'es': 'nombre', 'fr': 'nom'},
        'is': {'hi': 'है', 'es': 'es', 'fr': 'est'},
        'am': {'hi': 'हूँ', 'es': 'soy', 'fr': 'suis'},
        'learning': {'hi': 'सीख रहा', 'es': 'aprendiendo', 'fr': 'apprenant'},
        'programming': {'hi': 'प्रोग्रामिंग', 'es': 'programación', 'fr': 'programmation'},
        'and': {'hi': 'और', 'es': 'y', 'fr': 'et'},
        'it': {'hi': 'यह', 'es': 'eso', 'fr': 'il'},
        'very': {'hi': 'बहुत', 'es': 'muy', 'fr': 'très'},
        'interesting': {'hi': 'दिलचस्प', 'es': 'interesante', 'fr': 'intéressant'},
        
        # Additional common words
        'the': {'hi': '', 'es': 'el', 'fr': 'le'},
        'a': {'hi': 'एक', 'es': 'un', 'fr': 'un'},
        'an': {'hi': 'एक', 'es': 'un', 'fr': 'un'},
        'to': {'hi': 'को', 'es': 'a', 'fr': 'à'},
        'for': {'hi': 'के लिए', 'es': 'para', 'fr': 'pour'},
        'of': {'hi': 'का', 'es': 'de', 'fr': 'de'},
        'in': {'hi': 'में', 'es': 'en', 'fr': 'dans'},
        'on': {'hi': 'पर', 'es': 'en', 'fr': 'sur'},
        'at': {'hi': 'पर', 'es': 'en', 'fr': 'à'},
        'with': {'hi': 'के साथ', 'es': 'con', 'fr': 'avec'},
        'without': {'hi': 'के बिना', 'es': 'sin', 'fr': 'sans'},
        'man': {'hi': 'आदमी', 'es': 'hombre', 'fr': 'homme'},
        'men': {'hi': 'आदमी', 'es': 'hombres', 'fr': 'hommes'},
        'woman': {'hi': 'औरत', 'es': 'mujer', 'fr': 'femme'},
        'grow': {'hi': 'बढ़ना', 'es': 'crecer', 'fr': 'grandir'},
        'old': {'hi': 'बूढ़ा', 'es': 'viejo', 'fr': 'vieux'},
        'seeing': {'hi': 'देखना', 'es': 'viendo', 'fr': 'voir'},
        'beauty': {'hi': 'सुंदरता', 'es': 'belleza', 'fr': 'beauté'},
        'beast': {'hi': 'जानवर', 'es': 'bestia', 'fr': 'bête'},
        'inside': {'hi': 'अंदर', 'es': 'dentro', 'fr': 'à l\'intérieur'},
        'him': {'hi': 'उसे', 'es': 'él', 'fr': 'lui'},
        'her': {'hi': 'उसे', 'es': 'ella', 'fr': 'elle'},
        'its': {'hi': 'इसका', 'es': 'su', 'fr': 'son'},
        'shame': {'hi': 'शर्म', 'es': 'vergüenza', 'fr': 'honte'},
        'this': {'hi': 'यह', 'es': 'esto', 'fr': 'ceci'},
        'that': {'hi': 'वह', 'es': 'eso', 'fr': 'cela'},
        'what': {'hi': 'क्या', 'es': 'qué', 'fr': 'quoi'},
        'where': {'hi': 'कहाँ', 'es': 'dónde', 'fr': 'où'},
        'when': {'hi': 'कब', 'es': 'cuándo', 'fr': 'quand'},
        'why': {'hi': 'क्यों', 'es': 'por qué', 'fr': 'pourquoi'},
        'who': {'hi': 'कौन', 'es': 'quién', 'fr': 'qui'},
        'which': {'hi': 'कौन सा', 'es': 'cuál', 'fr': 'lequel'},
        'can': {'hi': 'सकता', 'es': 'puede', 'fr': 'peut'},
        'will': {'hi': 'होगा', 'es': 'será', 'fr': 'sera'},
        'would': {'hi': 'होगा', 'es': 'sería', 'fr': 'serait'},
        'should': {'hi': 'चाहिए', 'es': 'debería', 'fr': 'devrait'},
        'could': {'hi': 'सकता था', 'es': 'podría', 'fr': 'pourrait'},
        'have': {'hi': 'है', 'es': 'tener', 'fr': 'avoir'},
        'has': {'hi': 'है', 'es': 'tiene', 'fr': 'a'},
        'had': {'hi': 'था', 'es': 'tenía', 'fr': 'avait'},
        'do': {'hi': 'करना', 'es': 'hacer', 'fr': 'faire'},
        'does': {'hi': 'करता', 'es': 'hace', 'fr': 'fait'},
        'did': {'hi': 'किया', 'es': 'hizo', 'fr': 'a fait'},
        'be': {'hi': 'होना', 'es': 'ser', 'fr': 'être'},
        'been': {'hi': 'था', 'es': 'sido', 'fr': 'été'},
        'being': {'hi': 'होना', 'es': 'siendo', 'fr': 'étant'},
        'was': {'hi': 'था', 'es': 'era', 'fr': 'était'},
        'were': {'hi': 'थे', 'es': 'eran', 'fr': 'étaient'},
        'get': {'hi': 'पाना', 'es': 'obtener', 'fr': 'obtenir'},
        'got': {'hi': 'मिला', 'es': 'obtuvo', 'fr': 'a obtenu'},
        'go': {'hi': 'जाना', 'es': 'ir', 'fr': 'aller'},
        'went': {'hi': 'गया', 'es': 'fue', 'fr': 'est allé'},
        'come': {'hi': 'आना', 'es': 'venir', 'fr': 'venir'},
        'came': {'hi': 'आया', 'es': 'vino', 'fr': 'est venu'},
        'see': {'hi': 'देखना', 'es': 'ver', 'fr': 'voir'},
        'saw': {'hi': 'देखा', 'es': 'vio', 'fr': 'a vu'},
        'know': {'hi': 'जानना', 'es': 'saber', 'fr': 'savoir'},
        'knew': {'hi': 'जानता था', 'es': 'sabía', 'fr': 'savait'},
        'think': {'hi': 'सोचना', 'es': 'pensar', 'fr': 'penser'},
        'thought': {'hi': 'सोचा', 'es': 'pensó', 'fr': 'a pensé'},
        'say': {'hi': 'कहना', 'es': 'decir', 'fr': 'dire'},
        'said': {'hi': 'कहा', 'es': 'dijo', 'fr': 'a dit'},
        'tell': {'hi': 'बताना', 'es': 'contar', 'fr': 'dire'},
        'told': {'hi': 'बताया', 'es': 'contó', 'fr': 'a dit'},
        'ask': {'hi': 'पूछना', 'es': 'preguntar', 'fr': 'demander'},
        'asked': {'hi': 'पूछा', 'es': 'preguntó', 'fr': 'a demandé'},
        'give': {'hi': 'देना', 'es': 'dar', 'fr': 'donner'},
        'gave': {'hi': 'दिया', 'es': 'dio', 'fr': 'a donné'},
        'take': {'hi': 'लेना', 'es': 'tomar', 'fr': 'prendre'},
        'took': {'hi': 'लिया', 'es': 'tomó', 'fr': 'a pris'},
        'make': {'hi': 'बनाना', 'es': 'hacer', 'fr': 'faire'},
        'made': {'hi': 'बनाया', 'es': 'hizo', 'fr': 'a fait'},
        'put': {'hi': 'रखना', 'es': 'poner', 'fr': 'mettre'},
        'find': {'hi': 'खोजना', 'es': 'encontrar', 'fr': 'trouver'},
        'found': {'hi': 'मिला', 'es': 'encontró', 'fr': 'a trouvé'},
        'work': {'hi': 'काम', 'es': 'trabajo', 'fr': 'travail'},
        'worked': {'hi': 'काम किया', 'es': 'trabajó', 'fr': 'a travaillé'},
        'play': {'hi': 'खेलना', 'es': 'jugar', 'fr': 'jouer'},
        'played': {'hi': 'खेला', 'es': 'jugó', 'fr': 'a joué'},
        'live': {'hi': 'रहना', 'es': 'vivir', 'fr': 'vivre'},
        'lived': {'hi': 'रहा', 'es': 'vivió', 'fr': 'a vécu'},
        'help': {'hi': 'मदद', 'es': 'ayuda', 'fr': 'aide'},
        'helped': {'hi': 'मदद की', 'es': 'ayudó', 'fr': 'a aidé'},
        'want': {'hi': 'चाहना', 'es': 'querer', 'fr': 'vouloir'},
        'wanted': {'hi': 'चाहा', 'es': 'quería', 'fr': 'voulait'},
        'need': {'hi': 'जरूरत', 'es': 'necesitar', 'fr': 'besoin'},
        'needed': {'hi': 'जरूरत थी', 'es': 'necesitaba', 'fr': 'avait besoin'},
        'like': {'hi': 'पसंद', 'es': 'gustar', 'fr': 'aimer'},
        'liked': {'hi': 'पसंद किया', 'es': 'gustó', 'fr': 'a aimé'},
        'try': {'hi': 'कोशिश', 'es': 'intentar', 'fr': 'essayer'},
        'tried': {'hi': 'कोशिश की', 'es': 'intentó', 'fr': 'a essayé'},
        'use': {'hi': 'उपयोग', 'es': 'usar', 'fr': 'utiliser'},
        'used': {'hi': 'उपयोग किया', 'es': 'usó', 'fr': 'a utilisé'},
        'call': {'hi': 'बुलाना', 'es': 'llamar', 'fr': 'appeler'},
        'called': {'hi': 'बुलाया', 'es': 'llamó', 'fr': 'a appelé'},
        'look': {'hi': 'देखना', 'es': 'mirar', 'fr': 'regarder'},
        'looked': {'hi': 'देखा', 'es': 'miró', 'fr': 'a regardé'},
        'feel': {'hi': 'महसूस', 'es': 'sentir', 'fr': 'sentir'},
        'felt': {'hi': 'महसूस किया', 'es': 'sintió', 'fr': 'a senti'},
        'seem': {'hi': 'लगना', 'es': 'parecer', 'fr': 'sembler'},
        'seemed': {'hi': 'लगा', 'es': 'parecía', 'fr': 'semblait'},
        'become': {'hi': 'बनना', 'es': 'convertirse', 'fr': 'devenir'},
        'became': {'hi': 'बना', 'es': 'se convirtió', 'fr': 'est devenu'},
        'leave': {'hi': 'छोड़ना', 'es': 'dejar', 'fr': 'laisser'},
        'left': {'hi': 'छोड़ा', 'es': 'dejó', 'fr': 'a laissé'},
        'turn': {'hi': 'मोड़ना', 'es': 'girar', 'fr': 'tourner'},
        'turned': {'hi': 'मोड़ा', 'es': 'giró', 'fr': 'a tourné'},
        'move': {'hi': 'हिलना', 'es': 'mover', 'fr': 'bouger'},
        'moved': {'hi': 'हिला', 'es': 'movió', 'fr': 'a bougé'},
        'bring': {'hi': 'लाना', 'es': 'traer', 'fr': 'apporter'},
        'brought': {'hi': 'लाया', 'es': 'trajo', 'fr': 'a apporté'},
        'build': {'hi': 'बनाना', 'es': 'construir', 'fr': 'construire'},
        'built': {'hi': 'बनाया', 'es': 'construyó', 'fr': 'a construit'}
    }
    
    # Phrases
    phrases = {
        'hello world': {'hi': 'नमस्ते दुनिया', 'es': 'hola mundo', 'fr': 'bonjour le monde'},
        'how are you': {'hi': 'आप कैसे हैं', 'es': 'cómo estás', 'fr': 'comment allez-vous'},
        'good morning': {'hi': 'सुप्रभात', 'es': 'buenos días', 'fr': 'bonjour'},
        'thank you': {'hi': 'धन्यवाद', 'es': 'gracias', 'fr': 'merci'},
        'i love you': {'hi': 'मैं तुमसे प्यार करता हूँ', 'es': 'te amo', 'fr': 'je t\'aime'},
        'my name is': {'hi': 'मेरा नाम है', 'es': 'mi nombre es', 'fr': 'je m\'appelle'}
    }
    
    text_lower = text.lower().strip()
    
    # Check phrases first
    if text_lower in phrases and target_lang in phrases[text_lower]:
        return {
            'success': True,
            'translated_text': phrases[text_lower][target_lang],
            'detected_language': 'English',
            'confidence': 0.95,
            'api_used': 'Simple Translation (Phrase)'
        }
    
    # Word by word translation
    words = text_lower.split()
    translated_words = []
    
    for word in words:
        clean_word = word.strip('.,!?;:"()[]{}')
        if clean_word in translations and target_lang in translations[clean_word]:
            translated_words.append(translations[clean_word][target_lang])
        else:
            translated_words.append(word)
    
    result = ' '.join(translated_words)
    
    return {
        'success': True,
        'translated_text': result,
        'detected_language': 'English',
        'confidence': 0.80,
        'api_used': 'Simple Translation (Word-by-Word)'
    }

def translate_with_enhanced_local_system(text, source_lang, target_lang):
    """Enhanced local translation system with comprehensive word coverage"""
    
    # Comprehensive translation dictionary
    translations = {
        # English to Hindi
        ('hello', 'hi'): 'नमस्ते', ('world', 'hi'): 'दुनिया', ('how', 'hi'): 'कैसे',
        ('are', 'hi'): 'हैं', ('you', 'hi'): 'आप', ('good', 'hi'): 'अच्छा',
        ('morning', 'hi'): 'सुबह', ('afternoon', 'hi'): 'दोपहर', ('evening', 'hi'): 'शाम',
        ('night', 'hi'): 'रात', ('thank', 'hi'): 'धन्यवाद', ('please', 'hi'): 'कृपया',
        ('yes', 'hi'): 'हाँ', ('no', 'hi'): 'नहीं', ('sorry', 'hi'): 'माफ करें',
        ('excuse', 'hi'): 'माफ', ('me', 'hi'): 'मुझे', ('i', 'hi'): 'मैं',
        ('am', 'hi'): 'हूँ', ('is', 'hi'): 'है', ('was', 'hi'): 'था',
        ('will', 'hi'): 'होगा', ('have', 'hi'): 'है', ('has', 'hi'): 'है',
        ('do', 'hi'): 'करना', ('does', 'hi'): 'करता', ('did', 'hi'): 'किया',
        ('can', 'hi'): 'सकता', ('could', 'hi'): 'सकता था', ('should', 'hi'): 'चाहिए',
        ('would', 'hi'): 'होगा', ('may', 'hi'): 'हो सकता', ('might', 'hi'): 'हो सकता',
        ('must', 'hi'): 'जरूर', ('shall', 'hi'): 'होगा', ('will', 'hi'): 'होगा',
        ('the', 'hi'): '', ('a', 'hi'): 'एक', ('an', 'hi'): 'एक',
        ('and', 'hi'): 'और', ('or', 'hi'): 'या', ('but', 'hi'): 'लेकिन',
        ('if', 'hi'): 'अगर', ('then', 'hi'): 'तो', ('else', 'hi'): 'और',
        ('when', 'hi'): 'कब', ('where', 'hi'): 'कहाँ', ('what', 'hi'): 'क्या',
        ('who', 'hi'): 'कौन', ('why', 'hi'): 'क्यों', ('which', 'hi'): 'कौन सा',
        ('this', 'hi'): 'यह', ('that', 'hi'): 'वह', ('these', 'hi'): 'ये',
        ('those', 'hi'): 'वे', ('here', 'hi'): 'यहाँ', ('there', 'hi'): 'वहाँ',
        ('now', 'hi'): 'अब', ('today', 'hi'): 'आज', ('tomorrow', 'hi'): 'कल',
        ('yesterday', 'hi'): 'कल', ('time', 'hi'): 'समय', ('day', 'hi'): 'दिन',
        ('week', 'hi'): 'सप्ताह', ('month', 'hi'): 'महीना', ('year', 'hi'): 'साल',
        ('love', 'hi'): 'प्यार', ('like', 'hi'): 'पसंद', ('want', 'hi'): 'चाहना',
        ('need', 'hi'): 'जरूरत', ('know', 'hi'): 'जानना', ('think', 'hi'): 'सोचना',
        ('see', 'hi'): 'देखना', ('look', 'hi'): 'देखना', ('hear', 'hi'): 'सुनना',
        ('speak', 'hi'): 'बोलना', ('say', 'hi'): 'कहना', ('tell', 'hi'): 'बताना',
        ('ask', 'hi'): 'पूछना', ('answer', 'hi'): 'जवाब', ('help', 'hi'): 'मदद',
        ('work', 'hi'): 'काम', ('study', 'hi'): 'पढ़ाई', ('learn', 'hi'): 'सीखना',
        ('teach', 'hi'): 'सिखाना', ('read', 'hi'): 'पढ़ना', ('write', 'hi'): 'लिखना',
        ('eat', 'hi'): 'खाना', ('drink', 'hi'): 'पीना', ('sleep', 'hi'): 'सोना',
        ('walk', 'hi'): 'चलना', ('run', 'hi'): 'दौड़ना', ('sit', 'hi'): 'बैठना',
        ('stand', 'hi'): 'खड़ा', ('come', 'hi'): 'आना', ('go', 'hi'): 'जाना',
        ('give', 'hi'): 'देना', ('take', 'hi'): 'लेना', ('get', 'hi'): 'पाना',
        ('put', 'hi'): 'रखना', ('make', 'hi'): 'बनाना', ('buy', 'hi'): 'खरीदना',
        ('sell', 'hi'): 'बेचना', ('pay', 'hi'): 'भुगतान', ('money', 'hi'): 'पैसा',
        ('house', 'hi'): 'घर', ('home', 'hi'): 'घर', ('family', 'hi'): 'परिवार',
        ('friend', 'hi'): 'दोस्त', ('name', 'hi'): 'नाम', ('age', 'hi'): 'उम्र',
        ('man', 'hi'): 'आदमी', ('woman', 'hi'): 'औरत', ('child', 'hi'): 'बच्चा',
        ('boy', 'hi'): 'लड़का', ('girl', 'hi'): 'लड़की', ('father', 'hi'): 'पिता',
        ('mother', 'hi'): 'माता', ('brother', 'hi'): 'भाई', ('sister', 'hi'): 'बहन',
        ('big', 'hi'): 'बड़ा', ('small', 'hi'): 'छोटा', ('new', 'hi'): 'नया',
        ('old', 'hi'): 'पुराना', ('hot', 'hi'): 'गर्म', ('cold', 'hi'): 'ठंडा',
        ('fast', 'hi'): 'तेज', ('slow', 'hi'): 'धीमा', ('easy', 'hi'): 'आसान',
        ('hard', 'hi'): 'कठिन', ('happy', 'hi'): 'खुश', ('sad', 'hi'): 'दुखी',
        ('beautiful', 'hi'): 'सुंदर', ('ugly', 'hi'): 'बदसूरत', ('nice', 'hi'): 'अच्छा',
        ('bad', 'hi'): 'बुरा', ('right', 'hi'): 'सही', ('wrong', 'hi'): 'गलत',
        ('true', 'hi'): 'सच', ('false', 'hi'): 'झूठ', ('important', 'hi'): 'महत्वपूर्ण',
        
        # English to Spanish
        ('hello', 'es'): 'hola', ('world', 'es'): 'mundo', ('how', 'es'): 'cómo',
        ('are', 'es'): 'estás', ('you', 'es'): 'tú', ('good', 'es'): 'bueno',
        ('morning', 'es'): 'mañana', ('afternoon', 'es'): 'tarde', ('evening', 'es'): 'noche',
        ('night', 'es'): 'noche', ('thank', 'es'): 'gracias', ('please', 'es'): 'por favor',
        ('yes', 'es'): 'sí', ('no', 'es'): 'no', ('sorry', 'es'): 'lo siento',
        ('excuse', 'es'): 'disculpe', ('me', 'es'): 'me', ('i', 'es'): 'yo',
        ('am', 'es'): 'soy', ('is', 'es'): 'es', ('was', 'es'): 'era',
        ('will', 'es'): 'será', ('have', 'es'): 'tener', ('has', 'es'): 'tiene',
        ('do', 'es'): 'hacer', ('does', 'es'): 'hace', ('did', 'es'): 'hizo',
        ('can', 'es'): 'puede', ('could', 'es'): 'podría', ('should', 'es'): 'debería',
        ('would', 'es'): 'sería', ('may', 'es'): 'puede', ('might', 'es'): 'podría',
        ('must', 'es'): 'debe', ('the', 'es'): 'el', ('a', 'es'): 'un',
        ('and', 'es'): 'y', ('or', 'es'): 'o', ('but', 'es'): 'pero',
        ('if', 'es'): 'si', ('then', 'es'): 'entonces', ('when', 'es'): 'cuándo',
        ('where', 'es'): 'dónde', ('what', 'es'): 'qué', ('who', 'es'): 'quién',
        ('why', 'es'): 'por qué', ('this', 'es'): 'esto', ('that', 'es'): 'eso',
        ('here', 'es'): 'aquí', ('there', 'es'): 'allí', ('now', 'es'): 'ahora',
        ('today', 'es'): 'hoy', ('tomorrow', 'es'): 'mañana', ('yesterday', 'es'): 'ayer',
        ('time', 'es'): 'tiempo', ('day', 'es'): 'día', ('love', 'es'): 'amor',
        ('like', 'es'): 'gustar', ('want', 'es'): 'querer', ('need', 'es'): 'necesitar',
        ('know', 'es'): 'saber', ('see', 'es'): 'ver', ('work', 'es'): 'trabajo',
        ('study', 'es'): 'estudiar', ('learn', 'es'): 'aprender', ('eat', 'es'): 'comer',
        ('drink', 'es'): 'beber', ('house', 'es'): 'casa', ('family', 'es'): 'familia',
        ('friend', 'es'): 'amigo', ('name', 'es'): 'nombre', ('big', 'es'): 'grande',
        ('small', 'es'): 'pequeño', ('new', 'es'): 'nuevo', ('old', 'es'): 'viejo',
        ('happy', 'es'): 'feliz', ('beautiful', 'es'): 'hermoso', ('nice', 'es'): 'agradable',
        
        # English to French  
        ('hello', 'fr'): 'bonjour', ('world', 'fr'): 'monde', ('how', 'fr'): 'comment',
        ('are', 'fr'): 'êtes', ('you', 'fr'): 'vous', ('good', 'fr'): 'bon',
        ('morning', 'fr'): 'matin', ('thank', 'fr'): 'merci', ('please', 'fr'): 's\'il vous plaît',
        ('yes', 'fr'): 'oui', ('no', 'fr'): 'non', ('sorry', 'fr'): 'désolé',
        ('i', 'fr'): 'je', ('am', 'fr'): 'suis', ('is', 'fr'): 'est',
        ('the', 'fr'): 'le', ('a', 'fr'): 'un', ('and', 'fr'): 'et',
        ('love', 'fr'): 'amour', ('like', 'fr'): 'aimer', ('beautiful', 'fr'): 'beau'
    }
    
    # Complete phrases (highest priority)
    phrases = {
        ('hello world', 'hi'): 'नमस्ते दुनिया',
        ('how are you', 'hi'): 'आप कैसे हैं',
        ('good morning', 'hi'): 'सुप्रभात',
        ('good afternoon', 'hi'): 'नमस्कार',
        ('good evening', 'hi'): 'शुभ संध्या',
        ('good night', 'hi'): 'शुभ रात्रि',
        ('thank you', 'hi'): 'धन्यवाद',
        ('i love you', 'hi'): 'मैं तुमसे प्यार करता हूँ',
        ('what is your name', 'hi'): 'आपका नाम क्या है',
        ('my name is', 'hi'): 'मेरा नाम है',
        ('nice to meet you', 'hi'): 'आपसे मिलकर खुशी हुई',
        ('see you later', 'hi'): 'फिर मिलेंगे',
        ('how much', 'hi'): 'कितना',
        ('where is', 'hi'): 'कहाँ है',
        
        ('hello world', 'es'): 'hola mundo',
        ('how are you', 'es'): 'cómo estás',
        ('good morning', 'es'): 'buenos días',
        ('good afternoon', 'es'): 'buenas tardes',
        ('good evening', 'es'): 'buenas noches',
        ('thank you', 'es'): 'gracias',
        ('i love you', 'es'): 'te amo',
        ('what is your name', 'es'): 'cómo te llamas',
        ('my name is', 'es'): 'mi nombre es',
        ('nice to meet you', 'es'): 'mucho gusto',
        ('see you later', 'es'): 'hasta luego',
        
        ('hello world', 'fr'): 'bonjour le monde',
        ('how are you', 'fr'): 'comment allez-vous',
        ('good morning', 'fr'): 'bonjour',
        ('thank you', 'fr'): 'merci',
        ('i love you', 'fr'): 'je t\'aime'
    }
    
    # Combine dictionaries
    all_translations = {**phrases, **translations}
    
    # Clean and normalize input
    text_lower = text.lower().strip()
    
    # Try exact phrase match first
    if (text_lower, target_lang) in all_translations:
        return {
            'success': True,
            'translated_text': all_translations[(text_lower, target_lang)],
            'detected_language': 'English',
            'confidence': 0.95,
            'api_used': 'Enhanced Local System (Exact Match)'
        }
    
    # Try word-by-word translation for longer texts
    words = text_lower.split()
    translated_words = []
    translation_count = 0
    
    for word in words:
        # Remove punctuation for lookup
        clean_word = word.strip('.,!?;:"()[]{}')
        if (clean_word, target_lang) in all_translations:
            translated_word = all_translations[(clean_word, target_lang)]
            if translated_word:  # Skip empty translations like 'the' -> ''
                translated_words.append(translated_word)
                translation_count += 1
            else:
                translated_words.append(word)
        else:
            translated_words.append(word)
    
    # Return translation if we translated at least 30% of words
    if len(words) > 0 and translation_count / len(words) >= 0.3:
        result = ' '.join(translated_words)
        return {
            'success': True,
            'translated_text': result,
            'detected_language': 'English',
            'confidence': min(0.85, 0.5 + (translation_count / len(words)) * 0.4),
            'api_used': 'Enhanced Local System (Word-by-Word)'
        }
    
    # Fallback for unsupported text
    return {
        'success': True,
        'translated_text': f'Translation not available. Try common phrases like: "hello", "how are you", "good morning", "thank you", "i love you"',
        'detected_language': 'English',
        'confidence': 0.50,
        'api_used': 'Enhanced Local System (Fallback)'
    }

def translate_with_mymemory(text, source_lang, target_lang):
    """Use MyMemory Translation API for free translations"""
    try:
        # Skip very short texts that are likely to be in local dictionary
        if len(text.split()) <= 3:
            return None
            
        # MyMemory API endpoint
        url = "https://api.mymemory.translated.net/get"
        
        # Map our language codes to MyMemory codes
        mymemory_codes = {
            'auto': 'en',  # Default auto to English for MyMemory
            'en': 'en',
            'hi': 'hi',
            'fr': 'fr', 
            'es': 'es',
            'de': 'de',
            'zh': 'zh-CN',
            'ja': 'ja',
            'ko': 'ko',
            'ar': 'ar',
            'pt': 'pt',
            'ru': 'ru',
            'it': 'it',
            'nl': 'nl',
            'tr': 'tr'
        }
        
        source_code = mymemory_codes.get(source_lang, 'en')
        target_code = mymemory_codes.get(target_lang, 'es')
        
        # Prepare request parameters
        params = {
            'q': text[:500],  # Limit text length
            'langpair': f'{source_code}|{target_code}'
        }
        
        # Make API request with shorter timeout
        response = requests.get(url, params=params, timeout=8)
        
        if response.status_code == 200:
            result = response.json()
            
            if 'responseData' in result and result['responseData']:
                translated_text = result['responseData']['translatedText']
                
                # Check if translation is valid (not just returning original text)
                if translated_text and translated_text.lower().strip() != text.lower().strip():
                    return {
                        'success': True,
                        'translated_text': translated_text,
                        'detected_language': source_code,
                        'confidence': 0.85,
                        'api_used': 'MyMemory Translation API'
                    }
        
        return None
        
    except Exception as e:
        print(f"MyMemory API error: {e}")
        return None

def translate_with_libretranslate(text, source_lang, target_lang):
    """Use LibreTranslate API for free translations"""
    try:
        # LibreTranslate public API endpoint
        url = "https://libretranslate.de/translate"
        
        # Map our language codes to LibreTranslate codes
        libretranslate_codes = {
            'auto': 'auto',
            'en': 'en',
            'hi': 'hi',
            'fr': 'fr', 
            'es': 'es',
            'de': 'de',
            'zh': 'zh',
            'ja': 'ja',
            'ko': 'ko',
            'ar': 'ar',
            'pt': 'pt',
            'ru': 'ru',
            'it': 'it',
            'nl': 'nl',
            'tr': 'tr'
        }
        
        source_code = libretranslate_codes.get(source_lang, 'en')
        target_code = libretranslate_codes.get(target_lang, 'es')
        
        # Prepare request data
        payload = {
            'q': text,
            'source': source_code,
            'target': target_code,
            'format': 'text'
        }
        
        # Make API request
        response = requests.post(url, json=payload, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            
            if 'translatedText' in result:
                return {
                    'success': True,
                    'translated_text': result['translatedText'],
                    'detected_language': result.get('detectedLanguage', {}).get('language', 'unknown'),
                    'confidence': 0.90,
                    'api_used': 'LibreTranslate API'
                }
        
        return None
        
    except Exception as e:
        print(f"LibreTranslate API error: {e}")
        return None

def translate_with_google_api(text, source_lang, target_lang, api_key):
    """Use Google Translate API for real translations"""
    try:
        # Google Translate API endpoint
        url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}"
        
        # Prepare request data
        payload = {
            'q': text,
            'target': LANGUAGE_CODES.get(target_lang, target_lang),
            'format': 'text'
        }
        
        if source_lang != 'auto':
            payload['source'] = LANGUAGE_CODES.get(source_lang, source_lang)
        
        # Make API request
        response = requests.post(url, data=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            
            if 'data' in result and 'translations' in result['data']:
                translation = result['data']['translations'][0]
                
                return {
                    'success': True,
                    'translated_text': translation['translatedText'],
                    'detected_language': translation.get('detectedSourceLanguage', 'unknown'),
                    'confidence': 0.95,
                    'api_used': 'Google Translate API'
                }
        
        return None
        
    except Exception as e:
        print(f"Google API error: {e}")
        return None

def translate_with_local_dictionary(text, source_lang, target_lang):
    """Enhanced local dictionary with complete phrase translation priority"""
    
    # Comprehensive translation dictionary with complete phrases first
    translations = {
        # Complete phrases (highest priority)
        ('hello world how are you', 'hi'): 'नमस्ते दुनिया आप कैसे हैं',
        ('hello how are you', 'hi'): 'नमस्ते आप कैसे हैं',
        ('hi how are you', 'hi'): 'नमस्ते आप कैसे हैं',
        ('hello world', 'hi'): 'नमस्ते दुनिया',
        ('how are you', 'hi'): 'आप कैसे हैं',
        ('good morning', 'hi'): 'सुप्रभात',
        ('good afternoon', 'hi'): 'नमस्कार',
        ('good evening', 'hi'): 'शुभ संध्या',
        ('good night', 'hi'): 'शुभ रात्रि',
        ('thank you', 'hi'): 'धन्यवाद',
        ('what is your name', 'hi'): 'आपका नाम क्या है',
        ('my name is', 'hi'): 'मेरा नाम है',
        ('see you later', 'hi'): 'फिर मिलेंगे',
        ('i love you', 'hi'): 'मैं तुमसे प्यार करता हूँ',
        ('where is', 'hi'): 'कहाँ है',
        ('how much', 'hi'): 'कितना',
        
        # Spanish complete phrases
        ('hello world how are you', 'es'): 'hola mundo cómo estás',
        ('hello how are you', 'es'): 'hola cómo estás',
        ('hi how are you', 'es'): 'hola cómo estás',
        ('hello world', 'es'): 'hola mundo',
        ('how are you', 'es'): 'cómo estás',
        ('good morning', 'es'): 'buenos días',
        ('good afternoon', 'es'): 'buenas tardes',
        ('good evening', 'es'): 'buenas noches',
        ('good night', 'es'): 'buenas noches',
        ('thank you', 'es'): 'gracias',
        ('what is your name', 'es'): 'cómo te llamas',
        ('my name is', 'es'): 'mi nombre es',
        ('see you later', 'es'): 'hasta luego',
        ('i love you', 'es'): 'te amo',
        ('where is', 'es'): 'dónde está',
        ('how much', 'es'): 'cuánto cuesta',
        
        # French complete phrases
        ('hello world how are you', 'fr'): 'bonjour le monde comment allez-vous',
        ('hello world', 'fr'): 'bonjour le monde',
        ('how are you', 'fr'): 'comment allez-vous',
        ('good morning', 'fr'): 'bonjour',
        ('good afternoon', 'fr'): 'bon après-midi',
        ('good evening', 'fr'): 'bonsoir',
        ('good night', 'fr'): 'bonne nuit',
        ('thank you', 'fr'): 'merci',
        ('what is your name', 'fr'): 'comment vous appelez-vous',
        ('my name is', 'fr'): 'je m\'appelle',
        ('see you later', 'fr'): 'à bientôt',
        ('i love you', 'fr'): 'je t\'aime',
        ('where is', 'fr'): 'où est',
        ('how much', 'fr'): 'combien',
        
        # German complete phrases
        ('hello world how are you', 'de'): 'hallo welt wie geht es dir',
        ('hello world', 'de'): 'hallo welt',
        ('how are you', 'de'): 'wie geht es dir',
        ('good morning', 'de'): 'guten morgen',
        ('good afternoon', 'de'): 'guten tag',
        ('good evening', 'de'): 'guten abend',
        ('good night', 'de'): 'gute nacht',
        ('thank you', 'de'): 'danke',
        ('what is your name', 'de'): 'wie heißt du',
        ('my name is', 'de'): 'ich heiße',
        ('see you later', 'de'): 'bis später',
        ('i love you', 'de'): 'ich liebe dich',
        ('where is', 'de'): 'wo ist',
        ('how much', 'de'): 'wie viel',
        
        # Chinese complete phrases
        ('hello world how are you', 'zh'): '你好世界你好吗',
        ('hello world', 'zh'): '你好世界',
        ('how are you', 'zh'): '你好吗',
        ('good morning', 'zh'): '早上好',
        ('good afternoon', 'zh'): '下午好',
        ('good evening', 'zh'): '晚上好',
        ('good night', 'zh'): '晚安',
        ('thank you', 'zh'): '谢谢',
        ('what is your name', 'zh'): '你叫什么名字',
        ('my name is', 'zh'): '我的名字是',
        ('see you later', 'zh'): '回头见',
        ('i love you', 'zh'): '我爱你',
        ('where is', 'zh'): '在哪里',
        ('how much', 'zh'): '多少钱',
        
        # Japanese complete phrases
        ('hello world how are you', 'ja'): 'こんにちは世界元気ですか',
        ('hello world', 'ja'): 'こんにちは世界',
        ('how are you', 'ja'): '元気ですか',
        ('good morning', 'ja'): 'おはよう',
        ('good afternoon', 'ja'): 'こんにちは',
        ('good evening', 'ja'): 'こんばんは',
        ('good night', 'ja'): 'おやすみ',
        ('thank you', 'ja'): 'ありがとう',
        ('what is your name', 'ja'): 'お名前は何ですか',
        ('my name is', 'ja'): '私の名前は',
        ('see you later', 'ja'): 'また後で',
        ('i love you', 'ja'): '愛してる',
        ('where is', 'ja'): 'どこですか',
        ('how much', 'ja'): 'いくら',
        
        # Individual words (lower priority)
        ('hello', 'hi'): 'नमस्ते',
        ('world', 'hi'): 'दुनिया',
        ('how', 'hi'): 'कैसे',
        ('are', 'hi'): 'हैं',
        ('you', 'hi'): 'आप',
        ('good', 'hi'): 'अच्छा',
        ('morning', 'hi'): 'सुबह',
        ('thank', 'hi'): 'धन्यवाद',
        ('please', 'hi'): 'कृपया',
        ('yes', 'hi'): 'हाँ',
        ('no', 'hi'): 'नहीं',
        ('sorry', 'hi'): 'माफ करें',
        ('excuse', 'hi'): 'माफ',
        ('me', 'hi'): 'मुझे',
        ('i', 'hi'): 'मैं',
        ('am', 'hi'): 'हूँ',
        ('fine', 'hi'): 'ठीक',
        ('today', 'hi'): 'आज',
        ('tomorrow', 'hi'): 'कल',
        ('yesterday', 'hi'): 'कल',
        ('goodbye', 'hi'): 'अलविदा',
        
        # Spanish individual words
        ('hello', 'es'): 'hola',
        ('world', 'es'): 'mundo',
        ('how', 'es'): 'cómo',
        ('are', 'es'): 'estás',
        ('you', 'es'): 'tú',
        ('good', 'es'): 'bueno',
        ('morning', 'es'): 'mañana',
        ('thank', 'es'): 'gracias',
        ('please', 'es'): 'por favor',
        ('yes', 'es'): 'sí',
        ('no', 'es'): 'no',
        ('sorry', 'es'): 'lo siento',
        ('excuse', 'es'): 'disculpe',
        ('me', 'es'): 'me',
        ('i', 'es'): 'yo',
        ('am', 'es'): 'soy',
        ('fine', 'es'): 'bien',
        ('today', 'es'): 'hoy',
        ('tomorrow', 'es'): 'mañana',
        ('yesterday', 'es'): 'ayer',
        ('goodbye', 'es'): 'adiós',
        
        # French individual words
        ('hello', 'fr'): 'bonjour',
        ('world', 'fr'): 'monde',
        ('how', 'fr'): 'comment',
        ('are', 'fr'): 'êtes',
        ('you', 'fr'): 'vous',
        ('good', 'fr'): 'bon',
        ('morning', 'fr'): 'matin',
        ('thank', 'fr'): 'merci',
        ('please', 'fr'): 's\'il vous plaît',
        ('yes', 'fr'): 'oui',
        ('no', 'fr'): 'non',
        ('sorry', 'fr'): 'désolé',
        ('excuse', 'fr'): 'excusez',
        ('me', 'fr'): 'moi',
        ('i', 'fr'): 'je',
        ('am', 'fr'): 'suis',
        ('fine', 'fr'): 'bien',
        ('today', 'fr'): 'aujourd\'hui',
        ('tomorrow', 'fr'): 'demain',
        ('yesterday', 'fr'): 'hier',
        ('goodbye', 'fr'): 'au revoir'
    }
    
    # Clean and normalize the input text
    text_lower = text.lower().strip()
    
    # Try exact match first (complete phrases have highest priority)
    key = (text_lower, target_lang)
    if key in translations:
        return {
            'success': True,
            'translated_text': translations[key],
            'detected_language': 'English',
            'confidence': 0.95,
            'api_used': 'Local Dictionary (Exact Match)'
        }
    
    # Try to find the longest matching phrases first
    import re
    
    # Sort phrases by length (longest first) to prioritize complete phrases
    phrase_translations = [(phrase, lang, trans) for (phrase, lang), trans in translations.items() 
                          if lang == target_lang and len(phrase.split()) > 1]
    phrase_translations.sort(key=lambda x: len(x[0].split()), reverse=True)
    
    # Check if the entire text matches any complete phrase exactly
    for phrase, lang, translation in phrase_translations:
        if text_lower.strip() == phrase:
            return {
                'success': True,
                'translated_text': translation,
                'detected_language': 'English',
                'confidence': 0.95,
                'api_used': 'Local Dictionary (Complete Phrase Match)'
            }
    
    # If no exact phrase match, check for single word translations
    words = text_lower.split()
    if len(words) == 1:
        word_key = (words[0], target_lang)
        if word_key in translations:
            return {
                'success': True,
                'translated_text': translations[word_key],
                'detected_language': 'English',
                'confidence': 0.85,
                'api_used': 'Local Dictionary (Single Word)'
            }
    
    # If no phrase matches, provide a basic word-by-word translation attempt
    words = text_lower.split()
    translated_words = []
    
    for word in words:
        word_key = (word, target_lang)
        if word_key in translations:
            translated_words.append(translations[word_key])
        else:
            # Keep original word if no translation found
            translated_words.append(word)
    
    # If we translated at least some words, return the result
    if any(word in [trans for (phrase, lang), trans in translations.items() if lang == target_lang] for word in translated_words):
        final_translation = ' '.join(translated_words)
        return {
            'success': True,
            'translated_text': final_translation,
            'detected_language': 'English',
            'confidence': 0.60,
            'api_used': 'Local Dictionary (Partial Translation)'
        }
    
    # Final fallback message
    return {
        'success': True,
        'translated_text': f'Translation service temporarily unavailable. Supported phrases: hello, how are you, good morning, thank you, i love you, etc.',
        'detected_language': 'English',
        'confidence': 0.50,
        'api_used': 'Fallback - Service Unavailable'
    }
