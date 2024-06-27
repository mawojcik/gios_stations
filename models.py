from typing import Optional, List
from dataclasses import dataclass, field


@dataclass
class Installation:
    """
    A class to represent an installation.

    Attributes:
        id (int): ID of the installation.
        param_code (str): Parameter code of the installation.
    """
    id: int
    param_code: str

    def __str__(self):
        return f"Installation: #{self.id}: '{self.param_code}'"


@dataclass
class Station:
    """
    A class to represent a Station.

    Attributes:
        id (int): ID of the Station.
        name (str): Name of the Station
        installations (List[Installation]): A list of all installations.
    """
    id: int
    name: str
    installations: Optional[List] = field(default_factory=list)

    def __str__(self):
        if not self.installations:
            return f"Station #{self.id} ({self.name}):\nNo installations found"
        installations_str = '\n'.join(str(installation) for installation in self.installations)
        return f"Station #{self.id} ({self.name}):\n{installations_str}"
