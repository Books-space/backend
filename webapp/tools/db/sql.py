from typing import Optional

from sqlalchemy import desc


def sqlorder(query, column, is_desc: bool):
    if is_desc:
        return query.order_by(desc(column))

    return query.order_by(column)


def sqlfilter(query, **kwargs):
    for field, field_value in kwargs.items():
        if not field_value:
            continue

        query = query.filter_by(**{field: field_value})

    return query


def field_contains(query, field, substring: Optional[str]):
    return query.filter(field.contains(substring))
