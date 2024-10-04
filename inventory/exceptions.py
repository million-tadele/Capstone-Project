from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # Customize the response data as needed
        response.data['status_code'] = response.status_code
        response.data['error'] = str(exc)

    return response
