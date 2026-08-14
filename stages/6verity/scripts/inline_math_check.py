# -*- coding: utf-8 -*-
"""内联公式与科学下标校验（6verity 文本质量门禁的一部分）。

用途：写作/终检阶段校验论文源码中
  1) 内联 $...$ 公式可被 mathtext 渲染（防损坏的 LaTeX 残留）；
  2) 无转义星号（如 W\\*）与裸下标/上标（如 r_A、λ_max 文本写法）；
  3) 可选：关键数值锚点完整性（防自动替换破坏数值，锚点文件每行一条）。

用法：
  python inline_math_check.py --file 论文.md [--anchors anchors.txt]
  python inline_math_check.py --file 论文.md [--skip-render]   # 无 matplotlib 时跳过渲染检查

退出码：0 = 全部通过；1 = 存在 FAIL（渲染失败/样式违规/锚点缺失）。

说明：只扫描文本，不生成论文，不编译 PDF。CJK 段与 $$ 块、图片路径行自动跳过。
依赖：matplotlib（不可用且未 --skip-render 时，渲染检查标记为 SKIP，其余检查照常）。
"""
import argparse
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def extract_inline(text):
    """提取内联 $...$（跳过 $$ 块、代码块、图片路径行与标题行）。"""
    lines = text.splitlines()
    in_math = False
    inline = []
    for line in lines:
        s = line.strip()
        if s.startswith("$$"):
            in_math = not in_math
            continue
        if in_math or "figures/" in line or s.startswith("#") or s.startswith("```"):
            continue
        inline += re.findall(r"\$[^$]+\$", line)
    return inline


def check_render(inline, skip=False):
    """渲染检查：返回 (bad_list, status)。status: 'PASS'/'FAIL'/'SKIP'。"""
    if skip:
        return [], "SKIP"
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
        plt.rcParams["axes.unicode_minus"] = False
    except Exception:
        return [], "SKIP"
    bad = []
    for seg in inline:
        if re.search(r"[一-鿿]", seg):
            bad.append((seg, "contains CJK"))
            continue
        try:
            plt.figure(figsize=(6, 1))
            plt.text(0.1, 0.5, seg, fontsize=11)
            plt.gcf().canvas.draw()
            plt.close()
        except Exception as e:
            bad.append((seg, str(e)[:90]))
    return bad, ("FAIL" if bad else "PASS")


def check_style(text):
    """样式检查：转义星号与裸下标/上标（排除 $$ 块、代码块、图片路径行）。"""
    issues = []
    lines = text.splitlines()
    in_math = False
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith("$$"):
            in_math = not in_math
            continue
        if in_math or "figures/" in line or s.startswith("#") or s.startswith("```"):
            continue
        for m in re.finditer(r"[A-Za-zα-ωΑ-Ω]\\\*", line):
            issues.append((i, "esc-star", m.group()))
        outside = re.sub(r"\$[^$]*\$", "$X$", line)
        for m in re.finditer(
            r"[A-Za-zα-ωΑ-ΩλΛμΜνρ](?:_[A-Za-z0-9]+|\^[A-Za-z0-9]+)", outside
        ):
            issues.append((i, "bare-sub", m.group()))
    return issues


def check_anchors(text, anchor_file):
    """锚点检查：锚点文件每行一条，缺失即 FAIL。"""
    if not anchor_file:
        return []
    with open(anchor_file, encoding="utf-8") as f:
        anchors = [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]
    return [a for a in anchors if a not in text]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--file", required=True, help="论文源码文件（md/typ/tex）")
    ap.add_argument("--anchors", default=None, help="锚点文件（每行一条，缺失即报）")
    ap.add_argument("--skip-render", action="store_true", help="跳过 mathtext 渲染检查")
    args = ap.parse_args()

    try:
        text = open(args.file, encoding="utf-8").read()
    except OSError as e:
        print(f"FATAL: 无法读取 {args.file}: {e}")
        sys.exit(2)

    inline = extract_inline(text)
    print(f"inline math segments: {len(inline)}")

    bad, status = check_render(inline, args.skip_render)
    print(f"render: {status} ({len(bad)} bad)")
    for seg, e in bad:
        print(f"  BAD: {seg} -> {e}")

    issues = check_style(text)
    print(f"style issues: {len(issues)}")
    for it in issues:
        print(f"  {it[0]}: {it[1]}: {it[2]}")

    missing = check_anchors(text, args.anchors)
    print(f"anchor missing: {missing if missing else 'NONE'}"
          if args.anchors else "anchor check: skipped (--anchors 未提供)")

    fail = (status == "FAIL") or bool(issues) or bool(missing)
    print("RESULT:", "FAIL" if fail else "PASS")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
