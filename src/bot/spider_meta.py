"""Contain metadata for spiders of middleman websites."""
from dataclasses import dataclass
from typing import Final, Type

from bot.easy_learning import EasyLearning
# from bot.freewebcart import Freewebcart
from bot.invent_high import InventHigh
from bot.idownloadcoupon import IDownloadCoupon
from bot.line51 import Line51


@dataclass
class SpiderMeta:
    """Contains metadata about the spiders for middleman websites."""
    sld: str
    brand: str
    spider_cls: Type


SPIDERS: Final[dict[str, Type]] = {
    'inventhigh': SpiderMeta(sld='inventhigh', brand='Invent High', spider_cls=InventHigh),
    'easylearn': SpiderMeta(sld='easylearn', brand='Easy Learning', spider_cls=EasyLearning),
    # 'freewebcart': SpiderMeta(sld='freewebcart', brand='Freewebcart', spider_cls=Freewebcart),
    'idownloadcoupon': SpiderMeta(sld='idownloadcoupon', brand='iDC', spider_cls=IDownloadCoupon),
    'line51': SpiderMeta(sld='line51', brand='Line 51', spider_cls=Line51),
}
