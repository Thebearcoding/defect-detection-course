# -*- coding: utf-8 -*-
"""
============================================================
第 01 课练习:从零实现一个会学习的神经元
============================================================

你将用纯 Python(零依赖)实现:神经元前向计算、激活函数、
损失函数、数值梯度,最后用梯度下降训练一个神经元,
让它自动学会区分「合格零件」和「缺陷零件」——
也就是课程页 §2 交互演示里你手动做的事,这次交给算法。

运行方式:  python exercise.py
完成所有 TODO 后,你应该看到所有测试通过

难度:⭐⭐
预计用时:30-45 分钟
"""

import math
import random

random.seed(42)  # 固定随机种子,保证结果可复现


# ============================================================
# 🧱 Part 1: 神经元的前向计算(对应课程 §2)
# ============================================================
#
# 神经元做的事:把每个输入乘上对应权重,求和,再加偏置。
#     z = w1*x1 + w2*x2 + ... + wn*xn + b
#

def neuron_forward(inputs, weights, bias):
    """计算神经元的加权和 z。

    Args:
        inputs:  输入列表,如 [0.5, 0.8]
        weights: 权重列表,与 inputs 等长,如 [1.0, -2.0]
        bias:    偏置,一个数

    Returns:
        加权和 z(一个数)
    """
    # ======== TODO 1: 在这里写你的代码 ========
    # 提示:用一个循环(或 zip)把 inputs[i] * weights[i] 累加起来,
    #       最后加上 bias。三行以内可以写完。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 1 ========


# ============================================================
# 🧱 Part 2: 激活函数(对应课程 §3)
# ============================================================
#
# sigmoid 把任意实数压到 (0,1),适合表示概率;
# relu 把负数归零、正数保留,是隐藏层的默认选择。
#

def sigmoid(z):
    """sigmoid(z) = 1 / (1 + e^(-z))"""
    # ======== TODO 2a: 在这里写你的代码 ========
    # 提示:math.exp(-z) 就是 e^(-z),一行可以写完。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 2a ========


def relu(z):
    """relu(z) = max(0, z)"""
    # ======== TODO 2b: 在这里写你的代码 ========
    # 提示:一行。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 2b ========


# ============================================================
# 🧱 Part 3: 损失函数(对应课程 §5)
# ============================================================
#
# 均方误差:预测与真实之差的平方,对所有样本取平均。
#     L = (1/N) * Σ (y_hat_i - y_i)^2
#

def mse_loss(predictions, targets):
    """计算均方误差。

    Args:
        predictions: 预测值列表,如 [0.9, 0.1, 0.4]
        targets:     真实值列表,与 predictions 等长,如 [1, 0, 0]

    Returns:
        均方误差(一个数)
    """
    # ======== TODO 3: 在这里写你的代码 ========
    # 提示:累加 (p - t) ** 2,最后除以样本个数 len(...)。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 3 ========


# ============================================================
# 🧱 Part 4: 数值梯度(对应课程 §6)
# ============================================================
#
# 梯度的定义:参数微调一点点,损失变化多少。
# 数值梯度用「有限差分」直接按定义近似:
#     dL/dw ≈ ( L(w + eps) - L(w - eps) ) / (2 * eps)
#
# 真实框架用反向传播(高效),但数值梯度是按定义计算的,
# 常用来「检验」反向传播实现得对不对(gradient check)。
#

def numerical_gradient(loss_fn, params, eps=1e-5):
    """对每个参数计算数值梯度。

    Args:
        loss_fn: 一个函数,接收参数列表,返回损失值。
                 例如 loss_fn([w1, w2, b]) -> 0.37
        params:  当前参数列表,如 [1.0, -2.0, 0.5]
        eps:     微扰大小

    Returns:
        梯度列表,与 params 等长:[dL/dp1, dL/dp2, ...]
    """
    # ======== TODO 4: 在这里写你的代码 ========
    # 提示:对第 i 个参数:
    #   1. 复制一份 params,把第 i 个值加 eps,算 loss_plus
    #   2. 再复制一份,把第 i 个值减 eps,算 loss_minus
    #   3. 梯度_i = (loss_plus - loss_minus) / (2 * eps)
    # 对每个 i 重复,收集成列表返回。
    # 复制列表可以用 list(params) 或 params[:]。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 4 ========


# ============================================================
# 🧱 Part 5: 训练!(对应课程 §6-§8,串联前面全部)
# ============================================================
#
# 数据:8 个零件样本,特征 = [尺寸偏差, 表面粗糙度],
# 标签 1 = 缺陷件,0 = 合格件(和课程页 §2 的演示相同)。
#
# 模型:单个神经元 + sigmoid:
#     y_hat = sigmoid( w1*x1 + w2*x2 + b )
#
# 训练循环(每一轮):
#     1. 定义损失函数:当前参数下,所有样本的 mse_loss
#     2. 用 numerical_gradient 算出 [dL/dw1, dL/dw2, dL/db]
#     3. 每个参数沿负梯度更新:p = p - lr * grad
#

DATA = [
    # (特征 [尺寸偏差, 粗糙度], 标签)
    ([0.20, 0.25], 0), ([0.30, 0.20], 0),
    ([0.25, 0.38], 0), ([0.38, 0.30], 0),
    ([0.65, 0.70], 1), ([0.75, 0.85], 1),
    ([0.85, 0.60], 1), ([0.70, 0.90], 1),
]


