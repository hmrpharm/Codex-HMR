# Original template handling

The two Word originals were retrieved from the approved Templates folder on 11 October 2026. IDs and byte hashes are in source-manifest.json; hashes identify this inspection, not future approval. Re-inspect structure whenever originals change. Never substitute an example report.

## DMMR Australia

The original has demographics, clinical discussion, issues/GP plan, GP signature/return instructions, formal letter, allergies, non-use/additional medicines/supplements, a four-column medication table, disclaimer, follow-up, pharmacist closing and feedback. It contains sample patient details, doses, histories, stock counselling and unsupported normal findings. Remove all sample clinical content, including text boxes and repeated letter metadata, before filling a working copy. Do not retain an apparent default “Yes” follow-up or “No known allergies” without evidence.

The feedback begins with `Thank you for your referral to DMMR Australia`; everything from this paragraph through the final section properties is protected. Also preserve the preceding disclaimer, follow-up and all intentional whitespace, signature/date and return fields. Complete only authorised pharmacist closing fields. The original medication heading contains a statement about bold discrepancies; preserve formal original wording but keep all newly entered patient text regular as the master prompt requires. Describe discrepancies in the comments column.

## HMR Pharmacist

The original has pharmacist/patient detail tables, clinical sections, a letter table, four-column medication table, issues/GP decision table, closing, signature/return block and feedback. Replace placeholder instructions and complete authorised identity fields with master-prompt details. Preserve business-specific return/contact information. Do not retain the original top email or closing qualification variants when they conflict with the master-prompt pharmacist identity instructions.

The feedback begins with the table containing `Thank you for your referral to HMR Pharmacist`; preserve it and everything after it, including rating tables, empty comment areas, Yes/No and Not known options, footer and section properties. Also preserve GP signature/return and disclaimer/follow-up blocks before it.

## Editing boundaries

Locate regions by text and structure, not fixed paragraph indices. Preserve all four medication column headings verbatim. Extra medicine rows may be copied from a clean original data row when needed; remove wholly unused data rows, never header or form rows. Preserve widths, borders, merges and original section/page settings. Avoid assigning entire cell or paragraph text when it would erase required runs, fields, links or drawings. Keep patient-specific additions out of protected regions except existing pharmacist/letter fields expressly authorised by the prompt. No handwritten signature without a supplied signature.
