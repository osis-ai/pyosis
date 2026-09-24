"""
pyosis

========
A library for A library for calling OSIS functions.
A library for extending OSIS functionality.
A library that allows users to use CAE with great flexibility.
"""

__version__ = "0.7.4"

from .core.engine import OSISEngine
from .core.batch import batch, flush, batch_state, BatchError
# from .core import engine
# from .ai.agents import BaseAgent
# from .core import osis_run

def get_version():
    return __version__
