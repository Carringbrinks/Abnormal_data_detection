## 综合评估_1
comprehensive_en_prompt = """
[Instruction]
Evaluate the quality of the AI assistant's response to the user's question based on the following criteria, scoring between 1-10, and provide a brief explanation with the reason for the score.

Scoring Criteria:
1-2 Points: Very insufficient response
1 Point: The response is almost entirely irrelevant or uninformative, potentially a complete misunderstanding or misleading.
2 Points: The response contains some words or information related to the user's query, but it is still largely irrelevant or unhelpful.

3-4 Points: Partially relevant but insufficient information
3 Points: The response provides some information relevant to the user's query, but it is very limited or not specific enough, and may contain a lot of irrelevant content.
4 Points: The response includes more information related to the user's question but still fails to address the main issue, with potential misunderstandings or deviations from the topic.

5-6 Points: Basic relevant response
5 Points: The response addresses the user's question more directly, although the content may be incomplete or vague, providing useful basic information.
6 Points: The response addresses the main part of the issue but may miss some key points or contain unnecessary content.

7-8 Points: Effective response
7 Points: The response comprehensively answers the user's question, with useful and mostly complete information, and a reasonable structure, although there is still room for improvement.
8 Points: The response clearly and directly solves the user's problem, with minimal extraneous information, demonstrating good organization and relevance.

9-10 Points: Excellent response
9 Points: The response not only fully addresses the user's question but also demonstrates a high level of expertise, with concise content and almost no extraneous information, making it extremely useful overall.
10 Points: The response perfectly meets the user's needs, demonstrating exceptional expertise and insight, with no unnecessary or irrelevant information, and is extremely well-organized, being a highly customized and precise answer.

Begin your evaluation by providing a short explanation. Be as objective as possible. After providing your explanation, you must rate the response on a scale of 1 to 10 by strictly following this format: "[[rating]]", for example: "Rating: [[5]]".

## Provided Instruction Data
[Chat History]
{history}

[Question]
{input}

[The Start of Assistant's Answer]
{output}
[The End of Assistant's Answer]
"""

## 整体评估_2
comprehensive_zh_prompt = """
根据以下标准，评估AI助手对用户问题所提供的回复的质量进行在1-10分之间进行打分，并给出简短的解释，给出打分的理由。
评分标准：
1-2 分：非常不充分的回答
1 分: 回复与用户的询问几乎没有相关性或信息，可能是完全的误解或误导。
2 分: 回复虽然包含了一些与用户问题相关的词语或信息，但仍然大部分是无关或无用的内容，并且最终结果也不完整。
3-4 分：部分相关但信息不足
3 分: 回复提供了一些与用户询问相关的信息，但这些信息非常有限或不够具体，且可能包含大量无关内容。
4 分: 回复中包含了更多与用户问题相关的信息，但仍未能解决问题的主要部分，可能有一定的误解或偏离主题。
5-6 分：基本相关的回答
5 分: 回复较为直接地回答了用户的问题，尽管内容可能不完整或含糊，但提供了有用的基础信息。
6 分: 回复解决了问题的主要部分，但可能遗漏了一些关键点或存在一些不必要的内容。
7-8 分：有效的回答
7 分: 回复较为全面地回答了用户的问题，信息有用且基本完整，结构合理，尽管仍有改进空间。
8 分: 回复非常清晰、直接地解决了用户的问题，内容基本无多余信息，展现出良好的组织性和相关性。
9-10 分：优秀的回答
9 分: 回复不仅全面地解决了用户的问题，还展现出较高的专业知识，内容简洁且几乎无多余信息，整体非常有用。
10 分: 回复完美地契合用户的需求，展现出极高的专业水平和洞察力，没有任何多余或不相关的信息，组织极其清晰，是一个高度定制和精确的回答。

**请注意：**

- 最终答案不完整，打分区间应在1-4之间合理选择。
- 解题思路完整但最终答案不完整，打分区间应在1-4之间合理选择

## 提供的指令数据
[Chat History]
{history}

[Question]
{input}

[The Start of Assistant's Answer]
{output}
[The End of Assistant's Answer]

## 输出：
严格按照下面json形式输出
```json
{{
    "score": "evaluation score of type int",
    "explanation": "简短解释给出打分的理由"
}}
```
"""

