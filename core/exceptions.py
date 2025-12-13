class InsightStreamException(Exception):
    def __init__(self, message: str, code: str = 'INTERNAL_ERROR'):
        self.message = message
        self.code = code
        super().__init__(self.message)

class AIServiceUnavailable(InsightStreamException):
    def __init__(self, message: str = 'AI service temporarily unavailable'):
        super().__init__(message, 'AI_SERVICE_UNAVAILABLE')

class RateLimitExceeded(InsightStreamException):
    def __init__(self, message: str = 'Rate limit exceeded'):
        super().__init__(message, 'RATE_LIMITED')

class YouTubeAPIError(InsightStreamException):
    def __init__(self, message: str = 'YouTube API error'):
        super().__init__(message, 'YOUTUBE_API_ERROR')
