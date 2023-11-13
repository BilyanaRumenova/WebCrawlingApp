import asyncio
import logging
import os
import uuid
import webbrowser

from fastapi import Depends, HTTPException
from playwright.async_api import async_playwright, Page
from sqlalchemy.orm import Session
from starlette import status

from database.db import get_db, Screenshot


logger = logging.getLogger("web_crawling_app")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


async def create_screenshot_record(task_id: str, start_url: str, db: Session = Depends(get_db)):
    try:
        screenshot = Screenshot(
            id=task_id,
            start_url=start_url,
        )
        db.add(screenshot)
        db.commit()
        db.refresh(screenshot)
        return screenshot

    except Exception as e:
        logger.error(f"Error saving screenshots information to database: {str(e)}")


async def capture_and_save_screenshots(url: str, num_links: int, task_id: str):
    async with async_playwright() as playwright:
        webkit = playwright.webkit
        browser = await webkit.launch()
        context = await browser.new_context()
        try:
            page = await context.new_page()
            await page.goto(url)
            screenshots_path = create_screenshots_directory(task_id)
            await page.screenshot(path=f"{screenshots_path}/{uuid.uuid4()}.png")

            # Parse HTML and collect links
            links = await page.query_selector_all("a")
            links_to_follow = links[:num_links]

            tasks = []
            for index, link in enumerate(links_to_follow):
                url = await page.evaluate('(element) => element.href', link)
                if url:
                    new_page = await context.new_page()
                    tasks.append(capture_screenshot(new_page, url, task_id))

            await asyncio.gather(*tasks)

        except Exception as e:
            logger.error(f"Invalid or non-existing URL - {url}: {str(e)}")

        finally:
            await browser.close()


async def capture_screenshot(page: Page, url: str, task_id: str):
    try:
        screenshots_path = get_screenshots_directory(task_id)
        await page.goto(url)
        await page.screenshot(path=f"{screenshots_path}/{uuid.uuid4()}.png")
        await page.close()
        logger.info(f"Screenshot captured for task {task_id} - {url}")

    except Exception as e:
        logger.error(f"Error capturing screenshot for task {task_id} - {url}: {str(e)}")


def create_screenshots_directory(task_id) -> str:
    screenshots_path = f"./screenshots/{task_id}"
    os.makedirs(screenshots_path)
    return screenshots_path


def get_screenshots_directory(task_id) -> str:
    return f"./screenshots/{task_id}"


async def open_files(screenshots_dir):
    webbrowser.open(screenshots_dir)
