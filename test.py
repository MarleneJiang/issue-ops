"""."""

from importlib.metadata import metadata

metadata = metadata("alicebot-plugin-template")

email=(metadata.get_all("Author-email"))
if email is not None and "<" in email[0]: # PDM发包问题
            print(email[0].split("<")[0].strip())