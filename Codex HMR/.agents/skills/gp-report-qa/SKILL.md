---
name: gp-report-qa
description: Review a completed clinical report from a GP perspective, flagging patient-safety, evidence, actionability and usability issues without editing or approving the report.
---

# GP-perspective Report QA

Use this as a separate, post-draft review step for a clinical report. It is a structured GP-perspective QA review, not a consultation with a registered GP, prescribing decision, clinical sign-off or replacement for pharmacist and GP judgement.

## Inputs

Obtain the completed report and the authorised patient sources needed to verify it, such as the referral, interview, medicine evidence, letters and relevant results. Do not infer facts from a report where the source is unavailable. If material sources are missing, identify the review limitation instead of guessing.

## Review

Assess whether a receiving GP can safely identify what is known, what action is requested, and what requires verification.

- Check that material patient facts, medicines, actual-use claims, allergies/ADRs, symptoms and discrepancies are supported by the supplied sources.
- Check that recommendations are clear, practical and patient-specific, with appropriate conditions, monitoring and time frame when the evidence supports them.
- Flag unsupported diagnoses, normal findings, doses, pathology results, counselling, medicine use or cessation authority.
- Flag unsafe, internally inconsistent, ambiguous or insufficiently prioritised recommendations. Identify time-sensitive concerns only when supported by the evidence.
- Check that GP decision fields, signatures and any protected feedback sections remain unfilled unless the user specifically authorises otherwise.

Use current authoritative guidance when needed for a safety check, but do not present a recommendation as validated if relevant patient information is missing. Do not edit, sign, upload, email or otherwise distribute the report.

## Findings format

Return findings only, grouped by severity:

- **Critical:** apparent urgent safety risk or unsafe recommendation.
- **Major:** material discrepancy, unsupported claim, omission or unclear GP action that should be resolved before delivery.
- **Minor:** clarity or usability improvement that does not alter clinical meaning.

For every finding, state the report section, supporting source evidence, why it matters to the receiving GP, and the corrective question or action. State `No findings` only after reviewing the complete report and all available relevant sources. The report owner resolves findings and retains responsibility for any revisions and final approval.
