def user_data(request):
    if request.user.is_authenticated:
        return {
            "user_data": {
                "is_authenticated": True,
                "username": request.user.username,
                "email": request.user.email,
            }
        }
    return {"user_data": {"is_authenticated": False}}
