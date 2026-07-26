# -*- coding: utf-8 -*-
"""
============================================================
第 03 课练习:亲手搭一套训练方法论工具箱
============================================================

模型代码只是舞台,训练方法论才是导演。
这份练习用纯 Python(零依赖)把本课的五件工具各造一遍:

    数据划分 → 症状诊断 → 数据增强 → 早停 → 学习率调度

最后把早停和调度串起来,完成一次最小的"训练复盘":
给定一条 val loss 曲线,自动找出最佳 checkpoint
和它对应的学习率。

运行方式:  python exercise.py
完成所有 TODO 后,你应该看到所有测试通过

难度:⭐⭐
预计用时:25-40 分钟
"""

import random


# ============================================================
# 🧱 Part 1: 可复现的数据划分(对应课程 §2)
# ============================================================
#
# 训练开工的第一行代码:把数据切成 train / val / test 三份。
# 两条铁律:
#   ① 可复现——写死随机种子,任何人任何时候运行,划分都一样
#     (否则两次实验用的数据不同,成绩根本没法比较);
#   ② 无重叠——同一个样本只能属于一个集合。
#
# 注意:不要修改传入的 items 本身,先复制一份再打乱。
#

def train_val_test_split(items, ratios=(0.6, 0.2, 0.2), seed=42):
    """把 items 随机切成 (train, val, test) 三个列表。

    Args:
        items:  样本列表,如 [0, 1, 2, ..., 9]
        ratios: 三份的比例,加起来为 1
        seed:   随机种子,保证划分可复现

    Returns:
        (train, val, test) 三个列表组成的元组
    """
    # ======== TODO 1: 在这里写你的代码 ========
    # 提示:rng = random.Random(seed) 创建一个独立随机源;
    #       pool = list(items) 复制一份,再 rng.shuffle(pool) 打乱;
    #       n_train = int(len(pool) * ratios[0]);
    #       n_val   = int(len(pool) * ratios[1]);
    #       按下标切三段返回:
    #       pool[:n_train], pool[n_train:n_train+n_val], pool[n_train+n_val:]

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 1 ========


# ============================================================
# 🧱 Part 2: 症状诊断器(对应课程 §3)
# ============================================================
#
# 看 train / val 两个准确率,判断训练处于什么状态。
# 规则(按顺序判断):
#   train_acc < 0.7            → 'underfit'  训练集都学不好:容量不够或没训够
#   train_acc - val_acc > 0.1  → 'overfit'   训练好验证差:模型在背题
#   其余情况                    → 'ok'        两边都不错且接近:健康
#

def diagnose(train_acc, val_acc):
    """根据训练/验证准确率返回 'underfit' / 'overfit' / 'ok'。"""
    # ======== TODO 2: 在这里写你的代码 ========
    # 提示:两个 if 一个 return,注意判断顺序:先欠拟合,再过拟合。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 2 ========


# ============================================================
# 🧱 Part 3: 两个数据增强算子(对应课程 §5)
# ============================================================
#
# 图像用"列表的列表"表示(行优先),和第 02 课练习一样。
# 水平翻转:每一行左右反转;
# 顺时针旋转 90°:新图第 r 行 = 原图第 r 列自下而上取值,
#   即 new[r][c] = old[H-1-c][r](H×W 的图旋转后变 W×H)。
#
# 这两个变换都不改变"图里有没有缺陷"——所以是合法增强。
#

def flip_horizontal(image):
    """水平翻转:每行反转。[[1,2],[3,4]] → [[2,1],[4,3]]"""
    # ======== TODO 3a: 在这里写你的代码 ========
    # 提示:一行列表推导式,row[::-1] 反转一行。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 3a ========


def rotate90(image):
    """顺时针旋转 90°。[[1,2],[3,4]] → [[3,1],[4,2]]"""
    # ======== TODO 3b: 在这里写你的代码 ========
    # 提示:H = len(image),W = len(image[0]),
    #       返回 [[image[H-1-c][r] for c in range(H)] for r in range(W)]。
    #       自己在纸上画一个 2×2 验证一下下标。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 3b ========


# ============================================================
# 🧱 Part 4: 早停(对应课程 §4)
# ============================================================
#
# 每个 epoch 结束看一眼 val loss:
#   刷新了历史最低 → 记下这个 epoch,耐心计数清零;
#   没刷新        → 耐心计数 +1;计数达到 patience 时就地停止。
#
# 例:val_losses = [1.0, 0.8, 0.7, 0.72, 0.71, 0.75], patience=2
#   epoch 0-2 一路刷新最低(best=2);
#   epoch 3 没刷新(计数 1),epoch 4 又没刷新(计数 2)→ 在 epoch 4 停;
#   返回 (best_epoch=2, stop_epoch=4)。
# 若直到最后都没触发,stop_epoch 就是最后一个 epoch 的下标。
#

