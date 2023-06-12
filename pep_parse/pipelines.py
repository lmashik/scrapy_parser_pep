import datetime as dt
from collections import defaultdict

from .settings import BASE_DIR, DATE_FORMAT, RESULT_FOLDER_NAME


class PepParsePipeline:
    status_dict = defaultdict(int)
    total = 0

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.status_dict[item['status']] += 1
        return item

    def close_spider(self, spider):
        self.total = sum(self.status_dict.values())
        current_dt = str(dt.datetime.now().strftime(DATE_FORMAT))
        filename = f'{RESULT_FOLDER_NAME}/status_summary_{current_dt}.csv'
        with open(
            BASE_DIR / filename, mode='w', encoding='utf-8'
        ) as f:
            f.write('Статус,Количество\n')
            for status in self.status_dict:
                f.write(f'{status},{self.status_dict[status]}\n')
            f.write(f'Total,{self.total}\n')
