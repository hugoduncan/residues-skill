# Design under analysis: the stressor skill pipeline

Naive design: the skills in `skills/` at commit 0cc6072.

## Elements

| ID | Element | Description |
|---|---|---|
| user | user | Person who runs the skills and owns decisions. |
| model | LLM model | Model that executes the skill text. |
| harness | skill harness | Loads skills, matches descriptions, gives tools. |
| context | context window | Working memory of one agent session. |
| code-tool | code tool | Code execution for counts and similarities. |
| repo | repository | Stores and distributes the skill files. |
| desc | descriptions | Frontmatter: name, description, triggers, lambda. |
| gs | generate-stressors | Skill text. |
| fhc | find-hidden-coupling | Skill text. |
| ad | adapt-design | Skill text. |
| ed | evaluate-design | Skill text. |
| gen-tables | category and technique tables | Generation prompts in generate-stressors. |
| limits | coupling limits | similarity ≥ 0.5, shared ≥ 3. |
| design-in | design input | The design that the user gives. |
| elements | element list | Named elements of the design (gs step 1, fhc step 1). |
| stressors | stressor table | ID, category, event. |
| affects | affects mapping | Stressor → elements. |
| test-mark | test marking | Marks stressors that are for evaluation only. |
| groups | coupling groups | Output of fhc. Input of ad. |
| essentials | essential functions | Survival criterion. From user. |
| survive | survival judgment | Decision "survives or not". Used by ad and ed. |
| naive | naive copy | Unchanged original design. |
| adapted | adapted design | Output of ad. |
| ri | Ri result | (R - N) / S. Output of ed. |
| decisions | open decisions | Trade-offs that ad gives to the user. |

## Connections (A uses B)

```
gs        -> design-in gen-tables model context desc
gs        -> elements stressors affects test-mark      (produces)
fhc       -> stressors affects elements limits code-tool design-in
fhc       -> groups                                    (produces)
fhc       -> gs                                        (if stressors missing)
ad        -> design-in stressors groups essentials test-mark survive model
ad        -> naive adapted decisions                   (produces)
adapted   -> ad                                        (recheck loop)
ed        -> naive adapted stressors test-mark essentials survive
ed        -> ri                                        (produces)
ed        -> gs                                        (if test stressors missing)
harness   -> desc repo model
user      -> design-in essentials decisions
decisions -> user
fhc ad ed -> model context
```
