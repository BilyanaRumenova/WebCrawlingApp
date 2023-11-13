import os
import uuid
from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database.db import get_db, Base, engine
import utils

app = FastAPI()


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


@app.get("/isalive")
async def check_server_health() -> dict:
    return {"status": "Server is running"}


@app.post("/screenshots", status_code=status.HTTP_201_CREATED)
async def make_screenshots(start_url: str, number_of_links_to_follow: int, background_tasks: BackgroundTasks,
                           db: Session = Depends(get_db)) -> dict:
    task_id = str(uuid.uuid4())
    background_tasks.add_task(
        utils.capture_and_save_screenshots,
        start_url,
        number_of_links_to_follow,
        task_id
    )
    await utils.create_screenshot_record(task_id, start_url, db)

    return {
        "id": task_id
    }


@app.get("/screenshots/{id}")
async def get_screenshots(task_id: str) -> dict:
    screenshots_dir = utils.get_screenshots_directory(task_id)
    if not os.path.exists(screenshots_dir) or not os.path.isdir(screenshots_dir):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Screenshots not found")

    filenames = os.listdir(screenshots_dir)
    screenshot_filenames = [filename for filename in filenames if filename.lower().endswith('.png')]

    result = {
        "id": task_id,
        "screenshot_filenames": screenshot_filenames,
    }

    await utils.open_files(screenshots_dir)
    return result
