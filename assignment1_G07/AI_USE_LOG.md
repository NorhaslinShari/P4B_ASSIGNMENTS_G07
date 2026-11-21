# AI USE LOG

<!-- SECB3203 prompt log. Policy: PROPOSED - for approval by the SECB3203 course team before circulation to students. Fill in, then run: python tools/check_ai_log.py AI_USE_LOG.md --assessment <key> -->

- Course: SECB3203
- Assessment: <e.g. Lab 4>
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