def early_stopping(val_losses, patience):
    """模拟早停。

    Args:
        val_losses: 每个 epoch 的验证损失列表(下标即 epoch)
        patience:   连续多少个 epoch 未刷新最优就停

    Returns:
        (best_epoch, stop_epoch):最优 epoch 下标、实际停止的 epoch 下标
    """
    # ======== TODO 4: 在这里写你的代码 ========
    # 提示:best = val_losses[0],best_epoch = 0,bad = 0;
    #       从 epoch 1 开始遍历:
    #         损失 < best → 更新 best / best_epoch,bad 清零;
    #         否则 bad += 1,bad 达到 patience 时 return (best_epoch, 当前下标);
    #       循环走完没触发,return (best_epoch, len(val_losses) - 1)。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 4 ========


# ============================================================
# 🧱 Part 5: 学习率调度 + 训练复盘(对应课程 §6)
# ============================================================
#
# 阶梯衰减(step decay):每过 drop_every 个 epoch,学习率乘一次 factor:
#
#     lr(epoch) = base_lr × factor ** (epoch // drop_every)
#
# 例:base_lr=0.1, drop_every=3, factor=0.1 时,
#     epoch 0-2 → 0.1,epoch 3-5 → 0.01,epoch 6-8 → 0.001 ...
#
# 然后串联:拿一条训练留下的 val loss 曲线,用早停找出最佳
# epoch,再用调度公式算出"那一刻模型用的学习率是多少"——
# 一次最小的训练复盘。
#

VAL_LOSSES = [1.0, 0.8, 0.7, 0.72, 0.71, 0.75]  # 一条示例 val loss 曲线


def step_decay(epoch, base_lr, drop_every, factor):
    """按阶梯衰减公式返回第 epoch 个 epoch 的学习率。"""
    # ======== TODO 5a: 在这里写你的代码 ========
    # 提示:一行,注意用 // 做整除。

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 5a ========


def schedule_at_best(val_losses, patience, base_lr, drop_every, factor):
    """训练复盘:早停选出最佳 epoch,并算出该 epoch 的学习率。

    Returns:
        (best_epoch, lr):最佳 epoch 下标,以及那一刻的学习率
    """
    # ======== TODO 5b: 在这里写你的代码 ========
    # 提示:两行——
    #       best_epoch, _ = early_stopping(val_losses, patience)
    #       return best_epoch, step_decay(best_epoch, base_lr, drop_every, factor)

    pass  # ← 删掉这行,写你的实现

    # ======== END TODO 5b ========


# ============================================================
# 🧪 测试
# ============================================================

def test_split():
    print("测试 1: train_val_test_split ...")
    items = list(range(10))
    result = train_val_test_split(items)
    if result is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 1 后再运行。")
        return False
    tr, va, te = result
    if items != list(range(10)):
        print("  ❌ 原列表 items 被修改了!提示:先 list(items) 复制一份再 shuffle。")
        return False
    if not (len(tr) == 6 and len(va) == 2 and len(te) == 2):
        print("  ❌ 长度不对:期望 6/2/2,得到 %d/%d/%d。检查 int(len*ratio) 与切片边界。"
              % (len(tr), len(va), len(te)))
        return False
    if set(tr) & set(va) or set(tr) & set(te) or set(va) & set(te):
        print("  ❌ 三份之间有重叠!同一个样本只能属于一个集合(§2 的铁律)。")
        return False
    if set(tr) | set(va) | set(te) != set(items):
        print("  ❌ 并集不等于全集:有样本被弄丢了。检查最后一段切片。")
        return False
    tr2, va2, te2 = train_val_test_split(list(range(10)))
    if (tr, va, te) != (tr2, va2, te2):
        print("  ❌ 两次调用结果不同:划分必须可复现(用 random.Random(seed))。")
        return False
    if tr == [0, 1, 2, 3, 4, 5]:
        print("  ❌ 划分看起来没有打乱:train 恰好是前 6 个。检查是否调用了 shuffle。")
        return False
    print("  ✅ 通过!6/2/2、无重叠、并集=全集,且两次运行结果一致。")
    return True


def test_diagnose():
    print("测试 2: diagnose ...")
    r1 = diagnose(0.99, 0.70)
    if r1 is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 2 后再运行。")
        return False
    r2 = diagnose(0.55, 0.53)
    r3 = diagnose(0.92, 0.90)
    if r1 == 'overfit' and r2 == 'underfit' and r3 == 'ok':
        print("  ✅ 通过!(0.99,0.70)→overfit、(0.55,0.53)→underfit、(0.92,0.90)→ok。")
        return True
    print("  ❌ 结果不对:期望 overfit/underfit/ok,得到 %r/%r/%r。" % (r1, r2, r3))
    print("     检查规则顺序:先判 train_acc < 0.7,再判 train_acc - val_acc > 0.1。")
    return False


