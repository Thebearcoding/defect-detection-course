# 缺陷检测:从深度学习基础到主流方法全景

一套 **13 课的中文交互式课程**,从神经网络零基础讲起,原子粒度拆解工业缺陷检测的所有主流方法族。

**在线阅读:https://athebear.me/defect-detection-course/(备用:https://thebearcoding.github.io/defect-detection-course/)**

## 课程结构

| Part | 课次 | 内容 |
|------|------|------|
| 深度学习地基 | 01-03 | 神经网络、CNN、训练方法论 |
| 问题与有监督路线 | 04-06 | 全景地图与指标、目标检测、语义分割 |
| 无监督五大方法族 | 07-11 | 重构、特征嵌入(PaDiM/PatchCore)、师生蒸馏、合成缺陷、归一化流 |
| 前沿与实践 | 12-13 | CLIP 零样本、anomalib 工程落地与选型 |

## 特点

- **30+ 交互演示**:手动训练神经元、卷积滑动步进、NMS 去重、PatchCore 查库打分、分布变形动画……
- **零依赖练习**:每课一个 `exercise.py`(纯 Python,`python3 exercise.py` 即可运行),5 个递进 TODO + 自动测试
- **40+ 篇原始论文**:每课延伸阅读挂对应方向的奠基论文(arXiv 链接均经验证)
- **划线笔记**:选中文字可提问 LLM / 请求修改 / 荧光笔划重点(本地存储)
- **移动端适配**:手机随时随地学习

## 本地使用

直接用浏览器打开 `index.html`,或:

```bash
python3 -m http.server 8000
# 访问 http://localhost:8000
```

---

课程由 [Claude](https://claude.com/claude-code) 生成,视觉风格基于 Anthropic 设计语言。
