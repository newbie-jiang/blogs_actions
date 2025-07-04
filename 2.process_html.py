


import os

output_root = "blogs"
index_html = os.path.join(output_root, "index.html")

def collect_html_files(root):
    data = {}
    total_count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        html_files = [f for f in filenames if f.lower().endswith('.html') and f.lower() != "index.html"]
        if html_files:
            rel_dir = os.path.relpath(dirpath, root)
            if rel_dir == ".":
                rel_dir = "主页"
            data.setdefault(rel_dir, [])
            for file in html_files:
                data[rel_dir].append(file)
                total_count += 1
    return data, total_count

def gen_index_html(data, total_count):
    # 跳过 index.html 并确定第一个可展示的页面
    first_href = ""
    html = [
        '<!DOCTYPE html>',
        '<html lang="zh-cn">',
        '<head>',
        '  <meta charset="utf-8">',
        '  <title>内容导航主页</title>',
        '  <style>',
        '    body { margin: 0; font-family: "Kaiti", "楷体", "Microsoft YaHei", "SimKai", "KaiTi", Helvetica, Arial, sans-serif; background: #eef0f7; }',
        '    .container { display: flex; height: 100vh; }',
        '    .sidebar { width: 300px; background: linear-gradient(180deg,#f9fafb 80%,#e9eefa); border-right: 1px solid #e1e4ed; box-shadow: 2px 0 8px 0 #ccd6e5; padding-top: 24px; overflow-y: auto; font-family: "Kaiti", "楷体", "Microsoft YaHei", "SimKai", "KaiTi", serif; }',
        '    .sidebar h1 { font-size: 1.5em; font-weight: 700; color: #1b3876; text-align: center; margin-bottom: 32px; letter-spacing: 1px; font-family: "Kaiti", "楷体", "Microsoft YaHei", "SimKai", "KaiTi", serif; }',
        '    .sidebar .dir-btn {',
        '        background: none; border: none; outline: none; cursor: pointer; font-size: 1.1em; font-weight: bold; color: #253768;',
        '        display: flex; align-items: center; width: 100%; padding: 8px 12px; margin-top: 10px; border-radius: 7px;',
        '        transition: background 0.2s;',
        '        font-family: "Kaiti", "楷体", "Microsoft YaHei", "SimKai", "KaiTi", serif;',
        '        justify-content: space-between;',
        '    }',
        '    .sidebar .dir-btn:hover { background: #dde8f7; }',
        '    .sidebar .dir-arrow { font-size: 1.0em; margin-right: 6px; transition: transform 0.2s; color: #7f8aa7;}',
        '    .sidebar .collapsed > .dir-arrow { transform: rotate(-90deg); }',
        '    .sidebar ul { list-style: none; padding-left: 28px; margin: 2px 0 10px 0; transition: max-height 0.3s; }',
        '    .sidebar li { margin: 4px 0; }',
        '    .sidebar a { color: #174e88; text-decoration: none; font-size: 1.0em; padding: 2px 4px; border-radius: 4px; display: inline-block; transition: all 0.15s; font-family: "Kaiti", "楷体", "Microsoft YaHei", "SimKai", "KaiTi", serif;}',
        '    .sidebar a:hover, .sidebar a.active { background: #cbe3fd; color: #22b94f; font-weight: bold;}',
        '    .sidebar .divider { border-top: 1px solid #ececec; margin: 16px 0; }',
        '    .main { flex: 1; min-width: 0; background: #fff; }',
        '    iframe { width: 100%; height: 100vh; border: none; background: #fff; }',
        '    @media (max-width: 700px) { .container { flex-direction: column; } .sidebar { width: 100vw; height: 250px; border-right: none; border-bottom: 1px solid #eee; } .main { height: calc(100vh - 250px); } }',
        '    ::-webkit-scrollbar { width: 8px; background: #e3e9f1; }',
        '    ::-webkit-scrollbar-thumb { background: #c1d4ee; border-radius: 5px; }',
        '  </style>',
        '</head>',
        '<body>',
        '<div class="container">',
        '  <nav class="sidebar">',
        f'    <h1>blogs内容导航 <span style="font-size:0.65em;color:#666;">（共{total_count}篇）</span></h1>',
    ]

    for i, dirname in enumerate(sorted(data.keys())):
        group_id = f"dir_{i}"
        collapsed = "" if i == 0 else "collapsed"
        count = len(data[dirname])
        html.append(f'<div class="dir-section {collapsed}">')
        if dirname == "主页":
            html.append(
                f'<button class="dir-btn" onclick="toggleDir(\'{group_id}\', this)" style="background:#e8eff9;font-size:1.2em;">🏠 {dirname} <span style="color:#8496b5;font-size:0.9em;">({count})</span></button>')
        else:
            html.append(
                f'<button class="dir-btn" onclick="toggleDir(\'{group_id}\', this)"><span class="dir-arrow">&#9654;</span>{dirname} <span style="color:#8496b5;font-size:0.9em;">({count})</span></button>')
        display = "" if i == 0 else 'style="display:none;"'
        html.append(f'<ul id="{group_id}" {display}>')
        for filename in sorted(data[dirname], key=lambda s: s.lower()):
            show_name = filename[:-5] if filename.lower().endswith('.html') else filename
            href = os.path.join(dirname, filename) if dirname != "主页" else filename
            if not first_href:
                first_href = href  # 只记录第一个内容页
            html.append(
                f'<li><a href="{href}" target="preview" onclick="setActive(this);return false;">{show_name}</a></li>')
        html.append('</ul>')
        html.append('</div>')
        html.append('<div class="divider"></div>')
    html += [
        '  </nav>',
        '  <main class="main">',
        f'    <iframe name="preview" src="{first_href if first_href else ""}"></iframe>',
        '  </main>',
        '</div>',
        '<script>',
        'function setActive(link) {',
        '  document.querySelectorAll(".sidebar a").forEach(a => a.classList.remove("active"));',
        '  link.classList.add("active");',
        '  document.querySelector("iframe").src = link.getAttribute("href");',
        '}',
        'function toggleDir(id, btn) {',
        '  var ul = document.getElementById(id);',
        '  if (ul.style.display === "none") {',
        '    ul.style.display = "";',
        '    btn.classList.remove("collapsed");',
        '  } else {',
        '    ul.style.display = "none";',
        '    btn.classList.add("collapsed");',
        '  }',
        '}',
        'window.onload = function() {',
        '  var first = document.querySelector(".sidebar a");',
        '  if(first) first.classList.add("active");',
        '};',
        '</script>',
        '</body></html>'
    ]
    return "\n".join(html)

if __name__ == "__main__":
    files_by_dir, total_count = collect_html_files(output_root)
    index = gen_index_html(files_by_dir, total_count)
    with open(index_html, "w", encoding="utf-8") as f:
        f.write(index)
    print(f"导航主页已生成: {index_html}")
