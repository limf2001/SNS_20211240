import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

books = []
page = 1
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36"
}

while True:
    try:
        url = f"https://www.yes24.com/product/category/bestseller?categoryNumber=001&pageNumber={page}&pageSize=24"
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        book_items = soup.find_all("li", attrs={"data-goods-no": True})

        if not book_items:
            print("데이터 수집 완료\n")
            break

        for item in book_items:
            rank_tag = item.select_one("em.ico.rank")
            title_tag = item.select_one("a.gd_name")
            author_tag = item.select_one("span.authPub.info_auth a")
            pub_tag = item.select_one("span.authPub.info_pub a")

            rank = rank_tag.get_text(strip=True) if rank_tag else ''
            title = title_tag.get_text(strip=True) if title_tag else ''
            author = author_tag.get_text(strip=True) if author_tag else ''
            publisher = pub_tag.get_text(strip=True) if pub_tag else ''

            books.append([rank, title, author, publisher])

        print(f"페이지 {page} 완료, 수집된 책 수: {len(books)}")
        page += 1

        time.sleep(1)  # 서버 부담 줄이기 위해 1초 대기

    except requests.exceptions.RequestException as e:
        print(f"HTTP 요청 중 오류 발생: {e}")
        break
    except Exception as e:
        print(f"알 수 없는 오류 발생: {e}")
        break

df = pd.DataFrame(books, columns=["순위", "책제목", "저자", "출판사"])

if not df.empty:
    df.to_csv("yes24목록.csv", index=False, encoding="utf-8-sig")
    print("수집 완료 및 CSV 저장!!")
else:
    print("수집된 데이터가 없습니다.")

print(df)
