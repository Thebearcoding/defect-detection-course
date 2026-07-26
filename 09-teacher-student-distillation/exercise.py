# -*- coding: utf-8 -*-
"""
============================================================
第 09 课练习:亲手实现师生差异检测器
============================================================

老师(预训练网络)见多识广,学生只在正常样本上学习。
推理时逐位置对比两者的特征:分歧大的地方就是缺陷。

你将用纯 Python(零依赖)实现这条链路的全部算子:
平方差、余弦相似度、异常曲线、滑动平均,
最后串成 find_anomaly_span,
在一条 12 个位置的特征序列上自动框出"师生分歧区间"。

运行方式:  python exercise.py
完成所有 TODO 后,你应该看到所有测试通过

难度:⭐⭐
预计用时:20-35 分钟
"""


# ============================================================
# 🧱 Part 1: 逐位置平方差(对应课程 §2)
# ============================================================
#
# 课程里的异常分数 A(p) = ‖F_T(p) − F_S(p)‖²,
# 最朴素的版本就是逐位置的平方差:
# 两条等长的一维"特征带",每个位置算 (t[i] - s[i])²。
#

def sq_diff(t, s):
    """计算两条等长一维特征的逐位置平方差。

    Args:
        t: 老师特征,如 [1, 2, 3]
        s: 学生特征,与 t 等长,如 [1, 2, 5]

    Returns:
        等长列表,第 i 位 = (t[i] - s[i]) ** 2
        例:[1,2,3] vs [1,2,5] → [0, 0, 4]
    """
    # ======== TODO 1: 在这里写你的代码 ========
    # 提示:一行列表推导。zip(t, s) 把两条特征按位置配对,
    #       每对算 (a - b) ** 2。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 1 ========


# ============================================================
# 🧱 Part 2: 余弦相似度(对应课程 §2)
# ============================================================
#
# 平方差既比方向又比长度;实际方法里更常用余弦相似度,
# 只比"方向像不像",对特征幅值变化更稳:
#
#     cos(a, b) = (a·b) / (‖a‖ × ‖b‖)
#
# 特殊约定:任一方是零向量(模长为 0)时,方向无定义,返回 0.0。
#

def cosine_sim(a, b):
    """计算两个等长向量的余弦相似度。

    Args:
        a, b: 等长的一维列表,如 [1, 0] 和 [0, 1]

    Returns:
        float,范围 [-1, 1];任一方为零向量时返回 0.0
    """
    # ======== TODO 2: 在这里写你的代码 ========
    # 提示:点积 dot = sum(x * y for x, y in zip(a, b));
    #       模长 na = sum(x * x for x in a) ** 0.5,nb 同理;
    #       na 或 nb 为 0 时返回 0.0,否则返回 dot / (na * nb)。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 2 ========


# ============================================================
# 🧱 Part 3: 异常曲线(对应课程 §2 / §6)
# ============================================================
#
# 现在每个位置的特征是一个 2 维向量(真实方法里是几百维,机制相同)。
# 该位置的异常分数 = 1 − cosine_sim(老师向量, 学生向量):
# 方向一致 → 0(正常);方向垂直 → 1(强异常)。
# 这就是课程 §6 交互里下方那条红色曲线。
#

def anomaly_curve(t_feats, s_feats):
    """逐位置计算 1 − 余弦相似度,得到异常分数曲线。

    Args:
        t_feats: 老师特征序列,每个元素是一个向量,如 [[1,0],[0,1]]
        s_feats: 学生特征序列,与 t_feats 等长同形

    Returns:
        等长的分数列表,例:
        t=[[1,0],[0,1],[1,0]], s=[[1,0],[0,1],[0,1]] → [0.0, 0.0, 1.0]
    """
    # ======== TODO 3: 在这里写你的代码 ========
    # 提示:一行列表推导,对 zip(t_feats, s_feats) 的每一对
    #       算 1 - cosine_sim(t, s)。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 3 ========


# ============================================================
# 🧱 Part 4: 居中滑动平均(对应课程 §6)
# ============================================================
#
# 真实方法在给异常图判阈值之前,都会先做一次平滑
# (常用高斯滤波),把孤立的毛刺磨掉,让检出区域更连贯。
# 我们实现它的一维简化版:窗口宽 w 的居中滑动平均,
# 边缘处窗口伸不满就截断,除以"实际窗口长度"。
#

