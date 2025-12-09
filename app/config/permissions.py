class Permission:
    #Проекты
    PROJECT_VIEW = "project.view"
    PROJECT_EDIT = "project.edit"
    PROJECT_DELETE = "project.delete"
    PROJECT_ADD_MEMBER = "project.add_member"

    #Задачи
    TASK_VIEW = "task.view"
    TASK_CREATE = "task.create"
    TASK_EDIT = "task.edit"
    TASK_DELETE = "task.delete"
    TASK_ASSIGN = "task.assign"

ALL_PERMISSIONS = [
    Permission.PROJECT_VIEW,
    Permission.PROJECT_EDIT,
    Permission.PROJECT_DELETE,
    Permission.PROJECT_ADD_MEMBER,
    Permission.TASK_VIEW,
    Permission.TASK_CREATE,
    Permission.TASK_EDIT,
    Permission.TASK_DELETE,
    Permission.TASK_ASSIGN
]