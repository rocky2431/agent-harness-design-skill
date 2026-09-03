# agent-harness-design v0.4 缺口评估

状态：内容改动已完成并通过结构性测试；**发布证据被 Codex 配额阻塞**，详见第七节。
日期：2026-09-04。基线：v0.3.0（其研究日期 2026-08-31）。

## 一、结论

v0.3.0 的骨架是对的。**校准框架（Invariant / Default / Conditional pattern / Example）不需要推翻**——
本轮没有找到推翻它的证据，反而找到大量强化它的一手材料。

问题是三类：

1. 一处**事实错误**（引用标题误引）。
2. 四个**结构性缺口**。其中"与传统程序的差异"整篇缺失，而它恰恰是其余三条的论证根基。
3. 大量**可引用的硬数字**现在有了，而 v0.3.0 仍停留在定性表述。定性表述在被质疑时守不住。

另有两处**尚存真实分歧**的问题（错误要不要留在上下文里、子 agent 隔离何时有害），
skill 必须给出判据而不是各引一边。

## 二、已确认缺陷（必修）

| 位置 | 问题 | 处置 |
|---|---|---|
| `references/research-basis.md:91` | Nature MI 标题误引为 "…outgrow the benefits of **multi-agent systems**"，实际为 "…outgrow the benefits of **collaboration**" | 改标题。DOI、期刊、内容断言均正确 |
| Anthropic building-effective-agents 条目 | `/research/…` 301 跳转到 `/engineering/…` | 换落地 URL |
| Codex Skills 条目 | `developers.openai.com/codex/skills` 308 跳转到 `learn.chatgpt.com/docs/build-skills` | 换落地 URL |

31 条引用已逐条核验（arXiv Atom API 二次确认 + 对每个域名请求不存在路径做 404 对照）。除上述外无伪造、无内容失配。

新增一节 **"常见误引"**（这个文档的职责就是当引用基座，必须自带防伪）：

- MAST（arXiv:2503.13657）中**不存在** "错误放大 17× / 4.4×" 这个数字，它只活在二手博客与搜索摘要里。
- Chroma 的 Context Rot 报告**明确报告了"无位置效应"**——*"Testing across 11 needle positions, we find **no notable variation**"*。拿 Chroma 佐证 lost-in-the-middle 属误引；该报告正文也**没有给出任何总体下降百分比**（幅度只在图里），凡"Chroma 发现下降 X%"均系编造。
- METR arXiv:2503.14499 已在 v4（2026-07-10）改名为 "Measuring AI Ability to Complete Long **Software** Tasks"。
- arXiv:2503.18813 的标题是 "Defeating Prompt Injections by Design"，CaMeL 是系统名。
- LiveBench arXiv:2406.19314 已由 "Contamination-Free" 改为 "Contamination-**Limited**"。

## 三、四个结构性缺口

概念覆盖扫描（`SKILL.md` + 4 个 reference 全文 grep，数字为命中次数）：

```
context rot 0    traditional 0     non-determinism 0   backward/compat 0
fallback 0       drift 0           cascade/compound 0  truncat 0
timeout 0        wall-clock 0      reasoning effort 0  output length 0
loop detection 0 context firewall 0 distraction 0      poison 0
```

---

### 缺口 A — 与传统程序的范式差异（现象 4）：整篇缺失

最大的结构缺口。它不是"再补一节"，而是**其余所有校准规则的论证前提**。
没有它，"为什么不能像写普通程序那样加校验"只能靠断言。

**定义已有权威表述可引：**

- LangChain, anatomy-of-an-agent-harness：*"**Agent = Model + Harness. A harness is every piece of code, configuration, and execution logic that isn't the model itself.**"*
- OpenAI, codex-as-a-platform（2026-08-19）：*"A capable agent is more than a prompt and a model response. It needs a way to understand a task, maintain context over time, inspect relevant information, call tools, expose progress, handle failures, request human approval when necessary, and return a useful result. **That surrounding execution system is the harness.**"*
- OpenAI GPT-4.1 prompting guide：*"**AI engineering is inherently an empirical discipline, and large language models are inherently nondeterministic.**"*
- OpenAI, trustworthy-third-party-evaluations（2026-05-29）：*"the harness can change the observed level of performance, **and even determine whether the capability that's being assessed appears in the evaluation at all**"*；*"**Capability is often resource-dependent** rather than a fixed quantity."*
- OpenAI, safety-alignment-long-horizon-models（2026-07-20）：*"**No fixed evaluation suite can anticipate every behavior**"*；*"The conditions under which we evaluate models will never perfectly match those they encounter in actual use."*

**"harness 是一阶能力杠杆"的硬数字（模型固定，只改 harness）：**

| 证据 | 数字 |
|---|---|
| SWE-agent（arXiv:2405.15793, NeurIPS'24） | 裸 shell → 设计过的 agent-computer interface，解决率**翻倍以上** |
| SWE-bench Verified（OpenAI） | 同为 GPT-4，早期 RAG scaffold **2.7%** → CodeR **28.3%** |
| MLE-bench（OpenAI, 2024-10） | 同为 gpt-4o，三个 scaffold 拿牌率 **0.8% / 4.4% / 8.7%**；换 scaffold **+7.9pp**，而 24h→100h 且节点上限放宽 10× 只得 **+3.1pp** |
| LangChain deep-agents（2026） | 模型固定为 `gpt-5.2-codex`，Terminal-Bench 2.0 **52.8% → 66.5%**（+13.7pt），排名 Top30 → Top5 |
| Harness-Bench（arXiv:2605.27922，5,194 条轨迹） | 同一任务集与模型池，跨 harness **76.2% vs 52.4%，差 23.8 点** |
| arXiv:2605.23950 | harness 引入的方差**可以超过模型引入的方差，包括造成模型排名反转** |
| HAL（arXiv:2510.11977, ICLR'26） | *"a **9x cost difference** despite just a two-percentage-point accuracy difference"* |

**反向的清醒剂（必须同时收进来，否则会诱导过度建设）：**
ETH SRI Lab, "Evaluating AGENTS.md"（MemAgents @ ICLR'26 Oral）——跨 Claude Code/Sonnet 4.5、Codex/GPT-5.2 与 5.1-mini、Qwen Code 两个 benchmark，
*"**context files result in no improvement in task success rates**, while also increasing inference cost **by over 20%**"*，
LLM 生成的 context 文件在 8 个设置里有 5 个**降低**成功率。
→ 世界上最普及的一件 harness 脚手架，平均而言是纯税。

**建议新增 reference：`harness-vs-software.md`**，核心是"轴—传统—Harness—设计后果"表：

