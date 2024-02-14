SETUP
=====

# Things that are useful for Python development

## 1. LSP (Language Server Protocol)

LSP allows developers to build language support for various programming languages without having to create a dedicated plugin or extension for each language in every IDE.
Instead, a single language server can be implemented for a specific programming language, and any IDE or editor that supports LSP can benefit from it.

In VsCode all we need to do is open up the "Extensions" menu (on Linux Ctrl-Shift-x, on Windows I don't care... :-D), then search for "Python".
The very first search result should be called "Python" and that is what we need, so we click and install it. This should give us most of the
tools that can serve as a crutch for easier development.

![lsp installation](https://github.com/Gabaldonlab/how2code/blob/main/1-environment-setup/assets/python-lsp-installation.png?raw=true)

---

## 2. Formatter - Why use Black for Python code formatting?

Well, imagine your code as a disco dance floor—Black ensures that every line follows the same funky
rhythm and nobody's doing the robot in the middle of your elegant tango. Let your code boogie with style, not with syntax chaos!

In VsCode "Extensions" menu search for "Black Formatter", then install the very first search result. This will ensure that
your code is nice, elegant and readable. No need to be smart, let the tools be smart for you!

*Installation:*
![black installation](https://github.com/Gabaldonlab/how2code/blob/main/1-environment-setup/assets/black-formatter-installation.png?raw=true)

*Before formatting:*

![before formatting example](https://github.com/Gabaldonlab/how2code/blob/main/1-environment-setup/assets/before-formatting.png?raw=true)

*After formatting:*
![after formatting example](https://github.com/Gabaldonlab/how2code/blob/main/1-environment-setup/assets/after-formatting.png?raw=true)

---

## 3. Static type checker - MyPy

This is already included in the previously installed Microsoft Pylance LSP, but worth to mention it.
Strongly typed code is always sexier, than a weak typed one. (Not a joke, it can save a lot of daily brain power for you!)

![static type checking](https://github.com/Gabaldonlab/how2code/blob/main/1-environment-setup/assets/type-checker-example.png?raw=true)

---

## 4. Pytest

![pytest example](https://github.com/Gabaldonlab/how2code/blob/main/1-environment-setup/assets/pytest-example.png?raw=true)
Testing can save you time in development/debugging and maintenance.

```bash
pip install pytest
```

**OR**

```bash
conda install anaconda::pytest
```
