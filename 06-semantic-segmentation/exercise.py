# -*- coding: utf-8 -*-
"""
============================================================
第 06 课练习:亲手实现分割的上采样与评价
============================================================

分割网络的"放大"和"打分",拆开都不神秘:
上采样把特征图放大回去(decoder 的日常),
Dice / IoU 给预测 mask 打分,
阈值把概率图切成非黑即白的 mask。
最后把它们串起来,复现课程 §7 交互里的现象:
Dice 随阈值先升后降,最优阈值在中间。

运行方式:  python exercise.py
完成所有 TODO 后,你应该看到所有测试通过

难度:⭐⭐
预计用时:25-40 分钟
"""


# ============================================================
# 🧱 Part 1: 最近邻上采样(对应课程 §3)
# ============================================================
#
# decoder 每一级都要把特征图放大 2 倍。
# 最近邻是最朴素的放大:每个值原地复制成 factor×factor 的小方块。
#
#   [1 2]      [1 1 2 2]
#   [3 4]  →   [1 1 2 2]
#              [3 3 4 4]
#              [3 3 4 4]
#

def upsample_nearest(fmap, factor=2):
    """最近邻上采样:每个值复制成 factor×factor 的小方块。

    Args:
        fmap:   H×W 的二维列表,如 [[1,2],[3,4]]
        factor: 放大倍数(正整数),默认 2

    Returns:
        (H*factor)×(W*factor) 的二维列表
    """
    # ======== TODO 1: 在这里写你的代码 ========
    # 提示:输出位置 (r, c) 的值 = fmap[r // factor][c // factor]。
    #       两层循环遍历输出的每个 (r, c),逐行 append 即可。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 1 ========


# ============================================================
# 🧱 Part 2: Dice 系数(对应课程 §6)
# ============================================================
#
#     Dice = 2|A∩B| / (|A| + |B|)
#
# 分子:两个 mask 都为 1 的像素数 × 2;
# 分母:两个 mask 各自的 1 像素数直接相加(不是并集!)。
# 背景像素(两边都 0)完全不进公式——这就是它免疫类别不平衡的原因。
#

def dice_score(pred_mask, gt_mask):
    """计算两个 0/1 mask 的 Dice 系数。

    Args:
        pred_mask: H×W 的二维列表,元素为 0 或 1
        gt_mask:   H×W 的二维列表,元素为 0 或 1

    Returns:
        float:2*交 / (|pred|+|gt|)。两个 mask 都全空时返回 1.0
        (空对空 = 完美一致:没缺陷,也没报缺陷)。
    """
    # ======== TODO 2: 在这里写你的代码 ========
    # 提示:三个计数器扫一遍矩阵:
    #       inter(两边都是 1)、p(pred 里 1 的个数)、g(gt 里 1 的个数)。
    #       若 p + g == 0 返回 1.0,否则返回 2 * inter / (p + g)。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 2 ========


# ============================================================
# 🧱 Part 3: mask 版 IoU(对应课程 §6,和第 05 课的框 IoU 一脉相承)
# ============================================================
#
#     IoU = |A∩B| / |A∪B|,其中 |A∪B| = |A| + |B| − |A∩B|
#
# 第 05 课算的是两个矩形框的 IoU,这里把"框"换成任意形状的像素集合,
# 公式一个字都不用改。
#

def iou_mask(pred_mask, gt_mask):
    """计算两个 0/1 mask 的 IoU(交并比)。

    Returns:
        float:交 / 并。两个 mask 都全空时返回 1.0。
    """
    # ======== TODO 3: 在这里写你的代码 ========
    # 提示:和 TODO 2 同样的三个计数器;并集 = p + g − inter。
    #       并集为 0 返回 1.0,否则返回 inter / 并集。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 3 ========


# ============================================================
# 🧱 Part 4: 阈值二值化(对应课程 §7)
# ============================================================
#
# 分割网络输出的是概率图,不是 mask。
# 部署时要切一刀:大于等于阈值记 1(缺陷),否则记 0(背景)。
#

def binarize(prob_map, thr):
    """把概率图按阈值切成 0/1 mask。

    Args:
        prob_map: H×W 的二维列表,元素为 0~1 的浮点数
        thr:      阈值。大于等于 thr 记 1,否则记 0

    Returns:
        H×W 的 0/1 二维列表
    """
    # ======== TODO 4: 在这里写你的代码 ========
    # 提示:一个双层列表推导就够:
    #       [[1 if v >= thr else 0 for v in row] for row in prob_map]

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 4 ========


