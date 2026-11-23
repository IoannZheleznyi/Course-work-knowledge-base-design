
import os
import re
import requests
import xml.etree.ElementTree as ET

from functools import lru_cache
from urllib.parse import quote_plus


REQUEST_TIMEOUT = 12

HEADERS = {
    "User-Agent": "SpiceSearch/1.0 (educational knowledge base)"
}

WIKIPEDIA_API = "https://ru.wikipedia.org/w/api.php"


# Известные названия специй и соответствующие статьи Википедии.
# Если специи здесь нет, система попробует определить её через Википедию.
WIKIPEDIA_ALIASES = {
    "анис": ["Анис"],
    "базилик": ["Базилик"],
    "белый перец": ["Перец белый", "Белый перец"],
    "гвоздика": ["Гвоздика (пряность)", "Гвоздика"],
    "горчица": ["Горчица (приправа)", "Горчица"],
    "зира": ["Зира", "Кумин"],
    "имбирь": ["Имбирь"],
    "кардамон": ["Кардамон"],
    "кориандр": ["Кориандр"],
    "корица": ["Корица"],
    "красный перец": ["Перец красный", "Красный перец"],
    "куркума": ["Куркума"],
    "мускатный орех": ["Мускатный орех"],
    "орегано": ["Душица обыкновенная", "Орегано"],
    "паприка": ["Паприка (специя)", "Паприка"],
    "розмарин": ["Розмарин"],
    "тимьян": ["Тимьян", "Чабрец"],
    "фенхель": ["Фенхель"],
    "чёрный перец": ["Перец чёрный", "Чёрный перец"],
    "шафран": ["Шафран"],
    "ваниль": ["Ваниль"],
    "бадьян": ["Бадьян настоящий", "Бадьян"],
    "пажитник": ["Пажитник сенной", "Пажитник"],
    "душистый перец": ["Душистый перец"],
    "лавровый лист": ["Лавровый лист"],
    "майоран": ["Майоран"],
    "эстрагон": ["Эстрагон"],
    "кунжут": ["Кунжут"]
}


# Английские названия для поиска изображений.
WIKIMEDIA_IMAGE_NAMES = {
    "анис": "anise",
    "базилик": "basil",
    "белый перец": "white pepper",
    "гвоздика": "cloves",
    "горчица": "mustard",
    "зира": "cumin",
    "имбирь": "ginger",
    "кардамон": "cardamom",
    "кориандр": "coriander",
    "корица": "cinnamon",
    "красный перец": "red chili pepper",
    "куркума": "turmeric",
    "мускатный орех": "nutmeg",
    "орегано": "oregano",
    "паприка": "paprika",
    "розмарин": "rosemary",
    "тимьян": "thyme",
    "фенхель": "fennel",
    "чёрный перец": "black pepper",
    "шафран": "saffron",
    "ваниль": "vanilla",
    "бадьян": "star anise",
    "пажитник": "fenugreek",
    "душистый перец": "allspice",
    "лавровый лист": "bay leaf",
    "майоран": "marjoram",
    "эстрагон": "tarragon",
    "кунжут": "sesame"
}


def normalize_text(value):
    """Приводит текст к единому виду для сравнения."""
    value = (value or "").lower().replace("ё", "е")
    value = re.sub(r"[^а-яa-z0-9]+", " ", value)
    return " ".join(value.split())


def is_spice_article(title, extract, categories):
    """Проверяет, похожа ли статья Википедии на статью о специи."""
    spice_words = (
        "пряност",
        "специ",
        "приправа",
        "приправ",
        "пряное растение",
        "пряный"
    )

    category_text = " ".join(categories).lower()
    article_text = (title + " " + extract[:1800]).lower()

    if any(word in category_text for word in spice_words):
        return True

    return any(word in article_text for word in spice_words)