def test_augment():
    print("测试 3: flip_horizontal / rotate90 ...")
    f = flip_horizontal([[1, 2], [3, 4]])
    if f is None:
        print("  ❌ flip_horizontal 还没实现(返回了 None)。完成 TODO 3a 后再运行。")
        return False
    if f != [[2, 1], [4, 3]]:
        print("  ❌ flip_horizontal 不对:期望 [[2,1],[4,3]],得到 %r。提示:每行 row[::-1]。" % f)
        return False
    r = rotate90([[1, 2], [3, 4]])
    if r is None:
        print("  ❌ rotate90 还没实现(返回了 None)。完成 TODO 3b 后再运行。")
        return False
    if r != [[3, 1], [4, 2]]:
        print("  ❌ rotate90 不对:期望 [[3,1],[4,2]],得到 %r。" % r)
        print("     顺时针 90°:new[r][c] = old[H-1-c][r],在纸上画 2×2 验证下标。")
        return False
    r2 = rotate90([[1, 2, 3], [4, 5, 6]])
    if r2 != [[4, 1], [5, 2], [6, 3]]:
        print("  ❌ 非方阵情况不对:2×3 旋转后应为 3×2 的 [[4,1],[5,2],[6,3]],得到 %r。" % r2)
        print("     检查 H、W 有没有用反:新图有 W 行、每行 H 个。")
        return False
    print("  ✅ 通过!翻转与旋转都正确——两行代码,一张图免费变四张。")
    return True


def test_early_stopping():
    print("测试 4: early_stopping ...")
    result = early_stopping([1.0, 0.8, 0.7, 0.72, 0.71, 0.75], 2)
    if result is None:
        print("  ❌ 还没实现(返回了 None)。完成 TODO 4 后再运行。")
        return False
    best, stop = result
    if (best, stop) != (2, 4):
        print("  ❌ 结果不对:期望 (2, 4),得到 (%r, %r)。" % (best, stop))
        print("     最优是 epoch 2 的 0.7;epoch 3、4 连续两次没刷新 → 在 epoch 4 停。")
        return False
    result2 = early_stopping([0.9, 0.8, 0.7], 5)
    if result2 != (2, 2):
        print("  ❌ 未触发早停的情况不对:一路下降时应返回 (2, 2)(最后一个 epoch),得到 %r。" % (result2,))
        return False
    print("  ✅ 通过!和课程 §4 的规则一致:best=2,连续 2 次未刷新在 epoch 4 停。")
    return True


def test_schedule():
    print("测试 5: step_decay 与训练复盘 ...")
    lr = step_decay(7, 0.1, 3, 0.1)
    if lr is None:
        print("  ❌ step_decay 还没实现(返回了 None)。完成 TODO 5a 后再运行。")
        return False
    if abs(lr - 0.001) >= 1e-9:
        print("  ❌ step_decay(7, 0.1, 3, 0.1) 应为 0.001,得到 %r。" % lr)
        print("     公式:0.1 × 0.1 ** (7 // 3) = 0.1 × 0.01 = 0.001,注意整除。")
        return False
    prereq = early_stopping([1.0, 0.9, 0.95], 1) is not None
    if not prereq:
        print("  ❌ 先完成 TODO 4(early_stopping),再来串联训练复盘。")
        return False
    recap = schedule_at_best(VAL_LOSSES, 2, 0.1, 3, 0.1)
    if recap is None:
        print("  ❌ schedule_at_best 还没实现(返回了 None)。完成 TODO 5b 后再运行。")
        return False
    best, best_lr = recap
    print("    复盘:val 最优出现在 epoch %s,那一刻的学习率是 %s" % (best, best_lr))
    if best == 2 and abs(best_lr - 0.1) < 1e-9:
        print("  ✅ 通过!早停选出 epoch 2 的 checkpoint,当时 lr 还停在初始值 0.1。")
        return True
    print("  ❌ 结果不对:期望 (2, 0.1),得到 (%r, %r)。" % (best, best_lr))
    print("     检查:early_stopping 返回的是 (best_epoch, stop_epoch),复盘用的是前者。")
    return False


if __name__ == "__main__":
    print("=" * 52)
    print("第 03 课练习:亲手搭一套训练方法论工具箱")
    print("=" * 52)
    all_passed = True
    all_passed = test_split() and all_passed
    all_passed = test_diagnose() and all_passed
    all_passed = test_augment() and all_passed
    all_passed = test_early_stopping() and all_passed
    all_passed = test_schedule() and all_passed
    print("-" * 52)
    if all_passed:
        print("🎉 全部通过!这套工具箱会陪你走完后面每一课的训练。下一课见。")
    else:
        print("💪 还有测试没通过,按提示继续加油!")
