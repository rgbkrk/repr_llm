# repr-llm

<img src="https://github.com/rgbkrk/repr_llm/assets/836375/f1b8b252-7e70-4897-bfbf-e87d48bb46bd" height="64px" />

Create lightweight representations of objects for Large Language Model consumption

## Background

In Python, we have a way to represent our objects within interpreters: `repr`.

In IPython, it goes even further. We can register rich represenations of plots, tables, and all kinds of objects. As an example, developers can augment their objects with a `_repr_html_` method to expose a rich HTML version of their object. The most common example most Pythonistas know about is showing tables for their data inside notebooks via `pandas`.

```python
import pandas as pd
df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
df
```

|     |   a |   b |
| --: | --: | --: |
|   0 |   1 |   4 |
|   1 |   2 |   5 |
|   2 |   3 |   6 |

This is a great way to show data in a notebook for humans. What if there was a way to provide a compact yet rich representation for Large Language Models?

## The Idea

The `repr_llm` package introduces the idea that python objects can emit a rich representation for LLM consumption. With the advent of [OpenAI's Code Interpreter](https://openai.com/blog/chatgpt-plugins#code-interpreter), [Noteable plugin for ChatGPT](https://noteable.io/chatgpt-plugin-for-notebook/), and [LangChain's Python REPL Tool](https://github.com/hwchase17/langchain/blob/fcb3a647997c6275e3d341abb032e5106ea39cac/langchain/tools/python/tool.py#L42C1-L42C1), we have massive opportunity to create rich visualizations for humans and rich text for models.

Let's begin by creating a `Book` class that has a regular `__repr__` and a `_repr_llm_`:

```python
class Book:
    def __init__(self, title, author, year, genre):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre

    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', {self.year}, '{self.genre}')"

    def _repr_llm_(self):
        return (f"A Book object representing '{self.title}' by {self.author}, "
                f"published in the year {self.year}. Genre: {self.genre}. "
                f"Instantiated with `{repr(self)}`"
               )

from repr_llm import register_llm_formatter

ip = get_ipython() # Current IPython shell
register_llm_formatter(ip)

# This is how IPython creates the Out[*] prompt in the notebook
data, _ = ip.display_formatter.format(
    Book('Attack of the Black Rectangles', 'Amy Sarig King', 2022, "Middle Grade")
)
data
```

```json
{
  "text/plain": "Book('Attack of the Black Rectangles', 'Amy Sarig King', 2022, 'Middle Grade')",
  "text/llm+plain": "A Book object representing 'Attack of the Black Rectangles' by Amy Sarig King, published in the year 2022. Genre: Middle Grade. Instantiated with `Book('Attack of the Black Rectangles', 'Amy Sarig King', 2022, 'Middle Grade')`"
}
```

## How it works

The `repr_llm` package provides a `register_llm_formatter` function that takes an IPython shell and registers a new formatter for the `text/llm+plain` mimetype.

When IPython goes to display an object, it will first check if the object has a `_repr_llm_` method. If it does, it will call that method and include the result as part of the representation for the object.

## FAQ

### Why not just use `_repr_markdown_`? (or `__repr__`)

The `_repr_markdown_` method is a great way to show rich text in a notebook. The reason is that it's meant for humans to read. Large Language Models can read that too. However, there are going to be times when `Markdown` is too big for the model (token limit) or too complex (too many tokens to understand).

Originally I was going to suggest more package authors use `_repr_markdown_` (and they should!). Then [Peter Wang](https://github.com/pzwang) suggested that we have a version written for the models, just like OpenAI's `ai-plugin.json` does, especially since the LLMs _can_ be a more advanced reader.

Any LLM user can still use `_repr_markdown_` to show rich text to the model. This provides an extra option that is _explicit_. It's a way for developers to say "this is what I want the model to see".

### Where does the `text/llm+plain` mimetype come from?

The mimetype is a convention being proposed. It's a way to say "this is a plain text representation for a Large Language Model". It's not a standard (yet!). It's a way to say "this is what I want the model to see" while we explore this space.

### Are there examples of this in the wild?

ChatGPT plugins provide something very similar to repr vs repr_llm with the `api_plugin_json` and OpenAPI specs, especially since there's a delineation of `description_for_human` and `description_for_model`.

### How did this originate?

While experimenting with Large Language Models directly [💬](https://platform.openai.com/docs/api-reference/chat/create) [🤗](https://huggingface.co/) and with tools like [genai](https://github.com/noteable-io/genai), [dangermode](https://github.com/rgbkrk/dangermode), and [langchain](https://github.com/hwchase17/langchain) I've been naturally converting representations of my data or text to markdown as a format that GPT models can understand and converse with a user about.

## What's next?

Convince as many library authors as possible, just like we did with `_repr_html_` to use `_repr_llm_` to provide a lightweight representation of their objects that is:

- Deterministic - no side effects
- Navigable - states what other functions can be run to get more information, create better plots, etc.
- Lightweight - take into account how much text a GPT model can read
- Safe - no secrets, no PII, no sensitive data

## Credit

Thank you to [Dave Shoup](https://github.com/shouples) for the conversations about pandas representation and how we can keep improving what we send for `Out[*]` to Large Language Models.
