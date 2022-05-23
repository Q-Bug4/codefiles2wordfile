# codefiles2wordfile
遍历目录下所有代码文件，生成markdown文件后转为MS Word文件

# 环境
`Python3 + Docker`

# 使用
1. 遍历所有代码放入一个markdown文件中：`python main.py -p path -o mdFile`


2. 使用pandoc将md文件转为MS Word文件
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
