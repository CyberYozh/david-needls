import difflib
import re
from collections import Counter

# Нормализация текста: убираем всё кроме букв/цифр и приводим к нижнему регистру
def normalize(text):
    return re.sub(r'\W+', '', text.lower())

# Сравнение никнеймов (коэффициент схожести)
def username_similarity(u1, u2):
    return difflib.SequenceMatcher(None, u1, u2).ratio()

# Подсчёт частоты символов в тексте
def char_frequency(text):
    text = normalize(text)
    return Counter(text)

# Простая косинусная схожесть
def cosine_similarity(c1, c2):
    all_keys = set(c1.keys()).union(set(c2.keys()))
    v1 = [c1.get(k, 0) for k in all_keys]
    v2 = [c2.get(k, 0) for k in all_keys]

    dot = sum(a*b for a, b in zip(v1, v2))
    mag1 = sum(a*a for a in v1) ** 0.5
    mag2 = sum(b*b for b in v2) ** 0.5

    if mag1 == 0 or mag2 == 0:
        return 0

    return dot / (mag1 * mag2)

# Сравнение текстов по стилю
def text_similarity(t1, t2):
    c1 = char_frequency(t1)
    c2 = char_frequency(t2)
    return cosine_similarity(c1, c2)

# Основная функция сравнения аккаунтов
def compare_accounts(acc1, acc2):
    print("=== СРАВНЕНИЕ АККАУНТОВ ===\n")

    u_sim = username_similarity(acc1['username'], acc2['username'])
    print(f"Схожесть никнеймов: {u_sim:.2f}")

    t_sim = text_similarity(acc1['text'], acc2['text'])
    print(f"Схожесть текстового стиля: {t_sim:.2f}")

    score = (u_sim + t_sim) / 2
    print(f"\nОбщий коэффициент схожести: {score:.2f}")

    if score > 0.75:
        print("⚠️ Высокая схожесть (возможно один пользователь)")
    elif score > 0.5:
        print("⚠️ Средняя схожесть (нужно больше данных)")
    else:
        print("Низкая схожесть")

# === Чтение текста из файлов ===
def load_text(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

acc1 = {
    "username": "super_crow_123_xdd",
    "text": load_text("file1.txt")
}

acc2 = {
    "username": "supercrowxdd",
    "text": load_text("file2.txt")
}

acc3 = {
    "username": "random_player_998",
    "text": load_text("file3.txt")
}

# Сравнения
print("\nСравнение 1 и 2:")
compare_accounts(acc1, acc2)

print("\nСравнение 1 и 3:")
compare_accounts(acc1, acc3)

compare_accounts(acc1, acc2)