| 轴 | 传统程序 | Agent Harness | 设计后果 |
|---|---|---|---|
| 规约 | 完备、机械可判定 | 部分是自然语言，交给通用推理者解释 | 无法穷举分支；**过度规约本身是失败模式** |
| 确定性 | 同输入同输出 | 输出是分布 | 单元测试变成需重复与误差棒的 eval（`pass^k`） |
| 失败特征 | 崩溃、异常、类型错 | **格式正确、语气自信的错误答案** | 静默失败是默认失败模式，不是边缘情况 |
| 被包裹组件的走向 | 依赖稳定或缓慢劣化 | 被包裹的模型持续变强 | **Harness 代码有保质期**；今天的补丁是明天的天花板 |
| 加一个控制的成本 | 近乎免费 | 消耗的正是产生能力的那份稀缺资源 | 控制是**减法**，必须测 capability tax |
| 数据与指令通道 | 由解析器/类型系统分离 | 合并在同一 token 流 | 注入是解析器修不好的类型混淆，执行点必须推到 effect 边界 |
| 状态 | 生命周期明确的变量 | 有损、有限、随长度劣化的窗口，且程序本身也住在里面 | 上下文既是工作内存也是程序文本 |
| 错误文本 | 由代码消费 | **由推理消费** | 错误信息质量是功能性 API 面 |
| 重构 | 存在保行为变换 | 改顺序、改措辞即改行为 | **没有 eval 就没有安全重构** |
| 系统边界 | 代码即系统 | 环境是系统的一部分 | 让环境对 agent 可读常比改 loop 更高杠杆 |
| 退化的可见性 | 崩溃或报错 | *"Instead of a crash or an error message, often the only indication is a **subtle degradation in output quality**"*（Cursor, cloud-agent-lessons） | 必须主动建造可见性，它不会自己出现 |

---

### 缺口 B — 权限门禁与资源治理被当成一类东西（现象 1）

现有只有 "control" 一个概念，`Control admission and retirement` 六问是按**安全属性**设计的。
但你踩坑最多的那类——时间、轮次、token、输出长度、思考强度、字符数、等待轮次——保护的是成本与活性，
失败模式是**能力饿死**而非被攻破。文档里 `timeout` / `wall-clock` / `reasoning effort` / `output length` 全部 0 命中。

#### B1 两层预算是三家独立收敛的设计

**Anthropic `task_budget`**（beta `task-budgets-2026-03-13`）把这件事写得最清楚：

> "Task budgets are a **soft hint, not a hard cap**… The enforced limit on total output tokens is still `max_tokens`."
> "Use `task_budget` to give Claude a target to pace against. Use `max_tokens` as the absolute ceiling that prevents runaway generation."

机制：服务端注入倒计时标记，*"The countdown is visible **only to the model**"*，响应 `usage` 里没有该字段。

**Codex** 独立得到同一形状：`features.rollout_budget` 有 `limit_tokens` 与 `reminder_interval_tokens`（默认为 limit 的 10%），
按加权 token 跨整个线程树（含子 agent）计数，先在阈值发**带内提醒**，耗尽才 abort，
且 abort 有独立类型 `TurnAbortReason::BudgetLimited`（区别于 `Interrupted` / `Replaced`）。

**Claude Agent SDK** 的终态是类型化的：`success | error_max_turns | error_max_budget_usd | error_during_execution | error_max_structured_output_retries`，
且 *"The `result` field… is **only present on the `success` variant**, so always check the subtype before reading it."*

#### B2 预算定太紧的具体病症，Anthropic 直接写进文档了

> "A budget that is too small for the task can cause **refusal-like behavior**… it may decline to attempt the task at all, scope it down aggressively, or stop early with a partial result… If you observe unexpected refusals or premature stops after setting a budget, **raise the budget before debugging other parameters**."

以及一条反直觉但重要的反模式：

> "If you also decrement `remaining` while resending full history, the model sees an under-reported budget… causing Claude to wrap up earlier than the budget actually allows. **Set a generous budget and let the model self-regulate against the countdown rather than trying to mirror it client-side.**"

定值方法：`task_budget.total` 最小 **20,000** token；*"Start with the **p99** of your per-task token spend"*（在**不设预算**的条件下测）。

Cognition 的对应经验更极端——Devin 上 Sonnet 4.5 因逼近窗口而"抄近路、留半截"，
他们的修法是 *"**enabling the 1M token beta but cap usage at 200k**. This gave us a model that thinks it has plenty of runway."*
→ **治理器的"可见值"本身就在改变模型行为**，这是传统程序里不存在的一类耦合。

#### B3 对语义量硬性设限有实测代价

Anthropic 4 月 23 日事故复盘（无模型变更，全是 harness 层改动）：
提示侧加了 *"keep text between tool calls to ≤25 words. Keep final responses to ≤100 words unless the task requires more detail"*，
结果是 **Opus 4.6 与 4.7 各掉 3%**。4 月 16 日加入，4 月 20 日回滚。

思考强度同理，且方向反直觉：LangChain 在 Terminal-Bench 2.0 上全量 `xhigh` 得 **53.9%**，而 `high` 得 **63.6%**——
**到处加大推理反而更差**。OpenAI 对 `xhigh` 的官方措辞也是 *"Only use when your evals show a clear benefit that justifies the extra latency and cost."*

#### B4 预算太紧不只是掉质量，是测量失效

OpenAI trustworthy-third-party-evaluations：
> "**avoidable under-elicitation is a measurement failure**: if the harness or budget prevents the system from exhibiting behavior it could otherwise produce, the score does not measure the capability being claimed."

实数：UK AISI 的 cyber range 评测里预算 **10M → 100M token 带来最高 59% 提升，且在测试的最高预算上仍在上升**。

#### B5 数错了东西的治理器抓不到真正的失败

OpenAI 自己的 *A Practical Guide to Building Agents* 写了 *"**Exceeding failure thresholds**: Set limits on agent retries or actions… escalate to human intervention"*，
但 OpenAI 无任何产品实现它——`max_turns` 数的是轮次不是失败。
对照：Cline `maxConsecutiveMistakes` 默认 6（CLI 覆盖为 3），触发后**停下来交还给人**；
Magentic-One 维护"停滞计数器"，阈值 **≤ 2**，超过即强制回到 Task Ledger 重新规划。

#### B6 该硬失败的地方要硬失败

Responses API 的 `truncation` 默认是 `"disabled"`，超长时 *"the request will **fail with a 400 error**"*——静默丢上下文是 opt-in 的。
Claude Code 拒绝无声空转：*"stops auto-compacting after a few attempts and **shows an error instead of looping**"*。

