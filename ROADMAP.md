# ULTRA FORCE Roadmap

This file tracks the product roadmap requested for the OCR, reconciliation, and accounting workspace.

Status key:

- `planned`
- `in_progress`
- `done`

## 1. Reconciliation Workspace

Status: `done`

Goal:
- Dedicated workspace for bank transactions needing action
- Side-by-side review of bank row and linked receipt/invoice
- Approve, reject, mark not needed, and review unresolved items

Current progress:
- Bank reconciliation logic exists
- Dashboard drill-down exists
- Linked record modal exists
- Dedicated `Reconciliation` tab added to the web app
- Queue filters, prioritization, pagination, detail panel, and session review actions added

## 2. Review Queue

Status: `done`

Goal:
- Queue for `missing_receipt`, `low_confidence`, duplicates, parsing issues, and unresolved matches

Current progress:
- Dedicated `Review Queue` tab added
- Queue covers `missing_receipt`, `low_confidence`, `duplicate_suspect`, and `parsing_issue`
- Filters, pagination, issue detail panel, and open-document actions added

## 3. Vendor Normalization Table

Status: `done`

Goal:
- Maintain canonical vendors and aliases
- Reuse normalized vendors across reconciliation and dashboarding

Current progress:
- Dedicated `Vendors` tab added
- Canonical vendor override storage added per project
- Variant grouping and canonical rename workflow added
- Canonical vendor names are now reused across major UI views
- Vendor aliases are now persisted through backend APIs

## 4. Rule Engine

Status: `done`

Goal:
- User-defined rules for classification, exclusion, and tagging

Current progress:
- Dedicated `Rules` tab added
- Project-scoped keyword rules added
- Rules can suggest status, category, and subcategory
- Rule-derived status now affects dashboard-style reconciliation logic
- Rules are now persisted through backend APIs and project storage

## 5. Categories And Accounting Tags

Status: `done`

Goal:
- Category, subcategory, cost center, project code, VAT/tax flags, payment method

Current progress:
- Dedicated `Tags` tab added
- Per-record accounting tags can now be saved
- Category and subcategory can also be suggested from rules
- Tags now persist in stored document records through backend APIs

## 6. Exception Intelligence

Status: `done`

Goal:
- Detect duplicates, refunds, reversals, split payments, repeated charges, and mismatches

Current progress:
- Review Queue now detects duplicates, repeated charges, refund/reversal language, and credit rows that likely need special handling
- Dedicated `Exceptions` tab added with grouped server-side cases for installment chains, refund pairs, split payment groups, duplicate clusters, and amount mismatch cases

## 7. Human Feedback Loop

Status: `done`

Goal:
- Learn from manual corrections and confirmed/rejected matches

Current progress:
- Reconciliation review actions now persist review state and notes in stored documents
- Manual document corrections and tagging flow back into persisted records
- Dedicated `Feedback` tab added with server-side alias and rule suggestions derived from repeated corrections and review outcomes, plus one-click apply actions into vendor aliases and project rules

## 8. Processed Resources Center

Status: `done`

Goal:
- Stronger source-level status, warnings, timing, rerun controls, and quality summaries

Current progress:
- Dedicated `Processed Resources` tab exists
- Resource summary and detail data now have paginated backend support
- Source-level evidence export now exists through project evidence-pack export
- Source-level diagnostics, activity history, rerun controls, health scoring, and resource detail pagination are now exposed directly in the UI and backend

## 9. Better Dashboards

Status: `done`

Goal:
- Stronger financial, reconciliation, trend, and anomaly dashboards

Current progress:
- KPI cards, charts, drill-down, filters, and processed resources were added
- UX/UI refinement pass completed
- Overview analytics are now server-side
- Overview now includes period comparison, unresolved aging snapshot, and exception snapshot with drill-down support
- Dashboard drill-down, reconciliation, review queue, and processed resource views now use server-side analytics or pagination where needed for larger projects

## 10. Attachments And Evidence Pack

Status: `done`

Goal:
- Multiple attachments, notes, and exportable audit evidence packs

Current progress:
- Dedicated `Evidence` tab added
- Document-level attachments can now be added, listed, removed, and included in exported evidence packs
- Attachment types, evidence preview/open flow, audit summary context, and richer evidence-pack manifests are now added

