# -*- coding: utf-8 -*-
"""
============================================================
第 07 课练习:亲手实现重构误差检测器
============================================================

重构类方法的检测端出奇地朴素,只有一条链:
    异常图 = (输入 − 重构)²  →  归一化  →  阈值  →  定位

本练习用纯 Python(零依赖)把这条链完整走一遍。
"重构"从哪来?我们采用"完美画师"假设——直接拿正常模板
充当网络画出的重构图(真实 AE 训练好之后干的就是这件事,
只是画得没这么完美),这样你可以把注意力全部放在检测端的
几何上。

运行方式:  python exercise.py
完成所有 TODO 后,你应该看到所有测试通过

难度:⭐⭐
预计用时:25-40 分钟
"""


# ============================================================
# 🧱 Part 1: 逐像素平方误差图(对应课程 §3)
# ============================================================
#
# anomaly map 的原子操作:两张同尺寸的图逐像素相减、再平方。
# 平方的作用:① 去掉正负号(画亮了、画暗了都是"画错了");
#             ② 放大大误差、压低小误差。
#

def mse_map(img, recon):
    """逐像素计算 (img - recon)²。

    Args:
        img:   H×W 的二维列表(输入图)
        recon: H×W 的二维列表(重构图,与 img 同尺寸)

    Returns:
        H×W 的二维列表,每个元素 = (img[r][c] - recon[r][c]) ** 2
    """
    # ======== TODO 1: 在这里写你的代码 ========
    # 提示:两层循环(或列表推导式),
    #       out[r][c] = (img[r][c] - recon[r][c]) ** 2

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 1 ========


# ============================================================
# 🧱 Part 2: 图像级分数(对应课程 §3)
# ============================================================
#
# 像素级异常图回答"缺陷在哪",图像级分数回答"这件要不要拦下"。
# 两种常用口径:
#   max  —— 对小而尖锐的缺陷敏感(一个像素画错就报警)
#   mean —— 对大面积缺陷稳健(整体画不像才报警)
#

def image_score(amap, mode):
    """把整张异常图汇总成一个数。

    Args:
        amap: H×W 的二维列表
        mode: 'max' 或 'mean'

    Returns:
        mode='max'  → 全图最大值
        mode='mean' → 全图平均值(浮点数)
    """
    # ======== TODO 2: 在这里写你的代码 ========
    # 提示:先把二维摊平成一维列表(双层循环或推导式),
    #       'max' 用 max(...),'mean' 用 sum(...) / 元素个数。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 2 ========


# ============================================================
# 🧱 Part 3: 归一化(对应课程 §3 与交互 1)
# ============================================================
#
# 不同图的误差量级差很远,先做 min-max 归一化压到 [0, 1],
# 后面才能用统一的阈值(比如 0.5)切分。
#
#     v  →  (v - min) / (max - min)
#
# 特殊情况:全图同一个值(max == min)时,分母为 0——
# 约定返回全 0(一张"毫无起伏"的误差图就是毫无异常)。
#

def normalize_map(amap):
    """把 amap 线性归一化到 [0, 1];max == min 时返回同尺寸的全 0。"""
    # ======== TODO 3: 在这里写你的代码 ========
    # 提示:先求全图 min 和 max;
    #       若 max == min,返回 [[0, 0, ...], ...](尺寸同 amap);
    #       否则每个元素替换为 (v - mn) / (mx - mn)。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 3 ========


# ============================================================
# 🧱 Part 4: 阈值分割(对应课程交互 1 的滑块)
# ============================================================
#
# 把连续的异常图切成非黑即白的判定:≥ 阈值记 1(异常像素),
# 否则记 0。顺手数一数检出了多少个像素。
#

def threshold_map(amap, thr):
    """阈值分割。

    Args:
        amap: H×W 的二维列表(通常已归一化到 0~1)
        thr:  阈值

    Returns:
        (mask, count):mask 是 H×W 的 0/1 二维列表;count 是 1 的个数
    """
    # ======== TODO 4: 在这里写你的代码 ========
    # 提示:mask[r][c] = 1 if amap[r][c] >= thr else 0,
    #       count 把所有 1 加起来,最后 return mask, count。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 4 ========


# ============================================================
# 🧱 Part 5: 串联!最小可用的"重构检测器"(对应课程 §3)
# ============================================================
#
# "完美画师"假设:不管输入什么,画师都返回正常模板 TEMPLATE。
# 于是 |输入 − 重构| 的几何完全由缺陷贡献。
#
# 流水线:
#   ① amap = mse_map(img, template)      画不像的地方误差大
#   ② norm = normalize_map(amap)          压到 0~1
#   ③ mask, count = threshold_map(norm, 0.5)
#   ④ 用 mask 中所有 1 的行列范围,框出缺陷包围盒
#

TEMPLATE = [[5] * 8 for _ in range(8)]      # 正常件:8×8,亮度均匀为 5

DEFECT_IMG = [[5] * 8 for _ in range(8)]    # 同一件,但右上多了一块亮斑
for _r in (2, 3):
    for _c in (5, 6):
        DEFECT_IMG[_r][_c] = 9              # 2×2 的缺陷区,亮度 9


def locate_defect(img, template):
    """返回缺陷包围盒 (min_r, min_c, max_r, max_c);没有缺陷像素时返回 None。"""
    # ======== TODO 5: 在这里写你的代码 ========
    # 提示(四步,每步一两行):
    #   1. amap = mse_map(img, template)
    #   2. norm = normalize_map(amap)
    #   3. mask, count = threshold_map(norm, 0.5)
    #      若 count == 0,return None(正常件,零检出)
    #   4. 遍历 mask,收集所有值为 1 的 (r, c),
    #      返回 (min(所有r), min(所有c), max(所有r), max(所有c))

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 5 ========


