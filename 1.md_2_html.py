
import os
import markdown

def find_md_files(root):
    """递归查找所有md文件（含中文）"""
    md_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            if filename.lower().endswith('.md') and os.path.isfile(os.path.join(dirpath, filename)):
                md_files.append(os.path.join(dirpath, filename))
    return md_files

md_files = find_md_files('.')

for md_file in md_files:
    with open(md_file, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # 转HTML内容
    html = markdown.markdown(
        md_text,
        extensions=['toc', 'fenced_code', 'tables'],
        extension_configs={
            'toc': {
                'toc_depth': '3',
                'title': ''
            }
        }
    )

    # 目录生成，必须加fenced_code避免误识别代码块里的#
    md_obj = markdown.Markdown(extensions=['toc', 'fenced_code'])
    md_obj.convert(md_text)
    toc_html = md_obj.toc

    tpl = f"""
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>{os.path.splitext(os.path.basename(md_file))[0]}</title>
<style>
body {{ margin: 0; padding: 0; font-family: sans-serif; background: #f5f5f5; }}
#wrapper {{ max-width: 950px; margin: 0 auto; padding-right: 300px; }}
#content {{
    background: #fff;
    padding: 40px;
    min-height: 100vh;
    box-shadow: 0 2px 14px #eee;
}}
#content img {{
    display: block;
    margin: 24px auto;
    max-width: 100%;
    height: auto;
    box-shadow: 0 4px 12px #eee;
    background: #fff;
}}
#content pre {{
    background: #fafbfc;
    border-radius: 6px;
    padding: 16px;
    margin: 20px 0;
    overflow-x: auto;
    font-size: 16px;
}}
#content pre:empty {{
    display: none;
}}
#content div:empty {{
    min-height: 0 !important;
    background: none !important;
}}
#toc {{
    position: fixed;
    top: 0;
    right: 0;
    width: 270px;
    height: 100vh;
    overflow-y: auto;
    background: #f8f8f8;
    border-left: 1px solid #e0e0e0;
    padding: 32px 16px 32px 24px;
    box-shadow: -3px 0 7px 0 #eee;
    z-index: 100;
}}
#toc ul {{
    list-style: none;
    padding-left: 0;
    margin: 0;
}}
#toc ul ul {{
    padding-left: 18px;
    border-left: 2px solid #e0e0e0;
    margin-left: 8px;
}}
#toc li {{
    margin-bottom: 3px;
}}
#toc a {{
    color: #222;
    text-decoration: none;
    font-size: 15px;
    transition: color 0.2s;
}}
#toc a:hover {{
    color: #1a73e8;
}}
@media (max-width: 1200px) {{
    #toc {{ display: none; }}
    #wrapper {{ padding-right: 0; }}
}}
</style>
</head>
<body>
<div id="wrapper">
    <div id="content">
        {html}
    </div>
</div>
<div id="toc">
    <div style="font-weight:bold;margin-bottom:12px;">目录</div>
    {toc_html}
</div>
</body>
</html>
"""

    # 输出html到同目录同名文件
    html_file = os.path.splitext(md_file)[0] + '.html'
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(tpl)
    print(f"已生成 {html_file}")

print('全部转换完成！')
