import re
from abc import ABC, abstractmethod
from typing import Any, Dict

import numpy as np


class Activation(ABC):
    def __call__(
        self, **kwargs: Any
    ) -> np.ndarray:  # TODO: Does this need a super lock?
        raise NotImplementedError(
            "Activation subclasses must implement a __call__ method"
        )

    @staticmethod
    def lower_case(name: str) -> str:  # TODO: what about leaky_relu?
        """
        Convert CamelCase class names (e.g., 'RandomNormal')
        into snake_case strings (e.g., 'random_normal').
        """
        return name.lower()

    @classmethod
    def name(cls) -> str:
        """
        By default, convert the class name from CamelCase to snake_case.
        Subclasses can override this classmethod if they want a custom name.
        """
        return cls.lower_case(cls.__name__)

    @abstractmethod
    def get_config(self) -> Dict[str, Any]:
        pass

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "Activation":
        return cls(**config)


class ReLU(Activation):
    def __init__(self):
        super().__init__()

    def __call__(self, data: np.ndarray, **kwargs: Any) -> np.ndarray:
        return np.maximum(0, data)

    def get_config(self) -> Dict[str, Any]:
        return {}