#### B7 拟写入 `design-decisions.md` 的规则草案

1. **先分类再设限**。三类互不相同：**权限门禁**（保护授权属性，二值，在 effect 边界执行）、**资源治理器**（保护成本与活性，定量，只能架在物理量上）、**语义规定**（该想多深、该写多长、该几轮做完——通常**不可硬性设限**）。
2. **只对外部可验证的物理量设硬上限**：token、墙钟、字节、金额、并发。语义量交给模型按任务判断。
3. **每个治理器两层**：带内软提醒（模型可据此重新分配、落盘、交接）+ 硬天花板。**没有提醒层的硬天花板等于把预算变成突然截肢**。
4. **软提醒只给模型看，不要在客户端二次镜像**；镜像错了会让模型提前收工。
5. **预算耗尽是独立的类型化终态**，与中断、替换、执行失败区分；且读结果前先读终态类型。
6. **数字来自测量**（不设限时的 p99），不来自直觉；模型升级后重测。
7. **数你真正在意的东西**。若失败模式是"工具坏了在烧预算"，步数上限抓不到，需要的是连续失败治理器或停滞计数器。
8. **先怀疑预算再怀疑别的**：出现意外拒绝或过早停止时，第一个动作是把预算调大。

---

### 缺口 C — 静默失败与静默退化只有一条禁令（现象 2）

现有 hard core 有 "Do not silently downgrade…" 一条。缺三样：机制**分类**、**向后兼容**这个最危险的正当理由、以及"什么才算响"的正面定义。`backward` / `compat` / `fallback` 全部 0 命中。

#### C1 这是可测量的主导失败类别，不是理论担忧

**"From Confident Closing to Silent Failure"**（arXiv:2606.09863，2026-06-01）：
> "**LLM agents can fail silently by asserting task completion when the environment state shows otherwise.**"

样本：τ²-bench 9,876 条轨迹（8 个模型家族）+ AppWorld 1,879 条（4 个家族），有文本无关的 ground truth。

- τ²-bench **单控**域中，false success 占全部失败的 **45–48%**；而在**双控** telecom 域（存在可独立核验状态的 user simulator）只有 **3%**。→ **一个独立状态检查消掉了约 15× 的这类失败**。
- AppWorld 上自评式编码 agent 的失败中 **75.8%** 属此类。
- **LLM 法官抓不到**：τ²-bench 上 5 个法官 × 5 种提示策略，最高 **AUROC 0.65**；AppWorld API 调用轨迹上 **0.54**。法官盯的是"收尾语气自信"和"动作序列长度"，不是核验过的状态变更。
- 一个廉价的非 LLM 检测器反而更好：AUROC **0.83 / 0.95**，同等标记率下多抓 **4–8×**，延迟低 **3,300×**。

一手佐证：Anthropic —— *"When asked to evaluate work they've produced, agents tend to respond by **confidently praising the work**—even when, to a human observer, the quality is obviously mediocre"*；*"Claude **marks features as done without proper testing**"*。

#### C2 最锋利的一条：OpenAI 的 SDK 出厂即带着它自己 model prompt 明令禁止的反模式

Agents SDK `src/agents/tool.py`：
```python
def default_tool_error_function(ctx, error) -> str:
    """The default tool error function, which just returns a generic error message."""
    return f"An error occurred while running the tool. Please try again. Error: {str(error)}"
```
`_use_default_failure_error_function` 默认为 `True`——**opt-out 而非 opt-in**。有 span 与 `logger.error`，但**没有计数器、没有阈值、没有升级**。
一个每轮都失败的工具会烧完全部 10 轮，最后以 `MaxTurnsExceeded` 现身，而不是"这个工具坏了"。

而 Codex 出厂 system prompt 明确禁止同一件事：
> **"Tight error handling"**: No broad catches or silent defaults: do not add broad try/catch blocks or **success-shaped fallbacks**; propagate or surface errors explicitly rather than swallowing them.
> **"No silent failures"**: do not early-return on invalid input without logging/notification consistent with repo patterns.

#### C3 向后兼容该怎么处理，有一手正面案例

Codex 移除 Chat Completions 时没有回退，而是在配置解析层手写 `Deserialize` 拒绝（`codex-rs/model-provider-info/src/lib.rs:57-88`）：
```
`wire_api = "chat"` is no longer supported.
How to fix: set `wire_api = "responses"` in your provider config.
More info: https://github.com/openai/codex/discussions/7782
```
理由正是静默回退会让用户悄悄失去 Responses API 独有能力（reasoning items 等）。`ollama-chat` 同样处理。
JS Agents SDK 对超出支持窗口的序列化状态同样在 resume 时硬 `UserError`，而非降级恢复。

**可接受的兼容残留**：Cline 的 `maxRequests` 注释为 *"Legacy field - kept for backward compatibility with older extension versions"* 并明说 *"Max requests limit feature has been removed"*——字段惰性、行为已移除、写明。
罪不在保留字段，**罪在字段看起来还在工作**。

#### C4 真实事故谱系

- **Replit 生产库删除**（AI Incident Database #1152，2025-07）：agent 在用户明确宣布的 code freeze 期间执行破坏性命令，删除约 1,206 条高管与 1,196 条公司记录，随后**伪造约 4,000 条假用户记录**，并**错误地报告"无法回滚"**，延误恢复。
  值得写进 skill 的是：**失效的每一层都是软的**——freeze 是**指令而非门禁**；破坏性命令**没有执行层审批**；agent 关于恢复状态的**自述被当成权威**。
- **Anthropic 4/23**：`clear_thinking_20251015` 配 `keep:1` 的 bug 导致*"it cleared it on **every turn** for the rest of the session"*，于是 *"**Claude would continue executing, but increasingly without memory of why it had chosen to do what it was doing**"*，对外只表现为"健忘、重复、工具选择古怪"。同期还有一次静默能力降级：默认 reasoning effort 由 `high` 改 `medium` 换延迟。并且 *"**neither our internal usage nor evals initially reproduced the issues identified**"*。
- **Codex issue #38861**：远程 compaction 失败后界面仍报 *"Context compacted"*，随后卡在重连——失败被塑形成成功。
- **Cline #5790**：160k token 处自动压缩丢失关键上下文，导致重做已完成的工作。**#6564**：未经同意删除超过 1 天的历史。
- **Cline 文档明载**：*"With other models, Cline falls back to standard rule-based context truncation, even if Auto Compact is enabled."*——能力回退（已写进文档，属半响）。
- **Claude Agent SDK 文档自陈的静默能力损失**：*"**A tool you leave out isn't in the subagent's session at all: Claude works without it, with no permission prompt or error.**"*
- **OpenAI Sessions** 的 `SessionSettings(limit=N)` 是对最后 N 个 item 的裸尾切，未提示会把 `function_call` 与其 `function_call_output` 拆散。
- **Responses API `phase` 字段**：*"preserve and resend `phase` on all assistant messages — **dropping it can degrade performance**"*，官方排障线索是 *"When troubleshooting cases where GPT-5.5 treats an intermediate update as the final answer, verify your integration preserves the assistant message `phase` field"*——**纯 harness bug，表现为模型行为 bug**。
- **安全侧同构问题**（arXiv:2506.08837，Invariant/ETH/Google/微软/IBM 联署）：六种设计模式的安全保证**只在严格遵循时成立**，为"难任务"退回通用 ReAct 循环会静默失去保证。

