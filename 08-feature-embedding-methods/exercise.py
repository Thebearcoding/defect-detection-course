# -*- coding: utf-8 -*-
"""
============================================================
第 08 课练习:亲手实现 PatchCore 的三大件
============================================================

你将用纯 Python(零依赖)实现特征嵌入类方法的核心零件:
距离度量(欧氏 / 马氏)、kNN 打分、coreset 贪心降采样,
最后把它们串成一个 4×4 patch 网格的迷你 PatchCore,
看异常格的分数自己"亮"起来。

运行方式:  python exercise.py
完成所有 TODO 后,你应该看到所有测试通过

难度:⭐⭐⭐
预计用时:30-45 分钟
"""

import math


# ============================================================
# 🧱 Part 1: 欧氏距离(对应课程 §2)
# ============================================================
#
# 一切检索的地基:两个特征向量差多远。
#
#     d(a, b) = √( Σᵢ (aᵢ − bᵢ)² )
#
# SPADE / PatchCore 的"查档案",查的就是这个距离。
#

def euclidean(a, b):
    """计算两个等长向量的欧氏距离。

    Args:
        a, b: 等长的数字列表,如 [0, 0] 和 [3, 4]

    Returns:
        float:欧氏距离
    """
    # ======== TODO 1: 在这里写你的代码 ========
    # 提示:对每一对 (aᵢ, bᵢ) 累加 (aᵢ - bᵢ) ** 2,最后 math.sqrt。
    #       一行写法:math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 1 ========


# ============================================================
# 🧱 Part 2: 马氏距离·对角协方差简化版(对应课程 §3)
# ============================================================
#
# PaDiM 用马氏距离给"逐位置高斯档案"打分。
# 完整版要对协方差矩阵求逆;这里取对角协方差的简化版
# (假设维度间不相关,只保留"各维方差不同"这一半精髓):
#
#     d_M(x) = √( Σᵢ (xᵢ − μᵢ)² / σᵢ² )
#
# 直觉:每一维的偏离,先除以这一维自己的"正常波动幅度",
# 再汇总——爱晃的维度偏得多不稀奇,稳定的维度偏一点就反常。
#

def mahalanobis_diag(x, mean, var):
    """对角协方差版马氏距离。

    Args:
        x:    特征向量,如 [2, 0]
        mean: 各维均值 μ,如 [0, 0]
        var:  各维方差 σ²(注意是方差,不是标准差),如 [4, 1]

    Returns:
        float:马氏距离
    """
    # ======== TODO 2: 在这里写你的代码 ========
    # 提示:和 TODO 1 几乎一样,只是每项 (xᵢ-μᵢ)**2 先除以该维方差 vᵢ
    #       再累加,最后开根号。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 2 ========


# ============================================================
# 🧱 Part 3: kNN 打分(对应课程 §2 与 §4 第③步)
# ============================================================
#
# SPADE / PatchCore 的打分器:
# x 到记忆库每条特征算欧氏距离,升序排序,取前 k 个的平均。
# k=1 时就是"最近邻距离"——课程交互演示用的正是它。
#

def knn_score(x, bank, k):
    """x 到记忆库 bank 的 k 近邻平均距离。

    Args:
        x:    查询特征,如 [1, 2]
        bank: 记忆库,特征列表,如 [[0, 0], [1, 1], [5, 5]]
        k:    取最近的 k 个(1 <= k <= len(bank))

    Returns:
        float:前 k 小距离的平均值
    """
    # ======== TODO 3: 在这里写你的代码 ========
    # 提示:ds = sorted(euclidean(x, b) for b in bank)
    #       返回 sum(ds[:k]) / k

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 3 ========


# ============================================================
# 🧱 Part 4: coreset 贪心降采样(对应课程 §4 第②步)
# ============================================================
#
# 最远点采样,规则一句话:
#     每一轮,选"到已选集合的最近距离"最大的那个点。
# 它每步都在填补覆盖最薄弱的空洞,用极少的点守住整个分布。
# 课程 §4 的 5 点手推例子,就是本题的测试用例。
#

