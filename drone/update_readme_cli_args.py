import marko
import subprocess

CLI_ARGS_HEADER_TEXT = "Command-line Arguments"
GLOWL_HELP_OUTPUT = subprocess.run(["glowl", "--help"], capture_output=True)


def main():
    with open("README.md", "r") as readme:
        markdown = marko.Markdown(extensions=["footnote"])
        markdown_renderer = marko.md_renderer.MarkdownRenderer()

        document = markdown.parse(readme.read())
        document.children = list(document.children)

        for index, child in enumerate(document.children):
            if isinstance(child, marko.block.Heading):
                text = markdown_renderer.render_children(child)
                if text == CLI_ARGS_HEADER_TEXT:
                    usage_info_latest = str(GLOWL_HELP_OUTPUT.stdout, "utf-8").strip()
                    usage_info_prev = markdown_renderer.render_children(
                        document.children[index + 1]
                    ).strip()
                    if usage_info_latest != usage_info_prev:
                        document.children[index + 1] = markdown.parse(
                            f"```\n{usage_info_latest}\n```"
                        ).children[0]

        new_readme_text = markdown_renderer.render(document)

    with open("README.md", "w") as readme:
        readme.write(new_readme_text)


if __name__ == "__main__":
    main()
