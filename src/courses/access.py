def get_user_course_ids(user):
    """
    Returns a frozenset of Course PKs accessible to the user,
    or None if the user has unrestricted access (admin / superuser).
    """
    if user.is_superuser or user.role in ('admin', 'staff'):
        return None
    if user.role == 'trainer':
        return frozenset(user.assigned_courses.values_list('pk', flat=True))
    if user.role == 'student':
        return frozenset(user.enrolled_courses.values_list('pk', flat=True))
    return frozenset()


def can_access_course(user, course):
    ids = get_user_course_ids(user)
    return ids is None or course.pk in ids
