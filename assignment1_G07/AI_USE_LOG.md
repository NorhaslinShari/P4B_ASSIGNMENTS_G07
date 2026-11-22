# AI USE LOG

<!-- SECB3203 prompt log. Policy: PROPOSED - for approval by the SECB3203 course team before circulation to students. Fill in, then run: python tools/check_ai_log.py AI_USE_LOG.md --assessment <key> -->

- Course: SECB3203
- Assessment: Assignment 1
- Student name: <full name>
- Matric no: <matric>
- Group ID: <group work only, else n/a>
- AI level: <0, 1 or 2 - see the assessment brief>
- Tools cited: <UTM format, e.g. OpenAI (2026). ChatGPT (GPT-5). Retrieved 12 October 2026 from https://chat.openai.com>

## Declaration (tick exactly one)

- [ ] NIL RETURN: I did not use any generative AI tool for this assessment.
- [/] I used AI. Every interaction that influenced my work is logged below. The log is true and complete.

## Entry 1

- Date: 20 November 2026 (4:45 PM)
- Tool: Tools cited: Microsoft Copilot (GPT-5 Chat Model). Accessed 21 November 2026. Available at: https://copilot.microsoft.com/ 
- Purpose: explain and hint
- Prompt: can u help me with task 5? but do not give me answer just explain and hint.......help me until my code is correct and follow what instruction want 
- Output: T5.1 CSV Export (results_to_csv)

The specification is basically asking:
Take a list of result dictionaries and convert them into a CSV string.

If your results look something like:

Python
[
{
"variant": "v1",
"gene": "BRCA1",
"chrom": "17",
"pos": 100,
...
}
]
and
Python
CSV_COLUMNS = [
"variant",
"gene",
"chrom",
...
]
the function should:

Step 1: Create the header row

Think:
Plain Text
variant,gene,chrom,pos,depth,...

How can you turn a list into a comma-separated string?

Hint:
Python
",".join(...)
Step 2: Create one CSV row per result
Loop through every dictionary in results.

For each result:
get values in the order specified by CSV_COLUMNS
convert each value to a string
join with commas

Think:
Python
for result in results:
...
and
Python
for column in CSV_COLUMNS:
...
Step 3: Build all lines together

You'll eventually have:
Python
[
header,
row1,
row2,
row3
]
How do you combine lines into one string?

Hint:
Python
"\n".join(...)
Step 4: Important detail

The specification said:
Every line ends with a newline.
Many students miss this.

If you do only:
Python
"\n".join(lines)
the final line usually has no trailing newline.

Think about how to add one final \n.
Common mistakes
Wrong column order

Don't do:
Python
for value in result.values():

Dictionary order is not guaranteed by the assignment.
Use
Python
CSV_COLUMNS
to control the order
Forgetting str()
CSV is text.

Numbers like:
Python
100
80

must become:
Python
"100"
"80"
before joining.

Returning list instead of string
Wrong:
Python
return lines

Need:
Python
return some_string
T5.2 Report Generation (build_report)

The assignment gives a very strict format.
The report contains specific lines.
Think of it as building:

Plain Text
Variant Triage Report
Thresholds: ...
Priority genes: ...
Decision counts:
Review: 4
Monitor: 2
Ignore: 1
Top variants:
...

(Your actual format depends on the spec.)

Step 1: Start with report title
Create a list:
Python
lines = []
First add the title.

Python
lines.append(...)
Step 2: Threshold line

You have:
Python
params

Inside:
Python
params["min_depth"]
params["min_quality"]

Need to produce exactly:

Plain Text
Thresholds: min_depth=D min_quality=Q

Question:
How do you insert variables into a string?
Hint:
Python
f"...{variable}..."
Step 3: Priority genes line

You have something like:
Python
["BRCA1", "TP53"]

Need one string.
Hint:

Python
", ".join(...)

produces

Plain Text
BRCA1, TP53
Step 4: Decision counts

You already wrote:
Python
decision_counts(results)

That function returns counts.

Something like
Python
{
"Review": 3,
"Monitor": 2,
"Ignore": 1
}

Loop through the decisions and add lines.
Think
Python
for decision in ...
Step 5: Top variants

You already have:
Python
rank_variants(...)