def predict(params, features):
    """用当前参数对一个样本给出预测概率。params = [w1, w2, b]"""
    w1, w2, b = params
    return sigmoid(neuron_forward(features, [w1, w2], b))


def train(epochs=300, lr=1.0):
    """用梯度下降训练神经元,返回训练好的参数 [w1, w2, b]。"""

    params = [0.0, 0.0, 0.0]  # 从全零开始

    def data_loss(p):
        """当前参数下,整份数据的平均损失。"""
        preds = [predict(p, feats) for feats, _ in DATA]
        labels = [label for _, label in DATA]
        return mse_loss(preds, labels)

    for epoch in range(epochs):
        # ======== TODO 5: 在这里写你的代码 ========
        # 提示(两行核心逻辑):
        #   1. grads = numerical_gradient(data_loss, params)
        #   2. params = [p - lr * g for p, g in zip(params, grads)]

        pass  # ← 删掉这行,写你的实现

        # ======== END TODO 5 ========

        if epoch % 60 == 0:
            cur = data_loss(params)
            if cur is None:
                print("    (前面的 TODO 还没完成,损失暂时算不出来)")
                break
            print("    epoch %3d | loss = %.4f" % (epoch, cur))

    return params


# ============================================================
# 🧪 测试
# ============================================================

def _close(a, b, tol=1e-4):
    return abs(a - b) < tol


def test_neuron_forward():
    print("测试 1: neuron_forward ...")
    z = neuron_forward([1.0, 2.0], [0.5, -1.0], 0.3)
    if z is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 1 后再运行。")
        return False
    if _close(z, 0.5 * 1.0 + (-1.0) * 2.0 + 0.3):  # = -1.2
        print("  ✅ 通过!加权和计算正确。")
        return True
    print("  ❌ 结果不对:期望 -1.2,得到 %r。检查乘加顺序和偏置。" % z)
    return False


def test_activations():
    print("测试 2: sigmoid / relu ...")
    s0, s1 = sigmoid(0.0), sigmoid(1.0)
    if s0 is None or relu(1.5) is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 2a/2b 后再运行。")
        return False
    ok = (_close(s0, 0.5) and _close(s1, 0.731058, 1e-4)
          and relu(-3.0) == 0 and relu(1.5) == 1.5)
    if ok:
        print("  ✅ 通过!σ(0)=0.5、σ(1)≈0.731、ReLU 行为正确。")
        return True
    print("  ❌ 有错误:σ(0)=%r(期望 0.5),σ(1)=%r(期望≈0.731),"
          "relu(-3)=%r(期望 0),relu(1.5)=%r(期望 1.5)"
          % (s0, s1, relu(-3.0), relu(1.5)))
    return False


def test_mse():
    print("测试 3: mse_loss ...")
    l = mse_loss([1.0, 0.0], [0.0, 0.0])
    if l is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 3 后再运行。")
        return False
    if _close(l, 0.5) and _close(mse_loss([0.5], [1.0]), 0.25):
        print("  ✅ 通过!均方误差计算正确。")
        return True
    print("  ❌ 结果不对:mse([1,0],[0,0]) 期望 0.5,得到 %r。别忘了除以样本数。" % l)
    return False


def test_numerical_gradient():
    print("测试 4: numerical_gradient ...")
    # 用一个已知导数的函数检验:L(p) = p0^2 + 3*p1,梯度应为 [2*p0, 3]
    grads = numerical_gradient(lambda p: p[0] ** 2 + 3 * p[1], [2.0, 5.0])
    if grads is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 4 后再运行。")
        return False
    if _close(grads[0], 4.0, 1e-3) and _close(grads[1], 3.0, 1e-3):
        print("  ✅ 通过!数值梯度与解析导数 [4, 3] 一致。")
        return True
    print("  ❌ 结果不对:期望约 [4.0, 3.0],得到 %r。检查 ± eps 与除以 2*eps。" % grads)
    return False


def test_train():
    print("测试 5: 训练一个会分零件的神经元 ...")
    if sigmoid(0.0) is None or neuron_forward([1.0], [1.0], 0.0) is None \
            or mse_loss([0.5], [1.0]) is None:
        print("  ❌ 先完成 TODO 1-4,再来挑战训练。")
        return False
    params = train()
    if params == [0.0, 0.0, 0.0]:
        print("  ❌ 参数没有被更新(仍是全零)。完成 TODO 5 后再运行。")
        return False
    correct = 0
    for feats, label in DATA:
        pred = 1 if predict(params, feats) > 0.5 else 0
        if pred == label:
            correct += 1
    print("    训练后参数: w1=%.2f  w2=%.2f  b=%.2f" % tuple(params))
    print("    分类正确: %d / 8" % correct)
    if correct == 8:
        print("  ✅ 通过!神经元自动学会了你在课程页里手动调出的分界线。")
        return True
    print("  ❌ 未全部分对。检查 TODO 5 的更新方向(是减去 lr*grad,不是加上)。")
    return False


if __name__ == "__main__":
    print("=" * 52)
    print("第 01 课练习:从零实现一个会学习的神经元")
    print("=" * 52)
    all_passed = True
    all_passed = test_neuron_forward() and all_passed
    all_passed = test_activations() and all_passed
    all_passed = test_mse() and all_passed
    all_passed = test_numerical_gradient() and all_passed
    all_passed = test_train() and all_passed
    print("-" * 52)
    if all_passed:
        print("🎉 全部通过!你已经亲手实现了'学习'本身。下一课见。")
    else:
        print("💪 还有测试没通过,按提示继续加油!")
