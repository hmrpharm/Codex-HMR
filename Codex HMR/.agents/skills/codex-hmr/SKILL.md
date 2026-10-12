---
name: codex-hmr
description: Complete Australian initial HMR/DMMR reports for Mike Lau from a patient's referral, interview and supporting evidence using two approved original Word templates, with medication reconciliation, clinical and formatting QA, and verified Google Drive uploads.
---

# Codex HMR

Produce one clinical review and exactly two final Word reports, using the original templates. Keep clinical notes, profiles, reconciliation and QA internal; do not deliver extra files or appendices. Use the patient's name for the chat title where supported.

## Authority and required inputs

The approved October 2026 master prompt is authoritative for this workflow. Retrieve its current approved content from Google Doc `1c4my3pxyDarff_RZq7JAwz7BETtpd-T8zSAahfDzB84` in HMR Database / Master Prompts. Confirm parent membership using [source-manifest.json](references/source-manifest.json). Its current instructions supersede this packaged snapshot; do not assume newest modification means approved. Resolve material approval ambiguity before finalising. User instructions govern any explicit changes.

This intentionally supersedes the historical four-output workflow and generic “Not stated” missing-data convention. Unconfirmed actual-regimen cells stay blank; omit undiscussed narrative and leave unsupported optional fields blank. Explain safety-critical uncertainty explicitly.

Read [Google Drive workflow](references/google-drive-workflow.md) and [template map](references/template-map.md) before retrieval. Obtain both original DOCX templates from the approved Templates folder only. Inspect every provided source for this patient. Missing mandatory templates or essential clinical evidence require the user's input; continue independent preparation, but do not fabricate completion. Optional examples may be used only from Approved Formatting References and never supply patient facts.

## Patient attachment filing

After the patient's identity is confirmed from the supplied sources, automatically file each patient-specific attachment supplied for that run in `HMR Database / Referrals / FirstName LastName`, preserving its original format and filename. Reuse the exact existing folder under `Referrals` or create it once if absent; never use the similarly named `Patient Reports` folder for source attachments. Do not file generic instructions, templates, skill packages, or attachments that cannot be confidently tied to that patient. Before uploading, inspect the destination for a matching filename and content where the connector exposes comparison metadata: skip an already-filed identical attachment; retain an existing non-identical file and give the new attachment a clear received-date suffix rather than overwriting it. Verify each successful upload by metadata readback, including filename and parent. If identity, destination or upload result is ambiguous, preserve the local attachment and request clarification rather than risk filing it under another patient. Do not alter sharing settings, convert files or send them externally.

## Clinical review

Read [clinical reconciliation](references/clinical-reconciliation.md) in full. Internally reconcile every prescribed medicine once, then populate both reports from the same verified facts and recommendations. Maintain source/date and confidence for material discrepancies. The referral records prescribed therapy; interview/current administration evidence establishes actual use. A photograph or recommended change does not prove use. Keep patient-stated purpose distinct from inferred indication. Do not invent counselling, normal findings or cessation authority.

Use current Australian clinical guidance for patient-specific recommendations and verify relevant contraindications, interactions, renal/hepatic function, frailty, transitions and monitoring. Search using de-identified clinical terms only. Do not claim access to AMH or Therapeutic Guidelines if unavailable; use accessible authoritative Australian sources and disclose material evidence gaps to the user. Obtain missing essentials or make the GP action conditional instead of inventing a dose. GP decides prescribing. High-risk or complex findings warrant additional clinical scrutiny; this skill does not automatically switch models, create other chats or send patient information elsewhere.

When an authorised signed-in Clinical Knowledge Network (CKN) browser session is available, use its linked Australian medicines and clinical-reference resources to support the above checks. Treat CKN access as optional and session-dependent: do not attempt sign-in, save credentials, bypass access controls or claim CKN verification when the resource could not be opened. Search CKN only with de-identified clinical terms; never enter patient-identifying information, upload patient files or transmit report contents to CKN or its linked services.

## Populate and verify

Read [formatting](references/formatting.md), [template map](references/template-map.md) and [QA](references/qa.md). Work on copies of the retrieved originals; never rebuild or globally restyle them. Use the available document-editing skill/runtime for DOCX handling and rendering. The portable checker needs Python 3 standard library only; rendering requires a capable local document runtime and Montserrat font.

New patient-specific text is Montserrat 10 pt regular pure black, left aligned and top-left in cells, without highlighting or added shading. Preserve headings, branding, boilerplate, layout and protected forms. Remove sample content, unsupported stock statements, contradictory options, unused counselling headings and entirely unused medication rows only in editable clinical regions. Never compact feedback or signature spacing.

Run `python3 scripts/validate_docx.py TEMPLATE.docx REPORT.docx --kind dmmr` (or `hmr`) for each report. Read [validation guide](references/validation-guide.md) for scope, findings and limitations. Resolve every finding or establish that it is a permitted original-template feature. The checker is read-only and is not clinical approval. Complete the clinical checklist and independently render/inspect every page of both final files. Recheck after corrections. If rendering is unavailable, report the limitation; do not claim visual QA passed or deliver as fully checked.

## Save and deliver

Use exactly `FirstName_LastName_Follow_Up_HMR.docx` and `FirstName_LastName_HMR_Pharmacist.docx`, despite this being an initial review. Upload both without conversion to HMR Database / Patient Reports / FirstName LastName, after successful QA. Reuse the verified patient folder and inspect existing filenames. Do not overwrite approved, signed or historical reports without explicit permission. Verify uploads and return only the two verified report links (optional local DOCX links) and patient-folder link. If an upload fails, preserve the files, check for accidental duplicates, retry once through a supported route, then report the failure and local download links. Never claim saved means clinically approved or sent; emailing or external sharing needs separate authorisation.

## Package privacy

Do not add patient sources, examples, completed reports, credentials, signed URLs or validation output to this skill. Original templates are retrieved at use time; they are deliberately not bundled because sample patient content exists in the originals. Keep per-patient working artifacts outside the installed skill. Synced project sources remain read-only.
