from loguru import logger

format_ = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> ' \
            '| <magenta>{process}</magenta>:<yellow>{thread}</yellow> ' \
            '| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<yellow>{line}</yellow> - <level>{message}</level>'
logger.add(
    sink="log",
    level="INFO",
    enqueue=True,
    rotation="1 weeks",
    retention=10,
    encoding="utf-8",
    backtrace=True,
    diagnose=True,
    compression="zip",
    format=format_
)