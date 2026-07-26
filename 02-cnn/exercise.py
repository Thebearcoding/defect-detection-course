# -*- coding: utf-8 -*-
"""
============================================================
第 02 课练习:从零实现卷积,并抓到一道划痕
============================================================

你将用纯 Python(零依赖)实现 CNN 的三大件:
卷积、填充、池化,以及输出尺寸公式。
最后把它们串成一条 conv → ReLU → pool 流水线,
在一张 8×8 的"工件图"里自动定位划痕的位置。

运行方式:  python exercise.py
完成所有 TODO 后,你应该看到所有测试通过

难度:⭐⭐⭐
预计用时:30-45 分钟
"""


# ============================================================
# 🧱 Part 1: 二维卷积(对应课程 §2)
# ============================================================
#
# 卷积三步:盖上窗口 → 对位相乘 → 求和,然后滑动。
# 输入和核都是"列表的列表"(行优先),输出尺寸 = 输入 - 核 + 1。
#
# 说明:深度学习里的"卷积"实际是互相关(不翻转核),
# 我们和 PyTorch 保持一致,也不翻转。
#

def conv2d(image, kernel):
    """对 image 做 valid 卷积(无填充,步长 1)。

    Args:
        image:  H×W 的二维列表,如 [[1,2,3],[4,5,6],[7,8,9]]
        kernel: k×k 的二维列表,如 [[1,0],[0,-1]]

    Returns:
        (H-k+1)×(W-k+1) 的二维列表
    """
    # ======== TODO 1: 在这里写你的代码 ========
    # 提示:四层循环。外两层遍历输出位置 (r, c),
    #       内两层遍历核 (i, j),累加 image[r+i][c+j] * kernel[i][j]。
    #       每个 (r, c) 累加完 append 到当前行。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 1 ========


# ============================================================
# 🧱 Part 2: 零填充(对应课程 §3)
# ============================================================
#
# 在图像四周补 p 圈 0,让卷积核能"骑"在边缘上。
# H×W 的输入 → (H+2p)×(W+2p) 的输出。
#

def zero_pad(image, p):
    """在 image 四周填充 p 圈 0。

    Args:
        image: H×W 的二维列表
        p:     填充圈数(非负整数)

    Returns:
        (H+2p)×(W+2p) 的二维列表
    """
    # ======== TODO 2: 在这里写你的代码 ========
    # 提示:新宽度 = 原宽度 + 2p。
    #       先加 p 行全 0,中间每行是 [0]*p + 原行 + [0]*p,最后再加 p 行全 0。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 2 ========


# ============================================================
# 🧱 Part 3: 输出尺寸公式(对应课程 §3)
# ============================================================
#
#     输出尺寸 = ⌊(N − K + 2P) / S⌋ + 1
#
# 这是读任何网络结构图时都要心算的公式。
#

def conv_output_size(n, k, p, s):
    """按公式计算卷积输出的边长(向下取整用整除 //)。"""
    # ======== TODO 3: 在这里写你的代码 ========
    # 提示:一行,注意用 // 做整除。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 3 ========


# ============================================================
# 🧱 Part 4: 2×2 最大池化(对应课程 §5)
# ============================================================
#
# 把特征图切成 2×2 的块,每块取最大值,尺寸减半。
# 假设输入的高宽都是偶数。
#

def max_pool2x2(fmap):
    """对 fmap 做 2×2、步长 2 的最大池化。

    Args:
        fmap: H×W 的二维列表(H、W 为偶数)

    Returns:
        (H/2)×(W/2) 的二维列表
    """
    # ======== TODO 4: 在这里写你的代码 ========
    # 提示:输出位置 (r, c) 对应输入的 4 个数:
    #       fmap[2r][2c], fmap[2r][2c+1], fmap[2r+1][2c], fmap[2r+1][2c+1]
    #       用 max(...) 取最大。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 4 ========


# ============================================================
# 🧱 Part 5: 串联!一个最小的"划痕定位器"(对应课程 §2-§6)
# ============================================================
#
# 8×8 的工件图:背景亮度 1,第 5 列有一道竖直亮划痕(亮度 9)。
#
# 流水线(真实 CNN 每一层都在做同样的事):
#   ① conv2d:用"左暗右亮"竖直边缘核扫全图
#   ② ReLU:负值归零(只保留"左暗右亮"方向的边缘)
#   ③ max_pool2x2:6×6 → 3×3,压缩成 9 个区域的响应图
#   ④ 找响应最大的区域 → 划痕就在那里
#

SCRATCH_IMAGE = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 9, 1, 1],
    [1, 1, 1, 1, 1, 9, 1, 1],
    [1, 1, 1, 1, 1, 9, 1, 1],
    [1, 1, 1, 1, 1, 9, 1, 1],
    [1, 1, 1, 1, 1, 9, 1, 1],
    [1, 1, 1, 1, 1, 9, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]

VERTICAL_EDGE_K = [
    [-1, 0, 1],
    [-1, 0, 1],
    [-1, 0, 1],
]


