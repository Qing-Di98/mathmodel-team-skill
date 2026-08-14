#!/usr/bin/env python3
"""为课件提取版 md 添加"## 目录"（TOC）— 渐进式披露：>100 行的参考文件顶部加目录。

用法:
    python add_toc.py                 # 扫描本目录及子目录全部 *.md
    python add_toc.py 文件1.md 文件2   # 只处理指定文件

规则:
    - 已含 "## 目录" 的文件跳过（幂等，可重复运行）。
    - 类 A（已有 Markdown 标题语法 `^#{1,3} `）：直接提取标题生成 TOC，不动正文。
    - 类 B（纯中文序号文本）：行首匹配序号模式（第X讲/第一部分：/一、/X.Y）→ 转成
      `##`/`###`/`####` 标题（内容不变，只加前缀），再生成 TOC。
    - 代码块防护:位于 ``` 围栏内的行一律不处理（课件 md 中 `#` 常是 Python 注释，
      不能当标题）。

退出码: 0=全部成功; 1=有文件处理失败。
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOC_MARKER = "## 目录"
FENCE = re.compile(r"^```")
# 类 B 序号模式 -> (正则, 标题级数)
# 注意：单数字序号（"1. xxx"）在课件里几乎全是列表项，禁止作为章节模式。
NUM_PATTERNS = [
    (re.compile(r"^第[一二三四五六七八九十百]+[章节讲部分]"), 2),   # 第X讲 / 第一部分：
    (re.compile(r"^[一二三四五六七八九十百]+、"), 3),               # 一、二、...
    (re.compile(r"^\d+\.\d+\.?\s*"), 4),                            # 2.1 / 3.2.1 子节编号
]
HEADING_RE = re.compile(r"^(#{1,3})\s+(.+?)\s*$")
# 代码特征：docx 提取可能丢 ``` 围栏，裸 `# 注释` 会伪装成标题。
# 含这些符号的行视为代码注释而非标题（防御性过滤）。
CODE_CHARS = re.compile(r"[=()\[\]\"'{}*]|LpVariable|np\.|prob\.|print\(|range\(|for |import ")


def toc_anchor(text: str) -> str:
    """GitHub 风格锚点：小写、空格转连字符、去标点（中文保留）。"""
    slug = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return slug.replace(" ", "-")


def looks_like_code(line: str) -> bool:
    """启发式：标题行含代码特征符号则判为代码注释。"""
    return bool(CODE_CHARS.search(line))


def build_toc_from_headings(lines):
    """类 A：从现有标题行提取 TOC 条目（带锚点链接），跳过代码块与代码注释。"""
    entries = []
    in_fence = False
    for line in lines:
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if m:
            title = m.group(2).strip()
            if looks_like_code(title):
                continue  # 无围栏代码注释伪装成标题
            entries.append((len(m.group(1)), title))
    if not entries:
        return None
    body = ["- " + ("  " * (lvl - 2)) + f"[{title}](#{toc_anchor(title)})"
            for lvl, title in entries]
    return body


def heading_for(line):
    """类 B：序号行转标题，返回 (标题级数, 标题文本)；不匹配返回 None。"""
    for pat, level in NUM_PATTERNS:
        if pat.match(line):
            text = line.strip()
            return level, text
    return None


def process(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if TOC_MARKER in text:
        return f"skip  (已有目录) {path.name}"
    lines = text.splitlines()

    # 判断类型：存在真正标题语法（不在代码块内）即为类 A
    in_fence = False
    has_md_heading = False
    for line in lines:
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence and HEADING_RE.match(line):
            has_md_heading = True
            break

    toc_body = None
    if has_md_heading:
        toc_body = build_toc_from_headings(lines)
    if toc_body is None:
        # 类 B（或类 A 过滤后为空）：序号转标题 + 生成纯文本 TOC
        out, toc_lines = [], []
        in_fence = False
        converted = 0
        for line in lines:
            if FENCE.match(line):
                in_fence = not in_fence
                out.append(line)
                continue
            if not in_fence:
                h = heading_for(line)
                if h and not HEADING_RE.match(line):
                    lvl, title = h
                    out.append("#" * lvl + " " + title)
                    toc_lines.append("- " + title)
                    converted += 1
                    continue
            out.append(line)
        if toc_lines:
            toc_body = toc_lines
            lines = out
        else:
            return f"warn  (未找到可提取结构) {path.name}"

    if not toc_body:
        return f"warn  (未找到可提取结构) {path.name}"

    header = [TOC_MARKER, ""] + toc_body + ["", "---", ""]
    new_text = "\n".join(header + lines) + "\n"
    path.write_text(new_text, encoding="utf-8")
    n = len(toc_body)
    kind = "标题" if has_md_heading else "序号转标题"
    return f"ok    ({kind} {n} 条) {path.name}"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = [Path(a) for a in sys.argv[1:]]
    if args:
        targets = [p if p.is_absolute() else (HERE / p) for p in args]
    else:
        targets = sorted(HERE.rglob("*.md"))
    targets = [p for p in targets if p.is_file()]

    bad = 0
    for p in targets:
        try:
            print(process(p))
        except Exception as e:  # noqa: BLE001 — 单个文件失败不影响其余
            bad += 1
            print(f"error ({e}) {p.name}")
    print(f"共 {len(targets)} 个文件，失败 {bad} 个")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