def moving_avg(xs, w=3):
    """对一维序列做居中滑动平均(边缘窗口截断)。

    Args:
        xs: 数值列表,如 [0, 0, 3, 0, 0]
        w:  窗口宽度(奇数),默认 3

    Returns:
        等长的浮点列表,例:
        [0,0,3,0,0], w=3 → [0.0, 1.0, 1.0, 1.0, 0.0]
        (两端的窗口只剩 2 个数,所以除以 2)
    """
    # ======== TODO 4: 在这里写你的代码 ========
    # 提示:half = w // 2。对每个位置 i:
    #       lo = max(0, i - half),hi = min(len(xs), i + half + 1),
    #       取 seg = xs[lo:hi],append sum(seg) / len(seg)。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 4 ========


# ============================================================
# 🧱 Part 5: 串联!框出"师生分歧区间"(对应课程 §2 / §6)
# ============================================================
#
# 固定的玩具数据:一条 12 个位置的特征带。
# 老师全程输出 [1, 0];学生在位置 0-4 和 8-11 背得一字不差,
# 但位置 5-7 是它没学过的图案——只会答 [0, 1]。
#
# 流水线(§6 交互的纯代码版):
#   ① anomaly_curve:逐位置算 1 − cos → [0,0,0,0,0,1,1,1,0,0,0,0]
#   ② 阈值一刀(thr=0.5):收集所有超阈值的位置
#   ③ 返回 (起点, 终点) —— 检出区间,也就是缺陷所在
#
# (本数据曲线干净,不需要先平滑;真实管线里 moving_avg
#  会插在 ① 和 ② 之间,§6 交互的差异曲线就是这么做的。)
#

TEACHER_FEATS = [
    [1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0],
    [1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0],
]

STUDENT_FEATS = [
    [1, 0], [1, 0], [1, 0], [1, 0], [1, 0],   # 位置 0-4:正常,背得一字不差
    [0, 1], [0, 1], [0, 1],                    # 位置 5-7:没学过,模仿失灵
    [1, 0], [1, 0], [1, 0], [1, 0],            # 位置 8-11:正常
]


def find_anomaly_span(t_feats, s_feats, thr=0.5):
    """算异常曲线,框出连续超阈值区段。

    Args:
        t_feats, s_feats: 等长的特征序列(每个位置一个向量)
        thr: 判定阈值,默认 0.5

    Returns:
        (start, end):超阈值位置的起止下标(含两端)。
        没有任何位置超阈值时返回 None。
        (本练习的数据保证超阈值位置恰好连成一段。)
    """
    # ======== TODO 5: 在这里写你的代码 ========
    # 提示(三步):
    #   1. scores = anomaly_curve(t_feats, s_feats)
    #   2. idx = [i for i, v in enumerate(scores) if v > thr]
    #   3. idx 为空返回 None,否则返回 (idx[0], idx[-1])

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 5 ========


# ============================================================
# 🧪 测试
# ============================================================

def _list_close(xs, ys, tol=1e-9):
    """逐元素比较两个数值列表(容差 tol)。"""
    try:
        return (isinstance(xs, list) and len(xs) == len(ys)
                and all(abs(x - y) <= tol for x, y in zip(xs, ys)))
    except TypeError:
        return False


def test_sq_diff():
    print("测试 1: sq_diff ...")
    out = sq_diff([1, 2, 3], [1, 2, 5])
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 1 后再运行。")
        return False
    if out == [0, 0, 4] and sq_diff([2], [5]) == [9]:
        print("  ✅ 通过![1,2,3] vs [1,2,5] → [0,0,4],逐位置平方差正确。")
        return True
    print("  ❌ 结果不对:期望 [0, 0, 4],得到 %r。" % out)
    print("     检查:输出长度应与输入相同,第 i 位 = (t[i]-s[i])**2,(3-5)**2 = 4。")
    return False


def test_cosine_sim():
    print("测试 2: cosine_sim ...")
    c1 = cosine_sim([1, 0], [0, 1])
    if c1 is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 2 后再运行。")
        return False
    c2 = cosine_sim([1, 1], [2, 2])
    c3 = cosine_sim([0, 0], [1, 2])
    ok1 = abs(c1 - 0.0) <= 1e-9
    ok2 = c2 is not None and abs(c2 - 1.0) <= 1e-9
    ok3 = c3 == 0.0
    if ok1 and ok2 and ok3:
        print("  ✅ 通过!垂直→0、同向→1、零向量→0.0,三种情况都正确。")
        return True
    if not ok1:
        print("  ❌ cosine_sim([1,0],[0,1]) 期望 0.0,得到 %r。垂直向量点积为 0。" % c1)
    if not ok2:
        print("  ❌ cosine_sim([1,1],[2,2]) 期望 1.0(容差 1e-9),得到 %r。" % c2)
        print("     同方向的向量,无论长度,余弦相似度都是 1。")
    if not ok3:
        print("  ❌ cosine_sim([0,0],[1,2]) 期望 0.0,得到 %r。" % c3)
        print("     零向量没有方向——先判断模长是否为 0,再做除法。")
    return False


