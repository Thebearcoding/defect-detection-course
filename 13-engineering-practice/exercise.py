# -*- coding: utf-8 -*-
"""
============================================================
第 13 课练习:把十三课装进一个决策引擎
============================================================

课程收官练习:不再实现某一个模型,而是把工程落地的
四个关键判断写成代码——方法选型(§2 决策树)、
验证集定阈值(§3)、时延预算(§4)、分数漂移报警(§3),
最后串成一条完整的"产线决策链"。

运行方式:  python exercise.py
完成所有 TODO 后,你应该看到所有测试通过

难度:⭐⭐
预计用时:25-40 分钟
"""

# 验证集分数与标签(§3 定阈值用,贯穿 TODO 2 和 TODO 5)
# 分数越高 = 模型越怀疑它有缺陷;标签 1 = 真缺陷,0 = 真正常
SCORES = [0.95, 0.9, 0.85, 0.6, 0.55, 0.5, 0.3, 0.1]
LABELS = [1,    1,   1,    0,   1,    0,   0,   0]

# 上线时留存的"基线分数"(确认正常时期的分数,TODO 4 用)
BASELINE = [0.1, 0.12, 0.11, 0.09, 0.1, 0.08]


# ============================================================
# 🧱 Part 1: 选型决策树(对应课程 §2)
# ============================================================
#
# 把课程 §2 那棵交互决策树写成一条 if 规则链,按顺序判断:
#   ① 连正常样本都没有、也无标注     → 'winclip'    零样本兜底(第 12 课)
#   ② 有标注,且需要像素级轮廓       → 'unet'       监督分割(第 6 课)
#   ③ 有标注(不需要像素级)         → 'yolo'       目标检测(第 5 课)
#   ④ 时延预算 < 5ms                 → 'efficientad' 师生蒸馏(第 9 课)
#   ⑤ 其余情况(默认答案)           → 'patchcore'  特征嵌入(第 8 课)
#
# 规则的先后顺序就是选型的优先级:数据可得性 > 输出粒度 > 时延。
#

def recommend(has_defect_labels, need_pixel_mask, latency_ms, n_normal):
    """按规则链返回推荐方法名(小写字符串)。

    Args:
        has_defect_labels: bool,是否有带标注的缺陷样本
        need_pixel_mask:   bool,是否需要像素级缺陷轮廓
        latency_ms:        float,推理时延预算(毫秒)
        n_normal:          int,手头正常样本的数量

    Returns:
        'winclip' / 'unet' / 'yolo' / 'efficientad' / 'patchcore' 之一
    """
    # ======== TODO 1: 在这里写你的代码 ========
    # 提示:五条 if 按注释顺序写,命中即 return;
    #       第 ① 条是 n_normal == 0 且 not has_defect_labels;
    #       最后一条直接 return 'patchcore'(默认答案)。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 1 ========


# ============================================================
# 🧱 Part 2: 验证集上扫最优 F1 阈值(对应课程 §3,回收第 4 课)
# ============================================================
#
# 分数 ≥ 阈值 → 报警(预测为缺陷)。候选阈值取 scores 里出现过的
# 每个分数(其他阈值的报警结果必与某个候选相同)。
# 对每个候选:统计 TP/FP/FN → P、R → F1,取 F1 最大的阈值。
#

def best_f1_threshold(scores, labels):
    """扫描候选阈值,返回 (最优阈值, 对应的 F1)。

    F1 并列时返回其中更大的阈值(报警越少越省复检人力)。

    Returns:
        (thr, f1)
    """
    # ======== TODO 2: 在这里写你的代码 ========
    # 提示:候选阈值从大到小遍历:sorted(scores, reverse=True);
    #       每个 thr 用 zip(scores, labels) 数出 tp / fp / fn
    #       (pred = s >= thr,注意是 >=);
    #       p = tp/(tp+fp),r = tp/(tp+fn),分母为 0 时取 0.0;
    #       f1 = 2*p*r/(p+r),p+r 为 0 时取 0.0;
    #       只在 f1「严格大于」当前最优时更新——并列时自动保留更大的阈值。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 2 ========


# ============================================================
# 🧱 Part 3: 时延预算判断(对应课程 §4)
# ============================================================
#
# 工程铁律:纸面时延 ≠ 产线时延。预处理、传图、抖动都要吃余量,
# 所以判断能否满足预算时,给模型时延乘一个安全系数(默认 1.2,
# 即预留 20% 余量),再和预算比较。
#