# ============================================================
# 🧪 测试
# ============================================================

def _close(a, b, tol=1e-9):
    """嵌套列表的近似相等比较(对浮点误差友好)。"""
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_close(x, y, tol) for x, y in zip(a, b))
    try:
        return abs(a - b) <= tol
    except TypeError:
        return a == b


def test_mse_map():
    print("测试 1: mse_map ...")
    out = mse_map([[1, 2], [3, 4]], [[1, 0], [3, 0]])
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 1 后再运行。")
        return False
    if out == [[0, 4], [0, 16]]:
        print("  ✅ 通过!逐像素 (a−b)² 正确:[[0,4],[0,16]]。")
        return True
    print("  ❌ 结果不对:期望 [[0,4],[0,16]],得到 %r。" % out)
    print("     检查:out[0][1] = (2−0)² = 4,out[1][1] = (4−0)² = 16。")
    return False


def test_image_score():
    print("测试 2: image_score ...")
    amap = [[0, 4], [0, 16]]
    s_max = image_score(amap, 'max')
    if s_max is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 2 后再运行。")
        return False
    s_mean = image_score(amap, 'mean')
    if s_max == 16 and s_mean is not None and _close(s_mean, 5.0):
        print("  ✅ 通过!max=16(最尖的误差),mean=5.0(平均误差)。")
        return True
    print("  ❌ 结果不对:期望 max→16、mean→5.0,得到 %r / %r。" % (s_max, s_mean))
    print("     检查:mean = (0+4+0+16) / 4 = 5.0,注意除的是元素个数。")
    return False


def test_normalize_map():
    print("测试 3: normalize_map ...")
    out = normalize_map([[0, 4], [0, 16]])
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 3 后再运行。")
        return False
    if not _close(out, [[0, 0.25], [0, 1.0]]):
        print("  ❌ 结果不对:期望 [[0,0.25],[0,1.0]],得到 %r。" % out)
        print("     公式:(v − min) / (max − min),这里 min=0、max=16。")
        return False
    flat = normalize_map([[3, 3], [3, 3]])
    if not _close(flat, [[0, 0], [0, 0]]):
        print("  ❌ 特殊情况没处理:全图同值(max==min)时应返回全 0,得到 %r。" % flat)
        print("     否则会除以 0 —— 一张'毫无起伏'的误差图不该让程序崩溃。")
        return False
    print("  ✅ 通过!含 max==min 的保护分支。")
    return True


def test_threshold_map():
    print("测试 4: threshold_map ...")
    res = threshold_map([[0, 0.25], [0, 1.0]], 0.5)
    if res is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 4 后再运行。")
        return False
    if not (isinstance(res, (tuple, list)) and len(res) == 2):
        print("  ❌ 返回值应是 (mask, count) 二元组,得到 %r。" % (res,))
        return False
    mask, count = res
    if mask == [[0, 0], [0, 1]] and count == 1:
        print("  ✅ 通过!只有 1.0 ≥ 0.5,检出 1 个像素 —— 交互 1 里滑块做的就是这件事。")
        return True
    print("  ❌ 结果不对:期望 ([[0,0],[0,1]], 1),得到 (%r, %r)。" % (mask, count))
    print("     注意:是 ≥ 阈值记 1;0.25 < 0.5,所以不算。")
    return False


def test_locate_defect():
    print("测试 5: 重构检测器串联 ...")
    prereq = (mse_map([[1]], [[0]]) is not None
              and normalize_map([[0, 1]]) is not None
              and threshold_map([[0.6]], 0.5) is not None)
    if not prereq:
        print("  ❌ 先完成 TODO 1、3、4,再来串流水线。")
        return False
    bbox = locate_defect(DEFECT_IMG, TEMPLATE)
    if bbox is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 5 后再运行。")
        return False
    if tuple(bbox) == (2, 5, 3, 6):
        print("    缺陷包围盒 (min_r, min_c, max_r, max_c) = (2, 5, 3, 6) —— 正中亮斑!")
        try:
            clean = locate_defect(TEMPLATE, TEMPLATE)
        except Exception as e:
            print("  ❌ 正常件(输入=模板)让程序抛了异常:%s" % e)
            print("     检查:count == 0 时要提前返回 None,别对空列表取 min/max。")
            return False
        if clean is not None:
            print("  ❌ 正常件(输入=模板)应返回 None(无缺陷像素),得到 %r。" % (clean,))
            print("     检查:count == 0 时要提前返回 None。")
            return False
        print("    正常件输入 → None(零误检)。")
        print("  ✅ 通过!重构类检测 = |输入 − 重构| 的几何:")
        print("     画师只会画正常(这里由模板代劳),减一下,缺陷自己现形;")
        print("     真实 AE 无非把'查模板'换成'网络画一张正常件',后面的链路一模一样。")
        return True
    print("  ❌ 结果不对:期望 (2, 5, 3, 6),得到 %r。" % (bbox,))
    print("     检查:mask 中为 1 的像素应恰好是 rows 2-3 × cols 5-6 这四个。")
    return False


if __name__ == "__main__":
    print("=" * 52)
    print("第 07 课练习:亲手实现重构误差检测器")
    print("=" * 52)
    all_passed = True
    all_passed = test_mse_map() and all_passed
    all_passed = test_image_score() and all_passed
    all_passed = test_normalize_map() and all_passed
    all_passed = test_threshold_map() and all_passed
    all_passed = test_locate_defect() and all_passed
    print("-" * 52)
    if all_passed:
        print("🎉 全部通过!你已经写出了重构类方法的整个检测端。")
        print("   下一课:不重构图像,直接在特征空间给'正常'建档案。")
    else:
        print("💪 还有测试没通过,按提示继续加油!")
