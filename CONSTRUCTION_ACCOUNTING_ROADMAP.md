# ULTRA FORCE Construction Accounting Roadmap

This roadmap expands ULTRA FORCE from an OCR and reconciliation workspace into a construction-focused accounting system for an AC contractor.

Status key:

- `planned`
- `in_progress`
- `done`

## Phase 1. Accounting Foundation

Status: `done`

Goal:
- Establish the accounting structures that every downstream workflow depends on.

Scope:
- Chart of accounts
- Account types and account codes
- Accounting periods and close locks
- Journal entry groundwork
- Export presets for accounting and ERP handoff

Current progress:
- Export presets are now being added for accountant and ERP-oriented exports
- Close workspace is being extended into an accounting export control point
- Company-level chart of accounts and accounting periods workspace is now added
- Construction AC contractor seed accounts are now available as a starting COA
- Record-level primary/offset account mapping, derived journal drafts, manual journals, and general ledger are now added as posting groundwork
- Accounting foundation ownership is now company scope, with projects acting as costing dimensions into the same company book
- Posted journal entries, trial balance, ledger filters, draft-quarter seeding, missing-quarter creation for drafts, and company auto-posting rules are now in place

## Phase 2. AP And Procurement

Status: `in_progress`

Goal:
- Control supplier spend from request through payment.

Scope:
- Supplier master
- Purchase requests
- Purchase orders
- Goods/service receipt
- Supplier invoice capture
- 3-way match
- Payment vouchers
- Retention payable

Current progress:
- Supplier master is now added at company level
- AP aging summary is now available under `Companies`
- Supplier exposure is now matched from company documents against supplier master names
- Settlement allocation is now available so payment rows can be allocated to supplier bill exposure
- Paginated supplier bill candidate table is now available under `Companies`
- Company-level purchase order log is now added so committed cost can be tracked before actual supplier billing
- Procurement control summary is now added to compare committed PO value against billed supplier exposure and paid allocations by project and supplier
- Goods/service receipt log is now added so procurement control can show committed, received, billed, and paid progression
- Supplier bills can now be linked explicitly to purchase orders
- Procurement exceptions now have workflow state, assignee, note, and company activity history

## Phase 3. AR And Contract Billing

Status: `in_progress`

Goal:
- Track customer billing and collection around projects and contracts.

Scope:
- Customer master
- Contracts and line items
- Progress billing
- Milestone billing
- Variation orders
- Retention receivable
- Credit/debit notes
- Collection tracking and aging

Current progress:
- Customer master is now added at company level
- AR aging summary is now available under `Companies`
- Customer exposure is now matched from company documents against customer master names and revenue-tagged records
- Settlement allocation is now available so receipt rows can be allocated to customer invoice exposure
- Paginated customer invoice candidate table is now available under `Companies`
- Company-level billing event log is now added for progress claims, milestones, variations, retention invoices, debit notes, and credit notes
- Company job costing now consumes billing events to drive billed-to-date and variation values

## Phase 4. Construction Job Costing

Status: `in_progress`

Goal:
- Turn every supplier invoice, bank transaction, and receipt into project cost intelligence.

Scope:
- Project master
- Sites and contracts
- Cost codes
- Budget vs actual
- Committed vs actual cost
- WIP
- Project profitability
- Overhead allocation
- Labor, material, subcontractor, and equipment cost buckets

Current progress:
- Project master fields now include job code, client, site, contract number, budget, and project status
- Cost code master data is now available under `Companies`
- First company-level budget-vs-actual job costing summary is now available using project codes and tagged cost codes
- Project master now also carries contract value, variation value, billed-to-date, certified progress, retention percent, and advance received
- Companies job costing now includes certified revenue, billed value, retention, and unbilled WIP summary fields per project
- Job costing now consumes company billing events so billed-to-date and variation values can come from actual billing rows instead of only project master totals
- Job costing now also consumes company purchase orders so committed cost can be compared against actual project cost
- Company UI now includes project management, company directory, company settings, cost codes, and project/job-code alignment under `Companies`

## Phase 5. Inventory, Stores, And Site Material Control

Status: `planned`

Goal:
- Track material movement and consumption by site.

Scope:
- Item master
- Units of measure
- Warehouse and site stores
- Stock transfer
- Material issue and return
- Material consumption by project
- Reorder alerts

## Phase 6. Labor, Payroll, And Equipment Costing

Status: `planned`

Goal:
- Push labor and equipment into project cost visibility.

Scope:
- Employee and labor master
- Timesheets by project and cost code
- Payroll import/export
- Labor cost allocation
- Equipment register
- Equipment usage logs
- Maintenance and fuel
- Depreciation / internal charge-out

## Phase 7. Treasury, VAT, And Compliance

Status: `planned`

Goal:
- Make the product operational for real UAE accounting control.

Scope:
- Full bank reconciliation
- Cash accounts and cheque handling
- Payment scheduling
- UAE VAT setup and reporting
- Tax invoice checks
- Audit logs and approval trails
- Lock periods and close checklist

## Phase 8. Financial Statements And Management Reporting

Status: `in_progress`

Goal:
- Produce accounting outputs, not just operational exports.

Scope:
- AP aging
- AR aging
- Trial balance
- P&L
- Balance sheet
- Cash flow
- Project profitability dashboard
- Budget vs actual by project and cost code
- Retention summary
- Unbilled/WIP summary

Current progress:
- AP aging, AR aging, trial balance, general ledger, project profitability summary, budget-vs-actual summary, retention summary fields, and unbilled/WIP summary fields are now available
- Full financial statements are still the main remaining gap in this phase

## Phase 9. Collaboration And Controls

Status: `planned`

Goal:
- Support maker-checker workflows and accounting approvals safely across multiple users.

Scope:
- Approval flows
- Role-based accounting permissions
- Assignment queues
- Review ownership
- Audit logs per action
- Close approvals
