"""
all enums in our services
"""

from enum import Enum


class TaskStatus(Enum):
    TODO ='todo'
    IN_PROGRESS='in_progress'
    DONE = 'done'

class TaskPriority(Enum):
    LOW = 'low'
    MEDIUM ="medium"
    HIGH = "high"