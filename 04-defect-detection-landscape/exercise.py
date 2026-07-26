# -*- coding: utf-8 -*-
"""
============================================================
第 04 课练习:亲手算清缺陷检测的每一个指标
============================================================

数据只有 8 个样本——与课程 §6 的"阈值-指标计算器"
完全同一组。你在网页上拖动滑块看到的每一个数字
(混淆矩阵四格、P/R/F1、AUROC、最优阈值),
这个练习都要你亲手算出来,算完可以回网页对账。

运行方式:  python exercise.py
完成所有 TODO 后,你应该看到所有测试通过

难度:⭐⭐
预计用时:30-45 分钟
"""

# 与课程 §6 交互计算器完全同一组数据
# 分数越高 = 模型越怀疑它有缺陷;标签 1 = 真缺陷,0 = 真正常
SCORES = [0.9, 0.8, 0.7, 0.6, 0.4, 0.3, 0.2, 0.1]
LABELS = [1,   1,   0,   1,   0,   0,   1,   0]


# ============================================================
# 🧱 Part 1: 混淆矩阵计数(对应课程 §5)
# ============================================================
#
# 卡一个阈值,分数就变成判断:分数 ≥ 阈值 → 报警(预测为缺陷)。
# 判断与真实标签对照,每个样本必落入四格之一:
#   TP 抓对:真缺陷,报了警        FP 误杀:真正常,却报警
#   FN 漏检:真缺陷,却放行        TN 放对:真正常,放行了
#

def confusion_counts(scores, labels, thr):
    """在阈值 thr 下统计混淆矩阵四格。

    Args:
        scores: 异常分数列表,如 [0.9, 0.1]
        labels: 真实标签列表(1=缺陷,0=正常),与 scores 等长
        thr:    阈值,分数 >= thr 判为报警(预测缺陷)

    Returns:
        (tp, fp, fn, tn) 四个整数
    """
    # ======== TODO 1: 在这里写你的代码 ========
    # 提示:用 zip(scores, labels) 逐对遍历;
    #       pred = s >= thr(注意是 >=,分数等于阈值也要报警);
    #       pred 与 label 的四种组合分别计入 tp / fp / fn / tn。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 1 ========


# ============================================================
# 🧱 Part 2: 精确率、召回率与 F1(对应课程 §5)
# ============================================================
#
#   精确率 P = 抓对 / 所有报警   = TP / (TP + FP)  → 报警可信吗?
#   召回率 R = 抓对 / 所有真缺陷 = TP / (TP + FN)  → 缺陷抓全了吗?
#   F1 = 2PR / (P + R):调和平均,重罚偏科。
#

def precision_recall_f1(tp, fp, fn):
    """由三格计数算 (p, r, f1);任何分母为 0 时,对应值返回 0.0。

    Returns:
        (p, r, f1) 三个浮点数
    """
    # ======== TODO 2: 在这里写你的代码 ========
    # 提示:p = tp/(tp+fp),但 tp+fp == 0 时 p = 0.0;r 同理;
    #       f1 = 2*p*r/(p+r),p+r == 0 时 f1 = 0.0。
    #       (请按 2*p*r/(p+r) 这个形式算,测试用精确断言)

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 2 ========


# ============================================================
# 🧱 Part 3: ROC 曲线(对应课程 §6)
# ============================================================
#
# 把阈值从"高过所有分数"一路降到最低分,每个阈值算一对:
#   FPR = FP / 所有真正常(冤枉了多少良品)→ 横轴
#   TPR = TP / 所有真缺陷(抓住了多少缺陷,就是召回率)→ 纵轴
# 阈值最高时谁都不报警 → (0,0);阈值最低时全报警 → (1,1)。
#

def roc_curve(scores, labels):
    """扫描全部阈值,返回 ROC 点列 [(fpr, tpr), ...]。

    阈值依次取:[1.1] + 按降序排列的 scores(共 len(scores)+1 个)。

    Returns:
        [(fpr, tpr), ...],从 (0.0, 0.0) 单调爬到 (1.0, 1.0)
    """
    # ======== TODO 3: 在这里写你的代码 ========
    # 提示:thrs = [1.1] + sorted(scores, reverse=True)
    #       npos = sum(labels);nneg = len(labels) - npos
    #       每个 thr 调 confusion_counts(复用 TODO 1!)拿到 tp、fp,
    #       往结果里 append (fp / nneg, tp / npos)。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 3 ========


