from dataclasses import dataclass
from typing import Final, Type

from bot.easylearning import EasyLearning
from bot.freewebcart import Freewebcart
from bot.idownloadcoupon import IDownloadCoupon
from bot.line51 import Line51


@dataclass
class SpiderMeta:
    """Contains metadata about the spiders for middleman websites."""
    sld: str
    brand: str
    spider_cls: Type


SPIDERS: Final[dict[str, Type]] = {
    'easylearn': SpiderMeta(sld='easylearn', brand='Easy Learning', spider_cls=EasyLearning),
    'freewebcart': SpiderMeta(sld='freewebcart', brand='Freewebcart', spider_cls=Freewebcart),
    'idownloadcoupon': SpiderMeta(sld='idownloadcoupon', brand='iDC', spider_cls=IDownloadCoupon),
    'line51': SpiderMeta(sld='line51', brand='Line 51', spider_cls=Line51),
}
