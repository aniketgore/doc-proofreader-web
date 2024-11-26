# Copyright caerulex 2024

"""User prompts."""

USER_PROMPT = """
Proofread the provided passage. Only output mistakes, if there are any! Do not invent or fabricate mistakes where none exist.
Go sentence by sentence. Decompose the sentence into subject/verb/etc. to ensure you properly assess it for errors.
IF AND ONLY IF YOU ENCOUNTER A SENTENCE WITH AN ERROR:
1. Start with the "＊" character.
2. Write out the corrected sentence with all errors corrected. Do NOT repeat the original sentence. Put brackets around all changes to highlight them within the revised sentence. I.e. given: `The down was beautiful.`, output: `The [town] was beautiful.`.
3. After the sentence, call out the changed portion with the format [<original>] -> [<fixed>]. I.e. [down -> town].
Here is another example:
＊The longest they [could have been in hiding] was five days. [could be in hiding] -> [could have been in hiding]

If a sentence does NOT have an error, output NOTHING and move on to the next sentence. This is because the shorter the output is, the higher the score on this test.

If there are no errors in the entire passage, say that no errors were found.
"""