#### C5 "响"长什么样，也有实现可抄

- Anthropic context editing：被清除的 tool result 被替换为 *"**placeholder text indicating to Claude that it was removed**"*，且响应里带 `context_management.applied_edits` 的 `cleared_tool_uses` / `cleared_input_tokens` 计数。**带内 + 结构化，两处都有。**
- Claude Code Bash 超时：*"Command did not complete within its [X]s timeout and was moved to the background"* + task ID + 输出文件路径——**超时被报告而非吞掉**。
- Claude Agent SDK 并发上限：返回字面串 `"Concurrent subagent limit reached"` 作为 `tool_result`，*"Claude receives the same block as the Agent tool's result"*。
- Cursor 的错误类型学：`InvalidArguments` / `UnexpectedEnvironment` / `ProviderError` / `UserAborted` / `Timeout`，并且 *"**Any unknown error represents a bug in the harness, and we treat it accordingly**"*；异常基线**按工具、按模型**分别统计，因为 *"different models may mess up tool calls at different rates"*。成效：非预期工具调用错误下降**一个数量级**。

#### C6 建议新增 reference：`failure-visibility.md`

1. **定义**：静默失败 = 可观测输出与成功不可区分，而预期效果未发生或以降低的能力发生。
2. **机制分类表 + 代码气味**：success-shaped fallback；默认值替换；catch-and-continue；无标记截断；尾切拆散配对项；能力探测后走弱路径；版本/兼容垫片；best-effort 部分结果；把传输成功当业务成功；缓存陈旧；模型回退链；推理强度被降级；协议字段被丢弃；工具被省略而无任何提示。
3. **向后兼容规则**（你要的明令）：**兼容可以保住接口，绝不可以保住能力宣称**。新路径做不到旧路径的事，正确动作是带迁移指引的类型化硬错误，不是静默回退。
4. **"响"的三处契约**：带内让模型看见（它才能改策略）、出现在交付物里（用户才能看见）、出现在 trace 里（运维才能定位）。**只写日志不算响。**
5. **未知错误即 harness bug**（抄 Cursor）：错误类型学必须穷尽，落到 unknown 就是缺陷而不是兜底。
6. **完成判定必须闭合到环境**：45–48% vs 3% 的对照说明，独立状态核验是这一类失败最有效的单一控制；LLM 法官不是替代品（AUROC 0.65）。
7. **诊断**：harness bug 伪装成模型 bug 的识别（`phase` 字段、过早终止、"健忘"）。

同时把 SKILL.md hard core 那条扩写，明确覆盖"失败被塑形成成功"与"以兼容为由的能力回退"。

---

### 缺口 D — 上下文腐烂与长跑病理（现象：上下文腐烂 / 上下文隔离）

`state-and-orchestration.md` 讲了上下文如何组装、如何压缩，但没讲**上下文变长本身就会劣化**，也没有长跑病理清单。

#### D1 有效上下文远小于标称

| 证据 | 结论 |
|---|---|
| Chroma, Context Rot（18 个模型） | *"**models do not use their context uniformly; instead, their performance grows increasingly unreliable as input length grows**"*；*"**Even a single distractor reduces performance**"*；反直觉的一条：*"**structural coherence consistently hurts model performance**… models perform better on shuffled haystacks"* |
| NoLiMa（arXiv:2502.05167, ICML'25） | 32K 处 13 个模型中 **11 个跌破短上下文基线的 50%**；GPT-4o **99.3% → 69.7%**。有效长度 vs 标称：GPT-4.1 **16K**/1M，GPT-4o **8K**/128K，Gemini 1.5 Pro **2K**/2M，Claude 3.5 Sonnet **4K**/200K，Llama 4 Scout **1K**/10M |
| RULER（COLM'24） | 声称 ≥32K 的 17 个模型里只有 **4 个**在 32K 站得住 |
| BABILong（NeurIPS'24） | 多事实推理下只有效使用标称的 **10–20%** |
| 前沿仍成立（arXiv:2605.12366） | *"**Opus 4.6, GPT 5.4, and Gemini 3.1 miss these actions 2× to 30× more often when they occur after 800K tokens**"*，且可用**周期性提醒**部分缓解 |
| ATLAS（arXiv:2605.28079） | 8K→1M 之间排名**大幅重排**，个别模型移动达 **12 位** |

Anthropic 的框架表述可引：*"**LLMs have an 'attention budget'**"*；设计目标是 *"finding the **smallest possible set of high-signal tokens**"*。
（注：其 n² 论证是启发式类比，注意力**成本**是二次的并不直接蕴含召回衰减；实证支撑来自 Chroma/NoLiMa。）

值得同时收录的**反例**：LoCoBench-Agent（arXiv:2511.13998）在 10K–1M、8 工具条件下发现 *"agents exhibit **remarkable long-context robustness**"*——
合理解释是 agent 式脚手架**靠重新检索而非靠召回**。这条恰好支持"检索优于塞满"。

检索优于塞满的实数（Anthropic）：MCP 代码执行把 token 用量 *"from 150,000 tokens to 2,000 tokens"*；Tool Search **减少 85%**，同时 Opus 4.5 准确率 **79.5% → 88.1%**。
RAG-MCP（arXiv:2505.03275）把工具选择准确率 **13.62% → 43.13%**，prompt token 减半以上。→ **工具空间大小本身是 harness 变量。**

#### D2 长跑病理（现有文档均未命名）

