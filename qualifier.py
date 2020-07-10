"""
Use this file to write your solution for the Summer Code Jam 2020 Qualifier.

Important notes for submission:

- Do not change the names of the two classes included below. The test suite we
  will use to test your submission relies on existence these two classes.

- You can leave the `ArticleField` class as-is if you do not wish to tackle the
  advanced requirements.

- Do not include "debug"-code in your submission. This means that you should
  remove all debug prints and other debug statements before you submit your
  solution.
"""
import datetime
import typing
import string

from collections import OrderedDict


class ArticleField:
    """The `ArticleField` class for the Advanced Requirements."""

    def __init__(self, field_type: typing.Type[typing.Any]):
        pass


class Article:
    """The `Article` class you need to write for the qualifier."""
    
    id = 0

    def __init__(self, title: str, author: str, publication_date: datetime.datetime, content: str):
        self.id = self.get_id()

        self.title = title
        self.author = author
        self.publication_date = publication_date
        self._content = content
        self.last_edited = None

    def get_id(self) -> int:
        id = self.__class__.id
        self.__class__.id += 1
        
        return id

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, new_content: str):
        self.last_edited = datetime.datetime.now()
        self._content = new_content

    def short_introduction(self, n_characters: int) -> str:
        if self.__len__() <= n_characters:
            introduction = self.content
        else:
            next_character = self.content[n_characters]
            
            if next_character in string.ascii_letters:
                introduction = self.truncate_content(self.content[:n_characters])
            else:
                introduction = self.content[:n_characters]

        return introduction

    def truncate_content(self, content_up_to_n: str) -> str:
        while content_up_to_n[-1] not in ' \n':
          content_up_to_n = content_up_to_n[:-1]
        
        return content_up_to_n[:-1]

    def most_common_words(self, n_words: int) -> dict:        
        result = OrderedDict()
        
        for word in self.get_words():
            if word not in result:
                result[word] = 1
            else:
                result[word] += 1

        return self.top(n_words, result)

    def get_words(self) -> list:
        content = self.remove_redundant_apostrophes(self.content)
        content = self.remove_punctuation(content.lower())
        content = content.replace('\n', ' ')
        content = content.replace('\'', ' ')
        
        return content.split(' ')

    def remove_redundant_apostrophes(self, content: str) -> str:
        # Remove leading and trailing apostrophes
        content = self.content.strip('\'')
        # Remove trailing apostrophes followed by a new line
        content = content.replace('\'\n', ' ')
        # Remove quotes from words or sub texts
        # something 'word' something :-> something word' something
        content = content.replace(' \'', ' ')
        # something word' something :-> something word something
        content = content.replace('\' ', ' ')

        return content

    def remove_punctuation(self, content: str) -> str:
        punctuation_characters = string.punctuation.replace('\'', '')
        
        for punctuation_character in punctuation_characters:
            content = content.replace(punctuation_character, '')

        return content

    def top(self, n_words: int, word_count: dict) -> dict:
        return dict(sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:n_words])

    def __lt__(self, other_article) -> bool:
        return self.publication_date < other_article.publication_date

    def __repr__(self) -> str:
        return f'<Article title={repr(self.title)} author={repr(self.author)} publication_date={repr(self.publication_date.isoformat())}>'

    def __len__(self) -> int:
        return len(self.content)

