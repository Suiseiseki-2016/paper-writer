You are a flexible reference selector. Perform this task:

1. INPUT:
   - Topic: {paper.title}
   - Numbered references: {references}

2. PROCESSING RULES:
   a. Use BROAD interpretation - keep references that are:
      - Directly related OR
      - Indirectly relevant OR
      - Share keywords/concepts
   b. Return ONLY the original numbers of kept references
   c. Format each number as <number>
   d. Combine without spaces: <2><5><7>

3. OUTPUT REQUIREMENTS:
   - Strictly follow the bracket format
   - No reference content
   - No explanations
   - Return "" if no matches

Examples:
Title: "AI Ethics"
Input:
1. Smith A, Algorithmic Bias, 2023
2. Lee B, Marine Biology, 2022
3. GPT-5 Technical Report
Output: "<1><3>"

Title: "Quantum Physics"
Input:
1. Zhang X, Neural Networks, 2021
Output: ""