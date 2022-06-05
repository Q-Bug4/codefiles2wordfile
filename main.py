import os
import re
import argparse

# 参数定义
parser = argparse.ArgumentParser(description='Test for argparse')
parser.add_argument('--path', '-p', help='遍历路径', required = True)
parser.add_argument('--output', '-o', help='输出文件名', default='source.md')
args = parser.parse_args()

result = ''
highlights = {
        'vue': 'javascript',
        'py': 'python',
}

# 忽略文件
ignores = ['test', 'LICENSE'] # 完全匹配
ignoresReg = ['^\.', '^(mvnw)'] # 正则匹配
ignoresExt = ['iml', 'md', 'png', 'jpg'] # 后缀匹配

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
        # Windows用户需要转移反斜杠，否则word的标题会出错
        output('#' * level + ' ' + folder.replace("\\", "\\\\").replace("#", "\\#").replace(args.path,".", 1))
    else:
        level-=1
    for file in files:
        output('**' + file + '**')
        ext = file.split('.')[-1]
        highlight = ext
        if ext in highlights:
            highlight = highlights[ext]
        output('```' + highlight)
        output(read(folder, file).replace("#", "\\#"))
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