## 11. Global Search And Saved Searches

Status: `done`

Goal:
- Search across OCR text, vendors, references, amounts, files, and saved filters

Current progress:
- Dedicated `Search` tab added with paginated project-wide search across stored documents
- Search can filter by kind, status, and confidence and inspect matched/explainable context
- Saved searches are now supported for the Search workspace
- Saved searches can now also be deleted from the UI

## 12. Multi-User Readiness

Status: `in_progress`

Goal:
- Roles, task assignment, comments, and stronger collaboration controls

Current progress:
- Project/file ownership checks are enforced on the backend
- Project-scoped comment API groundwork was added for future collaboration flows
- Review Queue now surfaces project comments on document-level issues
- User role groundwork and evidence/comment collaboration structures were added in the backend
- Project member records and member-management UI are now added
- Review Queue now supports assignment of issues to project members
- Shared members can now access the main project workspaces according to project role
- Activity, comments, and resource history now include actor usernames for a clearer audit trail
- Company-level procurement exception workflow now also supports assignee, note, and review-state tracking

## 13. Data Trust And Explainability

Status: `done`

Goal:
- Why a match happened, why a row was excluded, parsing warnings, and traceability

Current progress:
- Review Queue and Search detail panels now surface explainability text, match basis, and source trace context
- Raw OCR text is exposed directly in the search detail panel for auditability
- Serialized records now include structured explainability, parser warnings, provenance, and field-level confidence breakdown
- Linked-record modal and Reconciliation detail now also surface explainability, warnings, confidence, and traceability, with match factors derived from stored match basis
- Accounting and matching flows now also expose clearer reasons for blocked drafts, skipped undated drafts, and missing-period handling

## 14. Import/Export Maturity

Status: `in_progress`

Goal:
- Accountant-friendly exports, ERP mappings, unresolved item exports, and close packages

Current progress:
- Project now supports direct unresolved CSV export from stored records
- Project now supports evidence-pack ZIP export and document-level attachments
- Accounting export presets are now being added for ERP/accounting-targeted CSV layouts and preset-aware close packages
- Company-level AP and AR aging summaries are now added under `Companies`, using supplier/customer master matching and company document exposure
- Company-level settlement allocations are now supported so payment rows can be allocated against AP/AR targets and open balances update accordingly
- Company-level AP and AR candidate tables are now paginated server-side, giving supplier-bill and customer-invoice review views beyond the summary cards
- Company-level accounting export presets, close-package exports, journal posting groundwork, procurement control, receipt tracking, and procurement exception workflow are now all part of the operational export/readiness layer

## Construction Accounting Expansion

Status: `in_progress`

Goal:
- Evolve ULTRA FORCE from reconciliation into a construction-oriented accounting system for an AC contractor.

Current progress:
- Detailed phased roadmap added in [CONSTRUCTION_ACCOUNTING_ROADMAP.md](/Users/engagendy/RiderProjects/invo/CONSTRUCTION_ACCOUNTING_ROADMAP.md)
- Phase 1 `Accounting Foundation` is now active
- Phase 1 now includes a company-level `Accounting` workspace with chart of accounts, accounting periods, journal drafts, manual journals, trial balance, and general ledger
- Company settings, supplier/customer masters, and project-code/cost-center dimension masters are now added under `Companies`
- Phase 2 `AP And Procurement` and Phase 3 `AR And Contract Billing` are now started with company-level AP/AR aging summaries and settlement allocation workflow
- Phase 4 `Construction Job Costing` is now started with project master fields, cost code master data, and a first budget-vs-actual job costing summary
- Construction job costing now also includes contract-billing fields and WIP-style company summary metrics such as certified revenue, billed-to-date, retention, and unbilled WIP
- Companies now also include a construction billing-event log so WIP and billed summaries can be driven by progress claims, milestones, variations, and retention rows
- Companies now also include purchase orders so committed project cost can be tracked separately from actual cost
- Companies finance now includes procurement control summary across committed, billed, paid, and open PO exposure
- Companies procurement now includes receipt tracking so committed, received, billed, and paid can be seen together
- Companies procurement now includes explicit bill-to-PO linking, procurement exceptions, review workflow state, and company-level activity tracking for procurement actions
