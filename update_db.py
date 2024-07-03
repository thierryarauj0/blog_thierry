import subprocess

# Comandos Git para adicionar e commitar as alterações
subprocess.run(["git", "add", "blog.db"])
subprocess.run(["git", "commit", "-m", "Atualização automática do banco de dados"])

# Comando Git para fazer push das alterações
subprocess.run(["git", "push", "origin", "master"])
