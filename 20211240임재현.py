import requests
from bs4 import BeautifulSoup
import time

def crawl_yes24_bestsellers():
    base_url = "https://www.yes24.com/Product/Category/BestSeller"
    category_number = "001001046"  # 국내도서 > 소설 등 카테고리 (수정 가능)
    page = 1
    all_books = []

    while True:
        params = {
            "categoryNumber": category_number,
            "pageNumber": page
        }

        response = requests.get(base_url, params=params, headers={
            'User-Agent': 'Mozilla/5.0'
        })

        if response.status_code != 200:
            print(f"[ERROR] 페이지 {page} 접근 실패")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        book_list = soup.select("ol#bestList > li")

        if not book_list:
            break  # 더 이상 책이 없으면 종료

        for book in book_list:
            title_tag = book.select_one("p.copy a")
            title = title_tag.text.strip() if title_tag else "제목 없음"

            detail_tag = book.select_one("p.auth")
            if detail_tag:
                parts = [s.strip() for s in detail_tag.text.split('|')]
                author = parts[0] if len(parts) > 0 else "저자 없음"
                publisher = parts[1] if len(parts) > 1 else "출판사 없음"
                pub_date = parts[2] if len(parts) > 2 else "출간일 없음"
            else:
                author = publisher = pub_date = "정보 없음"

            all_books.append({
                "제목": title,
                "저자": author,
                "출판사": publisher,
                "출간일": pub_date
            })

        print(f"{page}페이지 완료, 누적 {len(all_books)}권 수집")
        page += 1
        time.sleep(1)  # 과도한 요청 방지

    return all_books


if __name__ == "__main__":
    books = crawl_yes24_bestsellers()
    for idx, book in enumerate(books, 1):
        print(f"{idx}. {book['제목']} / {book['저자']} / {book['출판사']} / {book['출간일']}")
