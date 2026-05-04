# Presentation Slide Draft

Use this file to prepare the slide storyline and the visual assets Josiah can hand to the group leader.

## Slide Storyline

1. Title and team
- Project title, course, and member names.

2. Problem framing
- Show that the assignment has three AI tasks: search, optimization, and machine learning.
- Explain that the repo is organized to solve all three in one final notebook submission.

3. Part 1 - Flight connections
- Explain the graph model: cities are nodes and direct flights are edges.
- State that Breadth-First Search is used because every flight counts as one step.
- Show a simple example route and the evaluation chart `reports/figures/part1_route_lengths.png`.

4. Part 2 - Hospital scheduling
- Explain the CSP model: 21 shifts, nurse domains, and three constraint types.
- Mention node consistency, AC-3, MRV, and backtracking with forward checking.
- Show `reports/figures/part2_schedule_overview.png` and `reports/figures/part2_shift_distribution.png`.

5. Part 3 - Traffic sign recognition
- Explain the CNN pipeline: image loading, resizing, normalization, training, and testing.
- Clarify whether the slide uses the real GTSRB dataset or the repo's synthetic demo dataset.
- Show `reports/figures/training_curve.png`.

6. Evaluation highlights
- Show `reports/figures/confusion.png`.
- Show `reports/figures/sample_predictions.png`.
- Summarize the most important metrics from `reports/evaluation_notes.md`.

7. Limitations and next steps
- The repo currently relies on generated demo datasets because the official assignment datasets are not tracked here.
- Final results should be rerun on the real flight, staff, and GTSRB datasets before submission.

8. Closing slide
- GitHub repository link
- Final notebook / PDF link
- Questions

## Visual Asset Checklist

- `reports/figures/part1_route_lengths.png`
- `reports/figures/part2_schedule_overview.png`
- `reports/figures/part2_shift_distribution.png`
- `reports/figures/training_curve.png`
- `reports/figures/confusion.png`
- `reports/figures/sample_predictions.png`
- `reports/evaluation_notes.md`

## Presenter Notes

- Keep each technical part to one core idea and one visual.
- Spend the most time on what was validated, not only on what was built.
- Be explicit when a result comes from generated demo data versus the official assignment dataset.
