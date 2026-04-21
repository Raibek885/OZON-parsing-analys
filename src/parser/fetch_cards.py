import json
import requests
import random
import time
from urllib.parse import urlparse, urlencode

CATEGORIES = {
    "tablets": "https://ozon.kz/category/planshety-15525/",
    "smartphones": "https://ozon.kz/category/smartfony-15502/",
    "laptop": "https://ozon.kz/category/noutbuki-15692/"
}

cookies = {
    '__Secure-ETC': 'f046a6a9c58936acfd32c6028e96e074',
    'abt_data': '7.Y8MSzSbCE3HjOYSZsz0AqiWpnk564PMaBrF98wqABeAX4aznWzzKB7spx8s8BXiRlUSXlyw1JQdGZuZexx0WHxDXfZbaeKIcy7sP1gR4FeaLs3PK0_t7kHtqHg12Rce1SkIcuNytbMxj27QFy_IA_ReJXS8bH6Auxc-0OIAuABnNMzPG1yBBgCaoMCqqvngswmo1aE0Nrz9_jO_Eda8zB_tlFsHwMDbqlmoR6W2voO7T-qRFSoFZdfaxMf4v04ygxYpEVDq05VkYSOSC_sTYzFseBiZZiVk3RuoK1aZhq9t5GDftUlyvDy22qp1ShkXUjAupg2k7EP1-b0tp3J45fInvU9Q-IJkXQWnlm2VBD4ffeKAHC068uf3LEMsiB_oz72thed7BG5k2ePf-put84hUCGLkfdFDEUSOHxKITk-GqiIR9fY6yTDz0sC7F5DmvIFOBZZertQzz_hv0NdQCNqICZ5clGesK8dn9dPQTUNvv0L4nLczqaR8USbP8ow-uP3q56azR778-TWjG07HMQTxm6NES03yDzz0Zlsv6HNfebOCjDiQRfkVc60TTytbjsAE3F3Y5YB_jothujNnc2_HGi02h_urXj3LM_CRbzkxhf98DDtbGMGVmEUCHsBd1nE-G-77XevPfmRG73fxt6ji7PFCPUA',
    '__Secure-access-token': '12.0.UOgEFywAT6W9-bLLh7Srug.37.ARnEnvVsZGLSfTi_ZejTfXr40ZJq2jvPun5PkGQPNhjd0d-xXprIS3AB-XOmqZe5i6QywhBMr073NB24xHC7pJXOgl5v5H1-aTJz-ZIAJcgEVL0IgMeSUlfyGsu_EQRkiA..20260420132548.2._BEYtYUIEnEWQ5oOxqQS5jHjfo0pWIHrvWshEZIuaTI.178789bb35eaa45ba',
    '__Secure-refresh-token': '12.0.UOgEFywAT6W9-bLLh7Srug.37.ARnEnvVsZGLSfTi_ZejTfXr40ZJq2jvPun5PkGQPNhjd0d-xXprIS3AB-XOmqZe5i6QywhBMr073NB24xHC7pJXOgl5v5H1-aTJz-ZIAJcgEVL0IgMeSUlfyGsu_EQRkiA..20260420132548.2.CtWQZvQ6FYdbM-k7eL7Js-IvWz-ui-hQT6BcmH59BCU.1ff473a920b50c7a2',
    '__Secure-ab-group': '37',
    '__Secure-user-id': '0',
    '__Secure-ext_xcid': '96ffbfbb66dfebfb97a1079bea72f507',
    'ADDRESSBOOKBAR_WEB_CLARIFICATION': '1776589293',
    'rfuid': 'LTE5NTAyNjU0NzAsMzUuNzQ5OTcyMDkzODUwMzc0LDEzNzAwNjM5MTUsV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0LC04MjMzNTcwNjMsVzNzaWJtRnRaU0k2SWxCRVJpQldhV1YzWlhJaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMHNleUp1WVcxbElqb2lRMmh5YjIxbElGQkVSaUJXYVdWM1pYSWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3NpZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDBzZXlKdVlXMWxJam9pUTJoeWIyMXBkVzBnVUVSR0lGWnBaWGRsY2lJc0ltUmxjMk55YVhCMGFXOXVJam9pVUc5eWRHRmliR1VnUkc5amRXMWxiblFnUm05eWJXRjBJaXdpYldsdFpWUjVjR1Z6SWpwYmV5SjBlWEJsSWpvaVlYQndiR2xqWVhScGIyNHZjR1JtSWl3aWMzVm1abWw0WlhNaU9pSndaR1lpZlN4N0luUjVjR1VpT2lKMFpYaDBMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4xZGZTeDdJbTVoYldVaU9pSk5hV055YjNOdlpuUWdSV1JuWlNCUVJFWWdWbWxsZDJWeUlpd2laR1Z6WTNKcGNIUnBiMjRpT2lKUWIzSjBZV0pzWlNCRWIyTjFiV1Z1ZENCR2IzSnRZWFFpTENKdGFXMWxWSGx3WlhNaU9sdDdJblI1Y0dVaU9pSmhjSEJzYVdOaGRHbHZiaTl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOUxIc2lkSGx3WlNJNkluUmxlSFF2Y0dSbUlpd2ljM1ZtWm1sNFpYTWlPaUp3WkdZaWZWMTlMSHNpYm1GdFpTSTZJbGRsWWt0cGRDQmlkV2xzZEMxcGJpQlFSRVlpTENKa1pYTmpjbWx3ZEdsdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZMkYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5WFgxZCxXeUp5ZFMxU1ZTSXNJbkoxTFZKVklpd2ljblVpTENKbGJpMVZVeUlzSW1WdUlsMD0sMCwxLDAsMjQsMjM3NDE1OTMwLC0xLDIyNzEyNjUyMCwwLDEsMCwtNDkxMjc1NTIzLElFNWxkSE5qWVhCbElFZGxZMnR2SUZkcGJqTXlJRFV1TUNBb1YybHVaRzkzY3lrZ01qQXhNREF4TURFZ1RXOTZhV3hzWVE9PSxlMzA9LDY1LDEwMTczNDIwOCwxLDEsLTEsMTY5OTk1NDg4NywxNjk5OTU0ODg3LDMzNjAwNzkzMyw4',
    'xcid': '47d982a81021a7371e34a93ba221e23e',
    'guest': 'true',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0',
    'Accept': 'application/json',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://ozon.kz/product/apple-smartfon-iphone-15-sim-esim-128-gb-siniy-1185261285/?at=6WtZgrAoJswPgP2oS287mJLHqvG7zBIl73zrRtxoY4KP',
    'x-o3-app-name': 'dweb_client',
    'x-o3-app-version': 'release_17-3-2026_ce6c79ce',
    'x-o3-manifest-version': 'frontend-ozon-ru:ce6c79cef2b7331e4395150280f540142b988351,pdp-render-api:78e197ee0d8ae5c23c94ce213be958a3008657e8,checkout-render-api:5feb5c71178296edb24e269302b89b1634a840c5,sf-render-api:95ac8be2cfc5f71340c6200f8f03b667761aeb5b,search-render-api:d8b94ab92cb85a8ae66991d36f72b7eb32f069bb,fav-render-api:98a701174a7f5f23dff57e880f2c6fdf76ab5a5a',
    'x-o3-parent-requestid': '58d82b8787ef926b56109e6233582ae1',
    'x-page-view-id': 'ec2628d9-8353-4374-c744-82007ecf7d18',
    'x-page-previous': 'category',
    'Content-Type': 'application/json',
    'Connection': 'keep-alive',
    # 'Cookie': '__Secure-ETC=f046a6a9c58936acfd32c6028e96e074; abt_data=7.Y8MSzSbCE3HjOYSZsz0AqiWpnk564PMaBrF98wqABeAX4aznWzzKB7spx8s8BXiRlUSXlyw1JQdGZuZexx0WHxDXfZbaeKIcy7sP1gR4FeaLs3PK0_t7kHtqHg12Rce1SkIcuNytbMxj27QFy_IA_ReJXS8bH6Auxc-0OIAuABnNMzPG1yBBgCaoMCqqvngswmo1aE0Nrz9_jO_Eda8zB_tlFsHwMDbqlmoR6W2voO7T-qRFSoFZdfaxMf4v04ygxYpEVDq05VkYSOSC_sTYzFseBiZZiVk3RuoK1aZhq9t5GDftUlyvDy22qp1ShkXUjAupg2k7EP1-b0tp3J45fInvU9Q-IJkXQWnlm2VBD4ffeKAHC068uf3LEMsiB_oz72thed7BG5k2ePf-put84hUCGLkfdFDEUSOHxKITk-GqiIR9fY6yTDz0sC7F5DmvIFOBZZertQzz_hv0NdQCNqICZ5clGesK8dn9dPQTUNvv0L4nLczqaR8USbP8ow-uP3q56azR778-TWjG07HMQTxm6NES03yDzz0Zlsv6HNfebOCjDiQRfkVc60TTytbjsAE3F3Y5YB_jothujNnc2_HGi02h_urXj3LM_CRbzkxhf98DDtbGMGVmEUCHsBd1nE-G-77XevPfmRG73fxt6ji7PFCPUA; __Secure-access-token=12.0.UOgEFywAT6W9-bLLh7Srug.37.ARnEnvVsZGLSfTi_ZejTfXr40ZJq2jvPun5PkGQPNhjd0d-xXprIS3AB-XOmqZe5i6QywhBMr073NB24xHC7pJXOgl5v5H1-aTJz-ZIAJcgEVL0IgMeSUlfyGsu_EQRkiA..20260420132548.2._BEYtYUIEnEWQ5oOxqQS5jHjfo0pWIHrvWshEZIuaTI.178789bb35eaa45ba; __Secure-refresh-token=12.0.UOgEFywAT6W9-bLLh7Srug.37.ARnEnvVsZGLSfTi_ZejTfXr40ZJq2jvPun5PkGQPNhjd0d-xXprIS3AB-XOmqZe5i6QywhBMr073NB24xHC7pJXOgl5v5H1-aTJz-ZIAJcgEVL0IgMeSUlfyGsu_EQRkiA..20260420132548.2.CtWQZvQ6FYdbM-k7eL7Js-IvWz-ui-hQT6BcmH59BCU.1ff473a920b50c7a2; __Secure-ab-group=37; __Secure-user-id=0; __Secure-ext_xcid=96ffbfbb66dfebfb97a1079bea72f507; ADDRESSBOOKBAR_WEB_CLARIFICATION=1776589293; rfuid=LTE5NTAyNjU0NzAsMzUuNzQ5OTcyMDkzODUwMzc0LDEzNzAwNjM5MTUsV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0LC04MjMzNTcwNjMsVzNzaWJtRnRaU0k2SWxCRVJpQldhV1YzWlhJaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMHNleUp1WVcxbElqb2lRMmh5YjIxbElGQkVSaUJXYVdWM1pYSWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3NpZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDBzZXlKdVlXMWxJam9pUTJoeWIyMXBkVzBnVUVSR0lGWnBaWGRsY2lJc0ltUmxjMk55YVhCMGFXOXVJam9pVUc5eWRHRmliR1VnUkc5amRXMWxiblFnUm05eWJXRjBJaXdpYldsdFpWUjVjR1Z6SWpwYmV5SjBlWEJsSWpvaVlYQndiR2xqWVhScGIyNHZjR1JtSWl3aWMzVm1abWw0WlhNaU9pSndaR1lpZlN4N0luUjVjR1VpT2lKMFpYaDBMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4xZGZTeDdJbTVoYldVaU9pSk5hV055YjNOdlpuUWdSV1JuWlNCUVJFWWdWbWxsZDJWeUlpd2laR1Z6WTNKcGNIUnBiMjRpT2lKUWIzSjBZV0pzWlNCRWIyTjFiV1Z1ZENCR2IzSnRZWFFpTENKdGFXMWxWSGx3WlhNaU9sdDdJblI1Y0dVaU9pSmhjSEJzYVdOaGRHbHZiaTl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOUxIc2lkSGx3WlNJNkluUmxlSFF2Y0dSbUlpd2ljM1ZtWm1sNFpYTWlPaUp3WkdZaWZWMTlMSHNpYm1GdFpTSTZJbGRsWWt0cGRDQmlkV2xzZEMxcGJpQlFSRVlpTENKa1pYTmpjbWx3ZEdsdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZMkYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5WFgxZCxXeUp5ZFMxU1ZTSXNJbkoxTFZKVklpd2ljblVpTENKbGJpMVZVeUlzSW1WdUlsMD0sMCwxLDAsMjQsMjM3NDE1OTMwLC0xLDIyNzEyNjUyMCwwLDEsMCwtNDkxMjc1NTIzLElFNWxkSE5qWVhCbElFZGxZMnR2SUZkcGJqTXlJRFV1TUNBb1YybHVaRzkzY3lrZ01qQXhNREF4TURFZ1RXOTZhV3hzWVE9PSxlMzA9LDY1LDEwMTczNDIwOCwxLDEsLTEsMTY5OTk1NDg4NywxNjk5OTU0ODg3LDMzNjAwNzkzMyw4; xcid=47d982a81021a7371e34a93ba221e23e; guest=true',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=4',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}


def fetch_product_data(product_url):
    try:
        path = urlparse(product_url).path
        if not path.endswith('/'): path += '/'
        product_id = path.split('-')[-1].strip('/')
    except:
        return None

    result = {
        "url": product_url,
        "product_id": product_id,
        "base_info": {
            "name": None,
            "price": None,
            "old_price": None,
            "installment_price": None,
            "product_rating": None,
            "reviews_count": None,
            "seller_name": None,
            "seller_rating": None
        },
        "characteristics": {}
    }

    # 1. API BASIC INFORMATION
    api_url_1 = f"https://ozon.kz/api/entrypoint-api.bx/page/json/v2?url=%2Fproduct%2F{product_id}%2F"
    try:
        res1 = requests.get(api_url_1, headers=headers, cookies=cookies, timeout=10)
        if res1.status_code == 200:
            data = res1.json()
            states = data.get('widgetStates', {})
            
            for state_key, v in states.items():
                state_data = json.loads(v) if isinstance(v, str) else v
                if not state_data: continue

                # --- Price and Old Price ---
                if isinstance(state_data, dict) and 'price' in state_data and 'originalPrice' in state_data:
                    result["base_info"]["price"] = str(state_data.get('price'))
                    result["base_info"]["old_price"] = str(state_data.get('originalPrice'))

                # --- Installment plan ---
                if 'webInstallmentPurchase' in state_key and not result["base_info"]['installment_price']:
                    try:
                        raw_inst = state_data['colorBlock']['data']['text'][0]['content']
                        result["base_info"]['installment_price'] = str(raw_inst)
                    except: pass

                # --- Product Rating and Number of Reviews ---
                if 'webSingleProductScore' in state_key:
                    text_rating = state_data.get('text', '') # Формат: "4.8 • 150 отзывов"
                    if '•' in text_rating:
                        parts = text_rating.split('•')
                        result["base_info"]['product_rating'] = parts[0].strip()
                        result["base_info"]['reviews_count'] = ''.join(filter(str.isdigit, parts[1]))

                # --- Store and its rating ---
                if 'webCurrentSeller' in state_key:
                    seller_name = state_data.get('sellerCell', {}).get('centerBlock', {}).get('title', {}).get('text')
                    seller_rating = state_data.get('rating', {}).get('title', {}).get('text')
                    result["base_info"]['seller_name'] = seller_name
                    result["base_info"]['seller_rating'] = seller_rating

                # --- FULL ---
                if 'webStickyProducts' in state_key:
                    result["base_info"]['name'] = state_data.get('name')

    except Exception as e:
        print(f"Ошибка в блоке base_info: {e}")

    # 2.CHARACTERISTICS
    params2 = {'url': path, 'layout_container': 'pdpPage2column', 'layout_page_index': '2', 'sh': 'cdOwHlpGzA'}
    api_url_2 = f"https://ozon.kz/api/entrypoint-api.bx/page/json/v2?{urlencode(params2)}"
    
    try:
        headers['Referer'] = product_url
        res2 = requests.get(api_url_2, headers=headers, cookies=cookies, timeout=10)
        if res2.status_code == 200:
            states = res2.json().get('widgetStates', {})
            for k, v in states.items():
                if 'webCharacteristics' in k:
                    raw_data = json.loads(v) if isinstance(v, str) else v
                    all_chars = []
                    if 'characteristics' in raw_data:
                        for group in raw_data['characteristics']:
                            all_chars.extend(group.get('short', []))
                            all_chars.extend(group.get('long', []))
                    
                    for char in all_chars:
                        name = char.get('name')
                        vals = char.get('values', [])
                        val_text = ", ".join([v.get('text', '') for v in vals if v.get('text')])
                        if name and val_text:
                            result["characteristics"][name] = val_text
                    break
    except: pass

    return result