def detect_scratch(image):
    """用 conv → ReLU → pool 定位划痕。

    Returns:
        (row, col, value):池化图中响应最大的格子及其值。
        多个并列最大时,返回按行扫描遇到的第一个。
    """
    # ======== TODO 5: 在这里写你的代码 ========
    # 提示(四步,每步一两行):
    #   1. fmap = conv2d(image, VERTICAL_EDGE_K)
    #   2. ReLU:fmap = [[max(0, v) for v in row] for row in fmap]
    #   3. pooled = max_pool2x2(fmap)
    #   4. 找最大:遍历 pooled 的 (r, c),记录最大值及其位置,返回 (r, c, val)

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 5 ========


# ============================================================
# 🧪 测试
# ============================================================

def test_conv2d():
    print("测试 1: conv2d ...")
    out = conv2d([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[1, 0], [0, -1]])
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 1 后再运行。")
        return False
    if out == [[-4, -4], [-4, -4]]:
        ones = conv2d([[1] * 4 for _ in range(4)], [[1] * 3 for _ in range(3)])
        if ones == [[9, 9], [9, 9]]:
            print("  ✅ 通过!滑动窗口与对位相乘求和都正确。")
            return True
        print("  ❌ 3×3 核的情况不对:全 1 图卷全 1 核应得 [[9,9],[9,9]],得到 %r" % ones)
        return False
    print("  ❌ 结果不对:期望 [[-4,-4],[-4,-4]],得到 %r。" % out)
    print("     检查:输出尺寸应为 2×2,out[0][0] = 1×1 + 2×0 + 4×0 + 5×(-1) = -4")
    return False


def test_zero_pad():
    print("测试 2: zero_pad ...")
    out = zero_pad([[5]], 1)
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 2 后再运行。")
        return False
    ok1 = out == [[0, 0, 0], [0, 5, 0], [0, 0, 0]]
    out2 = zero_pad([[1, 2, 3], [4, 5, 6]], 1)
    ok2 = (len(out2) == 4 and len(out2[0]) == 5
           and out2[1][1:4] == [1, 2, 3] and out2[0] == [0] * 5)
    if ok1 and ok2:
        print("  ✅ 通过!四周都正确补上了 0。")
        return True
    print("  ❌ 结果不对:zero_pad([[5]],1) 期望 3×3 且中心为 5,得到 %r" % out)
    return False


def test_output_size():
    print("测试 3: conv_output_size ...")
    s1 = conv_output_size(32, 3, 1, 1)
    if s1 is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 3 后再运行。")
        return False
    s2 = conv_output_size(32, 3, 0, 2)
    s3 = conv_output_size(5, 3, 0, 1)
    if s1 == 32 and s2 == 15 and s3 == 3:
        print("  ✅ 通过!(32,3,1,1)→32、(32,3,0,2)→15、(5,3,0,1)→3。")
        return True
    print("  ❌ 结果不对:期望 32 / 15 / 3,得到 %r / %r / %r。检查整除与 +1。" % (s1, s2, s3))
    return False


def test_max_pool():
    print("测试 4: max_pool2x2 ...")
    out = max_pool2x2([[1, 3, 2, 0], [5, 6, 7, 1], [9, 2, 4, 8], [0, 1, 3, 5]])
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 4 后再运行。")
        return False
    if out == [[6, 7], [9, 8]]:
        print("  ✅ 通过!和课程 §5 的例子一致:[[6,7],[9,8]]。")
        return True
    print("  ❌ 结果不对:期望 [[6,7],[9,8]],得到 %r。检查 2r/2c 的下标。" % out)
    return False


def test_detect_scratch():
    print("测试 5: 划痕定位器 ...")
    prereq = (conv2d([[1, 1], [1, 1]], [[1]]) is not None
              and max_pool2x2([[1, 2], [3, 4]]) is not None)
    if not prereq:
        print("  ❌ 先完成 TODO 1 和 TODO 4,再来挑战流水线。")
        return False
    result = detect_scratch(SCRATCH_IMAGE)
    if result is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 5 后再运行。")
        return False
    r, c, val = result
    print("    定位结果: 池化图格子 (%d, %d),响应值 %s" % (r, c, val))
    if val == 24 and c == 1:
        print("    划痕在图像第 5 列(右半),对应池化图第 1 列 —— 定位正确!")
        print("  ✅ 通过!conv → ReLU → pool 把划痕位置从像素里挤出来了。")
        return True
    print("  ❌ 结果不对:期望响应值 24、列号 1,得到值 %s、列 %s。" % (val, c))
    print("     检查:ReLU 有没有做?找最大是否扫的是池化后的 3×3 图?")
    return False


if __name__ == "__main__":
    print("=" * 52)
    print("第 02 课练习:从零实现卷积,并抓到一道划痕")
    print("=" * 52)
    all_passed = True
    all_passed = test_conv2d() and all_passed
    all_passed = test_zero_pad() and all_passed
    all_passed = test_output_size() and all_passed
    all_passed = test_max_pool() and all_passed
    all_passed = test_detect_scratch() and all_passed
    print("-" * 52)
    if all_passed:
        print("🎉 全部通过!你已经亲手实现了 CNN 的全部核心算子。下一课见。")
    else:
        print("💪 还有测试没通过,按提示继续加油!")