def within_latency(model_ms, budget_ms, safety=1.2):
    """判断模型时延乘上安全系数后是否仍在预算内。

    Args:
        model_ms:  float,模型单帧推理时延(毫秒)
        budget_ms: float,产线允许的时延预算(毫秒)
        safety:    float,安全系数(默认 1.2)

    Returns:
        bool:model_ms * safety <= budget_ms
    """
    # ======== TODO 3: 在这里写你的代码 ========
    # 提示:一行,return 一个比较表达式。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 3 ========


# ============================================================
# 🧱 Part 4: 分数漂移报警(对应课程 §3)
# ============================================================
#
# 上线后监控分数分布:近期分数的均值一旦超过
#     基线均值 + k × 基线标准差(k 默认 3,即 3σ 规则)
# 就报警——大概率是分布漂移(换原料 / 镜头脏了 / 光照变化),
# 第一动作是查环境、重标定阈值,不是重训模型。
#
# 标准差用「总体标准差」:方差 = 偏差平方的平均值(除以 N)。
#

def drift_alarm(baseline, new, k=3.0):
    """判断近期分数 new 相对基线 baseline 是否触发漂移报警。

    Args:
        baseline: 基线分数列表(确认正常时期留存)
        new:      近期分数列表
        k:        报警倍数(默认 3.0,即 3σ)

    Returns:
        bool:mean(new) > mean(baseline) + k * std(baseline)
    """
    # ======== TODO 4: 在这里写你的代码 ========
    # 提示:m = sum(baseline) / len(baseline)
    #       var = sum((x - m) ** 2 for x in baseline) / len(baseline)
    #       std = var ** 0.5
    #       return sum(new) / len(new) > m + k * std

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 4 ========


# ============================================================
# 🧱 Part 5: 串联!一条完整的产线决策链(对应课程 §2-§4)
# ============================================================
#
# 把前面的零件拼成产线上真实发生的三步:
#   ① recommend 选方法(§2 决策树)
#   ② best_f1_threshold 在验证集上定阈值(§3)
#   ③ 对新一批工件的分数出判定:分数 ≥ 阈值 → 1(报警),否则 0(放行)
#

def production_pipeline(cfg, val_scores, val_labels, test_scores):
    """跑通"选型 → 定阈值 → 出判定"的完整决策链。

    Args:
        cfg:         四元组 (has_defect_labels, need_pixel_mask, latency_ms, n_normal)
        val_scores:  验证集异常分数
        val_labels:  验证集真实标签
        test_scores: 新一批工件的异常分数

    Returns:
        dict,含三个键:
          'method':    recommend 选出的方法名
          'threshold': best_f1_threshold 定出的阈值
          'decisions': 判定列表,每个元素 1(报警)或 0(放行)
    """
    # ======== TODO 5: 在这里写你的代码 ========
    # 提示(三步,每步一两行):
    #   1. method = recommend(*cfg)          # 解包四元组
    #   2. thr, _f1 = best_f1_threshold(val_scores, val_labels)
    #   3. decisions = [1 if s >= thr else 0 for s in test_scores]
    #   返回 {'method': method, 'threshold': thr, 'decisions': decisions}

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 5 ========


# ============================================================
# 🧪 测试
# ============================================================

def test_recommend():
    print("测试 1: recommend ...")
    out = recommend(True, True, 100, 500)
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 1 后再运行。")
        return False
    cases = [
        ((True,  True,  100, 500), 'unet'),
        ((False, False, 2,   200), 'efficientad'),
        ((False, True,  50,  100), 'patchcore'),
        ((False, False, 50,  0),   'winclip'),
    ]
    for args, want in cases:
        got = recommend(*args)
        if got != want:
            print("  ❌ 结果不对:recommend%r 期望 %r,得到 %r。" % (args, want, got))
            print("     检查:五条规则的先后顺序(①无样本无标注 ②有标注+像素级")
            print("     ③有标注 ④时延<5ms ⑤默认 patchcore),命中即返回。")
            return False
    print("  ✅ 通过!四种产线情境都走到了 §2 决策树的正确出口。")
    print("     注意 (False, True, 50, 100):没有标注,「要像素级」也轮不到 U-Net——")
    print("     PatchCore 的热力图本来就是像素级的。")
    return True


def test_best_f1_threshold():
    print("测试 2: best_f1_threshold ...")
    result = best_f1_threshold(SCORES, LABELS)
    if result is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 2 后再运行。")
        return False
    thr, f1 = result
    print("    扫描结果: 最优阈值 %s,F1 = %.4f" % (thr, f1))
    if thr == 0.55 and abs(f1 - 0.8889) <= 1e-3:
        print("  ✅ 通过!thr=0.55 时 TP=4、FP=1、FN=0 → P=0.8、R=1.0、F1=8/9≈0.8889。")
        return True
    print("  ❌ 结果不对:期望 (0.55, 0.8889),得到 (%r, %r)。" % (thr, f1))
    print("     手算对账:thr=0.55 → 报警 5 个(≥0.55),其中 4 真缺陷、1 误杀,")
    print("     漏检 0 → P=4/5, R=4/4, F1=2×0.8×1/(0.8+1)=8/9。检查 >= 与除零处理。")
    return False