Use it.
Don't reimplement ranking logic inside build_report.

Ask yourself:
"I already wrote a ranking function. Why calculate again?"
Step 6: Return final text
Again:
Python
"\n".join(lines)
plus whatever newline requirement the spec asks for.
- Verified by: i add my own test after each function i created and see if the output follows my expectation or not
- My change: i follow what Ai recommend 
- Used in: a1_triage.py

<!-- Copy the whole 'Entry' block for each extra interaction: ## Entry 2, ## Entry 3 ... -->

## Entry 2

- Date: 21 November 2026 (6:53 PM)
- Tool: Tools cited: Microsoft Copilot (GPT-5 Chat Model). Accessed 21 November 2026. Available at: https://copilot.microsoft.com/ 
- Purpose: explain and hint
- Prompt: gene_summary(results) dict of dicts
One entry per gene present, genes in alphabetical order. Each entry has total, prioritize, review, exclude and mean_depth (mean depth of ALL the gene's variants, rounded to 1 decimal). Empty input gives {}.....can u explain how the flow? not answer just flow
- Output:
For:

Python
gene_summary(results)

Input is probably a list like
Python
results = [
{"gene": "BRCA1", "decision": "prioritize", "depth": 100},
{"gene": "TP53", "decision": "review", "depth": 50},
{"gene": "BRCA1", "decision": "exclude", "depth": 80},
]
Step 1: Handle empty input

First check:

Python
results == []

If yes:
Python
return {}

because the specification says:

Empty input gives {}

Step 2: Create an empty summary dictionary

Think:

Plain Text
summary = {}
This dictionary will eventually look like:
=
Python
{
"BRCA1": {...},
"TP53": {...}
}
Step 3: Go through every variant in results

Flow:

Plain Text
for each variant:
 
Example first variant:
Python
{"gene": "BRCA1", "decision": "prioritize", "depth": 100}

Extract:
Plain Text
gene = BRCA1
decision = prioritize
depth = 100
Step 4: First time seeing a gene?

Ask:
Plain Text
Is BRCA1 already in summary?

If NO:
Create its counters.

Conceptually:
Python
summary["BRCA1"] = {
"total": 0,
"prioritize": 0,
"review": 0,
"exclude": 0,
"sum_depth": 0
}

Why sum_depth?

Because you need mean depth later.
Step 5: Update counts
For every variant:

Increase total:
Plain Text
total += 1
Then increase the matching decision count:

If decision is:
Plain Text
prioritize -> prioritize += 1
review -> review += 1
exclude -> exclude += 1
Step 6: Accumulate depth

Don't calculate mean yet.
Just keep adding depth:

Plain Text
sum_depth += current depth

Example:
Plain Text
BRCA1 depths:
100
80

Store:

Plain Text
sum_depth = 180
Step 7: Continue until all variants processed

Suppose after the loop:

Python
{
"BRCA1": {
"total": 2,
"prioritize": 1,
"review": 0,
"exclude": 1,
"sum_depth": 180
},
"TP53": {
"total": 1,
"prioritize": 0,
"review": 1,
"exclude": 0,
"sum_depth": 50
}
}
Step 8: Calculate mean_depth
Now go through each gene in the summary.

For each gene:
Plain Text
mean_depth = sum_depth / total

Example:
Plain Text
BRCA1
180 / 2 = 90.0
 
TP53
50 / 1 = 50.0

Round to 1 decimal place.
Step 9: Remove temporary data

The specification wants:

Plain Text
total
prioritize
review
exclude
mean_depth

It does not mention:

Plain Text
sum_depth

So after mean_depth is calculated:

Plain Text
remove sum_depth
Step 10: Return genes in alphabetical order

Required output:
Plain Text
BRCA1
TP53

because alphabetically:

Plain Text
B comes before T
Final structure:

Python
{
"BRCA1": {
"total": 2,
"prioritize": 1,
"review": 0,
"exclude": 1,
"mean_depth": 90.0
},
"TP53": {
"total": 1,
"prioritize": 0,
"review": 1,
"exclude": 0,
"mean_depth": 50.0
}
}

- Verified by: i add my own test after each function i created and see if the output follows my expectation or not
- My change: i follow what Ai recommend 
- Used in: a1_triage.py


