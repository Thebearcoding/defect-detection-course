# -*- coding: utf-8 -*-
"""
============================================================
第 05 课练习:亲手实现 IoU、anchor 匹配和 NMS
============================================================

你将用纯 Python(零依赖)实现目标检测的"后半程":
IoU 重叠度量、anchor 正负样本分配、NMS 去重,
以及评测时的 TP/FP 判定,最后把它们串成一条
"NMS 去重 → 对照真值评分"的完整流水线。

约定:框一律写成 [x1, y1, x2, y2](左上角、右下角,
x2 > x1,y2 > y1),分数为 0~1 的浮点数。

运行方式:  python exercise.py
完成所有 TODO 后,你应该看到所有测试通过

难度:⭐⭐⭐
预计用时:30-45 分钟
"""


# ============================================================
# 🧱 Part 1: 交并比 IoU(对应课程 §2)
# ============================================================
#
# IoU = 交集面积 / 并集面积,范围 [0, 1]。
# 交集框:x 方向取 [max(x1), min(x2)],y 方向同理;
# 任一方向的宽度 ≤ 0,说明两框不相交,交集面积为 0。
# 并集 = 面积A + 面积B − 交集。
#

def iou(a, b):
    """计算两个框的交并比。

    Args:
        a, b: [x1, y1, x2, y2]

    Returns:
        float,范围 [0, 1]
    """
    # ======== TODO 1: 在这里写你的代码 ========
    # 提示:1. 交集左上 = (max(a[0],b[0]), max(a[1],b[1]))
    #          交集右下 = (min(a[2],b[2]), min(a[3],b[3]))
    #       2. 交集宽 = max(0, 右 − 左),高同理,inter = 宽 × 高
    #       3. union = 面积a + 面积b − inter
    #       4. 返回 inter / union(union 为 0 时返回 0.0)

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 1 ========


# ============================================================
# 🧱 Part 2: anchor 正负样本分配(对应课程 §3)
# ============================================================
#
# 训练时,每个 anchor 要"领任务":
# 与真值框 IoU ≥ thr 的记正样本 'pos'(负责这个目标),
# 否则记负样本 'neg'(背景)。
# (真实检测器还有"忽略区间",这里简化成二分。)
#

def match_anchors(anchors, gt_box, thr=0.5):
    """给每个 anchor 分配 'pos' / 'neg' 标签。

    Args:
        anchors: 框列表,如 [[0,0,10,10], ...]
        gt_box:  真值框 [x1, y1, x2, y2]
        thr:     正样本 IoU 阈值,默认 0.5

    Returns:
        与 anchors 等长的列表,元素是 'pos' 或 'neg'
    """
    # ======== TODO 2: 在这里写你的代码 ========
    # 提示:一行列表推导即可:
    #       iou(a, gt_box) >= thr 时取 'pos',否则取 'neg'。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 2 ========


# ============================================================
# 🧱 Part 3: NMS 非极大值抑制(对应课程 §5)
# ============================================================
#
# 网络会对同一目标输出一堆重叠框,NMS 负责去重:
#   1. 所有下标按分数从高到低排序
#   2. 取还没被抑制的最高分框保留
#   3. 把与它 IoU > iou_thr 的其余候选全部抑制
#   4. 重复 2-3,直到候选取尽
#

def nms(boxes, scores, iou_thr=0.5):
    """非极大值抑制。

    Args:
        boxes:   框列表
        scores:  与 boxes 等长的分数列表
        iou_thr: 抑制阈值,默认 0.5

    Returns:
        保留框的"原始下标"列表,按分数从高到低的保留顺序
    """
    # ======== TODO 3: 在这里写你的代码 ========
    # 提示:order = sorted(range(len(boxes)), key=lambda i: -scores[i])
    #       用一个 set 记录被抑制的下标;
    #       遍历 order:跳过已被抑制的;否则 append 进 keep,
    #       再把 order 里其余未抑制、且与它 IoU > iou_thr 的下标加入抑制集。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 3 ========


# ============================================================
# 🧱 Part 4: 评测判定 TP/FP(对应课程 §6)
# ============================================================
#
# mAP 计算的第一步:按置信度从高到低,逐个预测框判定——
# 在"还没被认领"的真值框里找 IoU 最大的那个;
# 最大 IoU ≥ iou_thr → 记 TP(1),并占用该真值框;
# 否则 → 记 FP(0)。
# 一个真值框只能被认领一次,重复命中的框都算 FP。
#

