from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger


class CustomErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Description:
    A middleware class for handling errors in HTTP requests. 
    It logs the request details and any exceptions that occur during the request processing, providing a standardized error response.
    """
    async def dispatch(self, request: Request, call_next):
        """
        Description:
        Processes incoming HTTP requests, logging the request details and handling any exceptions 
        that may occur during the request processing.

        Parameters:
        request (Request): The incoming HTTP request object.
        call_next: A callable that takes the request as an argument and returns the response.
        
        Returns:
        Response: The response from the next middleware or endpoint."""
        try:
            # Process the request and log it
            logger.info(f"Processing request: {request.method} {request.url}")
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.error(f"An error occurred: {exc}")
            return self.handle_exception(exc)

    def handle_exception(self, exc: Exception) -> JSONResponse:
        """
        Description:
        Handles exceptions that occur during request processing. Logs the error and returns a standardized JSON response.

        Parameters:

        exc (Exception): The exception that was raised during request processing.
        Returns:

        JSONResponse: A JSON response with a status code of 500 and a message indicating that an unexpected error occurred.
        """
        logger.error(f"Handling exception: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred. Please try again later."}
        )
