from abc import abstractmethod, ABCMeta, ABC
from dataclasses import dataclass, is_dataclass, fields
from typing import Optional

from data_to_paper.conversation.stage import Stage


class data_to_paperException(Exception, metaclass=ABCMeta):
    """
    Base class for all exceptions in this package.
    """
    @abstractmethod
    def __str__(self):
        pass

    def __reduce__(self):
        if is_dataclass(self):
            # Collect the field values in the order they're defined in the dataclass
            field_values = [getattr(self, f.name) for f in fields(self)]
            return (self.__class__, tuple(field_values))
        else:
            # Fallback for non-dataclass exceptions
            return super().__reduce__()


class TerminateException(data_to_paperException, metaclass=ABCMeta):
    """
    Base class for all exceptions that terminate data-to-paper run.
    """
    pass


@dataclass
class ResetStepException(Exception):
    """
    An exception to reset the step.
    """
    stage: Optional[Stage]  # reset to this stage, None to exit the app