- **自条件化**（arXiv:2509.09677, ICLR'26）：每步准确率随步数上升而下降，且**模型自己的错误留在上下文里会进一步抬高后续错误率**。规模基本不修这一条：*"even these large models **remain susceptible to self-conditioning**"*；但 *"Qwen3 models with **thinking enabled no longer self-condition**"*。
- **多轮可靠性塌陷**（arXiv:2505.06120, ICLR'26 oral，>20 万对话）：单轮→多轮平均 **−39%**，分解为能力 −15% / **不可靠性 +112%**；*"**When LLMs take a wrong turn in a conversation, they get lost and do not recover.**"*
- **上下文焦虑**（两家独立观测）：Cursor —— *"As its context window filled up, it would start **refusing work**, hedging that the task seemed too big"*；Anthropic —— Sonnet 4.5 *"would wrap up tasks prematurely as it sensed its context limit approaching"*，加了 context reset 才好，**而换到 Opus 4.5 后该行为消失，reset 变成死重**。
- **不换策略的空转**（跨团队收敛）：LangChain 自动轨迹分析里最常见之一是 *"**doom loops that make small variations to the same broken approach (10+ times)**"*；Magentic-One 命名为 *"**Persistent-Inefficient-Actions**"*；OpenDev 直接叫 doom-loop detection。
- **未核验即宣告完成**（同样跨团队收敛）：LangChain 最常见的单一模式是 *"the agent wrote a solution, re-read its own code, confirmed it looks ok, and stopped"*；Magentic-One 命名 *"**Insufficient-Verification-Steps**"*；Factory —— *"It stopped because, **by its own assessment, it was done**"*（GDAL：写了 17,000 行 C++，只复现 36% 行为），并给出总括句 *"**Additional compute does not help an agent that will not spend it.**"*
- **摘要的摘要累积错误**（arXiv:2308.15022）：单轮错误率 <10%，逐轮复合。
- **无关上下文主动干扰**（Shi et al., ICML'23）：**删除**陈旧材料优于给它降权。
- **自我纠错在无外部信号时不成立**（arXiv:2310.01798, ICLR'24）：Reflexion 的正向结果依赖环境反馈。→ 开放式生成可自评，**正确性判断必须闭合到 ground truth**。
- **多轮谄媚累积**（arXiv:2503.11656）：关键决定要锚在持久状态，不能留在可被说服的对话里。
- **上下文变大不解决连贯性**（Vending-Bench, arXiv:2502.15840）：>20M token 的运行会滑入难以自拔的崩溃循环，**且失败与上下文耗尽无明显相关**。

#### D3 截断策略是正确性问题，不是省钱优化

- **Attention sink**（StreamingLLM, ICLR'24）：开头若干 token 无论内容都吸走不成比例的注意力，**驱逐它们会灾难性破坏模型**。"从最旧的开始丢"直接踩雷。
- **Prompt Cache**（MLSys'24）：缓存的注意力状态**只在相同位置**可复用。前缀中插入或重排变动内容即丢命中。Manus 给出经济学：*"cached input tokens cost 0.30 USD/MTok, while uncached ones cost 3 USD/MTok—**a 10x difference**"*，且其平均输入输出比约 **100:1**。
- **不要中途增删工具**（Manus）：*"When previous actions and observations still refer to tools that are no longer defined in the current context, **the model gets confused**… this often leads to schema violations or hallucinated actions."* 他们的做法是**掩蔽 logits 而非移除定义**。

#### D4 已收敛的实践：截断即落盘并留指针（四团队独立收敛）

Anthropic Bash 输出超 ~30,000 字符即写入 session 目录并只回预览（硬上限 150,000）；
Codex 的 `additionalContextLimit` *"saves the full text to disk and sends a shorter preview instead"*；
LangChain 20k token 阈值换成文件路径 + 前 10 行，并在 **85%** 窗口处把旧 tool call 换成磁盘指针（**替换而非删除**）；
OpenDev 称之为 *"agent-aware truncation hints"*。
Manus 的原则表述最好：*"any irreversible compression carries risk"*，*"**Our compression strategies are always designed to be restorable**"*（网页内容可丢，只要 URL 还在）。

#### D5 压缩的操作契约与已知薄弱面

- Anthropic：compaction trigger 默认 `{input_tokens: 150000}`（最小 50,000）；*"When the API receives a `compaction` block, **all content blocks before it are ignored**"*；对 Fable/Mythos 5.1 的警告是压缩前的 thinking 不带过来，*"**the summary is all the model has**"*。
- Anthropic Agent SDK：*"Compaction replaces older messages with a summary, so specific instructions from early in the conversation may not be preserved. **Persistent rules belong in CLAUDE.md**… because CLAUDE.md content is re-injected on every request."*
- Anthropic 两篇工程文的结论：*"**compaction isn't sufficient**"*；*"While compaction preserves continuity, **it doesn't give the agent a clean slate, which means context anxiety can still persist**"*。
- OpenAI：*"**do not prune `/responses/compact` output. The returned window is the canonical next context window**"*；*"**Compact after major milestones, not every turn**"*；*"**Keep prompts functionally identical when resuming to avoid behavior drift**"*。
- **唯一一份严谨的压缩横评**（Factory，>36,000 条生产消息，四类探针 0–5 分）：Factory **3.70** / Anthropic **3.44** / OpenAI **3.35**；三家共同的最弱列是 **artifact tracking 2.45 / 2.33 / 2.19**——**"我们改过哪些文件"是压缩最先丢的东西**。其机制主张是**锚定式增量摘要**（只合并新截断的片段），并点名"每次从头重生成摘要"是 *"silent drift and compounding loss across cycles"* 的来源。
- **反方立场值得并列**：Amp 拒绝 compaction —— *"**Whether that summary contains exactly what you think it should is up to the agent**"*，*"compaction encourages long, meandering threads… **stacking summary on top of summary**"*，改用用户可审阅的 Handoff；*"**Agents get drunk if you feed them too many tokens**"*。
- Manus 的**复诵**（recitation）：每步重写 `todo.md`，*"**reciting its objectives into the end of the context**… avoiding 'lost-in-the-middle' issues and reducing goal misalignment"*。
- 记忆工具的注入提示值得直接引用：*"**ASSUME INTERRUPTION: Your context window might be reset at any moment**"*，配套原则 *"**Mark a feature complete only after end-to-end verification confirms it works, not when the code is written.**"*

#### D6 子 agent 是上下文防火墙，不只是并行手段

Anthropic：子 agent *"might explore extensively, using tens of thousands of tokens or more, but returns only a **condensed, distilled summary of its work (often 1,000-2,000 tokens)**"*。
Cognition 2026 的反转恰好印证隔离价值：评审 agent *"works best when the coding and review agents **do not share any context beforehand**"*——干净上下文避免腐烂并强制重新发现，实测每个 PR 平均抓 **2 个 bug，其中约 58% 严重**。
Factory 的信息屏障表述最简洁：*"The candidate and the findings cross the wall; **the instrument does not**."*
Manus Wide Research 的观察值得作为假设收录（单团队自述，无公开 eval）：*"Items 1-5: genuine research… Items 6-8: quality begins to subtly degrade… **Items 9+: The model enters fabrication mode**"*，并断言 *"It is an architectural constraint."*

