#!/usr/bin/env python3
"""
观察者库同步脚本 — 将竞彩分析数据写入桌面竞彩分析库（Obsidian 格式）
用法：
  python3 obsidian_sync.py prediction <date> <json_data>   # 写每日预测
  python3 obsidian_sync.py review <date> <json_data>       # 写每日复盘
  python3 obsidian_sync.py model <json_data>               # 更新模型参数
  python3 obsidian_sync.py league <json_data>              # 更新联赛统计
"""
import sys, json, os
from datetime import datetime, date

VAULT = "/mnt/c/Users/Administrator/Desktop/竞彩分析库"

def today():
    return date.today().strftime("%Y-%m-%d")

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


### 每日预测 ###
def write_prediction(pred_date, data):
    """写入每日预测笔记"""
    path = f"{VAULT}/每日预测/{pred_date}.md"
    matches = data.get("matches", [])
    main_picks = data.get("main_picks", [])
    high_odds = data.get("high_odds", [])
    parlays = data.get("parlays", [])
    lotto14 = data.get("lotto14", [])
    ren9 = data.get("ren9", {})

    lines = []
    lines.append(f"# {pred_date} 每日预测")
    lines.append(f"\n> 自动抓取自 500.com | {now()}\n")

    # 竞彩场次表
    if matches:
        lines.append("## 📋 今日竞彩场次\n")
        lines.append("| 编号 | 联赛 | 主队 | 客队 | 开赛时间 | 主胜 | 平 | 客胜 |")
        lines.append("|:---:|:----:|:----:|:----:|:--------:|:----:|:--:|:----:|")
        for m in matches:
            lines.append(
                f"| {m.get('no','')} | {m.get('league','')} | {m.get('home','')} | "
                f"{m.get('away','')} | {m.get('time','')} | {m.get('win','')} | "
                f"{m.get('draw','')} | {m.get('lose','')} |"
            )
        lines.append("")

    # 主力推荐
    if main_picks:
        lines.append("## ⭐ 主力推荐\n")
        lines.append("| 优先 | 场次 | 推荐玩法 | 赔率 | 信心 | 理由 |")
        lines.append("|:----:|:-----|:--------:|:----:|:----:|:-----|")
        for p in main_picks:
            lines.append(
                f"| {p.get('priority','')} | {p.get('match','')} | {p.get('pick','')} | "
                f"{p.get('odds','')} | {p.get('confidence','')} | {p.get('reason','')} |"
            )
        lines.append("")

    # 高赔复式
    if high_odds:
        lines.append("## 🎯 高赔复式\n")
        lines.append("| 场次 | 玩法 | 选项 | 赔率 |")
        lines.append("|:-----|:----:|:----:|:----:|")
        for h in high_odds:
            lines.append(f"| {h.get('match','')} | {h.get('type','')} | {h.get('pick','')} | {h.get('odds','')} |")
        lines.append("")

    # 串关
    if parlays:
        lines.append("## ⛓️ 串关组合\n")
        lines.append("| 组合 | 场次 | 玩法 | 综合赔率 | 仓位 |")
        lines.append("|:----:|:-----|:----:|:--------:|:----:|")
        for p in parlays:
            lines.append(f"| {p.get('combo','')} | {p.get('matches','')} | {p.get('type','')} | {p.get('odds','')} | {p.get('stake','')} |")
        lines.append("")

    # 14场
    if lotto14:
        lines.append("## 📐 14场胜负彩\n")
        lines.append("| 场次 | 主队 | 客队 | 推荐 | 胆材 |")
        lines.append("|:----:|:----:|:----:|:----:|:----:|")
        for m in lotto14:
            lines.append(f"| {m.get('no','')} | {m.get('home','')} | {m.get('away','')} | {m.get('pick','')} | {m.get('dan','')} |")
        lines.append("")

        # 任9
        if ren9:
            lines.append("### 任选9方案\n")
            lines.append(f"> {ren9.get('desc','')}\n")
            lines.append("| 类型 | 场次 | 推荐 |")
            lines.append("|:----:|:-----|:----:|")
            for r in ren9.get("picks", []):
                lines.append(f"| {r.get('type','')} | {r.get('match','')} | {r.get('pick','')} |")
            lines.append("")

    lines.append("\n---\n")
    lines.append(f"*自动生成于 {now()}*")

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ 预测笔记已写入: {path}")


### 每日复盘 ###
def write_review(review_date, data):
    """写入每日复盘笔记"""
    path = f"{VAULT}/每日复盘/{review_date}.md"
    stats = data.get("stats", {})
    reviews = data.get("reviews", [])
    errors = data.get("errors", [])
    suggestions = data.get("suggestions", [])

    lines = []
    lines.append(f"# {review_date} 每日复盘")
    lines.append(f"\n> 自动复盘 | {now()}\n")

    # 命中统计
    if stats:
        lines.append("## 📊 命中统计\n")
        lines.append("| 指标 | 数值 |")
        lines.append("|:----|:----:|")
        for k, v in stats.items():
            lines.append(f"| {k} | {v} |")
        lines.append("")

    # 逐场复盘
    if reviews:
        lines.append("## 🔍 逐场复盘\n")
        lines.append("| 场次 | 推荐 | 赔率 | 实际比分 | 结果 | 分析 |")
        lines.append("|:----|:----:|:----:|:--------:|:----:|:----|")
        for r in reviews:
            lines.append(
                f"| {r.get('match','')} | {r.get('pick','')} | {r.get('odds','')} | "
                f"{r.get('score','')} | {r.get('result','')} | {r.get('analysis','')} |"
            )
        lines.append("")

    # 错误分析
    if errors:
        lines.append("## ❌ 错误分析\n")
        lines.append("| 场次 | 错误原因 | 修正措施 | 状态 |")
        lines.append("|:-----|:---------|:---------|:----:|")
        for e in errors:
            lines.append(f"| {e.get('match','')} | {e.get('reason','')} | {e.get('fix','')} | {e.get('status','')} |")
        lines.append("")

    # 模型更新建议
    if suggestions:
        lines.append("## 📈 模型更新建议\n")
        for s in suggestions:
            lines.append(f"- {s}")
        lines.append("")

    lines.append("\n---\n")
    lines.append(f"*自动生成于 {now()}*")

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ 复盘笔记已写入: {path}")