@lru_cache(maxsize=256)
def find_spice_in_wikipedia(normalized_query):
    """Ищет неизвестную специю в русской Википедии."""

    if not normalized_query:
        return None

    try:
        response = requests.get(
            WIKIPEDIA_API,
            params={
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": normalized_query,
                "srnamespace": 0,
                "srlimit": 10
            },
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()

        results = response.json().get("query", {}).get("search", [])

        matching_titles = []

        for item in results:
            title = item.get("title", "")
            normalized_title = normalize_text(title)

            if (
                normalized_title == normalized_query
                or normalized_title.startswith(normalized_query + " ")
            ):
                matching_titles.append(title)

        for title in matching_titles:
            page_response = requests.get(
                WIKIPEDIA_API,
                params={
                    "action": "query",
                    "format": "json",
                    "prop": "extracts|categories",
                    "exintro": 1,
                    "explaintext": 1,
                    "cllimit": 50,
                    "titles": title,
                    "redirects": 1
                },
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT
            )
            page_response.raise_for_status()

            pages = page_response.json().get(
                "query", {}
            ).get("pages", {})

            for page in pages.values():
                if page.get("missing"):
                    continue

                page_title = page.get("title", "")
                extract = page.get("extract", "").strip()

                categories = [
                    category.get("title", "")
                    for category in page.get("categories", [])
                ]

                if not extract:
                    continue

                if is_spice_article(
                    page_title,
                    extract,
                    categories
                ):
                    return page_title

    except (requests.RequestException, ValueError, KeyError):
        return None

    return None


def get_spice_name(query):
    """Определяет название специи по запросу."""
    normalized_query = normalize_text(query)

    if not normalized_query:
        return None

    # Сначала проверяем известные названия.
    for spice_name in WIKIPEDIA_ALIASES:
        normalized_name = normalize_text(spice_name)

        if (
            normalized_query == normalized_name
            or normalized_query.startswith(normalized_name + " ")
        ):
            return spice_name

    # Если названия нет в словаре, проверяем его через Википедию.
    return find_spice_in_wikipedia(normalized_query)


def contains_spice(text, spice_name):
    """Проверяет, упоминается ли нужная специя в тексте."""
    normalized_text = normalize_text(text)
    normalized_name = normalize_text(spice_name)

    return bool(
        re.search(
            rf"(?<![а-яa-z0-9]){re.escape(normalized_name)}(?![а-яa-z0-9])",
            normalized_text
        )
    )


def search_description(query):
    """Ищет описание специи в русской Википедии."""
    spice_name = get_spice_name(query)

    if not spice_name:
        return None

    try:
        aliases = WIKIPEDIA_ALIASES.get(spice_name, [spice_name])

        response = requests.get(
            WIKIPEDIA_API,
            params={
                "action": "query",
                "format": "json",
                "prop": "extracts|info",
                "exintro": 1,
                "explaintext": 1,
                "inprop": "url",
                "redirects": 1,
                "titles": "|".join(aliases)
            },
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()
        pages = data.get("query", {}).get("pages", {})

        allowed_titles = {
            normalize_text(title)
            for title in aliases
        }

        for page in pages.values():
            title = page.get("title", "")
            extract = page.get("extract", "").strip()

            if page.get("missing") or not extract:
                continue

            if normalize_text(title) not in allowed_titles:
                continue

            return {
                "title": title,
                "text": extract,
                "url": page.get("fullurl") or (
                    "https://ru.wikipedia.org/wiki/"
                    + quote_plus(title.replace(" ", "_"))
                ),
                "source_name": "Русская Википедия"
            }

        return None

    except (requests.RequestException, ValueError, KeyError):
        return None


def translate_to_english(query):
    """Переводит название специи на английский."""
    try:
        response = requests.get(
            "https://api.mymemory.translated.net/get",
            params={
                "q": query,
                "langpair": "ru|en"
            },
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        translated = (
            data.get("responseData", {})
            .get("translatedText", "")
            .strip()
        )

        if translated:
            return translated

    except (requests.RequestException, ValueError, KeyError):
        pass

    return query


def search_images(query, limit=12):
    """Ищет изображения специи на Wikimedia Commons."""
    spice_name = get_spice_name(query)

    if not spice_name:
        return []

    search_name = WIKIMEDIA_IMAGE_NAMES.get(spice_name)

    if not search_name:
        search_name = translate_to_english(spice_name)

    url = "https://commons.wikimedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": search_name,
        "gsrnamespace": 6,
        "gsrlimit": limit,
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": 600
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()
        pages = data.get("query", {}).get("pages", {})

        results = []

        for page in pages.values():
            image_info_list = page.get("imageinfo", [])

            if not image_info_list:
                continue

            image_info = image_info_list[0]

            image_url = (
                image_info.get("thumburl")
                or image_info.get("url")
            )

            if not image_url:
                continue

            results.append({
                "title": page.get("title", "").replace("File:", ""),
                "image_url": image_url,
                "source_url": image_info.get("descriptionurl")
                or "https://commons.wikimedia.org/"
            })

            if len(results) >= limit:
                break

        return results

    except (requests.RequestException, ValueError, KeyError):
        return []


def search_videos(query, limit=8):
    """Ищет видеоролики о конкретной специи через YouTube Data API."""
    spice_name = get_spice_name(query)

    if not spice_name:
        return []

    api_key = os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        return []

    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": f"{spice_name} специя",
        "type": "video",
        "maxResults": limit * 2,
        "relevanceLanguage": "ru",
        "regionCode": "RU",
        "key": api_key
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()
        results = []

        for item in data.get("items", []):
            video_id = item.get("id", {}).get("videoId")

            if not video_id:
                continue

            snippet = item.get("snippet", {})
            title = snippet.get("title", "")
            description = snippet.get("description", "")

            if not contains_spice(
                title + " " + description,
                spice_name
            ):
                continue

            thumbnails = snippet.get("thumbnails", {})

            thumbnail = (
                thumbnails.get("high")
                or thumbnails.get("medium")
                or thumbnails.get("default")
                or {}
            )

            results.append({
                "title": title,
                "description": description,
                "thumbnail": thumbnail.get("url"),
                "video_url": f"https://www.youtube.com/watch?v={video_id}",
                "published_at": snippet.get("publishedAt", ""),
                "source_name": snippet.get("channelTitle", "YouTube")
            })

            if len(results) >= limit:
                break

        return results

    except (requests.RequestException, ValueError, KeyError):
        return []


def search_news(query, limit=10):
    """Ищет русскоязычные статьи и новости о конкретной специи."""
    spice_name = get_spice_name(query)

    if not spice_name:
        return []

    url = (
        "https://news.google.com/rss/search?"
        f"q={quote_plus('"' + spice_name + '"')}"
        "&hl=ru&gl=RU&ceid=RU:ru"
    )

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        root = ET.fromstring(response.content)
        results = []

        for item in root.findall(".//item"):
            title = item.findtext("title", default="")
            description = item.findtext("description", default="")

            if not contains_spice(
                title + " " + description,
                spice_name
            ):
                continue

            link = item.findtext("link", default="")
            pub_date = item.findtext("pubDate", default="")
            source_element = item.find("source")

            source = (
                source_element.text
                if source_element is not None
                else "Интернет-источник"
            )

            results.append({
                "title": title,
                "url": link,
                "published_at": pub_date,
                "source_name": source
            })

            if len(results) >= limit:
                break

        return results

    except (requests.RequestException, ET.ParseError, ValueError):
        return []


def search_internet(query):
    """Запускает поиск только по запросам, относящимся к специям."""
    if not get_spice_name(query):
        return {
            "description": None,
            "images": [],
            "videos": [],
            "news": [],
            "youtube_configured": bool(os.getenv("YOUTUBE_API_KEY"))
        }

    return {
        "description": search_description(query),
        "images": search_images(query),
        "videos": search_videos(query),
        "news": search_news(query),
        "youtube_configured": bool(os.getenv("YOUTUBE_API_KEY"))
    }
