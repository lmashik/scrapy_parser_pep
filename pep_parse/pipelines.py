import datetime as dt
from collections import defaultdict

from .settings import BASE_DIR


class PepParsePipeline:
    status_dict = defaultdict(int)
    total = 0

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.total += 1
        self.status_dict[item['status']] += 1
        return item

    def close_spider(self, spider):
        current_datetime = str(dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        filename = 'results/status_summary_' + current_datetime + '.csv'
        with open(
            BASE_DIR / filename, mode='w', encoding='utf-8'
        ) as f:
            f.write('Статус,Количество\n')
            for status in self.status_dict:
                f.write(f'{status},{self.status_dict[status]}\n')
            f.write(f'Total,{self.total}\n')
