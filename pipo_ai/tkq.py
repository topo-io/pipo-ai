import taskiq_fastapi
from taskiq import InMemoryBroker, ZeroMQBroker

from pipo_ai.settings import settings

broker = ZeroMQBroker()

if settings.environment.lower() == "pytest":
    broker = InMemoryBroker()

taskiq_fastapi.init(
    broker,
    "pipo_ai.web.application:get_app",
)
