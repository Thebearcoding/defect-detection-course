# -*- coding: utf-8 -*-
"""
============================================================
第 11 课练习:亲手搭一个一维归一化流
============================================================

你将用纯 Python(只 import math)把本课的变量替换公式逐一落地:
标准高斯的 logpdf(落点项)→ 一层仿射流和它的"体积账本"
→ 完整的 log p(x) → 用正常数据拟合流参数(最大似然)
→ 串成一个最小可用的密度异常检测器。

运行方式:  python exercise.py
完成所有 TODO 后,你应该看到所有测试通过

难度:⭐⭐⭐
预计用时:30-45 分钟
"""

import math


# ============================================================
# 🧱 Part 1: 标准高斯的 log 密度(对应课程 §2 第一项)
# ============================================================
#
# 变量替换公式 log p(x) = log N(f(x)) + log|det J| 里,
# 第一项要"查标准高斯表"。标准高斯的密度有解析式:
#
#     N(z) = exp(-z²/2) / √(2π)
#     log N(z) = -0.5 · (z² + log 2π)
#
# z 离 0 越近,这一项越大——"落点好不好"由它说了算。
#

def gaussian_logpdf(z):
    """标准高斯 N(0,1) 在 z 处的对数密度。

    Args:
        z: 实数

    Returns:
        log N(z) = -0.5 * (z*z + log(2π))
    """
    # ======== TODO 1: 在这里写你的代码 ========
    # 提示:一行。math.log(2 * math.pi) 就是 log 2π。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 1 ========


# ============================================================
# 🧱 Part 2: 一层仿射流 + 它的账本(对应课程 §2 第二项)
# ============================================================
#
# 最简单的可逆变换:仿射流  z = f(x) = (x - b) / a
#   · 可逆:x = a·z + b,一一对应 ✓
#   · 账本:f'(x) = 1/a,所以 log|det J| = log|1/a| = -log|a| ✓
#
# a 就是"橡皮筋的拉伸倍数":a 越大,f 把 x 空间压得越扁,
# 账本上记的负账越多——概率密度要按比例打折。
#

def affine_forward(x, a, b):
    """做一次仿射变换,同时记下体积账本。

    Args:
        x: 输入(实数)
        a: 缩放参数(非零)
        b: 平移参数

    Returns:
        (z, logdet) 二元组:
        z      = (x - b) / a
        logdet = -log|a|
    """
    # ======== TODO 2: 在这里写你的代码 ========
    # 提示:两行算 z 和 logdet(用 math.log 和 abs),
    #       然后 return z, logdet

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 2 ========


# ============================================================
# 🧱 Part 3: 完整的 log p(x)(变量替换公式落地)
# ============================================================
#
#     log p(x) = log N( (x-b)/a ) - log|a|
#                ────────┬───────   ───┬──
#                   落点项(查表)    账本项
#
# 两项相加,才是 x 在"正常世界"里的真实对数密度。
#

def flow_logprob(x, a, b):
    """用一层仿射流计算 log p(x)。

    Args:
        x: 输入(实数)
        a: 缩放参数(非零)
        b: 平移参数

    Returns:
        log p(x) = gaussian_logpdf((x-b)/a) - log|a|
    """
    # ======== TODO 3: 在这里写你的代码 ========
    # 提示:调用前两个函数:z, logdet = affine_forward(x, a, b),
    #       然后 return gaussian_logpdf(z) + logdet

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 3 ========


# ============================================================
# 🧱 Part 4: 用正常数据"训练"这层流(对应课程 §4 的训练)
# ============================================================
#
# 训练流 = 最大化正常样本的平均 log p(最大似然)。
# 深层流要用梯度下降,但一维仿射流的最大似然有解析解:
#
#     b = 样本均值
#     a = 样本的总体标准差(平方和除以 N,不是 N-1)
#
# 也就是说:把数据的中心平移到 0、宽度缩放到 1,
# 剩下的形状交给标准高斯——这就是"归一化"三个字的由来。
#

def fit_affine(data):
    """从正常数据拟合仿射流参数。

    Args:
        data: 一维数值列表(至少 2 个、且不全相等)

    Returns:
        (a, b) 二元组:b = 均值,a = 总体标准差(除以 N)
    """
    # ======== TODO 4: 在这里写你的代码 ========
    # 提示:b = sum(data) / len(data)
    #       a = math.sqrt( sum((x - b)**2 for x in data) / len(data) )
    #       注意除以 len(data)(总体标准差),返回 (a, b)

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 4 ========


# ============================================================
# 🧱 Part 5: 串联!一个最小的密度异常检测器(对应课程全篇)
# ============================================================
#
# NORMAL 是 8 个"正常样本"(想象成某个 patch 特征的取值,
# 均值约 4.875)。流程和真实的 FastFlow 一模一样,只差规模:
#
#   ① fit_affine(data):用正常样本训练流
#   ② flow_logprob(x, a, b):算新样本的 log p
#   ③ log p < 阈值 → 低概率 → 异常!
#

NORMAL = [4.2, 4.8, 5.0, 5.1, 5.3, 4.9, 5.2, 4.5]


def is_anomaly(x, data, thr=-4.0):
    """密度异常检测器:log p(x) 低于阈值即判为异常。

    Args:
        x:    待检测的新样本
        data: 正常样本列表
        thr:  log p 阈值(默认 -4.0)

    Returns:
        True(异常)/ False(正常)
    """
    # ======== TODO 5: 在这里写你的代码 ========
    # 提示(两行):
    #   1. a, b = fit_affine(data)
    #   2. return flow_logprob(x, a, b) < thr

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 5 ========


# ============================================================
# 🧪 测试
# ============================================================

