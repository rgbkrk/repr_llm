from typing import Optional

from IPython.core.formatters import BaseFormatter
from IPython.core.interactiveshell import InteractiveShell
from traitlets import ObjectName, Unicode


class LLMFormatter(BaseFormatter):
    """A formatter for producing text content for LLMs.

    To define the callables that compute the LLM representation of your
    objects, define a :meth:`_repr_llm_` method or use the :meth:`for_type`
    or :meth:`for_type_by_name` methods to register functions that handle
    this.

    The return value of this formatter should be plaintext.
    """

    format_type = Unicode('text/llm+plain')  # type: ignore

    print_method = ObjectName('_repr_llm_')  # type: ignore


def register_llm_formatter(shell: Optional[InteractiveShell] = None):
    """Register the LLMFormatter"""

    if shell is None:
        from IPython.core.getipython import get_ipython

        ip = get_ipython()
        if ip is None:
            raise RuntimeError("register_llm_formatter must be called from an active IPython session")
        shell = ip

    llm_formatter = LLMFormatter(parent=shell.display_formatter)

    # Note: IPython 7.0+ (?) uses a dict of formatters.
    # The current type inference assumes are Unknown | Any | Traitlets.Dict
    # However it's definitely a dict
    formatters: dict[str, BaseFormatter] = shell.display_formatter.formatters  # type: ignore

    formatters['text/llm+plain'] = llm_formatter
    return llm_formatter
