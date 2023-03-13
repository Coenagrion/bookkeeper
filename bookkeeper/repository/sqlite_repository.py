import sqlite3
from typing import Any
from inspect import get_annotations
from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SQLiteRepository(AbstractRepository[T]):
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.cls = cls
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            res = cur.execute('SELECT name FROM sqlite_master')
            db_tables = [t[0].lower() for t in res.fetchall()]
            if self.table_name not in db_tables:
                col_names = ', '.join(self.fields.keys())
                text = f'CREATE TABLE {self.table_name} (' \
                    f'"pk" INTEGER PRIMARY KEY AUTOINCREMENT, {col_names})'
                cur.execute(text)
        con.close()

    def add(self, obj: T) -> int:
        names = ', '.join(self.fields.keys())
        val = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            text = f'INSERT INTO {self.table_name} ({names}) VALUES ({val})'
            cur.execute(text, values)
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk

    def __generate_object(self, db_row: tuple) -> T:
        obj = self.cls(self.fields)
        for field, value in zip(self.fields, db_row[1:]):
            setattr(obj, field, value)
        obj.pk = db_row[0]
        return obj

    def get(self, pk: int) -> T | None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            text = f'SELECT * FROM {self.table_name} WHERE pk = {pk}'
            row = cur.execute(text).fetchone()
        con.close()

        if row is None:
            return None
        return self.__generate_object(row)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T] | None:
        if where:
            names = list(where.keys())
            with sqlite3.connect(self.db_file) as con:
                cur = con.cursor()
                cur.execute('PRAGMA foreign_keys = ON')
                cur.execute(
                    f'SELECT FROM {self.table_name} '
                    f'WHERE {("{param} = {where[param]} , " for i in names)} = '
                )
                rows = cur.fetchall()
            con.close()
        else:
            with sqlite3.connect(self.db_file) as con:
                cur = con.cursor()
                cur.execute(f'SELECT * FROM {self.table_name}')
                rows = cur.fetchall()
            con.close()

        if not rows:
            return None
        return [self.__generate_object(row) for row in rows]

    def update(self, obj: T) -> None:
        param_dict = obj.__dict__
        del param_dict['pk']
        attributes = ''
        for attr in param_dict.keys():
            attributes += str(attr)
            attributes += " = '"
            attributes += str(param_dict[attr])
            attributes += "', "
        attributes = attributes[:-2]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            text = f'UPDATE {self.table_name} SET {attributes} WHERE pk = {obj.pk}'
            cur.execute(text)
        con.close()
        return None

    def delete(self, pk: int) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(
                f'DELETE FROM {self.table_name} WHERE rowid = {pk}'
            )
        con.close()
        return None
