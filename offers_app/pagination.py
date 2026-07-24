from rest_framework.pagination import PageNumberPagination


class OfferPagination(PageNumberPagination):
    """Paginate offer list responses."""

    page_query_param = "page"
    page_size_query_param = "page_size"
    page_size = 10