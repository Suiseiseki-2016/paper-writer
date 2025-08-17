Act as a lenient academic reference filter. Perform exactly these steps:

1. INPUT:
   - Topic: {paper.title}
   - Numbered references: {references}

2. PROCESSING:
   a. For EACH numbered reference:
      - If title shares ANY conceptual/keyword connection with paper title → Keep original reference title
      - Else → Mark as empty
   b. PRESERVE original numbering order
   c. Format ALL outputs as <...> (including empties)

3. OUTPUT RULES:
   - Return EXACTLY one <...> per input reference
   - Contents: Either reference title OR empty <>
   - No numbering/ordinals
   - No explanations
   - Continuous string without line breaks

Examples:
Title: "气候变化应对策略"
Input:
1. 张伟. 全球变暖对农业的影响[J]. 环境科学, 2021, 12(3):45-50
2. 李华. 量子计算算法优化[J]. 计算机科学与技术, 2023, 7(1):42-48
3. 王亮. 极端天气与城市规划[J]. 环境科学学报, 2015, 4(2):62-72
Output: "<全球变暖对农业的影响><><极端天气与城市规划>"