def greedy_coreset(points, m, start_idx=0):
    """贪心最远点采样,选出 m 个代表点的下标。

    Args:
        points:    特征列表,如 [[0, 0], [0.1, 0], [5, 5], ...]
        m:         要选出的代表点个数(1 <= m <= len(points))
        start_idx: 第一个入选的点的下标(默认 0)

    Returns:
        长度为 m 的下标列表,按入选顺序排列
    """
    # ======== TODO 4: 在这里写你的代码 ========
    # 提示:selected = [start_idx]
    #       循环直到凑够 m 个:
    #         对每个未选下标 i:
    #           d_i = min(euclidean(points[i], points[j]) for j in selected)
    #         选 d_i 最大的 i,append 进 selected
    #       返回 selected

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 4 ========


# ============================================================
# 🧱 Part 5: 串联!一个迷你 PatchCore(对应课程 §4 / §5)
# ============================================================
#
# 4×4 patch 网格,共 16 个 2 维特征(行优先展开:
# 下标 i 对应第 i//4 行、第 i%4 列)。
# 正常格循环取记忆库 NORMAL_BANK 里的值——所以它们在库里
# 都能找到一模一样的近亲;唯独下标 6(第 1 行第 2 列)被换成
# [4, 4]:一个混进产线的"划痕 patch"。
#
# 流水线(真实 PatchCore 的推理,一步不少):
#   ① 对每个格子,用 knn_score(k=1, bank=NORMAL_BANK) 打分
#   ② 拼成 4×4 分数图
#   ③ 找分数最大的格子 → 缺陷就在那里
#

NORMAL_BANK = [
    [1, 1], [1.1, 1], [0.9, 1.1], [1, 0.9],
    [1.05, 1.05], [0.95, 1], [1, 1.1], [1.1, 0.9],
]

GRID = [list(NORMAL_BANK[i % 8]) for i in range(16)]
GRID[6] = [4, 4]  # ← 藏进去的异常 patch(第 1 行第 2 列)


def patch_anomaly_map(grid, bank):
    """给 4×4 网格的每个 patch 打异常分,并找出最异常的位置。

    Args:
        grid: 16 个 2 维特征的列表(行优先展开)
        bank: 记忆库(特征列表)

    Returns:
        (score_map, (r, c)):
        score_map 是 4×4 的二维列表,score_map[r][c] 为该格的
        knn_score(k=1) 分数;(r, c) 是分数最大的格子位置。
    """
    # ======== TODO 5: 在这里写你的代码 ========
    # 提示(三步):
    #   1. 对每个 r, c(0..3):score = knn_score(grid[r*4 + c], bank, 1)
    #   2. 拼成 4×4 的 score_map
    #   3. 遍历 score_map 找最大值的位置 (r, c)
    #      返回 (score_map, (r, c))

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 5 ========


# ============================================================
# 🧪 测试
# ============================================================

def test_euclidean():
    print("测试 1: euclidean ...")
    out = euclidean([0, 0], [3, 4])
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 1 后再运行。")
        return False
    if abs(out - 5.0) < 1e-9 and abs(euclidean([1, 2], [1, 2])) < 1e-9:
        print("  ✅ 通过!勾股定理 3-4-5:d([0,0],[3,4]) = 5.0,同点距离 = 0。")
        return True
    print("  ❌ 结果不对:期望 5.0,得到 %r。检查平方、求和、开根号。" % out)
    return False


def test_mahalanobis():
    print("测试 2: mahalanobis_diag ...")
    out = mahalanobis_diag([2, 0], [0, 0], [4, 1])
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 2 后再运行。")
        return False
    out2 = mahalanobis_diag([0, 2], [0, 0], [4, 1])
    if abs(out - 1.0) < 1e-9 and abs(out2 - 2.0) < 1e-9:
        print("  ✅ 通过!同样偏 2:第一维(方差 4)马氏 = 1.0,第二维(方差 1)马氏 = 2.0。")
        print("     对比:两个点的欧氏距离都是 2.0——马氏把'各维波动尺度'算进了距离。")
        return True
    print("  ❌ 结果不对:期望 1.0 / 2.0,得到 %r / %r。" % (out, out2))
    print("     检查:每项应除以'方差'(不是标准差),最后开根号。")
    return False


