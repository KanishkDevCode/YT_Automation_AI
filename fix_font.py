
content = open('scripts/assembler.py', encoding='utf-8').read()
content = content.replace('font=\'{font}\':', 'fontfile=\'arial.ttf\':')
open('scripts/assembler.py', 'w', encoding='utf-8').write(content)
print('Font fixes applied.')