# ============================================================
# 🧱 Part 4: AUROC——ROC 曲线下面积(对应课程 §6)
# ============================================================
#
# 对 TODO 3 的点列做梯形积分:相邻两点 (x1,y1)、(x2,y2) 之间的
# 面积 = (x2 - x1) × (y1 + y2) / 2,全部加起来就是 AUROC。
#
# AUROC 的等价读法(课程 §6):随机抽一个真缺陷、一个真正常,
# 模型给缺陷更高分的概率。本组数据 4 正 × 4 负 = 16 对:
#   正样本分数 [0.9, 0.8, 0.6, 0.2],负样本分数 [0.7, 0.4, 0.3, 0.1]
#   0.9 赢 4 对,0.8 赢 4 对,0.6 赢 3 对,0.2 赢 1 对 → 共赢 12 对
#   12 / 16 = 0.75,与梯形积分的结果一模一样(数学上严格等价)。
#

def auroc(scores, labels):
    """AUROC = ROC 点列的梯形积分,返回一个浮点数。"""
    # ======== TODO 4: 在这里写你的代码 ========
    # 提示:pts = roc_curve(scores, labels)(复用 TODO 3!)
    #       遍历相邻点对,累加 (x2-x1)*(y1+y2)/2。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 4 ========


# ============================================================
# 🧱 Part 5: 扫描最优 F1 阈值(对应课程 §5-§6)
# ============================================================
#
# 部署前的常见操作:在候选阈值里逐个试,选 F1 最大的那个。
# 候选阈值就取 scores 里出现过的每个分数——其他任何阈值的
# 报警结果,都必然与某个候选相同(想想为什么)。
#

def best_f1_threshold(scores, labels):
    """扫描候选阈值,返回 (最优阈值, 对应的 F1)。

    F1 并列时返回其中最大的阈值(报警越少越省复检人力)。

    Returns:
        (thr, f1)
    """
    # ======== TODO 5: 在这里写你的代码 ========
    # 提示:候选阈值按从大到小遍历:sorted(scores, reverse=True);
    #       每个 thr:confusion_counts → precision_recall_f1(串联 TODO 1、2);
    #       只在 f1「严格大于」当前最优时更新——这样并列时自动保留更大的阈值。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 5 ========


# ============================================================
# 🧪 测试
# ============================================================

def test_confusion_counts():
    print("测试 1: confusion_counts ...")
    out = confusion_counts(SCORES, LABELS, 0.5)
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 1 后再运行。")
        return False
    if out != (3, 1, 1, 3):
        print("  ❌ 结果不对:thr=0.5 期望 (3, 1, 1, 3),得到 %r。" % (out,))
        print("     检查:报警的是 ①②③④(分数≥0.5),其中 ③ 是正常品(误杀);")
        print("     放行的 ⑤⑥⑦⑧ 里 ⑦ 是真缺陷(漏检)。")
        return False
    out2 = confusion_counts(SCORES, LABELS, 0.9)
    if out2 != (1, 0, 3, 4):
        print("  ❌ 边界不对:thr=0.9 期望 (1, 0, 3, 4),得到 %r。" % (out2,))
        print("     检查:分数「等于」阈值也要报警(用 >=,不是 >)。")
        return False
    print("  ✅ 通过!thr=0.5 → (3,1,1,3),与课程 §5 的数值例子一致。")
    return True


def test_precision_recall_f1():
    print("测试 2: precision_recall_f1 ...")
    out = precision_recall_f1(3, 1, 1)
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 2 后再运行。")
        return False
    if out != (0.75, 0.75, 0.75):
        print("  ❌ 结果不对:(3,1,1) 期望 (0.75, 0.75, 0.75),得到 %r。" % (out,))
        print("     检查:P = 3/4,R = 3/4,F1 = 2×0.75×0.75/(0.75+0.75)。")
        return False
    if precision_recall_f1(0, 0, 4) != (0.0, 0.0, 0.0):
        print("  ❌ 除零处理不对:一个都不报警时(tp=0, fp=0),")
        print("     (p, r, f1) 应返回 (0.0, 0.0, 0.0) 而不是抛异常。")
        return False
    print("  ✅ 通过!P/R/F1 与除零处理都正确。")
    return True