def test_gaussian_logpdf():
    print("测试 1: gaussian_logpdf ...")
    out0 = gaussian_logpdf(0.0)
    if out0 is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 1 后再运行。")
        return False
    out2 = gaussian_logpdf(2.0)
    ok0 = abs(out0 - (-0.9189385332)) < 1e-6
    ok2 = abs(out2 - (-2.9189385332)) < 1e-6
    if ok0 and ok2:
        print("  ✅ 通过!logN(0)≈-0.9189(峰顶),logN(2)≈-2.9189(两个标准差外)。")
        return True
    print("  ❌ 结果不对:期望 logN(0)≈-0.9189385、logN(2)≈-2.9189385,"
          "得到 %r / %r。" % (out0, out2))
    print("     检查:公式是 -0.5 * (z*z + math.log(2*math.pi))。")
    return False


def test_affine_forward():
    print("测试 2: affine_forward ...")
    out = affine_forward(5, 2, 1)
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 2 后再运行。")
        return False
    if not (isinstance(out, (tuple, list)) and len(out) == 2):
        print("  ❌ 应返回 (z, logdet) 二元组,得到 %r。" % (out,))
        return False
    z, logdet = out
    if abs(z - 2.0) < 1e-6 and abs(logdet - (-0.6931471806)) < 1e-6:
        print("  ✅ 通过!(5-1)/2 = 2.0,账本 -log|2| ≈ -0.6931。")
        return True
    print("  ❌ 结果不对:期望 z=2.0、logdet≈-0.6931472,得到 z=%r、logdet=%r。" % (z, logdet))
    print("     检查:z = (x - b) / a,logdet = -math.log(abs(a))。")
    return False


def test_flow_logprob():
    print("测试 3: flow_logprob ...")
    prereq = gaussian_logpdf(0.0) is not None and affine_forward(5, 2, 1) is not None
    if not prereq:
        print("  ❌ 先完成 TODO 1 和 TODO 2(flow_logprob 要用到它们)。")
        return False
    out = flow_logprob(1, 2, 1)
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 3 后再运行。")
        return False
    if abs(out - (-1.6120857)) < 1e-4:
        print("  ✅ 通过!落点项 -0.9189 + 账本项 -0.6931 = -1.6121。")
        return True
    print("  ❌ 结果不对:期望 ≈ -1.6121,得到 %r。" % out)
    print("     检查:x=1 平移后是 0(落在峰顶),但 a=2 的压缩要在账本上"
          "扣 log 2 ≈ 0.6931——两项都不能少。")
    return False


def test_fit_affine():
    print("测试 4: fit_affine ...")
    out = fit_affine([4, 5, 6])
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 4 后再运行。")
        return False
    if not (isinstance(out, (tuple, list)) and len(out) == 2):
        print("  ❌ 应返回 (a, b) 二元组,得到 %r。" % (out,))
        return False
    a, b = out
    if abs(b - 5.0) < 1e-4 and abs(a - 0.8164966) < 1e-4:
        print("  ✅ 通过!b=5.0(均值),a=√(2/3)≈0.8165(总体标准差)。")
        return True
    print("  ❌ 结果不对:期望 a≈0.8165、b=5.0,得到 a=%r、b=%r。" % (a, b))
    print("     检查:是不是除以了 N-1?最大似然解要除以 N(len(data))。")
    return False


def test_is_anomaly():
    print("测试 5: 密度异常检测器 ...")
    prereq = (gaussian_logpdf(0.0) is not None
              and affine_forward(5, 2, 1) is not None
              and flow_logprob(1, 2, 1) is not None
              and fit_affine([4, 5, 6]) is not None)
    if not prereq:
        print("  ❌ 先完成 TODO 1-4,再来串联检测器。")
        return False
    result = is_anomaly(9.0, NORMAL)
    if result is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 5 后再运行。")
        return False
    r_hi = is_anomaly(9.0, NORMAL)
    r_lo = is_anomaly(5.0, NORMAL)
    a, b = fit_affine(NORMAL)
    lp_hi = flow_logprob(9.0, a, b)
    lp_lo = flow_logprob(5.0, a, b)
    print("    拟合参数: b(均值)=%.4f,a(标准差)=%.4f" % (b, a))
    print("    log p(5.0) = %+.4f  →  判定: %s" % (lp_lo, "异常" if r_lo else "正常"))
    print("    log p(9.0) = %+.4f  →  判定: %s" % (lp_hi, "异常" if r_hi else "正常"))
    if r_hi is True and r_lo is False:
        print("    (log p 可以是正数——它是密度不是概率,分布很窄时密度能超过 1)")
        print("    两者相差约 e^71 ≈ 10^31 倍:概率密度给了异常检测一把有单位的尺子。")
        print("  ✅ 通过!训练流 → 算 log p → 低概率报警,FastFlow 的骨架就是它。")
        return True
    print("  ❌ 结果不对:期望 is_anomaly(9.0)=True、is_anomaly(5.0)=False,"
          "得到 %r / %r。" % (r_hi, r_lo))
    print("     检查:比较方向是 log p < thr(密度越低越异常),阈值默认 -4.0。")
    return False


if __name__ == "__main__":
    print("=" * 52)
    print("第 11 课练习:亲手搭一个一维归一化流")
    print("=" * 52)
    all_passed = True
    all_passed = test_gaussian_logpdf() and all_passed
    all_passed = test_affine_forward() and all_passed
    all_passed = test_flow_logprob() and all_passed
    all_passed = test_fit_affine() and all_passed
    all_passed = test_is_anomaly() and all_passed
    print("-" * 52)
    if all_passed:
        print("🎉 全部通过!你已经亲手搭出并\"训练\"了一个一维归一化流。下一课见。")
    else:
        print("💪 还有测试没通过,按提示继续加油!")
