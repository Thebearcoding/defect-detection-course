# -*- coding: utf-8 -*-
"""
============================================================
第 10 课练习:亲手造伪缺陷,并验证它自带免费标注
============================================================

你将用纯 Python(零依赖)实现 CutPaste 的完整流程:
剪一块 → 贴到别处 → 顺手生成像素级 mask,
最后逐像素比对,亲眼验证"标注是免费的"——
这正是合成缺陷路线把无监督问题变回监督问题的全部秘密。

运行方式:  python exercise.py
完成所有 TODO 后,你应该看到所有测试通过

难度:⭐⭐
预计用时:20-30 分钟
"""


# ============================================================
# 🧱 实验材料:一张 6×6 的"工件图"
# ============================================================
#
# 像素值 = 行号×10 + 列号,例如第 3 行第 4 列的值是 34。
# 这样设计的好处:看到任何一个值,立刻知道它"原本住在哪"——
# 补丁贴到哪里、哪些像素被换过,一眼可查。
#
#     [ 0,  1,  2,  3,  4,  5]
#     [10, 11, 12, 13, 14, 15]
#     [20, 21, 22, 23, 24, 25]
#     [30, 31, 32, 33, 34, 35]
#     [40, 41, 42, 43, 44, 45]
#     [50, 51, 52, 53, 54, 55]
#

IMG = [[r * 10 + c for c in range(6)] for r in range(6)]


# ============================================================
# 🧱 Part 1: 剪——从图上取一块补丁(对应课程 §2)
# ============================================================
#
# CutPaste 的第一步:在图像上剪下一小块。
# 取以 (r, c) 为左上角、高 h 宽 w 的子矩阵。
#

def cut_patch(img, r, c, h, w):
    """从 img 中剪出以 (r, c) 为左上角、尺寸 h×w 的补丁。

    Args:
        img: H×W 的二维列表
        r, c: 补丁左上角的行号、列号
        h, w: 补丁的高、宽

    Returns:
        h×w 的二维列表(新列表,不共享原图的行)
    """
    # ======== TODO 1: 在这里写你的代码 ========
    # 提示:双层推导式一行搞定:
    #       [[img[r+i][c+j] for j in range(w)] for i in range(h)]

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 1 ========


# ============================================================
# 🧱 Part 2: 贴——把补丁贴到另一个位置(对应课程 §2)
# ============================================================
#
# 关键要求:返回"新图",绝不能修改原图!
# 原因很实际:训练时同一张正常图要反复用来合成不同的伪缺陷,
# 如果第一次合成就把原图改了,后面全错。
# (这也是深拷贝 row[:] 与浅拷贝的经典陷阱。)
#

def paste_patch(img, patch, r, c):
    """把 patch 贴到 img 的 (r, c) 处,返回新图,不修改原图。

    Args:
        img:   H×W 的二维列表
        patch: h×w 的二维列表
        r, c:  粘贴位置左上角的行号、列号

    Returns:
        H×W 的二维列表(全新的图,原 img 保持原样)
    """
    # ======== TODO 2: 在这里写你的代码 ========
    # 提示:三步:
    #   1. 深拷贝:new = [row[:] for row in img](注意 row[:] 复制每一行)
    #   2. 双层循环遍历 patch 的 (i, j),写入 new[r+i][c+j] = patch[i][j]
    #   3. 返回 new

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 2 ========


# ============================================================
# 🧱 Part 3: 免费标注——生成 GT mask(对应课程 §5)
# ============================================================
#
# 全 0 图上,把"贴过补丁"的区域置 1。
# 注意:我们根本不需要"检测"补丁贴在哪——是我们自己贴的,
# 位置当然知道。这就是"标注免费"四个字的来历。
#

def make_mask(h_img, w_img, r, c, h, w):
    """生成 h_img×w_img 的二值 mask:粘贴区域为 1,其余为 0。

    Args:
        h_img, w_img: mask 的高、宽(与图像一致)
        r, c:         粘贴位置左上角
        h, w:         补丁的高、宽

    Returns:
        h_img×w_img 的二维列表,元素只有 0 和 1
    """
    # ======== TODO 3: 在这里写你的代码 ========
    # 提示:先造全 0 图:[[0] * w_img for _ in range(h_img)]
    #       (小心不要写成 [[0]*w_img]*h_img——那是同一行的 h_img 个引用!)
    #       再双层循环把 mask[r+i][c+j] 置 1。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 3 ========