def test_roc_curve():
    print("测试 3: roc_curve ...")
    if confusion_counts(SCORES, LABELS, 0.5) is None:
        print("  ❌ roc_curve 需要复用 confusion_counts,先完成 TODO 1。")
        return False
    pts = roc_curve(SCORES, LABELS)
    if pts is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 3 后再运行。")
        return False
    if len(pts) != 9:
        print("  ❌ 点数不对:阈值取 [1.1] + 8 个分数 → 应有 9 个点,得到 %d 个。" % len(pts))
        return False
    if pts[0] != (0.0, 0.0) or pts[-1] != (1.0, 1.0):
        print("  ❌ 端点不对:首点应为 (0.0, 0.0)(最严阈值谁都不报警),")
        print("     末点应为 (1.0, 1.0)(最松阈值全报警)。得到 %r ... %r" % (pts[0], pts[-1]))
        return False
    mono = all(pts[i + 1][0] >= pts[i][0] and pts[i + 1][1] >= pts[i][1]
               for i in range(len(pts) - 1))
    if not mono:
        print("  ❌ 点列不单调:阈值从高到低扫时,FPR 和 TPR 只会增不会减。")
        print("     检查:阈值是否按降序排列?")
        return False
    if (0.25, 0.75) not in pts:
        print("  ❌ 中间点不对:阈值 0.6 时 tp=3、fp=1,应有点 (0.25, 0.75),点列里没有它。")
        return False
    print("  ✅ 通过!9 个点从 (0,0) 单调爬到 (1,1)。")
    return True


def test_auroc():
    print("测试 4: auroc ...")
    if confusion_counts(SCORES, LABELS, 0.5) is None or roc_curve(SCORES, LABELS) is None:
        print("  ❌ auroc 需要复用 roc_curve,先完成 TODO 1 和 TODO 3。")
        return False
    val = auroc(SCORES, LABELS)
    if val is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 4 后再运行。")
        return False
    if abs(val - 0.75) > 1e-6:
        print("  ❌ 结果不对:期望 0.75(容差 1e-6),得到 %r。" % val)
        print("     检查:梯形面积是 (x2-x1)*(y1+y2)/2,别忘了除以 2。")
        return False
    print("  ✅ 通过!AUROC = 0.75 —— 正负 16 对里模型赢了 12 对,12/16 = 0.75,")
    print("     梯形积分和「排序胜率」两种算法答案一致(见 Part 4 注释)。")
    return True


def test_best_f1_threshold():
    print("测试 5: best_f1_threshold ...")
    prereq = (confusion_counts(SCORES, LABELS, 0.5) is not None
              and precision_recall_f1(1, 1, 1) is not None)
    if not prereq:
        print("  ❌ 先完成 TODO 1 和 TODO 2,再来挑战阈值扫描。")
        return False
    result = best_f1_threshold(SCORES, LABELS)
    if result is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 5 后再运行。")
        return False
    thr, f1 = result
    print("    扫描结果: 最优阈值 %s,F1 = %s" % (thr, f1))
    if thr == 0.6 and f1 == 0.75:
        print("  ✅ 通过!去课程 §6 把滑块拖到 0.6,网页上的 P/R/F1 应与你算的一致。")
        return True
    print("  ❌ 结果不对:期望 (0.6, 0.75),得到 (%r, %r)。" % (thr, f1))
    print("     检查:每个候选阈值都要走一遍 confusion_counts → precision_recall_f1;")
    print("     F1 并列时保留更大的阈值(从大到小扫 + 严格大于才更新)。")
    return False


if __name__ == "__main__":
    print("=" * 52)
    print("第 04 课练习:亲手算清缺陷检测的每一个指标")
    print("=" * 52)
    all_passed = True
    all_passed = test_confusion_counts() and all_passed
    all_passed = test_precision_recall_f1() and all_passed
    all_passed = test_roc_curve() and all_passed
    all_passed = test_auroc() and all_passed
    all_passed = test_best_f1_threshold() and all_passed
    print("-" * 52)
    if all_passed:
        print("🎉 全部通过!混淆矩阵、P/R/F1、ROC、AUROC、最优阈值——")
        print("   缺陷检测的整块记分牌你已经亲手算过一遍。下一课见。")
    else:
        print("💪 还有测试没通过,按提示继续加油!")
