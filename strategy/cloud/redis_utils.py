from datetime import date


class RedisUtils:
    def __init__(self, total_data_count: int, redis):
        self.data_count = total_data_count
        self.redis_manager = redis

    def update_file_progress(self, increment: int):
        self.redis_manager.set("progress", f"{increment}/{self.data_count}")
        if increment == self.data_count:
            self.redis_manager.mset({"status": "complete", "finish_date": str(date.today())})

    def update_file_status(self, status: str):
        self.redis_manager.mset({"status": status, "finish_date": str(date.today())})

    def is_new_file(self, url: str) -> bool:
        print(self.redis_manager.get("name"))
        if self.redis_manager.get("name") == url and self.redis_manager.get("status") == "completed":
            self.redis_manager.set("ERROR", f"Retry fill file\nDate:{str(date.today())}")
            return False
        else:
            self.redis_manager.mset(
                {"name": url, "loading_start_date": str(date.today()), "status": "in progress",
                 "progress": f"0/0"})
            return True