# ============================================================
# 🧱 Part 4: 串联——完整的 CutPaste 合成器(对应课程 §2 + §5)
# ============================================================
#
# 剪 + 贴 + 标注,一步到位。
# 真实训练循环里,这个函数每个 batch 都会被调用一次,
# src / dst / size 全部随机——每张正常图都能变出无穷多伪缺陷。
#

def make_cutpaste(img, src, dst, size):
    """对 img 执行一次 CutPaste,返回 (伪缺陷图, 免费 mask)。

    Args:
        img:  H×W 的二维列表
        src:  (r, c) 剪切位置左上角
        dst:  (r, c) 粘贴位置左上角
        size: (h, w) 补丁尺寸

    Returns:
        (aug_img, mask) 二元组:
        aug_img: 贴过补丁的新图(原图不变)
        mask:    与 aug_img 同尺寸的二值标注
    """
    # ======== TODO 4: 在这里写你的代码 ========
    # 提示:把 Part 1-3 串起来,共三行:
    #   patch = cut_patch(img, src[0], src[1], size[0], size[1])
    #   aug   = paste_patch(img, patch, dst[0], dst[1])
    #   mask  = make_mask(len(img), len(img[0]), dst[0], dst[1], size[0], size[1])
    #   返回 (aug, mask)

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 4 ========


# ============================================================
# 🧱 Part 5: 验证"标注是免费的"(对应课程 §5)
# ============================================================
#
# 把原图和伪缺陷图逐像素比对:不同记 1,相同记 0,得到 diff_map。
# 如果我们的流水线没毛病,diff_map 应该和 mask 一模一样——
# "哪些像素被动过"这个信息,构造过程顺手就给了,零标注成本。
#
# (第 7 课的重构类方法要训练一个网络才能近似算出"哪里不对";
#  这里连网络都不用,因为答案是我们自己写下的。)
#

def verify_free_label(img, aug, mask):
    """逐像素比对 img 与 aug,生成 diff_map(不同为 1,相同为 0)。

    Args:
        img:  原图,H×W 二维列表
        aug:  伪缺陷图,H×W 二维列表
        mask: 合成时生成的免费标注(本函数只负责算 diff_map,
              与 mask 的比对交给测试来做)

    Returns:
        H×W 的二维列表 diff_map,元素只有 0 和 1
    """
    # ======== TODO 5: 在这里写你的代码 ========
    # 提示:双层推导式:
    #   [[1 if img[i][j] != aug[i][j] else 0 for j in range(len(img[0]))]
    #    for i in range(len(img))]

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 5 ========


# ============================================================
# 🧪 测试
# ============================================================

def test_cut_patch():
    print("测试 1: cut_patch ...")
    out = cut_patch(IMG, 0, 0, 2, 2)
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 1 后再运行。")
        return False
    if out == [[0, 1], [10, 11]]:
        out2 = cut_patch(IMG, 2, 3, 1, 3)
        if out2 == [[23, 24, 25]]:
            print("  ✅ 通过!(0,0) 处剪 2×2 得 [[0,1],[10,11]],位置索引正确。")
            return True
        print("  ❌ 非方形补丁不对:(2,3) 处剪 1×3 应得 [[23,24,25]],得到 %r" % out2)
        return False
    print("  ❌ 结果不对:期望 [[0,1],[10,11]],得到 %r。" % out)
    print("     检查:行用 img[r+i],列用 [c+j],i 走 h 步、j 走 w 步。")
    return False


def test_paste_patch():
    print("测试 2: paste_patch ...")
    out = paste_patch(IMG, [[0, 1], [10, 11]], 3, 3)
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 2 后再运行。")
        return False
    ok_paste = (out[3][3] == 0 and out[3][4] == 1
                and out[4][3] == 10 and out[4][4] == 11)
    ok_rest = out[0][0] == 0 and out[2][2] == 22 and out[5][5] == 55
    if not (ok_paste and ok_rest):
        print("  ❌ 粘贴结果不对:aug[3][3..4] 应为 0,1、aug[4][3..4] 应为 10,11,")
        print("     其余像素保持原值。得到 aug[3][3]=%r aug[3][4]=%r aug[4][3]=%r aug[4][4]=%r"
              % (out[3][3], out[3][4], out[4][3], out[4][4]))
        return False
    if IMG[3][3] != 33:
        print("  ❌ 原图被改了!IMG[3][3] 应仍为 33,现在是 %r。" % IMG[3][3])
        print("     检查深拷贝:new = [row[:] for row in img],row[:] 不能少。")
        return False
    print("  ✅ 通过!补丁贴对了位置,且原图分毫未动(IMG[3][3] 仍是 33)。")
    return True


