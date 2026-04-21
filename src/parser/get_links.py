import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

options = uc.ChromeOptions()
options.add_argument('--blink-settings=imagesEnabled=false')
driver = uc.Chrome(options=options) 


def get_links_from_category(url, category_name):
    
    print(f"🔎 Собираем ссылки: {category_name}")
    all_urls = set()

    try:
        driver.get(url)
        time.sleep(5)
        scrolls = 0 
        no_new_count = 0
        
        while True:
            driver.execute_script("window.scrollBy(0, 4000);")
            time.sleep(0.1)
            
            soup = BeautifulSoup(driver.page_source, 'lxml')
            links = soup.find_all('a', href=True) 
            
            start_len = len(all_urls)
            for l in links:
                href = l['href']
                if '/product/' in href:
                    # Убираем лишний мусор из URL
                    clean_url = "https://www.ozon.kz" + href.split('?')[0]
                    all_urls.add(clean_url)
            
            if len(all_urls) == start_len:
                no_new_count += 1
            else:
                no_new_count = 0
            
            scrolls += 1
            if scrolls % 10 == 0:
                print(f"   [{category_name}] Скролл {scrolls} | Найдено: {len(all_urls)}")
            
            # Твой JS-код для очистки DOM (чтобы браузер не тормозил)
            js_query = """
                var container = document.querySelector('div[data-widget="megaPaginator"] > div');
                if (container && container.children.length > 50) {
                    for (var i = 0; i < container.children.length - 20; i++) {
                        container.children[0].remove();
                    }
                }
            """
            driver.execute_script(js_query)
            
            # Если новых ссылок долго нет или набрали достаточно — выходим
            if no_new_count > 15: 
                break
        
        return list(all_urls)
    finally:
        driver.quit()

# if __name__ == "__main__":
#     for name, url in CATEGORIES.items():
#         # 1. Собираем ссылки
#         links = get_links_from_category(url, name)
        
#         # Сохраняем промежуточный список ссылок
#         with open(f'{name}_urls.json', 'w', encoding='utf-8') as f: 
#             json.dump(links, f, indent=4, ensure_ascii=False)
            
#         print(f"✅ Ссылки для {name} (всего: {len(links)}) сохранены!")

#         # 2. Собираем данные по каждой ссылке
#         category_results = []
#         for i, link in enumerate(links[:50]): # Ограничил до 50 для теста
#             print(f"🚀 [{i+1}/{len(links)}] Парсим: {link}")
#             data = scrap(link)
#             if data:
#                 category_results.append(data)
            
#             # Чтобы Озон не забанил за слишком частые новые окна
#             tm.sleep(random.uniform(2, 4))

#         # Сохраняем финальный результат в CSV (удобнее для анализа)
#         if category_results:
#             pd.DataFrame(category_results).to_csv(f'ozon_{name}_data.csv', index=False, encoding='utf-8-sig')

#     print("🚀 Все задачи выполнены!")
# def scrap(url):

#     try:
#         driver.get(url)
#         tm.sleep(random.uniform(1, 3))
#         driver.execute_script("window.scrollBy(0, 2000);")
#         tm.sleep(0.1)
#         driver.execute_script("window.scrollBy(0, 1000);")
#         tm.sleep(random.uniform(1, 3)) 
        
#         soup = BeautifulSoup(driver.page_source.text, 'lxml')
#         product_data = {'url': url}
        
#         # name
#         title_tag = soup.find('h1')
#         product_data['name'] = title_tag.get_text(strip=True) if title_tag else None

#         # price_now
#         price_now_tag = soup.find('span', class_='tsHeadline600Large')
#         product_data['price_now'] = price_now_tag.get_text(strip=True) if price_now_tag else None

#         #price_before
#         price_before_tag = soup.find('span', class_='pdp_i9b pdp_bj0 pdp_bi9 tsBody400Small')
#         product_data['price_before'] = price_before_tag.get_text(strip=True) if price_before_tag else None

#         #installment_plan
#         installment_plan_tag = soup.find('span', class_='tsBodyControl500Medium')
#         product_data['installment_plan'] = installment_plan_tag.get_text(strip=True) if installment_plan_tag else None

#         #rating and review
#         rating_and_review_tag = soup.find('div', class_='ga5_3_15-a3 tsBodyControl500Medium')
#         product_data['rating_and_review'] = rating_and_review_tag.get_text(strip=True) if rating_and_review_tag else None

#         #seller
#         seller_tag = soup.find('span', class_='b35_3_30-b7')
#         product_data['seller'] = seller_tag.get_text(strip=True) if seller_tag else None

#         #categories
#         breadcrumbs_list = soup.find('ol', class_='c4c_7')
#         product_data['categories'] = [s.get_text(strip=True) for s in breadcrumbs_list.find_all('span')] if breadcrumbs_list else None
           

#         # all CHARACT
#         specs_rows = soup.find_all('dl') 
#         if not specs_rows:  # Если не нашли, пробуем скрольнуть еще чуть-чуть (бывают очень длинные страницы)
#             driver.execute_script("window.scrollBy(0, 1000);")
#             soup = BeautifulSoup(driver.page_source, 'lxml')
#             specs_rows = soup.find_all('dl')


#         if not specs_rows:
#             print(f"⚠️ Характеристики всё еще не найдены: {url}")
#             return product_data # Возвращаем хотя бы URL и название 
        
        
#         target_features = {
#             'Артикул': 'articul', 'Тип': 'type', 'Бренд': 'brand',
#             'Страна-изготовитель': 'country', 'Гарантийный срок': 'warranty',
#             'Диагональ экрана': 'screen_size', 'Разрешение экрана': 'resolution',
#             'Технология матрицы': 'matrix_type', 'Частота обновления экрана': 'refresh_rate',
#             'Бренд процессора': 'cpu_brand', 'Модель процессора': 'cpu_model',
#             'Частота процессора': 'cpu_freq', 'Оперативная память': 'ram',
#             'Общий объем SSD': 'storage_ssd', 'Встроенная память': 'storage_mobile',
#             'Bluetooth': 'bluetooth', 'WiFi': 'wifi', 'Интерфейсы': 'interfaces',
#             'Цвет': 'color', 'Материал корпуса': 'material', 'Вес': 'weight'
#         }

#         for row in specs_rows:
#             key_tag = row.find('dt')
#             val_tag = row.find('dd')
#             if key_tag and val_tag:
#                 # Извлекаем чистый ключ (убираем иконки и лишний текст из кнопок внутри dt)
#                 raw_key = key_tag.find('span', class_='pdp_i8a')
#                 key_text = raw_key.get_text(strip=True) if raw_key else key_tag.get_text(strip=True)
#                 key_text = key_text.replace(':', '').strip().lower()
                
#                 # Проверяем, есть ли этот ключ в нашем списке интересов
#                 for feature_name, dict_key in target_features.items():
#                     if feature_name.lower() in key_text:
#                         # Забираем значение, разделяя ссылки пробелами
#                         value_text = val_tag.get_text(separator=" ", strip=True)
#                         product_data[dict_key] = value_text
#                         break
                
#         return product_data

#     except Exception as e:
#         print(f"❌ Ошибка на ссылке {url}: {e}")
#         return {'url': url, 'error': str(e)}
