from datetime import datetime


def constant_value(request):
    import datetime
    return {
        "Now": datetime.datetime.now()
    }