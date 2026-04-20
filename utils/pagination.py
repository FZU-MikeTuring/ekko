from fastapi import Query


async def compute_pagination_params(
        current_page:int=Query(1,ge=1),
        page_size:int=Query(5,ge=5),
):
    offset = (current_page-1)*page_size
    limit = page_size
    return {
        "current_page":current_page,
        "page_size":page_size,
        "offset":offset,
        "limit":limit
    }