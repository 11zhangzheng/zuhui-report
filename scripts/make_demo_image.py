#!/usr/bin/env python3
"""make_demo_image.py — 生成 README 用的"输入 → 输出"对比图。

依赖：Pillow、Windows 自带中文字体（微软雅黑 / Consolas）。
用法：python scripts/make_demo_image.py
输出：assets/demo.png
"""

import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "demo.png")

FONT_REG = "C:/Windows/Fonts/msyh.ttc"
FONT_BOLD = "C:/Windows/Fonts/msyhbd.ttc"
FONT_MONO = "C:/Windows/Fonts/consola.ttf"

INK = (30, 41, 59, 255)
BODY = (51, 65, 85, 255)
MUTED = (100, 116, 139, 255)
INDIGO = (90, 103, 216, 255)
INDIGO_D = (67, 56, 202, 255)
EMERALD = (16, 185, 129, 255)
PANEL = (255, 255, 255, 255)
BUBBLE_AI = (241, 245, 249, 255)


def font(size, bold=False, mono=False):
    path = FONT_MONO if mono else (FONT_BOLD if bold else FONT_REG)
    return ImageFont.truetype(path, size)


def wrap(text, f, max_w):
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur)
            cur = ""
            continue
        if f.getlength(cur + ch) <= max_w:
            cur += ch
        else:
            lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines


def gradient_bg(w, h):
    top, bot = (238, 242, 255), (248, 250, 252)
    img = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / (h - 1)
        img.putpixel((0, y), tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    return img.resize((w, h)).convert("RGBA")


def panel(base, box, radius=30):
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle([box[0] + 4, box[1] + 16, box[2] + 4, box[3] + 16],
                         radius=radius, fill=(15, 23, 42, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    base.alpha_composite(sh)
    ImageDraw.Draw(base).rounded_rectangle(box, radius=radius, fill=PANEL)


def draw_bubble(d, x_left, content_w, y, text, is_user, f, max_w=540):
    lines = wrap(text, f, max_w - 44)
    lh = f.size + 12
    h = lh * len(lines) + 28
    w = min(max(f.getlength(l) for l in lines) + 44, max_w)
    if is_user:
        x0 = x_left + content_w - w
        bg, fg = INDIGO, (255, 255, 255, 255)
    else:
        x0 = x_left
        bg, fg = BUBBLE_AI, BODY
    d.rounded_rectangle([x0, y, x0 + w, y + h], radius=18, fill=bg)
    ty = y + 14
    for l in lines:
        d.text((x0 + 22, ty), l, font=f, fill=fg)
        ty += lh
    return y + h


def main():
    img = gradient_bg(W, H)
    d = ImageDraw.Draw(img)

    # ---- title ----
    d.text((W // 2, 66), "从一整段对话，到一份组会汇报", font=font(58, True),
           fill=INK, anchor="ma")
    d.text((W // 2, 148), "zuhui-report  ·  Agent Skill", font=font(30),
           fill=MUTED, anchor="ma")

    left = [70, 215, 870, 1010]
    right = [1050, 215, 1850, 1010]
    panel(img, left)
    panel(img, right)
    d = ImageDraw.Draw(img)

    # ---- left header ----
    d.rounded_rectangle([100, 248, 322, 292], radius=22, fill=(238, 242, 255, 255))
    d.text((118, 258), "输入 · 当前会话", font=font(24, True), fill=INDIGO_D)
    d.text((100, 306), "和 AI 迭代科研的零散对话", font=font(22), fill=MUTED)

    # ---- chat ----
    f_chat = font(23)
    lx, lw = 100, 740
    y = 356
    chat = [
        ("帮我跑一下 GNN 基线实验", True),
        ("数据管线完成：ChEMBL 12,480 条，8:1:1 划分", False),
        ("再加个 2D 骨架特征试试", True),
        ("验证集 RMSE 反升到 0.83，疑似过拟合", False),
        ("batch>64 会 OOM，我用梯度累积绕过了", False),
        ("组会要汇报，帮我整理一下", True),
    ]
    for text, is_user in chat:
        y = draw_bubble(d, lx, lw, y, text, is_user, f_chat) + 20

    # ---- trigger caption (balance the left panel) ----
    d.rounded_rectangle([100, 884, 840, 966], radius=18, fill=(238, 242, 255, 255))
    d.rounded_rectangle([100, 884, 108, 966], radius=4, fill=INDIGO)
    d.text((132, 925), "触发：把这次对话整理成组会汇报",
           font=font(23, True), fill=INDIGO_D, anchor="lm")

    # ---- right header ----
    d.rounded_rectangle([1080, 248, 1302, 292], radius=22, fill=(236, 253, 245, 255))
    d.text((1098, 258), "输出 · 组会汇报", font=font(24, True), fill=(5, 150, 105, 255))
    d.text((1330, 258), "Markdown", font=font(20, True), fill=EMERALD)
    d.text((1080, 306), "可直接发给导师", font=font(22), fill=MUTED)
    # ---- report ----
    rx, rw = 1080, 740
    f_doc_title = font(30, True)
    f_h = font(25, True)
    f_b = font(22)
    yy = 356
    d.text((rx, yy), "组会汇报 · 分子性质预测", font=f_doc_title, fill=INK)
    yy += 52

    sections = [
        ("一、本周工作进展", ["GNN 基线搭建完成（3 层 MP + 注意力池化）",
                        "数据管线：12,480 条，8:1:1 划分"]),
        ("二、实验 / 研究结果", ["基线 RMSE 0.71，优于随机森林 0.89",
                          "失败：+2D 骨架特征 → 0.83（疑过拟合）"]),
        ("三、现存难点", ["数据划分可能泄漏 → 改 scaffold split【待验证】"]),
        ("四、下一步工作计划", ["scaffold split 重跑基线（2–3 天）"]),
        ("五、需要组会讨论的问题", ["骨架拆分结果如何在论文中呈现？"]),
    ]
    for title, bullets in sections:
        d.text((rx, yy), title, font=f_h, fill=INDIGO_D)
        yy += 38
        for b in bullets:
            d.ellipse([rx + 6, yy + 11, rx + 16, yy + 21], fill=EMERALD)
            d.text((rx + 28, yy), b, font=f_b, fill=BODY)
            yy += 36
        yy += 16

    # ---- highlight box ----
    box = [rx, yy + 4, rx + rw, yy + 96]
    d.rounded_rectangle(box, radius=18, fill=(236, 253, 245, 255))
    d.rounded_rectangle([rx, yy + 4, rx + 8, yy + 96], radius=4, fill=EMERALD)
    d.text((rx + 30, yy + 22), "导师潜在提问预判", font=font(23, True), fill=(5, 150, 105, 255))
    d.text((rx + 30, yy + 56), "已生成 3 条 · 让你提前想好怎么答", font=font(21), fill=BODY)

    # ---- arrow ----
    cx, cy = 960, 612
    d.ellipse([cx - 66, cy - 66, cx + 66, cy + 66], fill=INDIGO)
    d.text((cx, cy - 4), "→", font=font(76, True), fill=(255, 255, 255, 255), anchor="mm")
    d.text((cx, cy + 96), "一句话生成", font=font(24, True), fill=INDIGO_D, anchor="ma")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.convert("RGB").save(OUT, quality=95)
    print("saved:", os.path.abspath(OUT), img.size)


if __name__ == "__main__":
    main()