def eval_detections(pred_boxes, pred_scores, gt_boxes, iou_thr=0.5):
    """按分数降序逐个判定 TP/FP。

    Args:
        pred_boxes:  预测框列表
        pred_scores: 与 pred_boxes 等长的置信度列表
        gt_boxes:    真值框列表
        iou_thr:     命中阈值,默认 0.5

    Returns:
        tp_flags:0/1 列表,按分数从高到低排列(1=TP,0=FP)
    """
    # ======== TODO 4: 在这里写你的代码 ========
    # 提示:order = sorted(range(len(pred_boxes)), key=lambda i: -pred_scores[i])
    #       used = set() 记录已被认领的真值下标;
    #       对每个预测:遍历未认领的 gt,找最大 IoU 及其下标;
    #       最大 IoU >= iou_thr → flags.append(1) 并 used.add(该下标),
    #       否则 flags.append(0)。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 4 ========


# ============================================================
# 🧱 Part 5: 串联!完整的后处理 + 评分流水线(对应课程 §5-§6)
# ============================================================
#
# 把前面的零件接起来,走一遍检测器输出之后的全流程:
#   ① nms:一堆重叠候选 → 去重后的最终预测
#   ② eval_detections:对照真值,逐个判 TP/FP
#   ③ 汇总:TP 个数、FP 个数
#

def detect_pipeline(boxes, scores, gts, iou_thr=0.5):
    """先 NMS 去重,再对照真值评测。

    Args:
        boxes, scores: 网络原始输出的候选框与分数
        gts:           真值框列表
        iou_thr:       NMS 与评测共用的阈值,默认 0.5

    Returns:
        (tp, fp):保留框中命中真值的个数、误报的个数
    """
    # ======== TODO 5: 在这里写你的代码 ========
    # 提示(四行):
    #   1. keep = nms(boxes, scores, iou_thr)
    #   2. kept_boxes  = [boxes[i] for i in keep]
    #      kept_scores = [scores[i] for i in keep]
    #   3. flags = eval_detections(kept_boxes, kept_scores, gts, iou_thr)
    #   4. return (sum(flags), len(flags) - sum(flags))

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 5 ========


# ============================================================
# 🧪 测试
# ============================================================
#
# NMS 测试数据 = 课程 §5 步进演示里的 6 个框(下标 0..5 = A..F):
# 左上一簇 A/B/C,右侧一簇 D/E,右下独立框 F。
#

NMS_BOXES = [
    [20, 20, 80, 80],      # 0 = A  s=0.92  ┐
    [26, 24, 86, 84],      # 1 = B  s=0.85  │ 左上一簇(B、C 应被 A 抑制)
    [30, 30, 85, 88],      # 2 = C  s=0.70  ┘
    [140, 40, 200, 100],   # 3 = D  s=0.88  ┐ 右侧一簇(E 应被 D 抑制)
    [146, 44, 206, 104],   # 4 = E  s=0.66  ┘
    [90, 130, 130, 170],   # 5 = F  s=0.45  — 独立,应保留
]
NMS_SCORES = [0.92, 0.85, 0.70, 0.88, 0.66, 0.45]


def test_iou():
    print("测试 1: iou ...")
    v = iou([0, 0, 10, 10], [5, 5, 15, 15])
    if v is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 1 后再运行。")
        return False
    # 课程 §2 的手算例子:交 25 / 并 175 = 1/7
    ok1 = abs(v - 1.0 / 7.0) < 1e-6
    v2 = iou([3, 3, 8, 9], [3, 3, 8, 9])
    ok2 = v2 is not None and abs(v2 - 1.0) < 1e-6
    v3 = iou([0, 0, 10, 10], [20, 20, 30, 30])
    ok3 = v3 is not None and abs(v3 - 0.0) < 1e-6
    if ok1 and ok2 and ok3:
        print("  ✅ 通过!斜角相交 1/7、同框 1.0、不相交 0.0 全部正确。")
        return True
    if not ok1:
        print("  ❌ 结果不对:iou([0,0,10,10],[5,5,15,15]) 期望 1/7≈0.142857,得到 %r。" % v)
        print("     检查:交集应是 [5,5,10,10],面积 25;并集 = 100+100−25 = 175。")
    if not ok2:
        print("  ❌ 完全相同的两个框 IoU 应为 1.0,得到 %r。" % v2)
    if not ok3:
        print("  ❌ 完全不相交的两个框 IoU 应为 0.0,得到 %r。检查宽高是否用了 max(0, ...)。" % v3)
    return False


def test_match_anchors():
    print("测试 2: match_anchors ...")
    if iou([0, 0, 2, 2], [0, 0, 2, 2]) is None:
        print("  ❌ 先完成 TODO 1(iou),anchor 匹配要用它。")
        return False
    out = match_anchors([[0, 0, 10, 10], [2, 2, 12, 12], [20, 20, 30, 30]],
                        [1, 1, 11, 11])
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 2 后再运行。")
        return False
    # 前两个 anchor 与 gt 的 IoU 都是 81/119 ≈ 0.6807(交 9×9=81,并 100+100−81=119),
    # 第三个完全不相交,IoU = 0。
    if out == ['pos', 'pos', 'neg']:
        print("  ✅ 通过!IoU≈[0.68, 0.68, 0.00] → ['pos','pos','neg'],anchor 领到了正确任务。")
        return True
    print("  ❌ 结果不对:期望 ['pos','pos','neg'],得到 %r。" % (out,))
    print("     检查:是否对每个 anchor 调用 iou(a, gt_box) 并与 thr 比较?")
    return False


