# -*- coding: utf-8 -*-
"""
============================================================
第 12 课练习:亲手实现 zero-shot 缺陷判定
============================================================

CLIP 的推理端出奇地简单:点积、余弦相似度、softmax,
三个函数就能复现"一句话当分类器"的全部机制。
你将从点积写起,一路串成 WinCLIP 式的异常打分器——
全程没有任何训练,分类器是"写"出来的。

规则:只允许 import math,不用任何第三方库。

运行方式:  python exercise.py
完成所有 TODO 后,你应该看到所有测试通过

难度:⭐⭐
预计用时:20-35 分钟
"""

import math


# ============================================================
# 🧱 Part 1: 点积(对应课程 §1)
# ============================================================
#
# CLIP 里图像向量和文本向量比相似度,原材料就是点积:
# 对应位置相乘,再全部加起来。
#

def dot(a, b):
    """计算两个等长向量的点积。

    Args:
        a, b: 等长的数字列表,如 [1, 2] 和 [3, 4]

    Returns:
        标量:a[0]*b[0] + a[1]*b[1] + ...
    """
    # ======== TODO 1: 在这里写你的代码 ========
    # 提示:一行即可:sum(x * y for x, y in zip(a, b))

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 1 ========


# ============================================================
# 🧱 Part 2: 余弦相似度(对应课程 §1)
# ============================================================
#
# CLIP 空间里的"距离尺":cos(a, b) = 点积 / (|a| × |b|)。
# 只看方向、不看长度,取值范围 [-1, 1]。
# 模长 |a| = sqrt(a·a),用 math.sqrt。
#

def cosine_sim(a, b):
    """计算两个向量的余弦相似度。

    Args:
        a, b: 等长的数字列表

    Returns:
        标量:dot(a,b) / (|a| * |b|)。
        任一向量是零向量(模长为 0)时,返回 0.0。
    """
    # ======== TODO 2: 在这里写你的代码 ========
    # 提示:模长 = math.sqrt(dot(a, a))。
    #       先算两个模长,任一为 0 就 return 0.0,
    #       否则 return dot(a, b) / (模长a * 模长b)。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 2 ========


# ============================================================
# 🧱 Part 3: 带温度的 softmax(对应课程 §2)
# ============================================================
#
# 把一串相似度变成一串概率(全为正、和为 1):
#
#     softmax(x_i) = exp(x_i / T) / Σ_j exp(x_j / T)
#
# T 是温度:T 越低,大的更大、小的更小,分布越"尖"。
# CLIP 用约 T=0.01 把细微的余弦差距放大成悬殊的概率。
#
# 数值稳定技巧:除完温度后,先给每个数减去最大值再 exp
# (不改变结果,但避免 exp 溢出)。
#

def softmax(xs, temperature=1.0):
    """带温度的 softmax。

    Args:
        xs:          数字列表
        temperature: 温度 T(正数),默认 1.0

    Returns:
        和 xs 等长的概率列表(全为正,和为 1)
    """
    # ======== TODO 3: 在这里写你的代码 ========
    # 提示(三步):
    #   1. zs = [x / temperature for x in xs]      # 先除温度
    #   2. m = max(zs); es = [math.exp(z - m) for z in zs]   # 减最大值再 exp
    #   3. s = sum(es); return [e / s for e in es]           # 归一化

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 3 ========


# ============================================================
# 🧱 Part 4: zero-shot 分类(对应课程 §2)
# ============================================================
#
# 串起前三步,复现课程 §2 图文匹配模拟器做的事:
#   ① 图像向量和每条文本向量算余弦相似度
#   ② softmax 变成概率
#   ③ 概率最大的那条文本,就是分类结果
#
# 没有训练,没有梯度——分类器就是那几条文本向量。
#

