import subprocess
import os

os.chdir(r'c:\CANTINA-FATEC\cantina-Fatec-2026')

print("Git status:")
subprocess.run(['git', 'status'])

print("\n\nAdicionando arquivos...")
subprocess.run(['git', 'add', '-A'])

print("\n\nFazendo commit...")
subprocess.run(['git', 'commit', '-m', 'Correção: adicionar classes Pagamento e Consumo, e métodos listar_estoque e listar_produtos_disponiveis'])

print("\n\nGit log (ultimas mudanças):")
subprocess.run(['git', 'log', '--oneline', '-5'])
