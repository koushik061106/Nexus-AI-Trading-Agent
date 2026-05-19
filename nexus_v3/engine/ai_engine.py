import time
import requests
import logging
import json
import config

log = logging.getLogger(__name__)

def call_ai(prompt: str, max_tokens: int = 1500) -> str | None:
    """
    Call Groq with automatic fallback chain.
    Returns clean JSON string or None if all fail.
    """
    
    # ALWAYS add to every prompt:
    instruction = (
        "\n\nReturn RAW JSON only. No markdown. No code blocks. "
        "No backticks. No explanations. Just the JSON object."
    )
    if instruction not in prompt:
        prompt += instruction

    providers = [
        {
            "url": "https://api.groq.com/openai/v1/chat/completions",
            "key": config.GROQ_API_KEY,
            "models": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant",
                       "gemma2-9b-it", "mixtral-8x7b-32768"]
        },
        {
            "url": "https://openrouter.ai/api/v1/chat/completions",
            "key": config.OPENROUTER_API_KEY,
            "models": []  # Auto-fetch live free models, or use config fallback
        }
    ]
    
    # If OpenRouter model is configured, add it to the models list
    if config.OPENROUTER_MODEL:
        providers[1]["models"].append(config.OPENROUTER_MODEL)
    else:
        # Generic fallback for openrouter
        providers[1]["models"].append("mistralai/mistral-7b-instruct:free")

    for provider in providers:
        if not provider["key"]:
            continue
            
        for model in provider["models"]:
            try:
                headers = {
                    "Authorization": f"Bearer {provider['key']}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://nexus-trader.local",
                    "X-Title": "NEXUS AI Trader v3"
                }
                data = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": 0.1
                }
                
                response = requests.post(
                    provider["url"], headers=headers,
                    json=data, timeout=30
                )
                
                try:
                    result = response.json()
                except Exception:
                    continue

                if response.status_code == 429:
                    time.sleep(3)
                    continue
                if response.status_code == 404:
                    continue
                if "error" in result:
                    continue
                if "choices" not in result:
                    continue

                raw = result["choices"][0]["message"]["content"].strip()

                # Strip markdown code blocks
                for prefix in ["```json", "```"]:
                    if raw.startswith(prefix):
                        raw = raw[len(prefix):]
                if raw.endswith("```"):
                    raw = raw[:-3]
                raw = raw.strip()

                log.info(f"AI success: {provider['url']} / {model}")
                return raw

            except Exception as e:
                log.warning(f"{model}: {e}")
                continue

    log.error("All AI providers failed — defaulting to HOLD")
    return None