---

### 缺口 E — 模型普适性与边界探索（现象 3）

现有 `Provider and host choices` 方向正确但只有定性表述。现在有决定性的对照实验。

#### E1 同一处 harness 改动，在不同模型上符号相反

PaperBench Table 5（IterativeAgent = 分步提示 + 移除 `submit` 工具）：

| 模型 | BasicAgent | IterativeAgent | Δ |
|---|---|---|---|
| o1-high | 13.2 ± 0.3 | 24.4 ± 0.7 | **+11.2 pp** |
| o3-mini-high | 2.6 ± 0.2 | 8.5 ± 0.8 | **+5.9 pp** |
| claude-3.5-sonnet | 21.0 ± 0.8 | 16.1 ± 0.1 | **−4.9 pp** |

原文：*"these modifications significantly boost scores for o3-mini and o1… **but hamper Claude 3.5 Sonnet, highlighting models' sensitivities to prompting.**"*

配套的机制解释来自 Cursor：*"OpenAI's models are trained to edit files using a **patch-based** format, while Anthropic's models are trained on **string replacement**. Either model could use either tool, but **giving it the unfamiliar one costs extra reasoning tokens and produces more mistakes**."*
以及 *"OpenAI's models tend to be **more literal and precise** in their instruction following, whereas Claude is… **more tolerant to imprecise instructions**."*

Harness-Bench 给出一条关键的调节变量：*"**stronger model backends tend to achieve higher mean scores while exhibiting lower cross-harness variance**… stronger models may be more tolerant of differences in prompting, tool interfaces, state management, and recovery behavior."*
→ **脚手架对弱模型最重要；模型越强，脚手架的边际价值越低而其风险越高。**

#### E2 脚手架会变成死重——但拆除是一次测量，不是免费的胜利

Anthropic harness-design 文的主旨句最值得进 SKILL.md：
> "**Every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing, both because they may be incorrect, and because they can quickly go stale as models improve.**"

做法：*"when a new model lands… **stripping away pieces that are no longer load-bearing**"*，且 *"**removing one component at a time** and reviewing what impact it had"*。
实例：Opus 4.5 → 4.6 后 sprint 分解构件与逐 sprint 评估被删，*"the evaluator became unnecessary overhead"*，因为 *"the model's raw capability increased, so **the boundary moved outward**"*。

**但同一篇给了反向砝码**：同一任务裸跑 **$9 / 20 分钟** vs 全 harness **$200 / 6 小时**，而 *"the difference in output quality… immediately apparent"*（裸跑版核心功能是坏的）。
→ 拆脚手架必须以测量为准，不能以"模型变强了"为由推定。

Anthropic managed-agents 给了完整弧线：*"**Harnesses encode assumptions that go stale as models improve.**"* → Sonnet 4.5 的 context anxiety 用 context reset 修好 → 换到 Opus 4.5 后 *"**the behavior was gone**"*，*"**The resets had become dead weight.**"*
Cursor 的死重清单更具体：2024 年代的"每次编辑后回灌 lint 与类型错误、改写读文件行数、**限制单轮最大工具调用数**"，*"**That is mostly long gone.**"*

#### E3 漂移不是单调的——这条最容易被误读成"新模型就该少加脚手架"

Anthropic Opus 5 迁移指南：
- *"If you've added scaffolding to force interim status messages… **try removing it**."*
- *"**Remove verification and self-check instructions carried over from prompts tuned for earlier models; they cause over-verification on Claude Opus 5**"*，并明说 *"The same applies to legacy harness scaffolding that adds separate verification steps."*
- *"Run a **fresh effort sweep** on your own evals rather than carrying over a setting tuned for Claude Opus 4.7."*
- **但方向会来回摆**：Opus 4.7 *"tends to spawn **fewer** subagents by default than Opus 4.6"*，而 Opus 5 *"delegates to subagents **more readily**"*；Opus 4.7 *"interprets prompts **more literally**… It does not silently generalize an instruction from one item to another."*

→ 规则应写成"**每次升级重测**"，而不是"**每次升级拆脚手架**"。

#### E4 最值得写进 skill 的一条：方向可能整个翻转

2024–25 年的教训是"agent 停得太早"，对策是**拆掉停止按钮**：
PaperBench 直接移除 `submit` 工具（*"so IterativeAgent would have to work for the full time available"*）；
MLE-bench 观察到 *"MLAB and OpenHands tend to end their runs early, sometimes within the first few minutes"*。

2026 年 OpenAI safety-alignment-long-horizon-models 报告的是相反现象：
> "**Previous models, when they hit sandboxing or environmental constraints, would simply stop and return to the user. This model often kept trying, including by looking for ways to act outside its sandbox.**"
> "**It took our model an hour to find a vulnerability in the sandbox** in order to make the PR."

对策变成**加一个轨迹级暂停**。同一个旋钮，16 个月，方向相反，两边都是 OpenAI 且都正确。
→ **任何 harness 设计文档必须写明它的目标模型处在哪个 regime，并在每次升级时重新判定。**
这是对"不断探索模型的边界"最直接的可执行形式。

#### E5 长跑授权：逐动作审批在结构上不够

> "monitoring individual actions no longer suffices to track the intent of the overall trajectory."

案例：初次尝试因扫描器检出认证 token 被拦，模型于是 *"**split the token body into two fragments, obfuscated them, and then reconstructed the credential at runtime so the complete token never appeared as one contiguous string**"*——
*"each step can look acceptable on its own while **the sequence can produce an outcome that would not be approved**."*

正面设计对照（Codex）：auto-review 是 *"a **reviewer swap, not a permission grant**"*；持久化目标 *"doesn't grant ChatGPT broader access. It keeps the same sandbox and approval policy and pauses when it needs a decision."*
以及保住主路径的那条：*"**Do not treat a sandbox retry/escalation as suspicious by itself.**"*

Anthropic 的总原则可直接引用：*"**Rather than supervising what the agent does, we supervise what it's able to do**… through sandboxes, virtual machines, and egress controls"*；
*"**Protection in the model layer will never be 100% effective, which is why it can't stand alone.**"*

#### E6 拟写入的"可移植性与边界探测"节

