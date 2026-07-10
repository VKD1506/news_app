import json
from config import Config


def evaluate_article(title, content):
    # If GROQ API key is not configured, return a neutral result
    if not Config.GROQ_API_KEY:
        return {"is_authentic": None, "reason": "Missing GROQ_API_KEY"}

    try:
        from groq import Groq
    except ImportError:
        return {"is_authentic": None, "reason": "GROQ support is unavailable in this build."}

    client = Groq(api_key=Config.GROQ_API_KEY)

    prompt = f"""
    You are a strict helper. Look at this article. Is it real or fake? 
    Look out for lies, massive bias, or clickbait.
    
    Title: {title}
    Content: {content[:1000]}
    
    Respond strictly in JSON format like this:
    {{"is_authentic": true or false, "reason": "one short sentence summary"}}
    """

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            response_format={"type": "json_object"}
        )

        # Try to robustly extract the assistant content whether response
        # is a dict or an object with attributes.
        content_text = None
        if isinstance(response, dict):
            choices = response.get("choices") or []
            if choices:
                first = choices[0]
                msg = first.get("message") or {}
                content_text = msg.get("content") or first.get("text")
        else:
            choices = getattr(response, "choices", None)
            if isinstance(choices, list) and len(choices) > 0:
                choice = choices[0]
                if hasattr(choice, "message") and hasattr(choice.message, "content"):
                    content_text = choice.message.content
                elif hasattr(choice, "text"):
                    content_text = choice.text

        if content_text:
            return json.loads(content_text)

    except Exception:
        pass

    return {"is_authentic": False, "reason": "Error checking this article."}
