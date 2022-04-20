import pathlib
import random
import time
import uuid

import vk_api
from cred import token
from loguru import logger

log_dir = pathlib.Path.home().joinpath("logs")
log_dir.mkdir(parents=True, exist_ok=True)

logger.add(
    log_dir.joinpath("yandex-zen-spam-service.log"),
    format="{time} [{level}] {module} {name} {function} - {message}",
    level="DEBUG",
    compression="zip",
    rotation="30 MB",
)

auth = vk_api.VkApi(token=token)

groups = {
    "adenformen": -102776528,  # Яндекс Дзен < Взаимопиар, взаимные подписки>
    "zen_yandex_podpiska": -165193784,  # Яндекс Дзен. Продвижение
    "club198719542": -198719542,  # Яндекс Дзен - Взаимная подписка, пиар.
    "club177968214": -177968214,  # Яндекс Дзен Взаимная реклама Пиар
    "dzen.help": -200070911,  # Яндекс Дзен Взаимопомощь
    "pr_zen": -193284181,  # Взаимный пиар • продвижение канала Яндекс Дзен
    "dzen_help": -177798387,  # Яндекс Дзен (Взаимопомощь)
    "allprinted": -106277433,  # Взаимный пиар • Яндекс Дзен/YOUTUBE
    "club170295129": -170295129,  # Яндекс дзен от ПРАКТИКА/ взаимная подписка
}

msg = f"""
💥 Добрый день! 

✍🏻 Взаимная подписка, пара лайков и пара комментов!
✅ Скидывай скрины в личку, договоримся! 
👉🏻 https://zen.yandex.ru/id/60b37982138da3784401d9bc

🤝🏻 {uuid.uuid4().hex}
"""

zen_url = "https://zen.yandex.ru/id/60b37982138da3784401d9bc"

for k, v in groups.items():
    try:
        pause = random.choice(range(2, 6)) * 60
        logger.info(f"spam: name: {k}, id: {v}")
        request = auth.method(
            "wall.post", {"owner_id": v, "message": msg, "attachments": zen_url}
        )
        logger.info(
            f'Result: https://vk.com/{k}?w=wall{v}_{request.get("post_id")}%2Fall'
        )
        logger.info(f"Pause: {pause/60} minutes")
        time.sleep(pause)
    except Exception as e:
        logger.error(f"some problem with wall.post. \nError: {e}")
        time.sleep(random.choice(range(3, 7)) * 60)
