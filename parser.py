from datetime import datetime
import os
import time
import xml.etree.ElementTree as ET
from xml.dom import minidom
import requests

def parse_and_save_news():
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    #
    RSS_FEEDS = [
        #LENTA.RU
        "https://lenta.ru/rss",
        "https://lenta.ru/rss/news",
        "https://lenta.ru/rss/articles",
        "https://lenta.ru/rss/top7",
        #ВЕДОМОСТИ
        "https://www.vedomosti.ru/rss/news.xml",
        "https://www.vedomosti.ru/rss/issue.xml",
        "https://www.vedomosti.ru/rss/articles.xml",

        #КОММЕРСАНТЪ
        "https://www.kommersant.ru/RSS/news.xml",
        "https://www.kommersant.ru/RSS/main.xml",
        "https://www.kommersant.ru/RSS/money.xml",
        "https://www.kommersant.ru/RSS/auto.xml",
        "https://www.kommersant.ru/RSS/weekend.xml",

        #РБК
        "https://rssexport.rbc.ru/rbcnews/news/100/full.rss",
        "https://rssexport.rbc.ru/rbcnews/news/30/full.rss",

        #ХАБР
        "https://habr.com/ru/rss/articles/all/?fl=ru",
        "https://habr.com/ru/rss/news/all/?fl=ru",
        "https://habr.com/ru/rss/best/daily/?fl=ru",
        "https://habr.com/ru/rss/best/weekly/?fl=ru",
        "https://habr.com/ru/rss/best/monthly/?fl=ru",
        "https://habr.com/ru/rss/hub/programming/all/?fl=ru",
        "https://habr.com/ru/rss/hub/python/all/?fl=ru",
        "https://habr.com/ru/rss/hub/infosecurity/all/?fl=ru",
        "https://habr.com/ru/rss/hub/webdev/all/?fl=ru",

        #VC.RU
        "https://vc.ru/rss/all",

        #DTF.RU
        "https://dtf.ru/rss/all",

        #3DNEWS
        "https://www.3dnews.ru/news/rss/",
        
        #КРУПНЫЕ РЕГИОНАЛЬНЫЕ СМИ
        "https://www.e1.ru/text/rss.xml",
        "https://www.ngs.ru/text/rss.xml",
        "https://www.74.ru/text/rss.xml",
        "https://www.63.ru/text/rss.xml",
        "https://www.59.ru/text/rss.xml",
        "https://www.76.ru/text/rss.xml",
        "https://www.116.ru/text/rss.xml",
        #ФЕДЕРАЛЬНЫЕ АГЕНТСТВА И ГАЗЕТЫ
        "https://tass.ru/rss/v2.xml",
        "https://www.interfax.ru/rss.asp",
        "https://rg.ru/xml/index.xml",


        #СПОРТ, КИНО И ГЕЙМДЕВ (8 лент)
        "https://www.kinonews.ru/rss/",
        "https://www.film.ru/rss.xml",
        "https://www.igromania.ru/rss/news.xml",
        "https://stopgame.ru/rss/rss_news.xml",

        #ТЕХНОЛОГИИ И НАУКА
        "https://www.cnews.ru/inc/rss/news.xml",
        "https://ixbt.com/export/news.rss",
        "https://ixbt.com/export/articles.rss",
        "https://naked-science.ru/feed",
        "https://www.banki.ru/xml/news.rss",
        "https://tproger.ru/feed/",
        #Федеральные СМИ, Новости и Политика
        "https://www.kp.ru/rss/allsections.xml",
        "https://aif.ru/rss/all.php",
        "https://vz.ru/rss.xml",
        "https://life.ru/rss",
        "https://inosmi.ru/export/rss2/archive/index.xml",
        "https://www.5-tv.ru/news/rss/",
        "https://www.mk.ru/rss/news/index.xml",
        "https://www.profile.ru/feed/",
        "https://www.fondsk.ru/rss.xml",

        #Региональные городские порталы
        "https://v1.ru/text/rss.xml",
        "https://72.ru/text/rss.xml",
        "https://86.ru/text/rss.xml",
        "https://29.ru/text/rss.xml",
        "https://161.ru/text/rss.xml",
        "https://93.ru/text/rss.xml",
        "https://sochi1.ru/text/rss.xml",
        "https://45.ru/text/rss.xml",
        "https://kazanfirst.ru/feed",
        "https://www.moe-online.ru/rss",
        "https://omskzdes.ru/rss/",

        #Технологии, Гаджеты, Наука и IT
        "https://wylsa.com/feed/",
        "https://kod.ru/rss/",
        "https://servernews.ru/rss",
        "https://nplus1.ru/rss",
        "https://elementy.ru/rss/news",
        "https://applespbevent.ru/feed/",
        "https://4pda.to/feed/",
        "https://androidinsider.ru/feed",
        "https://appleinsider.ru/feed",
        "https://www.securitylab.ru/_services/export/rss/",
        "https://www.anti-malware.ru/rss.xml",

        #Бизнес, Маркетинг, Экономика
        "https://1prime.ru/export/rss2/archive/index.xml",
        "https://www.bfm.ru/news.rss",
        "https://ru.investing.com/rss/news.rss",
        "https://rb.ru/feeds/all/",
        "https://www.audit-it.ru/rss/news_all.xml",
        "https://www.sostav.ru/rss/",
        "https://incrussia.ru/feed/",

        #Игры, Кино и Поп-культура
        "https://www.playground.ru/rss/news.xml",
        "https://www.goha.ru/rss/news",
        "https://cubiq.ru/feed/",
        "https://vgtimes.ru/rss.xml",
        "https://coop-land.ru/rss.xml",
        "https://www.gamedev.ru/rss/",
        "https://knife.media/feed/",
        "https://disgustingmen.com/feed/",
         #Крупные информагентства и медиа
        "https://ura.news/rss",
        "https://360tv.ru/rss/",
        "https://vm.ru/rss/",
        "https://www.tatar-inform.ru/rss",

        #Юриспруденция, Право и Ритейл
        "https://www.garant.ru/rss/news/",
        "https://www.retailer.ru/feed/",

        #IT, Linux и Digital-маркетинг
        "https://www.opennet.ru/opennews/opennews_all_utf.rss",
        "https://devby.io/rss",
        "https://www.cossa.ru/rss/",

        #Криптовалюты, Блокчейн и Web3
        "https://forklog.com/feed",
        "https://coinspot.io/feed/",

        #Наука, Культура и Образование
        "https://postnauka.ru/feed",

        #Автомобильная индустрия
        "https://www.kolesa.ru/feed",

        #Дизайн, Архитектура и Путешествия
        "https://losko.ru/feed/", 
        "https://brodude.ru/feed/" 
    ]
    def fetch_rss(url):
        items = []
        try:
            # Таймаут 5 секунд, чтобы не зависать надолго
            resp = requests.get(url, headers=HEADERS, timeout=5)
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

            print(f"[OK] {url.split('/')[2]} — {len(items)} записей")
        except Exception as e:
            # Ошибки отдельных лент не прерывают работу программы
            print(f"[ПРОПУЩЕНО] {url.split('/')[2]}: {e}")

        return items

    def collect_all_news():
        all_news = []
        seen = set()

        total_feeds = len(RSS_FEEDS)
        print(f"Начинаю обход {total_feeds} источников...")

        for index, url in enumerate(RSS_FEEDS, 1):
            # Небольшая пауза 0.3 сек для стабильности сетевых запросов
            time.sleep(0.3) 
            
            # Лог прогресса
            if index % 10 == 0 or index == total_feeds:
                print(f"--- Прогресс: обработано {index}/{total_feeds} лент ---")

            for news in fetch_rss(url):
                if news["title"] not in seen:
                    seen.add(news["title"])
                    all_news.append(news)

        print(f"\nИТОГО УНИКАЛЬНЫХ НОВОСТЕЙ СОБРАНО: {len(all_news)}")
        return all_news

    def save_batch_to_xml(new_items, folder="news_dataset"):
        if not new_items:
            print("Нет новостей для сохранения.")
            return

        if not os.path.exists(folder):
            os.makedirs(folder)

        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"news_mega_bulk_{current_time}.xml"
        file_path = os.path.join(folder, file_name)

        root = ET.Element("news_batch")
        root.set("created_at", current_time)

        for news in new_items:
            item_node = ET.SubElement(root, "item")
            for key, value in news.items():
                child = ET.SubElement(item_node, key)
                child.text = str(value)

        xml_string = ET.tostring(root, encoding="utf-8")
        parsed_string = minidom.parseString(xml_string)
        pretty_xml = parsed_string.toprettyxml(indent=" ", encoding="utf-8")

        with open(file_path, "wb") as f:
            f.write(pretty_xml)

        print(f"[УСПЕХ] Мега-пакет сохранен в: {file_path}\n")

    # Старт
    all_current_news = collect_all_news()
    save_batch_to_xml(all_current_news)

if __name__ == "__main__":
    print("=== ЗАПУСК МАКСИМАЛЬНОГО ОДНОКРАТНОГО СБОРА (101 ЛЕНТА) ===")
    start_time = time.time()
    
    parse_and_save_news()
    
    end_time = time.time()
    print(f"=== РАБОТА ЗАВЕРШЕНА ЗА {round(end_time - start_time, 1)} сек ===")