# ============================================================
# 🧱 Part 5: 串联!扫阈值,找 Dice 峰值(对应课程 §7)
# ============================================================
#
# 固定数据:一张 8×8 的"预测概率图"和它的 GT mask。
# GT:第 3-4 行 × 第 3-5 列共 6 个缺陷像素。
# 概率图:5 个缺陷像素很自信(0.80),缺陷像素 (4,5) 犹豫(0.55),
#         背景 (1,1) 有一处自信的误报(0.65),
#         缺陷边缘 4 个位置轻微扩散(0.40),其余背景 0.10。
#
# 对每个候选阈值:binarize → dice_score,看哪个阈值的 Dice 最高。
# 你会亲眼看到课程 §7 交互里那条"先升后降"的曲线。
#

GT_MASK = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

PROB_MAP = [
    [0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10],
    [0.10, 0.65, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10],  # (1,1):背景误报 0.65
    [0.10, 0.10, 0.10, 0.40, 0.40, 0.10, 0.10, 0.10],  # (2,3)(2,4):边缘扩散 0.40
    [0.10, 0.10, 0.10, 0.80, 0.80, 0.80, 0.10, 0.10],  # 缺陷像素 0.80
    [0.10, 0.10, 0.10, 0.80, 0.80, 0.55, 0.10, 0.10],  # (4,5):犹豫的缺陷像素 0.55
    [0.10, 0.10, 0.10, 0.10, 0.40, 0.40, 0.10, 0.10],  # (5,4)(5,5):边缘扩散 0.40
    [0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10],
    [0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10],
]


def best_threshold(prob_map, gt_mask, thrs=[0.3, 0.5, 0.6, 0.7]):
    """扫一遍候选阈值,返回 Dice 最高的那个。

    Args:
        prob_map: H×W 概率图
        gt_mask:  H×W 真值 mask
        thrs:     候选阈值列表

    Returns:
        (best_thr, best_dice):Dice 最高的阈值及其 Dice 值。
        并列时返回先遇到的那个。
    """
    # ======== TODO 5: 在这里写你的代码 ========
    # 提示(三步):
    #   1. 对每个 thr:pred = binarize(prob_map, thr)
    #   2. d = dice_score(pred, gt_mask)
    #   3. 记录最大的 d 及其 thr(严格大于才更新,保证并列取先者),
    #      最后返回 (best_thr, best_dice)

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 5 ========


# ============================================================
# 🧪 测试
# ============================================================

# ---- TODO 2 / TODO 3 共用的固定测试数据 ----
# GT 同 GT_MASK:6 个缺陷像素(第 3-4 行 × 第 3-5 列)。
# pred 也是 6 个像素:漏掉了 GT 的 (4,5),多报了背景的 (4,6)
# → |pred|=6、|gt|=6、交=5
# → Dice = 2×5/(6+6) = 10/12 ≈ 0.8333
# → IoU  = 5/(6+6−5) = 5/7   ≈ 0.7143
PRED_65 = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]


def test_upsample():
    print("测试 1: upsample_nearest ...")
    out = upsample_nearest([[1, 2], [3, 4]], 2)
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 1 后再运行。")
        return False
    expect = [[1, 1, 2, 2], [1, 1, 2, 2], [3, 3, 4, 4], [3, 3, 4, 4]]
    if out == expect:
        if upsample_nearest([[5]], 3) == [[5, 5, 5], [5, 5, 5], [5, 5, 5]]:
            print("  ✅ 通过!每个值都变成了 factor×factor 的小方块。")
            return True
        print("  ❌ factor=3 的情况不对:[[5]] 应变成 3×3 的全 5,检查 // factor 的下标。")
        return False
    print("  ❌ 结果不对:期望 %r,得到 %r。" % (expect, out))
    print("     检查:输出应为 4×4,out[r][c] = in[r//2][c//2]。")
    return False


def test_dice():
    print("测试 2: dice_score ...")
    d = dice_score(PRED_65, GT_MASK)
    if d is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 2 后再运行。")
        return False
    if abs(d - 10.0 / 12.0) < 1e-4:
        empty = [[0, 0], [0, 0]]
        if dice_score(empty, empty) == 1.0:
            print("  ✅ 通过!pred 6 px、gt 6 px、交 5 → Dice = 10/12 ≈ 0.8333,空对空 = 1.0。")
            return True
        print("  ❌ 空 mask 对空 mask 应返回 1.0(没缺陷,也没报缺陷 = 完美一致)。")
        return False
    print("  ❌ 结果不对:期望 10/12 ≈ 0.8333,得到 %r。" % d)
    print("     检查:分子是 2×交集(2×5),分母是两个 mask 的像素数之和(6+6),不是并集。")
    return False


