class ErrorHandler:
    def log_error(self, error: str):
        print(f"Error: {error}")

    def handle_error(self, error: Exception) -> dict:
        return {"status": "error", "message": str(error)}
