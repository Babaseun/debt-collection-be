from accounts.models import StatusType


class Utils:
    @staticmethod
    def parse_status(status_str):
        try:
            return StatusType[status_str]
        except KeyError:
            raise ValueError(f"Invalid status: {status_str}")
