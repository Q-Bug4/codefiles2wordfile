# codefiles2wordfile
遍历目录下所有代码文件，生成markdown文件后转为MS Word文件

# 环境
`Python3 + Docker`

# 使用
1. 查看`main.py`中的文件忽略配置，按需进行修改。
2. 遍历所有代码放入一个markdown文件中：`python main.py -p path -o mdFile`


3. 使用pandoc将md文件转为MS Word文件
```bash
docker run --rm \             
       --volume "$(pwd):/data" \
       --user $(id -u):$(id -g) \
       pandoc/core mdFile -o docxFile -t docx
```

# 例子
1. `python main.py -p /project/demo -o source.md`
2. 
```bash
docker run --rm \             
       --volume "$(pwd):/data" \
       --user $(id -u):$(id -g) \
       pandoc/core source.md -o outfile.docx -t docx
```

# 常见报错
1. 文件读取错误
一般该错误提示如下. 主要原因是因为没有过滤掉一些二进制或者非纯文本的文件，导致读取出错。
```python
File "/usr/lib/python3.10/codecs.py", line 322, in decode
    (result, consumed) = self._buffer_decode(data, self.errors, final)
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xa8 in position 14: invalid start byte
```
