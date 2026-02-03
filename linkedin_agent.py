import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


def generate_ice_breakers(bio_text: str, api_provider: str = "openai") -> list[str]:
    """
    Генерирует 3 персонализированных сообщения для знакомства на основе био профиля LinkedIn.
    
    Args:
        bio_text: Текст био из LinkedIn профиля
        api_provider: "openai" или "anthropic"
    
    Returns:
        Список из 3 персонализированных сообщений
    """
    
    if api_provider == "openai":
        return generate_with_openai(bio_text)
    elif api_provider == "anthropic":
        return generate_with_anthropic(bio_text)
    else:
        raise ValueError(f"Неподдерживаемый провайдер: {api_provider}")


def generate_with_openai(bio_text: str) -> list[str]:
    """Генерация сообщений через OpenAI API"""
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY не найден в переменных окружения")
    
    client = OpenAI(api_key=api_key)
    
    prompt = f"""Проанализируй следующий профиль LinkedIn и создай 3 варианта персонализированных сообщений для знакомства (ice-breakers).

Профиль:
{bio_text}

Требования к сообщениям:
1. На русском языке
2. Каждое сообщение строго не более 200 символов
3. Без официоза - выбери сам стиль общения: "на ты" или "вежливое на вы"
4. Персонализированные, основанные на конкретных деталях профиля
5. Естественные, дружелюбные и располагающие к диалогу
6. Каждое сообщение должно иметь свой уникальный подход

Верни только 3 сообщения, каждое с новой строки, без нумерации и дополнительных комментариев."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты эксперт по нетворкингу и составлению персонализированных сообщений для LinkedIn. Твои сообщения естественные, дружелюбные и эффективные."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=500
    )
    
    
    messages_text = response.choices[0].message.content.strip()
    messages = [msg.strip() for msg in messages_text.split('\n') if msg.strip()]
    
    
    valid_messages = [msg for msg in messages if len(msg) <= 200 and len(msg) > 10]
    
    return valid_messages[:3]


def generate_with_anthropic(bio_text: str) -> list[str]:
    """Генерация сообщений через Anthropic API"""
    
    try:
        from anthropic import Anthropic
    except ImportError:
        raise ImportError("Установите anthropic: pip install anthropic")
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY не найден в переменных окружения")
    
    client = Anthropic(api_key=api_key)
    
    prompt = f"""Проанализируй следующий профиль LinkedIn и создай 3 варианта персонализированных сообщений для знакомства (ice-breakers).

Профиль:
{bio_text}

Требования к сообщениям:
1. На русском языке
2. Каждое сообщение строго не более 200 символов
3. Без официоза - выбери сам стиль общения: "на ты" или "вежливое на вы"
4. Персонализированные, основанные на конкретных деталях профиля
5. Естественные, дружелюбные и располагающие к диалогу
6. Каждое сообщение должно иметь свой уникальный подход

Верни только 3 сообщения, каждое с новой строки, без нумерации и дополнительных комментариев."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        temperature=0.8,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    
    messages_text = message.content[0].text.strip()
    messages = [msg.strip() for msg in messages_text.split('\n') if msg.strip()]
    
    
    valid_messages = [msg for msg in messages if len(msg) <= 200 and len(msg) > 10]
    
    return valid_messages[:3]


def main():
    
    profile_bio = """Ахат, основатель ТОО в Казахстане. Занимаюсь оценкой, консалтингом и логистикой. 
Сейчас внедряю ИИ-агентов в свои бизнес-процессы, чтобы автоматизировать холодные продажи в LinkedIn 
и обработку заказов в WhatsApp. Ищу в команду быстрых разработчиков."""
    
    print("=" * 80)
    print("Мини-агент для LinkedIn: Генерация персонализированных сообщений")
    print("=" * 80)
    print(f"\nАнализируемый профиль:\n{profile_bio}\n")
    print("=" * 80)
    
    
    import sys
    provider = sys.argv[1] if len(sys.argv) > 1 else "openai"
    
    print(f"\nИспользуется API: {provider.upper()}")
    print("\nГенерирую персонализированные сообщения...\n")
    
    try:
        ice_breakers = generate_ice_breakers(profile_bio, api_provider=provider)
        
        print("=" * 80)
        print("РЕЗУЛЬТАТ: 3 варианта персонализированных сообщений")
        print("=" * 80)
        
        for i, message in enumerate(ice_breakers, 1):
            print(f"\n[Вариант {i}] ({len(message)} символов)")
            print(f"├─ {message}")
        
        print("\n" + "=" * 80)
        print("✓ Генерация завершена успешно!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        print("\nПроверьте:")
        print("1. Наличие файла .env с API ключом")
        print("2. Правильность API ключа")
        print("3. Установленные зависимости (pip install -r requirements.txt)")


if __name__ == "__main__":
    main()
