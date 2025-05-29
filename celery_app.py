# # celery_app.py
# from celery import Celery
# celery_app = Celery(__name__, broker="redis://localhost:6379/0")

# @celery_app.task(bind=True)
# def process_video_task(self, video_path: str) -> str:
#     # (same processing steps as above)
#     return pdf_path  # path to generated PDF
