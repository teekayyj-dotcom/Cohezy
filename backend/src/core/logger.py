import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from ..config.settings import settings

# Đường dẫn lưu log
LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True, parents=True)
LOG_FILE = LOG_DIR / "app.log"


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    # Nếu logger đã tồn tại handler thì không thêm nữa (tránh trùng log)
    if logger.handlers:
        return logger

    # Cấu hình mức độ log theo môi trường
    level = logging.DEBUG if settings.ENVIRONMENT == "development" else logging.INFO
    logger.setLevel(level)

    # Định dạng log chung
    formatter = logging.Formatter(
        fmt="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler xuất log ra console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler lưu log ra file
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,  # Giữ 5 file log cũ
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
