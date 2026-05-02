# LogCrew — Multi-Agent Log Triage System

一个基于多 Agent 协作的分布式日志排障系统，用于压缩微服务场景下的故障定位时间。

## 核心痛点

- 微服务日志分散在 ELK / Grafana / 各服务本地，排查需跨系统切换
- 已知问题重复消耗工程师时间，MTTR 平均 25 分钟以上
- 新成员缺乏历史故障上下文，上手慢

## 架构与核心逻辑流

采用长链推理（Long-Chain Reasoning）+ 多 Agent 协作架构：

1. **采集 Agent（Collector）**
   通过统一日志网关实时拉取各服务结构化日志，按 trace_id 做上下文关联。

2. **模式识别 Agent（Classifier）**
   对异常日志进行向量化聚类，比对历史故障库。已知问题直接返回历史修复方案，走短链快速响应。

3. **根因分析 Agent（Analyzer）**
   未知异常场景下启动长链推理。依次调用服务拓扑、近期发布记录、依赖健康状态等多维工具，通过 Chain-of-Thought 逐步缩小故障范围，输出带置信度的根因假设。

4. **修复建议 Agent（Remediator）**
   根据根因结果自动生成修复命令或代码补丁，通过 GitHub API 创建 Hotfix PR，并推送告警摘要到飞书。

## 技术栈

- 开发工具：Claude Code / Aider
- 底层模型：Claude 系列（复杂推理）、MiMo 系列（轻量任务，接入中）
- 日志网关：Vector + Kafka
- 向量检索：Qdrant

## 落地情况

目前在某后端小组（12 人）试运行，每日处理约 200 次异常日志分析，常规故障排查效率提升约 80%。
