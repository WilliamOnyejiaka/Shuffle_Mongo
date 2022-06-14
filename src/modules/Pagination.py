from math import ceil


class Pagination:

    def __init__(self, data, page=1, results_per_page=10):
        self.data = data
        self.data_length = len(data)
        self.page = page if page > 0 else 1
        self.results_per_page = results_per_page if results_per_page > 0 else 10
        self.__set_offsets()

    def __set_offsets(self):
        self.first_offset = (self.page-1) * self.results_per_page
        self.last_offset = self.first_offset + self.results_per_page

    def __page_results(self):
        pagination = self.data[self.first_offset:self.last_offset]
        return pagination

    def __total_pages(self): return ceil(
        self.data_length/self.results_per_page)

    def __page_counts(self):
        [has_next, has_prev, next_page, prev_page, total_pages] = [
            False, False, None, None, self.__total_pages()]
        if self.page == self.__total_pages() and total_pages == 1:
            return [has_next, has_prev, next_page, prev_page]
        elif total_pages > 1 and self.page == total_pages:
            has_next = False
            has_prev = True
            next_page = None
            prev_page = self.page - 1
        elif self.page == 1 and self.page < total_pages:
            has_next = True
            has_prev = False
            next_page = self.page + 1
            prev_page = None
        elif self.page > 1 and self.page < total_pages:
            has_next = True
            has_prev = True
            next_page = self.page + 1
            prev_page = self.page - 1
        return [has_next, has_prev, next_page, prev_page]

    def meta_data(self):
        page_counts = self.__page_counts()
        return {
            'page_data': self.__page_results(),
            'has_next': page_counts[0],
            'has_prev': page_counts[1],
            'next_page': page_counts[2],
            'prev_page': page_counts[3],
            'page_data_length': len(self.__page_results()),
            'total_pages': self.__total_pages()
        }
