from app.utils.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE


def paginate(query, page: int = 1, page_size: int = DEFAULT_PAGE_SIZE):
    page = max(1, page)
    page_size = min(max(1, page_size), MAX_PAGE_SIZE)

    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size if page_size else 0,
    }