def clip_zero_shot(img_feat, text_feats, temperature=1.0):
    """用文本向量当分类器,对图像向量做 zero-shot 分类。

    Args:
        img_feat:    图像特征向量,如 [0.9, 0.1]
        text_feats:  文本特征向量列表,如 [[1, 0], [0, 1]]
        temperature: softmax 温度

    Returns:
        (best_idx, probs):
        best_idx 是概率最大的文本下标,probs 是概率列表。
    """
    # ======== TODO 4: 在这里写你的代码 ========
    # 提示(三步):
    #   1. sims = [cosine_sim(img_feat, t) for t in text_feats]
    #   2. probs = softmax(sims, temperature)
    #   3. best_idx = probs.index(max(probs));  return (best_idx, probs)

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 4 ========


# ============================================================
# 🧱 Part 5: 串联!两句话的最小 WinCLIP(对应课程 §3)
# ============================================================
#
# WinCLIP 的异常分:normal / anomaly 两组 prompt 对垒,
# softmax 后取 anomaly 侧的概率。
# 这里做两句话的玩具版(向量退化为 2 维):
#
#   TEXT_NORMAL  = "a photo of a flawless metal disc" 的"文本向量"
#   TEXT_DAMAGED = "a photo of a damaged metal disc"  的"文本向量"
#
# 温度取 0.1:把不大的余弦差距放大成接近 0/1 的判断。
#

TEXT_NORMAL = [1, 0]    # "完好"句的文本向量(玩具版:2 维)
TEXT_DAMAGED = [0, 1]   # "损伤"句的文本向量


def anomaly_probability(img_feat, t=0.1):
    """算图像的异常概率:两句 prompt 对垒,取 damaged 侧的 softmax 概率。

    Args:
        img_feat: 图像特征向量(2 维)
        t:        softmax 温度,默认 0.1

    Returns:
        标量 ∈ (0, 1):越接近 1 越像 damaged。
    """
    # ======== TODO 5: 在这里写你的代码 ========
    # 提示:直接复用 TODO 4:
    #   _, probs = clip_zero_shot(img_feat, [TEXT_NORMAL, TEXT_DAMAGED], t)
    #   return probs[1]        # 下标 1 = TEXT_DAMAGED 那一侧

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 5 ========


# ============================================================
# 🧪 测试
# ============================================================

def test_dot():
    print("测试 1: dot ...")
    out = dot([1, 2], [3, 4])
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 1 后再运行。")
        return False
    if out == 11:
        print("  ✅ 通过!dot([1,2],[3,4]) = 1×3 + 2×4 = 11。")
        return True
    print("  ❌ 结果不对:期望 11,得到 %r。检查是否对位相乘后求和。" % out)
    return False


def test_cosine_sim():
    print("测试 2: cosine_sim ...")
    if dot([1, 2], [3, 4]) is None:
        print("  ❌ 先完成 TODO 1(cosine_sim 要用到 dot)。")
        return False
    out = cosine_sim([1, 0], [0, 1])
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 2 后再运行。")
        return False
    ok1 = abs(out - 0.0) < 1e-9
    ok2 = abs(cosine_sim([2, 0], [1, 0]) - 1.0) < 1e-9
    ok3 = cosine_sim([0, 0], [1, 2]) == 0.0
    if ok1 and ok2 and ok3:
        print("  ✅ 通过!垂直→0、同向→1、零向量→0.0,余弦只看方向不看长度。")
        return True
    print("  ❌ 结果不对:([1,0],[0,1]) 应为 0.0,([2,0],[1,0]) 应为 1.0,")
    print("     零向量应返回 0.0。得到 %r / %r / %r。" % (out, cosine_sim([2, 0], [1, 0]), cosine_sim([0, 0], [1, 2])))
    return False


def test_softmax():
    print("测试 3: softmax ...")
    out = softmax([2, 1, 0])
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 3 后再运行。")
        return False
    expect = [0.66524, 0.24473, 0.09003]
    ok1 = (len(out) == 3 and all(abs(o - e) < 1e-4 for o, e in zip(out, expect)))
    out2 = softmax([2, 1, 0], 0.5)
    ok2 = (out2 is not None and abs(out2[0] - 0.8668) < 1e-3)
    if ok1 and ok2:
        print("  ✅ 通过!softmax([2,1,0]) ≈ [0.665, 0.245, 0.090]。")
        print("  📌 教学点:温度 1.0 → 首项 0.665;温度 0.5 → 首项 %.4f。" % out2[0])
        print("     温度越低,分布越尖——CLIP 就是用小温度把细微差距放大成悬殊概率的。")
        return True
    print("  ❌ 结果不对:期望 ≈ [0.66524, 0.24473, 0.09003],得到 %r;" % out)
    print("     温度 0.5 时首项应 ≈ 0.8668,得到 %r。检查:先除温度,再减 max,再 exp、归一。" % (out2[0] if out2 else out2))
    return False


