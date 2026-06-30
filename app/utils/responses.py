def success_response(message: str = "Success", data=None):
    return {"success": True, "message": message, "data": data}


def error_response(message: str = "Something went wrong", errors=None):
    return {"success": False, "message": message, "errors": errors}