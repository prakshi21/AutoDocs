from parser.markdown_parser import MarkdownParser

parser = MarkdownParser()

sections = parser.parse("sample_repo/README.md")

for section in sections:
    print("=" * 60)
    print(f"Title      : {section.title}")
    print(f"Level      : {section.level}")
    print(f"Lines      : {section.start_line}-{section.end_line}")
    print(f"ID         : {section.id}")
    print("Content")
    print(section.content)