def test_within_latency():
    print("测试 3: within_latency ...")
    out = within_latency(3.0, 5)
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 3 后再运行。")
        return False
    if out is not True:
        print("  ❌ 结果不对:(3.0, 5) 期望 True(3.0×1.2=3.6 ≤ 5),得到 %r。" % (out,))
        return False
    out2 = within_latency(4.5, 5)
    if out2 is not False:
        print("  ❌ 结果不对:(4.5, 5) 期望 False(4.5×1.2=5.4 > 5),得到 %r。" % (out2,))
        print("     纸面 4.5ms 看似达标,乘上 20% 安全余量就超了——这正是安全系数的意义。")
        return False
    print("  ✅ 通过!(3.0,5)→True;(4.5,5)→False——纸面达标不等于产线达标。")
    return True


def test_drift_alarm():
    print("测试 4: drift_alarm ...")
    out = drift_alarm(BASELINE, [0.18, 0.2, 0.19])
    if out is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 4 后再运行。")
        return False
    if out is not True:
        print("  ❌ 结果不对:基线均值 0.1、总体 std≈0.0129,报警线≈0.1387;")
        print("     近期均值 0.19 已越线,应返回 True,得到 %r。" % (out,))
        print("     检查:标准差是否用「除以 N」的总体标准差?")
        return False
    out2 = drift_alarm(BASELINE, [0.11, 0.1, 0.12])
    if out2 is not False:
        print("  ❌ 结果不对:近期均值 0.11 未越过报警线 ≈0.1387,应返回 False,得到 %r。" % (out2,))
        return False
    print("  ✅ 通过!均值 0.19 越过 0.1+3σ≈0.1387 → 报警;0.11 未越线 → 安静。")
    return True


def test_production_pipeline():
    print("测试 5: 产线决策链 ...")
    prereq = (recommend(False, False, 50, 300) is not None
              and best_f1_threshold(SCORES, LABELS) is not None)
    if not prereq:
        print("  ❌ 先完成 TODO 1 和 TODO 2,再来串决策链。")
        return False
    result = production_pipeline((False, False, 50, 300), SCORES, LABELS, [0.7, 0.2, 0.6])
    if result is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 5 后再运行。")
        return False
    if not isinstance(result, dict):
        print("  ❌ 返回类型不对:应返回 dict,得到 %r。" % type(result).__name__)
        return False
    method = result.get('method')
    thr = result.get('threshold')
    decisions = result.get('decisions')
    if method != 'patchcore':
        print("  ❌ method 不对:cfg=(False,False,50,300) 应选 'patchcore'(默认答案),")
        print("     得到 %r。检查是否用 recommend(*cfg) 解包。" % (method,))
        return False
    if thr != 0.55:
        print("  ❌ threshold 不对:期望 0.55(TODO 2 在验证集上的结果),得到 %r。" % (thr,))
        return False
    if decisions != [1, 0, 1]:
        print("  ❌ decisions 不对:分数 [0.7, 0.2, 0.6] 对阈值 0.55,")
        print("     期望 [1, 0, 1],得到 %r。注意 >= 阈值才报警。" % (decisions,))
        return False
    print("    产线决策:方法=%s,阈值=%s,本批判定=[%s]"
          % (method, thr, ",".join(str(d) for d in decisions)))
    print("  ✅ 通过!选型 → 定阈值 → 出判定,一条产线决策链完整跑通——")
    print("     这就是 §2-§4 在代码里的样子:方法是决策树选的,阈值是验证集定的,")
    print("     判定只是一次比较。上线之后,别忘了 TODO 4 的漂移报警要一直守着它。")
    return True


if __name__ == "__main__":
    print("=" * 52)
    print("第 13 课练习:把十三课装进一个决策引擎")
    print("=" * 52)
    all_passed = True
    all_passed = test_recommend() and all_passed
    all_passed = test_best_f1_threshold() and all_passed
    all_passed = test_within_latency() and all_passed
    all_passed = test_drift_alarm() and all_passed
    all_passed = test_production_pipeline() and all_passed
    print("-" * 52)
    if all_passed:
        print("🎉 全部通过!选型、阈值、时延、漂移、串联——")
        print("   一条产线的决策链你已经亲手写完。十三课到此收官:")
        print("   pip install anomalib,去真实数据上开工吧。")
    else:
        print("💪 还有测试没通过,按提示继续加油!")
