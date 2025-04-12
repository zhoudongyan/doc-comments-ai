import argparse
import os
import sys

from dotenv import load_dotenv
from yaspin import yaspin

from doc_comments_ai import llm, utils
from doc_comments_ai.treesitter import Treesitter, TreesitterMethodNode


def run():
    # Load environment variables from .env file
    load_dotenv()
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dir",
        nargs="?",
        default=os.getcwd(),
        help="File to parse and generate doc comments for.",
    )
    parser.add_argument(
        "--inline",
        action="store_true",
        help="Adds inline comments to the code if necessary.",
    )
    parser.add_argument(
        "--model",
        type=str,
        help="OpenAI model to use (default: gpt-3.5-turbo). Can also be set via OPENAI_MODEL environment variable.",
    )
    parser.add_argument(
        "--guided",
        action="store_true",
        help="User will get asked to confirm the doc generation for each method.",
    )

    if sys.argv.__len__() < 2:
        sys.exit("Please provide a file")

    args = parser.parse_args()

    file_name = args.dir

    if not os.path.isfile(file_name):
        sys.exit(f"File {utils.get_bold_text(file_name)} does not exist")

    if utils.has_unstaged_changes(file_name):
        sys.exit(f"File {utils.get_bold_text(file_name)} has unstaged changes")

    utils.is_openai_api_key_available()
    llm_wrapper = llm.LLM(model=args.model)

    generated_doc_comments = {}

    with open(file_name, "r") as file:
        # Read the entire content of the file into a string
        file_bytes = file.read().encode()

        file_extension = utils.get_file_extension(file_name)
        programming_language = utils.get_programming_language(file_extension)

        treesitter_parser = Treesitter.create_treesitter(programming_language)
        treesitterNodes: list[TreesitterMethodNode] = treesitter_parser.parse(
            file_bytes
        )

        for node in treesitterNodes:
            method_name = utils.get_bold_text(node.name)

            if node.doc_comment:
                print(
                    f"⚠️  Method {method_name} already has a doc comment. Skipping..."
                )
                continue

            if args.guided:
                print(f"Generate doc for {utils.get_bold_text(method_name)}? (y/n)")
                if not input().lower() == "y":
                    continue

            method_source_code = node.method_source_code

            tokens = utils.count_tokens(method_source_code)
            if tokens > 2048 and "gpt-3.5-turbo" == llm_wrapper.model:
                print(
                    f"⚠️  Method {method_name} has too many tokens. "
                    f"Consider using {utils.get_bold_text('--model gpt-4')} "
                    f"or {utils.get_bold_text('--model gpt-3.5-turbo-16k')}. "
                    "Skipping for now..."
                )
                continue

            spinner = yaspin(text=f"🔧 Generating doc comment for {method_name}...")
            spinner.start()

            documented_method_source_code = llm_wrapper.generate_doc_comment(
                programming_language.value, method_source_code, args.inline
            )

            generated_doc_comments[
                method_source_code
            ] = utils.extract_content_from_markdown_code_block(
                documented_method_source_code
            )

            spinner.stop()

            print(f"✅ Doc comment for {method_name} generated.")

    file.close()

    for original_code, generated_doc_comment in generated_doc_comments.items():
        utils.write_code_snippet_to_file(
            file_name, original_code, generated_doc_comment
        )
