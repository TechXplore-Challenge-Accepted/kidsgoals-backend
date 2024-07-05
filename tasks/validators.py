from rest_framework.exceptions import ValidationError
from accounts.models import CustomUser


def validate_assigned_to(value, user):
    if not user.is_parent:
        raise ValidationError("Only parents can assign tasks.")

    if value == user:
        raise ValidationError("Parents cannot assign tasks to themselves.")

    if value.parent != user:
        raise ValidationError("Parents can only assign tasks to their own kids.")
    return value


def validate_task_completion(task, user):
    if task.assigned_to != user:
        raise ValidationError("You can only mark your own tasks as completed.")
    return task


def validate_task_approval(task, user):
    if not task.is_completed:
        raise ValidationError("Task must be completed before approval.")

    if task.created_by != user:
        raise ValidationError("You can only approve tasks you created.")
    return task

