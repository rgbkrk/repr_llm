"""Rich display for Large Language Model Consumption."""


class PlainForLLM:
    """A plain text representation of an object for Large Language Model Consumption.

    Similar to IPython.display.Markdown, this object can take a string and
    display it in a rich format. `_repr_llm_` for the model and `__repr__`
    for frontend human consumption (terminals and notebooks).
    """

    def __init__(self, content):
        """Create a new PlainForLLM object.

        Args:
            content (str): The content to be displayed. Make use of the fact
            that large language models can understand fairly compact text while
            also only being able to accept a limited number of tokens.

        Returns:
            A new PlainForLLM object.
        """
        self.content = content

    def _repr_llm_(self):
        """Return a string representation of the object, for models."""
        return self.content

    def __repr__(self):
        """Return a string representation of the object, for humans."""
        return f"PlainForLLM('{self.content})'"

    def _repr_mimebundle_(self, include=None, exclude=None):
        '''Include a mimebundle version for versions of IPython that do not support _repr_llm_.'''
        if include is None:
            include = []
        if exclude is None:
            exclude = []

        data = {}
        if "text/plain" not in exclude:
            data["text/plain"] = self.__repr__()

        if "text/llm+plain" not in exclude:
            data["text/llm+plain"] = self._repr_llm_()

        return data, {}
