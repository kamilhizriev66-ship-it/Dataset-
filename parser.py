from datetime import datetime  # Добавили импорт для работы с датами
import os
import time
import xml.etree.ElementTree as ET
from xml.dom import minidom
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

RSS_FEEDS = [
    "https://tass.ru/rss/v2.xml",
    "https://www.interfax.ru/rss.asp",
    "https://lenta.ru/rss",
    "https://ria.ru/export/rss2/archive/index.xml",
    "https://www.kommersant.ru/RSS/news.xml",
    "https://rssexport.rbc.ru/rbcnews/news/30/full.rss",
    "https://rg.ru/xml/index.xml"
]


def fetch_rss(url):
    """Загружает одну RSS-ленту и возвращает список новостей."""
    items = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()

        root = ET.fromstring(resp.content)

        for item in root.iter("item"):
            news = {
                "title": (item.findtext("title") or "").strip(),
                "link": (item.findtext("link") or "").strip(),
                "description": (item.findtext("description") or "").strip(),
                "pubDate": (item.findtext("pubDate") or "").strip(),
                "category": (item.findtext("category") or "").strip(),
                "source": url.split("/")[2],
            }
            if news["title"]:
                items.append(news)

        print(f"[OK] {url} — {len(items)} записей")
    except Exception as e:
        print(f"[ОШИБКА] {url}: {e}")

    return items


def collect_all_news(feeds=None, delay=2.0):
    """Собирает новости из всех RSS, убирает дубли по заголовку."""
    if feeds is None:
        feeds = RSS_FEEDS

    all_news = []
    seen = set()

    for url in feeds:
        for news in fetch_rss(url):
            if news["title"] not in seen:
                seen.add(news["title"])
                all_news.append(news)
        time.sleep(delay)

    print(f"\nВсего собрано за этот запуск: {len(all_news)} новостей")
    return all_news


def save_batch_to_xml(new_items, folder="news_dataset"):
    """Сохраняет порцию новостей в отдельный XML-файл с временной меткой."""
    if not new_items:
        print("Нет новостей для сохранения.")
        return

    # Создаем папку для датасета, если её еще нет
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Формируем имя файла: например, "news_2026-05-24_15-30-45.xml"
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"news_{current_time}.xml"
    file_path = os.path.join(folder, file_name)

    # Создаем XML-структуру для этой порции
    root = ET.Element("news_batch")
    root.set("created_at", current_time)

    for news in new_items:
        item_node = ET.SubElement(root, "item")
        for key, value in news.items():
            child = ET.SubElement(item_node, key)
            child.text = str(value)

    # Красивое форматирование с отступами
    xml_string = ET.tostring(root, encoding="utf-8")
    parsed_string = minidom.parseString(xml_string)
    pretty_xml = parsed_string.toprettyxml(indent="  ", encoding="utf-8")

    # Записываем в файл
    with open(file_path, "wb") as f:
        f.write(pretty_xml)

    print(f"[БАЗА] Данные сохранены в файл: {file_path}\n")


if __name__ == "__main__":
    # 1. Собираем новости со всех сайтов
    data = collect_all_news()

    # 2. Вместо простого print() вызываем функцию сохранения в файл
    save_batch_to_xml(data)