def test_make_mask():
    print("测试 3: make_mask ...")
    out = make_mask(6, 6, 3, 3, 2, 2)
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 3 后再运行。")
        return False
    if len(out) != 6 or len(out[0]) != 6:
        print("  ❌ 尺寸不对:应为 6×6,得到 %d×%d。" % (len(out), len(out[0])))
        return False
    ones = [(i, j) for i in range(6) for j in range(6) if out[i][j] == 1]
    total = sum(sum(row) for row in out)
    if total == 4 and ones == [(3, 3), (3, 4), (4, 3), (4, 4)]:
        print("  ✅ 通过!恰好 4 个 1,且都落在粘贴区域 (3,3)-(4,4)。")
        return True
    print("  ❌ 结果不对:应恰有 4 个 1,位于 (3,3)(3,4)(4,3)(4,4);")
    print("     实际共 %d 个 1,位置 %r。" % (total, ones))
    print("     若整列/多行同时变 1,检查是否用了 [[0]*w]*h 这种浅拷贝写法。")
    return False


def test_make_cutpaste():
    print("测试 4: make_cutpaste ...")
    prereq = (cut_patch(IMG, 0, 0, 1, 1) is not None
              and paste_patch(IMG, [[99]], 0, 0) is not None
              and make_mask(2, 2, 0, 0, 1, 1) is not None)
    if not prereq:
        print("  ❌ 先完成 TODO 1-3,再来串联。")
        return False
    result = make_cutpaste(IMG, (0, 0), (3, 3), (2, 2))
    if result is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 4 后再运行。")
        return False
    aug, mask = result
    ok_aug = (aug[3][3] == 0 and aug[3][4] == 1
              and aug[4][3] == 10 and aug[4][4] == 11 and aug[0][0] == 0)
    ok_mask = mask == make_mask(6, 6, 3, 3, 2, 2)
    ok_orig = IMG[3][3] == 33
    if ok_aug and ok_mask and ok_orig:
        print("  ✅ 通过!剪 (0,0)、贴 (3,3)、mask 同步生成——一次调用,样本和标注全有了。")
        return True
    if not ok_orig:
        print("  ❌ 原图被改了:IMG[3][3] 应仍为 33。检查 paste_patch 的深拷贝。")
        return False
    print("  ❌ 结果不对:aug 的 (3,3)-(4,4) 应为 0,1,10,11,mask 应只在该区域为 1。")
    print("     检查参数顺序:src 用于剪,dst 用于贴和 mask,size 是 (h, w)。")
    return False


def test_verify_free_label():
    print("测试 5: 免费标注验证 ...")
    prereq = make_cutpaste(IMG, (0, 0), (3, 3), (2, 2))
    if prereq is None:
        print("  ❌ 先完成 TODO 1-4,再来做最终验证。")
        return False
    aug, mask = prereq
    diff = verify_free_label(IMG, aug, mask)
    if diff is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 5 后再运行。")
        return False
    if diff == mask:
        print("    diff_map(逐像素比对原图与伪缺陷图)==")
        for row in diff:
            print("      %r" % row)
        print("    它与合成时生成的 mask 完全相等!")
        print("  ✅ 通过!伪缺陷的标注是构造过程免费送的——一个像素都没标,")
        print("     却拿到了像素级 GT。合成路线 = 把无监督变回监督。")
        return True
    print("  ❌ diff_map 与 mask 不相等。")
    print("     期望:仅 (3,3)(3,4)(4,3)(4,4) 为 1(贴入值 0,1,10,11 与原值 33,34,43,44 全不同)。")
    print("     得到 diff_map = %r" % diff)
    print("     检查:比较的是 img 与 aug 对应位置,不同记 1、相同记 0。")
    return False


if __name__ == "__main__":
    print("=" * 52)
    print("第 10 课练习:亲手造伪缺陷,并验证它自带免费标注")
    print("=" * 52)
    all_passed = True
    all_passed = test_cut_patch() and all_passed
    all_passed = test_paste_patch() and all_passed
    all_passed = test_make_mask() and all_passed
    all_passed = test_make_cutpaste() and all_passed
    all_passed = test_verify_free_label() and all_passed
    print("-" * 52)
    if all_passed:
        print("🎉 全部通过!你已经亲手实现了 CutPaste,并用 assert 证明了")
        print("   \"伪缺陷自带免费像素级标注\"。下一课:归一化流,见!")
    else:
        print("💪 还有测试没通过,按提示继续加油!")
