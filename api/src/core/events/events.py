from typing import Callable
from fastapi import FastAPI
from config.config import LearnHouseConfig, get_learnhouse_config
from src.core.events.autoinstall import auto_install
from src.core.events.content import check_content_directory
from src.core.events.database import close_database, connect_to_db
from src.core.events.logs import create_logs_dir


def startup_app(app: FastAPI) -> Callable:
    async def start_app() -> None:
        # Get LearnHouse Config
        learnhouse_config: LearnHouseConfig = get_learnhouse_config()
        app.learnhouse_config = learnhouse_config  # type: ignore

        # Connect to database
        await connect_to_db(app)

        # Create logs directory
        await create_logs_dir()

        # Create content directory
        await check_content_directory()

        # Check if auto-installation is needed
        auto_install()

    return start_app


def shutdown_app(app: FastAPI) -> Callable:
    async def close_app() -> None:
        await close_database(app)

    return close_app