def test_clip_zero_shot():
    print("测试 4: clip_zero_shot ...")
    prereq = (cosine_sim([1, 0], [1, 0]) is not None
              and softmax([1.0, 2.0]) is not None)
    if not prereq:
        print("  ❌ 先完成 TODO 2 和 TODO 3,再来串 zero-shot 分类。")
        return False
    result = clip_zero_shot([0.9, 0.1], [[1, 0], [0, 1]])
    if result is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 4 后再运行。")
        return False
    best_idx, probs = result
    if best_idx == 0 and len(probs) == 2 and abs(sum(probs) - 1.0) < 1e-9 and abs(probs[0] - 0.70754) < 1e-3:
        print("    图像 [0.9, 0.1] 更靠近文本 0([1,0]),概率 %.4f > %.4f" % (probs[0], probs[1]))
        print("  ✅ 通过!余弦 → softmax → argmax,一次完整的 zero-shot 分类。")
        return True
    print("  ❌ 结果不对:期望 (0, [≈0.7075, ≈0.2925]),得到 (%r, %r)。" % (best_idx, probs))
    print("     检查:是否对每条文本算 cosine_sim,再整体做 softmax?")
    return False


def test_anomaly_probability():
    print("测试 5: 零样本缺陷判定 ...")
    if clip_zero_shot([1, 0], [[1, 0], [0, 1]]) is None:
        print("  ❌ 先完成 TODO 4(anomaly_probability 要复用它)。")
        return False
    IMG_NORMAL = [0.95, 0.05]   # 完好盘的"图像向量":几乎指向 normal 方向
    IMG_SCRATCH = [0.3, 0.7]    # 划痕盘的"图像向量":明显偏向 damaged 方向
    p_normal = anomaly_probability(IMG_NORMAL)
    if p_normal is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 5 后再运行。")
        return False
    p_scratch = anomaly_probability(IMG_SCRATCH)
    print("    完好盘  IMG_NORMAL  = [0.95, 0.05] → 异常概率 %.4f" % p_normal)
    print("    划痕盘  IMG_SCRATCH = [0.3, 0.7]  → 异常概率 %.4f" % p_scratch)
    if p_normal < 0.5 and p_scratch > 0.5:
        print("  ✅ 通过!完好盘 < 0.5、划痕盘 > 0.5,零样本判定成功。")
        print("  📌 分类器是写出来的,不是训出来的:全程没有训练一步,")
        print("     判定标准只是 TEXT_NORMAL / TEXT_DAMAGED 两句话——换一种缺陷,换一句话即可。")
        return True
    print("  ❌ 结果不对:完好盘应 < 0.5,划痕盘应 > 0.5。")
    print("     检查:softmax 温度是否用了 t(默认 0.1)?返回的是不是 damaged 那一侧(下标 1)?")
    return False


if __name__ == "__main__":
    print("=" * 52)
    print("第 12 课练习:亲手实现 zero-shot 缺陷判定")
    print("=" * 52)
    all_passed = True
    all_passed = test_dot() and all_passed
    all_passed = test_cosine_sim() and all_passed
    all_passed = test_softmax() and all_passed
    all_passed = test_clip_zero_shot() and all_passed
    all_passed = test_anomaly_probability() and all_passed
    print("-" * 52)
    if all_passed:
        print("🎉 全部通过!你已经亲手复现了 zero-shot 缺陷判定的完整链路。")
        print("   下一课:工程实践与方法选型——把 12 课的方法拼成一棵决策树。")
    else:
        print("💪 还有测试没通过,按提示继续加油!")