def test_knn_score():
    print("测试 3: knn_score ...")
    if euclidean([0, 0], [3, 4]) is None:
        print("  ❌ 先完成 TODO 1(knn_score 要用它算距离)。")
        return False
    bank = [[0, 0], [1, 1], [5, 5]]
    s1 = knn_score([1, 2], bank, 1)
    if s1 is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 3 后再运行。")
        return False
    s2 = knn_score([1, 2], bank, 2)
    if abs(s1 - 1.0) < 1e-6 and abs(s2 - 1.6180) < 1e-3:
        print("  ✅ 通过!k=1 → 最近邻 [1,1] 距离 1.0;k=2 → (1.0 + √5)/2 ≈ 1.6180。")
        return True
    print("  ❌ 结果不对:期望 1.0 / 1.6180,得到 %r / %r。" % (s1, s2))
    print("     检查:距离要升序排序,取前 k 个的平均值。")
    return False


def test_greedy_coreset():
    print("测试 4: greedy_coreset ...")
    if euclidean([0, 0], [3, 4]) is None:
        print("  ❌ 先完成 TODO 1(greedy_coreset 要用它算距离)。")
        return False
    pts = [[0, 0], [0.1, 0], [5, 5], [5, 5.1], [10, 0]]
    out = greedy_coreset(pts, 3)
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 4 后再运行。")
        return False
    if list(out) == [0, 4, 3] and list(greedy_coreset(pts, 1)) == [0]:
        print("    入选顺序: %r" % (list(out),))
        print("  ✅ 通过!和课程 §4 的手推一致:P0 → P4(最远)→ P3;")
        print("     和 P0 几乎重合的冗余点 P1 永远轮不到——每一步都在补最大的覆盖空洞。")
        return True
    print("  ❌ 结果不对:期望 [0, 4, 3],得到 %r。" % (out,))
    print("     检查:每轮对每个未选点算'到已选集合的最近距离',选该距离最大的点。")
    return False


def test_patch_map():
    print("测试 5: 迷你 PatchCore ...")
    prereq = knn_score([1, 2], [[0, 0], [1, 1], [5, 5]], 1)
    if prereq is None:
        print("  ❌ 先完成 TODO 1 和 TODO 3,再来串联流水线。")
        return False
    result = patch_anomaly_map(GRID, NORMAL_BANK)
    if result is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 5 后再运行。")
        return False
    if not (isinstance(result, (list, tuple)) and len(result) == 2):
        print("  ❌ 返回值应是 (score_map, (r, c)) 二元组,得到 %r" % (result,))
        return False
    smap, pos = result
    print("    异常热力图(每格 = 该 patch 的 kNN 分数):")
    for r in range(4):
        print("      " + "  ".join("%.2f" % smap[r][c] for c in range(4)))
    print("    最异常位置: %s,分数 %.2f" % (tuple(pos), smap[pos[0]][pos[1]]))
    ok_pos = tuple(pos) == (1, 2)
    ok_anom = smap[1][2] > 4.0
    ok_rest = all(smap[r][c] < 0.3
                  for r in range(4) for c in range(4) if (r, c) != (1, 2))
    if ok_pos and ok_anom and ok_rest:
        print("    15 个正常格分数 ≈ 0(库里有一模一样的近亲),唯独异常格 > 4。")
        print("  ✅ 通过!零训练,'查档案'本身就完成了检测——异常格自己亮了起来。")
        return True
    print("  ❌ 结果不对:期望 argmax=(1,2) 且该格 > 4.0、其余格 < 0.3。")
    print("     检查:下标 i 对应第 i//4 行、第 i%%4 列;k 要用 1;bank 用 NORMAL_BANK。")
    return False


if __name__ == "__main__":
    print("=" * 52)
    print("第 08 课练习:亲手实现 PatchCore 的三大件")
    print("=" * 52)
    all_passed = True
    all_passed = test_euclidean() and all_passed
    all_passed = test_mahalanobis() and all_passed
    all_passed = test_knn_score() and all_passed
    all_passed = test_greedy_coreset() and all_passed
    all_passed = test_patch_map() and all_passed
    print("-" * 52)
    if all_passed:
        print("🎉 全部通过!距离、kNN、coreset——PatchCore 的三大件都在你手里了。下一课见。")
    else:
        print("💪 还有测试没通过,按提示继续加油!")
