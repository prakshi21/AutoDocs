from dotenv import load_dotenv

from app.bootstrap import build_repository_qa

load_dotenv()

qa = build_repository_qa("sample_repo")

response = qa.ask("How does login work?")

print("\n")
print("=" * 80)
print(response.answer)
print("=" * 80)