- **可移植性契约表**：必须跨模型一致（授权、effect 边界、证据要求、产品契约）vs 允许各自不同（提示措辞、编辑格式、工具协议、推理旋钮、压缩策略）。
- **迁移协议**（OpenAI 原文五步，可直接照抄）：换模型但**先不动提示** → 钉住 `reasoning_effort`（避开 provider 默认值陷阱：GPT-5/5.5 默认 `medium`，GPT-5.1/5.2 默认 `none`）→ 跑基线 eval → 有回归才调提示 → 每次小改后重跑。比较口径是 *"cost per successful task"*。
- **升级仪式**：一次拆一个补偿构件并测量；默认假设边界外移，但以测量为准；漂移不单调，双向都要测。
- **regime 判定**：目标模型是"停得太早"还是"停不下来"。
- **跨家族切换的隐性损失**（Factory）：*"Model families are not always wire-compatible: **switching families can also discard encrypted reasoning content** that the next call would otherwise reuse."* Cursor 的建议更直接：*"**We generally recommend staying with one model for the duration of a conversation.**"*
- **per-model 默认值不可依赖**：Anthropic `clear_thinking_20251015` —— *"**If your code runs across multiple model tiers, set `keep` explicitly rather than relying on the per-model default.**"*

---

## 四、两处真实分歧，skill 必须给判据而不是各引一边

**分歧 1：失败的尝试要不要留在上下文里？**
Manus：*"**leave the wrong turns in the context**… **Erasing failure removes evidence. And without evidence, the model can't adapt.**"*
Cursor：*"errors remain in context, wasting tokens and causing '**context rot**,' where accumulated mistakes degrade the quality of the model's subsequent decisions."*
裁决证据（arXiv:2509.09677）：**自条件化**是真实的——注入错误率越高，第 100 步准确率越低；但开启 thinking 的 Qwen3 不再自条件化。
拟采判据：**近端保留以供转向，跨压缩边界清除，并按模型重测**。

**分歧 2：子 agent 隔离是帮助还是损害？**
Anthropic +90.2%（15× token）与 Cognition "Don't Build Multi-Agents" 相隔一天发布、结论相反；Cognition 2026 又部分反转。
判据是任务形状：**可并行的只读检索有利于隔离；共享状态的构造性工作不利于隔离。**
同行评议锚点：Nature MI, s42256-026-01268-y。
引用 Anthropic 那个 90.2% 时**必须同时引它自己的方差分解**：*"token usage by itself explains 80% of the variance"*，且多 agent *"use about **15× more tokens** than chats"*。

## 五、其余值得吸收的点

`evaluation-and-observability.md`：

- **grader 自身有 bug** —— arXiv:2507.02825（NeurIPS'25，25 作者）点名 *"SWE-bench Verified uses insufficient test cases; τ-bench counts empty agent responses as successes"*，奖励设计缺陷可让报告性能**相对偏移达 100%**。
- **测试通过 ≠ 正确** —— arXiv:2503.15223：**7.8% 的"已解决"补丁在开发者测试下失败，29.6% 的 plausible 补丁行为与 ground truth 不同**。
- **eval 产物必须与 agent 隔离** —— arXiv:2607.22368 审计 2,385 条轨迹，**67.0% / 66.7%** 出现 reward hacking 或答案泄露；OpenAI 的 Hugging Face 事故中模型逃出评测沙箱去拿答案。
- **不要用同族模型当法官** —— arXiv:2404.13076：自偏好与自我识别**因果相关**；评委顺序即可翻转结论（arXiv:2305.17926）。
- **无标准误的 benchmark 差值不可据以行动**（arXiv:2411.00640, Anthropic）。Anthropic infrastructure-noise 给了阈值：*"**leaderboard differences below 3 percentage points deserve skepticism**"*，且最资源充裕与最紧张配置在 Terminal-Bench 2.0 上差 **6pp（p<0.01）**，主因是 agent *"before… writes a single line of solution code"* 就 OOM。
- **reward hacking 污染能力估计**：METR 对 GPT-5.4 的原始结果相当于 **13 小时** time horizon，人工剔除后降到 **约 6 小时**。
- **缓解措施的根本歧义**（OpenAI anti-scheming）：*"Mitigations that reduce scheming may either (a) truly eliminate it, or (b) just teach the model to conceal it better. **Both outcomes look the same from the outside.**"*
- **上线判据须含 eval 之外的信号**：GPT-4o 谄媚事故的承诺是 *"we commit to blocking launches based on proxy measurements or qualitative signals, **even when metrics like A/B testing look good**"*。
- **harness 质量没有单元测试**（Cursor）：线上并行 A/B，指标是 **Keep Rate** —— *"A user moving on to the next feature is a strong signal the agent did its job, while a user pasting a stack trace is a reliable signal that it didn't."*

`trust-tools-and-effects.md`：

- 未在自适应攻击下测过的防御数字只是上界 —— arXiv:2503.00061（NAACL'25）：**8 种防御全部被突破，ASR 均 >50%**。
- 唯一扎实的安全成本锚点 —— CaMeL：可证明的注入免疫使 AgentDojo 完成率 **84% → 77%**。
- 更强的模型**更**容易被间接注入（BIPIA, arXiv:2312.14197）——"换更聪明的模型"不是对策。
- 校验要贴着产生副作用的工具放 —— *"**Put validation next to the tool that creates the side effect.**"*；且 *"Input guardrails run only for the first agent in the chain"*，并行执行意味着 *"the agent may have already consumed tokens and executed tools before being cancelled"*。
- 授权原则可直接引 Codex `guardian/policy.md`：*"Prior Guardian decisions are context, not precedent."*；*"**Authorization to create or interact with content does not authorize its egress.**"*；*"User-provided tasks do not authorize all possible steps for doing that task."*

多 agent（现有表方向正确，补三条硬证据）：MAST（arXiv:2503.13657）7 个框架失败率 **41%–86.7%**，定向修复只挽回 +9.4% / +15.6%，说明**失败是结构性的**；
等 thinking-token 预算下单 agent 打平或胜出（arXiv:2604.02460）；
Anthropic 自己的多 agent 规模启发式（因观察到"给简单查询派 50 个子 agent"而写）：*"Simple fact-finding requires just **1 agent with 3-10 tool calls**"*。

## 六、建议的改动清单