def test_anomaly_curve():
    print("测试 3: anomaly_curve ...")
    if cosine_sim([1, 0], [1, 0]) is None:
        print("  ❌ anomaly_curve 依赖 cosine_sim,先完成 TODO 2。")
        return False
    out = anomaly_curve([[1, 0], [0, 1], [1, 0]], [[1, 0], [0, 1], [0, 1]])
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 3 后再运行。")
        return False
    if _list_close(out, [0.0, 0.0, 1.0]):
        print("  ✅ 通过!前两个位置方向一致 → 0,第三个位置方向垂直 → 1。")
        return True
    print("  ❌ 结果不对:期望 [0.0, 0.0, 1.0](容差 1e-9),得到 %r。" % out)
    print("     检查:每个位置的分数 = 1 - cosine_sim(t, s),不是 cosine_sim 本身。")
    return False


def test_moving_avg():
    print("测试 4: moving_avg ...")
    out = moving_avg([0, 0, 3, 0, 0], 3)
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 4 后再运行。")
        return False
    ok1 = _list_close(out, [0.0, 1.0, 1.0, 1.0, 0.0])
    out2 = moving_avg([2, 2, 2, 2])
    ok2 = _list_close(out2, [2.0, 2.0, 2.0, 2.0])
    if ok1 and ok2:
        print("  ✅ 通过![0,0,3,0,0] → [0.0,1.0,1.0,1.0,0.0],边缘窗口截断也正确。")
        return True
    if not ok1:
        print("  ❌ 结果不对:期望 [0.0, 1.0, 1.0, 1.0, 0.0],得到 %r。" % out)
        print("     检查:窗口要以 i 为中心(左右各 w//2),边缘处窗口变短,")
        print("     除以的是实际窗口长度 len(seg),而不是固定的 w。")
    if not ok2:
        print("  ❌ 默认参数不对:moving_avg([2,2,2,2]) 期望 [2.0]*4,得到 %r。" % out2)
    return False


def test_find_anomaly_span():
    print("测试 5: 师生分歧检测器 ...")
    prereq = (cosine_sim([1, 0], [1, 0]) is not None
              and anomaly_curve([[1, 0]], [[1, 0]]) is not None)
    if not prereq:
        print("  ❌ 先完成 TODO 2 和 TODO 3,再来挑战流水线。")
        return False
    result = find_anomaly_span(TEACHER_FEATS, STUDENT_FEATS)
    if result is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 5 后再运行。")
        print("     (若你已实现:阈值 0.5 下位置 5-7 的分数是 1.0,不该返回 None。)")
        return False
    if not (isinstance(result, (tuple, list)) and len(result) == 2):
        print("  ❌ 返回形状不对:期望 (start, end) 二元组,得到 %r。" % (result,))
        return False
    start, end = result
    print("    定位结果: 检出区间 (%s, %s)" % (start, end))
    if (start, end) == (5, 7):
        scores = anomaly_curve(TEACHER_FEATS, STUDENT_FEATS)
        print("    异常曲线(12 个位置,█ = 分数超过阈值 0.5):")
        print("      " + "".join("█" if v > 0.5 else "▁" for v in scores))
        print("      " + "".join("^" if start <= i <= end else " " for i in range(12))
              + "  ← 检出区间 (5, 7)")
        print("    位置 5-7 学生只会答 [0,1],和老师的 [1,0] 分道扬镳——")
        print("    师生分歧即缺陷:学生没学过的地方,答案对不上了。")
        print("  ✅ 通过!你已经复现了课程 §6 交互的完整逻辑。")
        return True
    print("  ❌ 结果不对:期望 (5, 7),得到 (%s, %s)。" % (start, end))
    print("     检查:曲线应为 [0]*5 + [1]*3 + [0]*4;")
    print("     用 > thr(严格大于)收集下标,取第一个和最后一个。")
    return False


if __name__ == "__main__":
    print("=" * 52)
    print("第 09 课练习:亲手实现师生差异检测器")
    print("=" * 52)
    all_passed = True
    all_passed = test_sq_diff() and all_passed
    all_passed = test_cosine_sim() and all_passed
    all_passed = test_anomaly_curve() and all_passed
    all_passed = test_moving_avg() and all_passed
    all_passed = test_find_anomaly_span() and all_passed
    print("-" * 52)
    if all_passed:
        print("🎉 全部通过!你已经亲手搭出师生蒸馏的完整检测链路。下一课见。")
    else:
        print("💪 还有测试没通过,按提示继续加油!")
