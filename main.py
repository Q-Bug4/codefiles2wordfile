import os
import re
import argparse

# 参数定义
parser = argparse.ArgumentParser(description='Test for argparse')
parser.add_argument('--path', '-p', help='遍历路径', required = True)
parser.add_argument('--output', '-o', help='输出文件名', default='source.md')
args = parser.parse_args()

result = ''
ignores = ['test', 'LICENSE']
ignoresReg = ['^\.', '^(mvnw)']
ignoresExt = ['iml', 'md', 'png', 'jpg']

highlights = {
        'vue': 'javascript',
        'py': 'python',
}

def isIgnore(dir):
    for reg in ignoresReg:
        if re.search(reg, dir) is not None:
            return True
    for ext in ignoresExt:
        if '.' in dir and dir.split('.')[-1] == ext:
            return True
    return dir in ignores

def walk(path):
    res = [path]
    if not os.path.isdir(path):
        return res

    nodes = os.listdir(path)
    for node in nodes:
        if isIgnore(node):
            continue
        p = os.path.join(path, node)
        if os.path.isfile(p):
            res.append(node)
        if os.path.isdir(p):
            res.append(walk(p))
    return res

def output(content):
    global result
    # print(content)
    result += content
    result += '\n'

def dir2md(dirs, level):
    folder = dirs[0]
    files = [f for f in dirs[1:] if isinstance(f, str)]
    dirs = [d for d in dirs[1:] if isinstance(d, list)]
    if len(files) > 0:
        output('#' * level + ' ' + folder)
    else:
        level-=1
    for file in files:
        output('**' + file + '**')
        ext = file.split('.')[-1]
        highlight = ext
        if ext in highlights:
            highlight = highlights[ext]
        output('```' + highlight)
        output(read(folder, file))
        output('```')
    for d in dirs:
        dir2md(d, level + 1)

def read(path, file):
    content = ''
    with open(os.path.join(path, file), 'r', encoding='utf8') as f:
        lines = f.readlines()
        content = '\n'.join(lines)

    return content

dir2md(walk(args.path), 1)
with open(args.output, 'w', encoding='utf8') as f:
    f.write(result)
