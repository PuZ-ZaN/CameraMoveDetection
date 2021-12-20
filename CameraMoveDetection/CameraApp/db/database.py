from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Topic(Base):

    __tablename__ = 'topic'
    __tableargs__ = {
        'comment': 'Темы цитат'
    }

    topic_id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    name = Column(String(128), comment='Наименование темы')
    description = Column(Text, comment='Описание темы')

    def __repr__(self):
        return f'{self.topic_id} {self.name} {self.description}'


class Author(Base):

    __tablename__ = 'author'
    __tableargs__ = {
        'comment': 'Авторы цитат'
    }

    author_id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    name = Column(String(128), comment='Имя автора')
    birth_date = Column(Date, comment='Дата рождения автора')
    country = Column(String(128), comment='Страна рождения автора')

    def __repr__(self):
        return f'{self.author_id} {self.name} {self.birth_date} {self.country}'


class Quote(Base):

    __tablename__ = 'quote'
    __tableargs__ = {
        'comment': 'Цитаты'
    }

    quote_id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    text = Column(Text, comment='Текст цитаты')
    created_at = Column(DateTime, comment='Дата и время создания цитаты')
    author_id = Column(Integer,  ForeignKey('author.author_id'), comment='Автор цитаты')
    topic_id = Column(Integer, ForeignKey('topic.topic_id'), comment='Тема цитаты')
    author = relationship('Author', backref='quote_author', lazy='subquery')
    topic = relationship('Topic', backref='quote_topic', lazy='subquery')

    def __repr__(self):
        return f'{self.text} {self.created_at} {self.author_id} {self.topic_id}'