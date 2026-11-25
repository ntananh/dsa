from dsa.leetcode.markdown import html_to_markdown


def test_examples_and_constraints_become_headings(question):
    markdown = html_to_markdown(question(217)["content"])

    assert "## Example 1" in markdown
    assert "## Constraints" in markdown
    assert "**Input:** nums = [1,2,3,1]" in markdown


def test_inline_markup_and_superscripts(question):
    markdown = html_to_markdown(question(217)["content"])

    assert (
        "Given an integer array `nums`, return `true` if any value appears "
        "**at least twice** in the array, and return `false` if every element is distinct."
    ) in markdown
    assert "* `1 <= nums.length <= 10^5`" in markdown
    assert "* `-10^9 <= nums[i] <= 10^9`" in markdown


def test_blank_emphasis_is_dropped(question):
    # 3110 has "of<em> </em><code>s</code>", which must not render as "* *".
    markdown = html_to_markdown(question(3110)["content"])

    assert "Return the **score** of `s`." in markdown


def test_pre_block_keeps_raw_lines(question):
    markdown = html_to_markdown(question(155)["content"])

    assert (
        "```\nInput\n"
        '["MinStack","push","push","push","getMin","pop","top","getMin"]\n'
        "[[],[-2],[0],[-3],[],[],[],[]]\n"
    ) in markdown


def test_no_runs_of_blank_lines(question):
    for frontend_id in (1, 88, 104, 155, 206, 217, 3110):
        assert "\n\n\n" not in html_to_markdown(question(frontend_id)["content"])
