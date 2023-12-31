from pathlib import Path

BASE_DIR = Path(__file__).absolute().parent.parent

BOT_NAME = 'pep_parse'

SPIDER_MODULES = ['pep_parse.spiders']
NEWSPIDER_MODULE = 'pep_parse.spiders'

ROBOTSTXT_OBEY = True

RESULT_FOLDER_NAME = 'results'
DATE_FORMAT = '%Y-%m-%d_%H-%M-%S'

ITEM_PIPELINES = {'pep_parse.pipelines.PepParsePipeline': 300}

FEED_EXPORT_ENCODING = "utf-8"
FEEDS = {
    f'{RESULT_FOLDER_NAME}/pep_%(time)s.csv': {
        'format': 'csv',
        'fields': ['number', 'name', 'status'],
        'overwrite': True
    },
}
