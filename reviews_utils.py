import json
import os
from collections import namedtuple
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup

Review = namedtuple('Review', 'date positive negative')


def get_page_url(hotel_id: str, page_no: int = 1) -> str:
    # hotel_id example is al22319
    return f"https://tophotels.ru/hotel/{hotel_id}/reviews/pros-n-cons?page={page_no}"


def get_last_page_number(url) -> int:
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Modify the selector as per the specific page structure
        paginator_buttons = soup.select('.paginatorNew__button a')
        last_page_number = paginator_buttons[-1].text.strip() if paginator_buttons else None

        return int(last_page_number)
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_reviews_from_page(url: str) -> List[Review]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        review_blocks = soup.select('article.card-hotel-rating-user')
        reviews = []

        for block in review_blocks:
            # Extracting the date
            date_str = block.select_one('.card-hotel-rating-user__right').get_text().strip()
            review_date = datetime.strptime(date_str, '%d.%m.%y').isoformat()

            # Extracting positives and negatives
            positives = negatives = ''

            positives_block = block.find('li', class_='bold green')
            if positives_block:
                positives = ' '.join([li.get_text().strip() for li in positives_block.find_next_siblings('li')])

            negatives_block = block.find('li', class_='bold red')
            if negatives_block:
                negatives = ' '.join([li.get_text().strip() for li in negatives_block.find_next_siblings('li')])

            review = Review(date=review_date, positive=positives, negative=negatives)
            reviews.append(review)

        return reviews
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def fetch_scores(hotel_id: str) -> List[Review]:
    pages_count = get_last_page_number(get_page_url(hotel_id))
    reviews: List[Review] = []
    for page_no in range(pages_count):
        print(f"{page_no=}")
        page_url = get_page_url(hotel_id, page_no)
        reviews.extend(
            get_reviews_from_page(page_url)
        )
    return reviews


def get_scores_conditional_download(hotel_id: str):
    filename = f"data/scores_{hotel_id}.json"
    hotel_scores = fetch_scores(hotel_id)
    if not os.path.exists(filename):
        with open(filename, 'w') as scores_file:
            scores_file.write(json.dumps(hotel_scores, indent=2, ensure_ascii=False))

    with open(filename, 'r') as r:
        scores = json.load(r)
        return scores


if __name__ == '__main__':
    hotel_id = 'al22319'
    hotel_scores = fetch_scores(hotel_id)
    with open(f"scores_{hotel_id}.json", 'w') as f:
        f.write(json.dumps(hotel_scores, indent=2, ensure_ascii=False))
