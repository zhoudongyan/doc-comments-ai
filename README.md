<div align="center">

# Code documentation generation with LLMs

[![Build](https://github.com/fynnfluegge/doc-comments.ai/actions/workflows/build.yaml/badge.svg)](https://github.com/fynnfluegge/doc-comments.ai/actions/workflows/build.yaml)
[![Publish](https://github.com/fynnfluegge/doc-comments.ai/actions/workflows/publish.yaml/badge.svg)](https://github.com/fynnfluegge/doc-comments.ai/actions/workflows/publish.yaml)
<img src="https://img.shields.io/badge/License-MIT-green.svg"/>
</a>

</div>

<div align="center">

Focus on writing your code, let LLMs write the documentation for you.  
Generate comprehensive documentation for your code using OpenAI's powerful language models.

Built with [treesitter](https://github.com/tree-sitter/tree-sitter) and OpenAI API

![doc_comments_ai_demo](https://github.com/fynnfluegge/doc-comments-ai/assets/16321871/664bc581-a2a0-49ea-87f9-343f49f05e97)

</div>

## ✨ Features

- 📝 &nbsp;Generate documentation comment blocks for all methods in a file
  - e.g. Javadoc, JSDoc, Docstring, Rustdoc etc.
- ✍️ &nbsp; Generate inline documentation comments in method bodies
- 🌳&nbsp; Treesitter integration for accurate code parsing
- 🔄&nbsp; Support for various OpenAI models (GPT-3.5, GPT-4, etc.)

> [!NOTE]  
> Documentation will only be added to files without unstaged changes, so nothing is overwritten.

## 📋 Requirements

- Python >= 3.9
- OpenAI API Key

## 📦 Installation

Install in an isolated environment with `pipx`:
```
pipx install doc-comments-ai
```
If you are facing issues using pipx you can also install directly from source through PyPI with:
```
pip install doc-comments-ai
```
However, it is recommended to use pipx instead to benefit from isolated environments for the dependencies.

## 🔧 Configuration

### Environment Variables

You can configure the application using environment variables. Create a `.env` file in your project root directory based on the provided `.env.example`:

```bash
# OpenAI API Key (Required)
OPENAI_API_KEY=your_api_key_here

# OpenAI Model Selection (Optional, defaults to gpt-3.5-turbo)
# Available options: gpt-3.5-turbo, gpt-4, gpt-3.5-turbo-16k, etc.
OPENAI_MODEL=gpt-3.5-turbo

# OpenAI API Base URL (Optional, for proxy or custom endpoints)
# OPENAI_BASE_URL=https://api.openai.com/v1
```

Or set them directly in your environment:

```bash
export OPENAI_API_KEY=your_api_key_here
export OPENAI_MODEL=gpt-4  # Optional
export OPENAI_BASE_URL=your_custom_url  # Optional
```

## 🚀 Usage

Generate documentation for methods in a file:
```bash
# Basic usage with default model (gpt-3.5-turbo)
aicomment <RELATIVE_FILE_PATH>

# Use a specific model
aicomment <RELATIVE_FILE_PATH> --model gpt-4

# Add inline comments to method bodies
aicomment <RELATIVE_FILE_PATH> --inline

# Confirm documentation generation for each method
aicomment <RELATIVE_FILE_PATH> --guided
```

> [!NOTE]  
> For extensive and descriptive documentation, consider using GPT-4 or GPT-3.5-turbo-16k models which have larger context windows.

## 📚 Supported Languages

- [x] Python
- [x] Typescript
- [x] Javascript
- [x] Java
- [x] Rust
- [x] Kotlin
- [x] Go
- [x] C++
- [x] C
- [x] C#
- [x] Haskell

## 🛟 Troubleshooting

- #### During installation with `pipx`
  ```
  pip failed to build package: tiktoken

  Some possibly relevant errors from pip install:
    error: subprocess-exited-with-error
    error: can't find Rust compiler
  ```
  Make sure the rust compiler is installed on your system from [here](https://www.rust-lang.org/tools/install).

## 🌟 Contributing

If you are missing a feature or facing a bug don't hesitate to open an issue or raise a PR.
Any kind of contribution is highly appreciated!