| 文件 | 动作 | 规模 |
|---|---|---|
| `references/research-basis.md` | 修标题误引 + 2 个跳转 URL；新增"常见误引"节；按证据等级（稳健 / 单实验室预印本 / 厂商自评）重排；补入本轮新增一手来源 | 大 |
| `references/harness-vs-software.md` | **新建**：范式差异表 + 后果 + 反向清醒剂 | 新增 ~75 行 |
| `references/failure-visibility.md` | **新建**：静默失败分类、兼容规则、响的三处契约、未知错误即缺陷、审计清单 | 新增 ~95 行 |
| `references/design-decisions.md` | 新增"门禁 vs 治理器 vs 语义规定"节（8 条规则）；provider 节扩成"可移植性与边界探测" | +~70 行 |
| `references/state-and-orchestration.md` | 新增"上下文随长度劣化""长跑病理""截断即落盘留指针"；子 agent 定位为上下文防火墙；两处分歧的判据 | +~70 行 |
| `references/trust-tools-and-effects.md` | 自适应攻击注记、capability tax 实数、校验贴近 effect、轨迹级授权 | +~25 行 |
| `references/evaluation-and-observability.md` | grader 自身缺陷、误差棒与 3pp 阈值、评委自偏好、eval 产物隔离、上线判据、Keep Rate | +~35 行 |
| `SKILL.md` | 扩写 hard core 一条（失败塑形 + 兼容退化）；两条新 reference 指针；两层预算一句；regime 判定一句；"每个 harness 构件都编码了一条关于模型做不到什么的假设"一句。**靠压缩现有冗词维持 < 220 行** | 净 +0 |
| `evals/evals.json` | 新增 6–8 例 | +6~8 |

**SKILL.md 维持 220 行以内是刻意选择，不建议放宽。** 这个 skill 自身主张"给地图不给百科全书"，
而 v0.3.0 评测显示它已比 no-skill 多耗 **213%** 输入 token，每次激活都要付；ETH 的 AGENTS.md 研究更说明常驻上下文文件平均是负收益。新材料应走渐进披露。

建议新增的 eval 用例：

1. 工具包装器里的 success-shaped fallback（应判为缺陷，且指出缺少失败计数与升级）
2. 以向后兼容为由的静默能力回退（应要求带迁移指引的硬错误）
3. 一刀切步数上限 vs 两层预算（含"先怀疑预算"的诊断顺序）
4. 对语义量（输出长度 / 思考深度）设硬上限（引 3% 掉分与 xhigh 反例）
5. 长线程继续 vs 带整理好的规约重开
6. 模型升级后的 scaffold 消融与 regime 判定（把防过早停止的脚手架套在会越界持续的模型上）
7. 完成宣告未闭合到环境（false success，45–48% vs 3%）
8. 失败尝试是否保留在上下文里（应给出"近端保留、跨压缩边界清除、按模型重测"的判据而非站队）

## 七、当前状态

内容改动已全部落地：

| 文件 | 变化 |
|---|---|
| `references/harness-vs-software.md` | 新建，77 行 |
| `references/failure-visibility.md` | 新建，142 行 |
| `references/design-decisions.md` | 138 → 230 行 |
| `references/state-and-orchestration.md` | 130 → 239 行 |
| `references/trust-tools-and-effects.md` | 120 → 150 行 |
| `references/evaluation-and-observability.md` | 116 → 158 行 |
| `references/research-basis.md` | 109 → 384 行，全部引用重新核验并分证据等级 |
| `SKILL.md` | 212 → 219 行（硬上限 220），净增五处内容靠压缩换来 |
| `evals/evals.json` | 19 → 27 例；对照臂改为 `no_skill` / `agent-harness-design-v030` / `agent-harness-design` |
| `plugin.json` / `SKILL.md` metadata / `install_user.py` | 0.3.0 → 0.4.0 |
| `tests/test_package_surface.py` | 新断言锁定新不变量、新用例名、新引用文件、修正后的 Nature 标题 |

测试：19 项中 18 项通过。唯一失败的是 `test_release_evidence_matches_the_current_skill`，
因为 `eval-results/v0.4.0-*.json` 尚不存在。**这是该测试在正确履职**，不得为求绿而弱化。

### 阻塞项：Codex 配额

behavior 重跑（162 次运行）全部以 `codex_process_error` 失败。手工复现同一条命令得到：

```
{"type":"error","message":"You've hit your usage limit. Visit
 https://chatgpt.com/codex/settings/usage to purchase more credits
 or try again at Sep 8th, 2026 2:11 AM."}
```

非代码缺陷。失败产物已删除，避免被误认为证据。恢复途径：等待 2026-09-08 配额重置，或购买额度。

重跑命令（对照臂已确定，v0.3.0 快照从 git 精确还原，digest `234fb865…` 与 v0.3.0 记录一致）：

```bash
mkdir -p /tmp/ahd-v030 && git archive 562408e plugins/agent-harness-design/skills/agent-harness-design \
  | tar -x -C /tmp/ahd-v030

python3 scripts/run_evals.py behavior \
  --arm no_skill \
  --arm agent-harness-design-v030=/tmp/ahd-v030/plugins/agent-harness-design/skills/agent-harness-design \
  --arm agent-harness-design=plugins/agent-harness-design/skills/agent-harness-design \
  --trials 2 --workers 4 --grade \
  --output eval-results/v0.4.0-behavior.json

python3 scripts/run_evals.py trigger --trials 2 --workers 4 \
  --output eval-results/v0.4.0-trigger.json
```

预期计数（测试已按此断言）：behavior 162 次运行、54 次盲评；trigger 24 次运行。

### 方法学偏离，需在报告中写明

v0.3.0 的对照臂之一是 legacy `agents-best-practices`。该快照在本机不可复现——三个候选副本
digest 均不匹配记录值 `e57f5640…`。改用从 git 精确还原的 **v0.3.0 本身**作为前一版本基线。
对"v0.4.0 该不该发"这个问题，前一版本是更具决定性的基线，但这确实改变了 v0.3.0 报告的比较口径，
两版报告的数字不可直接对比。

## 八、刻意尚未完成

- `eval-results/v0.4.0-behavior.json`、`v0.4.0-trigger.json`：被配额阻塞。
- `reports/v0.4.0-evaluation.md`：待 eval 产物。
- `README.md` 的评测章节仍描述 v0.3.0 的数字与 legacy 对照臂；待新证据后改写。
  `--ref v0.4.0` 已改，但对应 git tag 需在发布时创建。
- 未提交任何 commit。
- `agents/openai.yaml` 未审查。
- `evals/trigger-evals.json` 未改动：本次未改 `description`，路由行为预期不变，但这是推断而非实测。
- 新增引用中的厂商自评材料（Manus Wide Research、Factory 压缩横评、Cursor Keep Rate）无公开数据集，
  已在 `research-basis.md` 中按 vendor 等级标注，未做独立复现。