def test_iou():
    print("测试 3: iou_mask ...")
    v = iou_mask(PRED_65, GT_MASK)
    if v is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 3 后再运行。")
        return False
    if abs(v - 5.0 / 7.0) < 1e-4:
        print("  ✅ 通过!同一组 mask:交 5、并 7 → IoU = 5/7 ≈ 0.7143(注意比 Dice 的 0.8333 低)。")
        return True
    print("  ❌ 结果不对:期望 5/7 ≈ 0.7143,得到 %r。" % v)
    print("     检查:并集 = |pred| + |gt| − 交 = 6 + 6 − 5 = 7,别把分母写成了 |pred|+|gt|。")
    return False


def test_binarize():
    print("测试 4: binarize ...")
    out = binarize([[0.2, 0.8], [0.5, 0.3]], 0.5)
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 4 后再运行。")
        return False
    if out == [[0, 1], [1, 0]]:
        if binarize([[0.2, 0.8], [0.5, 0.3]], 0.9) == [[0, 0], [0, 0]]:
            print("  ✅ 通过!边界值 0.5 ≥ 0.5 正确记 1(是'大于等于',不是'大于')。")
            return True
        print("  ❌ thr=0.9 时应全为 0,检查比较方向。")
        return False
    print("  ❌ 结果不对:期望 [[0,1],[1,0]],得到 %r。" % out)
    print("     检查:0.5 ≥ 0.5 应记 1 —— 用 >=,不是 >。")
    return False


def test_best_threshold():
    print("测试 5: best_threshold(扫阈值找 Dice 峰值)...")
    prereq = (binarize([[0.6]], 0.5) is not None
              and dice_score([[1]], [[1]]) is not None)
    if not prereq:
        print("  ❌ 先完成 TODO 2 和 TODO 4,再来挑战串联。")
        return False
    result = best_threshold(PROB_MAP, GT_MASK)
    if result is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 5 后再运行。")
        return False
    # 打印整条曲线,亲眼看"先升后降"
    print("    阈值扫描(你的 binarize + dice_score 算出的曲线):")
    for t in [0.3, 0.5, 0.6, 0.7]:
        d = dice_score(binarize(PROB_MAP, t), GT_MASK)
        print("      阈值 %.1f → Dice %.4f" % (t, d))
    best_thr, best_dice = result
    if best_thr == 0.5 and abs(best_dice - 12.0 / 13.0) < 1e-3:
        print("    返回结果: (best_thr=%.1f, best_dice=%.4f)" % (best_thr, best_dice))
        print("  ✅ 通过!最优阈值是 0.5,不是最高的 0.7 ——")
        print("     0.7 虽然干净(Dice 0.909)但把犹豫的真缺陷 (4,5) 切掉了;")
        print("     0.5 把它捞回来,只多背一个误报,Dice 冲到 0.923;")
        print("     0.3 连边缘扩散全放进来,Dice 反而跌到 0.706。")
        print("     —— 最优阈值不是最高阈值,它在漏检和误报的拉锯中间(课程 §7)。")
        return True
    print("  ❌ 结果不对:期望 (0.5, ≈0.9231),得到 (%r, %r)。" % (best_thr, best_dice))
    print("     检查:是否对每个阈值都 binarize → dice_score?是否用'严格大于'更新最大值?")
    return False


if __name__ == "__main__":
    print("=" * 52)
    print("第 06 课练习:亲手实现分割的上采样与评价")
    print("=" * 52)
    all_passed = True
    all_passed = test_upsample() and all_passed
    all_passed = test_dice() and all_passed
    all_passed = test_iou() and all_passed
    all_passed = test_binarize() and all_passed
    all_passed = test_best_threshold() and all_passed
    print("-" * 52)
    if all_passed:
        print("🎉 全部通过!分割的上采样、评价和阈值选择你已全部亲手实现。")
        print("   下一课起转入无监督路线:零缺陷标注,只学\"正常长什么样\"。")
    else:
        print("💪 还有测试没通过,按提示继续加油!")
