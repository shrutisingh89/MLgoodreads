"""Class implementation for fetching goodreads data"""

from collections import OrderedDict
import pandas as pd
import os
import csv
import time
from goodreads import textcleaner
from datetime import datetime
from goodreads import client

class GoodreadsCollect():

    def __init__(self, grclient, data_directory):
        self._grclient = grclient
        self._data_directory = data_directory
        self._user_data_list = list()
        self._review_data_list = list()
        self._author_data_list = list()
        self._book_data_list = list()
        self._base_directory = os.path.join(data_directory, 'data')
        if not os.path.isdir(self._base_directory):
            os.makedirs(self._base_directory)

    def fetch_data(self):
        reviews = self._grclient.recent_reviews()
        for review in reviews:
            time.sleep(0.5)
            review_obj = self._grclient.review(review.gid)
            self._review_data_list.append(self._parse_review_data(review_obj))
            self._user_data_list.append(self._parse_user_data(review_obj))
            self._author_data_list.append(self._parse_author_data(review_obj))
            self._book_data_list.append(self._parse_book_data(review_obj))

        for module_name, module_data in zip(["reviews","user","author","book"], [self._review_data_list, self._user_data_list, self._author_data_list, self._book_data_list]):
            print(f"Writing data for : {module_name}")
            self._write_to_disk(module_name, module_data)

    def _write_to_disk(self, module_name, module_data):
        file = os.path.join(self._base_directory, f"{module_name}.csv")
        write_mode, header = ('a', False) if os.path.isfile(file) else ('w',True)

        if(len(module_data) > 0):
            pd\
                .DataFrame(module_data)\
                .to_csv(path_or_buf=file, index=False, mode=write_mode, header=header, quoting=csv.QUOTE_MINIMAL)
            self._user_data_list = list()
            self._review_data_list = list()
            self._author_data_list = list()
            self._book_data_list = list()


    def _parse_review_data(self, review_obj):
        """Parse review data from review object"""
        return OrderedDict(
            {
                "review_id": review_obj.gid,
                "user_id" : review_obj.user['id'],
                "book_id" : review_obj.book['id']['#text'],
                "author_id" : review_obj.book['authors']['author']['id'],
                "review_text": textcleaner.GoodreadsTextCleaner.clean_all(review_obj.body),
                "review_rating": review_obj.rating,
                "review_votes": review_obj.votes,
                "spoiler_flag": review_obj.spoiler_flag,
                "spoiler_state": review_obj.spoiler_state,
                "review_added_date": review_obj.data_added,
                "review_updated_date": review_obj.date_updated,
                "review_read_count": review_obj.read_count,
                "comments_count": review_obj.comments_count,
                "review_url": review_obj.url,
                "record_create_timestamp" : datetime.now()
            }.items()
        )

    def _parse_user_data(self, review_obj):
        """Parse user data from review object"""
        return OrderedDict(
            {
                "user_id": review_obj.user['id'],
                "user_name": review_obj.user['name'],
                "user_display_name": review_obj.user['display_name'],
                "location": review_obj.user['location'],
                "profile_link": review_obj.user['link'],
                "uri": review_obj.user['uri'],
                "user_image_url": review_obj.user['image_url'],
                "small_image_url": review_obj.user['small_image_url'],
                "has_image": review_obj.user['has_image'],
                "record_create_timestamp": datetime.now()
            }.items()
        )

    def _parse_book_data(self, review_obj):
        """Parse book data from review object"""
        return OrderedDict(
            {
                "book_id": review_obj.book['id']['#text'],
                "title": review_obj.book['title'],
                "title_without_series": review_obj.book['title_without_series'],
                "image_url": review_obj.book['image_url'],
                "book_url": review_obj.book['link'],
                "num_pages": review_obj.book['num_pages'],
                "format": review_obj.book['format'],
                "edition_information": review_obj.book['edition_information'],
                "publisher": review_obj.book['publisher'],
                "publication_day": review_obj.book['publication_day'],
                "publication_year": review_obj.book['publication_year'],
                "publication_month": review_obj.book['publication_month'],
                "average_rating": review_obj.book['average_rating'],
                "ratings_count": review_obj.book['ratings_count'],
                "description": textcleaner.GoodreadsTextCleaner.clean_all(review_obj.book['description']),
                "authors": review_obj.book['authors']['author']['id'],
                "published": review_obj.book['published'],
                "record_create_timestamp": datetime.now()
            }.items()
        )


    def _parse_author_data(self, review_obj):
        """Parse author data from review object"""
        author = review_obj.book['authors']['author']
        return OrderedDict(
                        {
                        "author_id" : author['id'],
                        "name": author['name'],
                        "role" : author['role'],
                        "profile_url" : author['link'],
                        "average_rating" : author['average_rating'],
                        "rating_count" : author['ratings_count'],
                        "text_review_count" : author['text_reviews_count'],
                        "record_create_timestamp": datetime.now()
                        }.items()
            )