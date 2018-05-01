def is_admin(request):
    if request.user.is_superuser:
        return True
    return False


def is_backoffice(request):
    if is_admin(request):
        return True

    grps = [g.name for g in request.user.groups.all()]
    if 'back_office' in grps:
        return True
    return False