### 更新模型参数 ###
def update_model(data):
    """更新模型参数笔记"""
    path = f"{VAULT}/模型参数/当前参数.md"
    leagues = data.get("leagues", [])
    weights = data.get("weights", {})
    stakes = data.get("stakes", [])

    lines = []
    lines.append(f"# 当前模型参数\n")
    lines.append(f"> 最后更新：{now()}\n")

    if leagues:
        lines.append("## 🎯 联赛基准率\n")
        lines.append("| 联赛 | 主胜 | 平局 | 客胜 | 样本数 |")
        lines.append("|:----|:----:|:----:|:----:|:------:|")
        for l in leagues:
            lines.append(f"| {l.get('name','')} | {l.get('home','')} | {l.get('draw','')} | {l.get('away','')} | {l.get('samples','')} |")
        lines.append("")

    if weights:
        lines.append("## ⚖️ 权重配置\n")
        lines.append("| 权重项 | 当前值 | 说明 |")
        lines.append("|:------|:------:|:-----|")
        for k, v in weights.items():
            lines.append(f"| {v.get('name',k)} | {v.get('value','')} | {v.get('desc','')} |")
        lines.append("")

    lines.append("---\n")
    lines.append("*此文件由自学习系统自动维护*\n")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ 模型参数已更新: {path}")

    # 同时更新修正日志
    update_error_log(data.get("error_log", []))


### 更新修正日志 ###
def update_error_log(errors):
    if not errors:
        return
    path = f"{VAULT}/模型参数/修正日志.md"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    new_entries = []
    for e in errors:
        entry = f"{e.get('date','')} | {e.get('match','')} | {e.get('type','')} | {e.get('reason','')} | {e.get('fix','')} | ✅已执行"
        new_entries.append(entry)

    # 在"## 日志格式"后面插入新条目
    marker = "## 错误类型分类"
    insert = "\n".join(new_entries) + "\n\n"
    # 找到日志格式示例后面
    content = content.replace("## 错误类型分类", insert + "## 错误类型分类")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 修正日志已更新")


### 更新联赛统计 ###
def update_league_stats(data):
    path = f"{VAULT}/联赛统计/联赛基准率.md"
    leagues = data.get("leagues", [])

    lines = []
    lines.append(f"# 联赛基准率统计\n")
    lines.append(f"> 基于历史数据的各联赛胜平负概率统计\n")
    lines.append("## 联赛基准率（当前）\n")
    lines.append("| 联赛 | 主胜 | 平局 | 客胜 | 样本 | 更新时间 |")
    lines.append("|:----|:----:|:----:|:----:|:----:|:--------:|")
    for l in leagues:
        lines.append(f"| {l.get('name','')} | {l.get('home','')} | {l.get('draw','')} | {l.get('away','')} | {l.get('samples','')} | {now()} |")
    lines.append("")

    lines.append("## 更新规则\n")
    lines.append("- 每新增 10 场同联赛数据 → 重新计算基准率")
    lines.append("- 计算公式：0.7×历史基准 + 0.3×新统计（最近50场）")
    lines.append("- 更新频率：每周自动校准\n")
    lines.append("---\n")
    lines.append("*自动维护*\n")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ 联赛统计已更新: {path}")


### 主入口 ###
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法:")
        print("  python3 obsidian_sync.py prediction <日期> <json数据>")
        print("  python3 obsidian_sync.py review <日期> <json数据>")
        print("  python3 obsidian_sync.py model <json数据>")
        print("  python3 obsidian_sync.py league <json数据>")
        print("  python3 obsidian_sync.py deep_warning <json数据>")
        print("  python3 obsidian_sync.py update_index <next_update>")
        sys.exit(1)

    action = sys.argv[1]

    if action == "prediction":
        pred_date = sys.argv[2] if len(sys.argv) > 2 else today()
        data = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        write_prediction(pred_date, data)

    elif action == "review":
        review_date = sys.argv[2] if len(sys.argv) > 2 else today()
        data = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        write_review(review_date, data)

    elif action == "model":
        data = json.loads(sys.argv[2])
        update_model(data)

    elif action == "league":
        data = json.loads(sys.argv[2])
        update_league_stats(data)

    elif action == "deep_warning":
        data = json.loads(sys.argv[2])
        # 更新深盘预警库 - 简化版，直接追加JSON数据
        path = f"{VAULT}/模型参数/深盘预警库.md"
        entry = data.get("entry", {})
        lines_to_add = f"\n| {entry.get('date','')} | {entry.get('match','')} | {entry.get('league','')} | {entry.get('odds','')} | {entry.get('result','')} | {entry.get('note','')} |"
        with open(path, "a", encoding="utf-8") as f:
            f.write(lines_to_add)
        print(f"✅ 深盘预警已更新")

    elif action == "update_index":
        next_update = sys.argv[2] if len(sys.argv) > 2 else "明日"
        idx_path = f"{VAULT}/索引.md"
        with open(idx_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("{{DATE}}", today())
        content = content.replace("{{NEXT_UPDATE}}", next_update)
        with open(idx_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ 索引已更新")

    else:
        print(f"未知操作: {action}")
        sys.exit(1)