def test_nms():
    print("测试 3: nms ...")
    if iou([0, 0, 2, 2], [0, 0, 2, 2]) is None:
        print("  ❌ 先完成 TODO 1(iou),NMS 要用它。")
        return False
    out = nms(NMS_BOXES, NMS_SCORES)
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 3 后再运行。")
        return False
    # 手算:IoU(A,B)=0.724、IoU(A,C)=0.583 → B、C 被 A 抑制;
    #       IoU(D,E)=0.724 → E 被 D 抑制;F 与谁都不重叠 → 保留。
    if out == [0, 3, 5]:
        print("  ✅ 通过!保留 [0,3,5](A、D、F):A 压掉了 B、C,D 压掉了 E,独立的 F 幸存。")
        return True
    print("  ❌ 结果不对:期望 [0, 3, 5],得到 %r。" % (out,))
    print("     检查:是否按分数降序?是否只与'已保留'的框比 IoU?返回的是原始下标吗?")
    return False


def test_eval_detections():
    print("测试 4: eval_detections ...")
    if iou([0, 0, 2, 2], [0, 0, 2, 2]) is None:
        print("  ❌ 先完成 TODO 1(iou),评测判定要用它。")
        return False
    preds = [[0, 0, 10, 10], [1, 1, 11, 11], [20, 20, 30, 30]]
    scores = [0.9, 0.8, 0.7]
    gts = [[0, 0, 10, 10], [20, 20, 30, 30]]
    out = eval_detections(preds, scores, gts)
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 4 后再运行。")
        return False
    # 0.9 的框与 gt1 完全重合 → TP 并占用 gt1;
    # 0.8 的框最像的 gt1 已被占用(剩下的 gt2 与它 IoU=0)→ FP;
    # 0.7 的框与 gt2 完全重合 → TP。
    if out == [1, 0, 1]:
        print("  ✅ 通过![1, 0, 1]:第二个框虽与 gt1 重叠 0.68,但 gt1 已被更高分的框认领 → FP。")
        return True
    print("  ❌ 结果不对:期望 [1, 0, 1],得到 %r。" % (out,))
    print("     检查:真值被认领后是否不再参与匹配?是否按分数从高到低处理?")
    return False


def test_detect_pipeline():
    print("测试 5: 完整流水线 ...")
    prereq = (nms([[0, 0, 2, 2]], [0.9]) is not None
              and eval_detections([[0, 0, 2, 2]], [0.9], [[0, 0, 2, 2]]) is not None)
    if not prereq:
        print("  ❌ 先完成 TODO 3 和 TODO 4,再来串流水线。")
        return False
    gts = [[20, 20, 82, 82], [142, 42, 202, 102]]
    result = detect_pipeline(NMS_BOXES, NMS_SCORES, gts)
    if result is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 5 后再运行。")
        return False
    tp, fp = result
    print("    流水线结果: TP=%s, FP=%s" % (tp, fp))
    # NMS 留下 A(0.92)、D(0.88)、F(0.45);
    # A 与 gt1:交 60×60=3600,并 3844+3600−3600=3844 → IoU≈0.9365 → TP;
    # D 与 gt2:交 58×58=3364,并 3600+3600−3364=3836 → IoU≈0.8770 → TP;
    # F 与两个真值都不沾边 → FP。tp_flags 按分数序 = [1, 1, 0]。
    if (tp, fp) == (2, 1):
        print("    A、D 各命中一个真值缺陷,独立框 F 是误报 —— 判定全部正确!")
        print("  ✅ 通过!NMS → 评测的完整后半程打通了。")
        return True
    print("  ❌ 结果不对:期望 (tp=2, fp=1),得到 (%r, %r)。" % (tp, fp))
    print("     检查:是否先 NMS 再评测?kept_scores 是否和 kept_boxes 一一对应?")
    return False


if __name__ == "__main__":
    print("=" * 52)
    print("第 05 课练习:亲手实现 IoU、anchor 匹配和 NMS")
    print("=" * 52)
    all_passed = True
    all_passed = test_iou() and all_passed
    all_passed = test_match_anchors() and all_passed
    all_passed = test_nms() and all_passed
    all_passed = test_eval_detections() and all_passed
    all_passed = test_detect_pipeline() and all_passed
    print("-" * 52)
    if all_passed:
        print("🎉 全部通过!检测的后半程(去重与评分)已经在你手里了。下一课见。")
    else:
        print("💪 还有测试没通过,按提示继续加油!")
