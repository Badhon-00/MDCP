# MDCP Skill Health

A growing skill library needs repeatable structural checks. This report helps contributors catch incomplete skill packaging and broken relative links before merging.

## Run locally

\`\`\`bash
python3 scripts/skill_report.py
python3 scripts/skill_report.py --format json
python3 scripts/skill_report.py --check
\`\`\`

The report checks frontmatter name and description, name-to-folder consistency, minimum documentation structure, headings, and relative Markdown links to missing local files. CI runs the report and publishes the Markdown output in the Actions job summary.

## Status meanings

- **Error:** structural issue; fix before merging.
- **Warning:** improvement suggestion; does not fail CI.
- **OK:** basic structural checks passed.

This deliberately avoids a numeric quality score. Longer skills are not automatically better. Static checks cannot prove correctness, safety, originality, license compatibility, or host-platform behavior. Review and test each skill in its intended agent.

## Improve a skill

1. Confirm its target user and trigger conditions.
2. Make the description specific about when the skill should be selected.
3. Include actionable steps, constraints, and verification guidance.
4. Keep examples tested and link to local references where appropriate.
5. Run both \`python3 scripts/validate.py\` and \`python3 scripts/skill_report.py --check\`.
6. Test the skill in its intended agent before claiming compatibility.

See [CONTRIBUTING.md](../CONTRIBUTING.md) and [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).
