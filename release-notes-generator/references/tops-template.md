# TOPS Release Note Template Reference

This reference contains the complete 43-column structure for enterprise/TOPS-compliant release notes.

## Quick Reference: Column Groups

| Section | Columns | Purpose |
|---------|---------|---------|
| Core Metadata | A-L (12 cols) | Release identity, status, tracking |
| Change Description | M-P (4 cols) | Business justification, RCA |
| Technical Details | Q-X (8 cols) | Files, DB, env, API changes |
| Testing & Sign-Off | Y-AD (6 cols) | Regression, evidence, sign-offs |
| Deployment & Rollback | AE-AQ (13 cols) | Plans, dependencies, status |

## Column Details

### A: Release
- Example: `RT_2 Hot Fix - 1`
- Format: `[Project]_[Sprint] [Type] - [Number]`

### B: Feature/Fix Title
- One-line description
- Should be clear to non-technical stakeholders
- Example: `Fix subscription lookup for unlinked users`

### C: Module
- Service area affected
- Examples: `Inbound`, `Outbound`, `Order Management`, `Customer`, `Analytics`

### D: Type
- **Bug Fix**: Corrects existing broken functionality
- **Feature**: New capability
- **Config**: Configuration change only
- **Env**: Environment variable change
- **DB**: Database schema/data change

### E: Category
- **APK**: Mobile app changes (Android/iOS)
- **Non-APK**: Backend/web changes
- **Independent**: No dependencies

### F: Source/Ticket ID
- DevRev/Jira ticket ID: `ISS-286043`
- Or `Internal` if no ticket

### G: PR Link
- Full GitHub PR URL
- Example: `https://github.com/org/repo/pull/816`

### H: Development Status
- `Completed` | `In Progress` | `Pending`

### I: Sanity Testing Status
- `Completed` | `Pending`

### J: Deployment Environment
- `SIT` | `UAT` | `Production`

### K: Deployment Status
- `Pending` | `Deployed` | `Rolled Back`

### L: ETA
- Target date: `21-Apr-2026`

### M: Change Description & Business Justification
- Why is this change needed?
- What business problem does it solve?
- What is the impact if not done?

### N: Root Cause Analysis (Bug Fix only)
- What was broken?
- Which workflow and users affected?
- Plain language, no code

### O: Solution Provided (Bug Fix only)
- What was fixed?
- Correct behavior post-fix?
- Plain language, no code

### P: Requirement Description (Feature only)
- What capability is being introduced?
- Who requested it?
- Expected outcome?

### Q: Files/Services Changed
- List all changed files with service/module
- Example: `create_grn.py — Inbound GRN`

### R: Impacted Components/Image Tags
- Service name + image tag
- Example: `stockone-wms: v2.0.5`
- Include SIT, UAT, PROD tags if different

### S: Env Variable Changes
- Format: `Variable | Before: old | After: new`
- Or `None`

### T: DB Changes (Y/N)
- `Yes` or `No`

### U: DB Column Affected
- Table.column: `orders.cancelled_quantity`
- Or `N/A`

### V: DB Rollback Script Available
- `Yes` | `No` | `N/A`

### W: New Config/Feature Flag Keys
- Format: `Key | Type | Default | Effect`
- Or `None`

### X: API Contract Changes
- Route, payload, response changes
- Or `None`

### Y: Regression Testing Scope
- List all test scenarios
- Cover happy path and edge cases

### Z: Regression Testing Result
- `PASS` | `FAIL` | `PARTIAL`
- If FAIL: explain gap and risk acceptance

### AA: Test Evidence
- Format: `Environment | Date | Tester | Evidence link`

### AB: RCA Document Reference
- Link to RCA document
- Or `Inline — see column N`

### AC: DEV SIGN-OFF (MANDATORY)
- Format: `[ ] Name: ___ | Date: ___`
- Dev certifies code complete and reviewed

### AD: QA SIGN-OFF (MANDATORY)
- Format: `[ ] Name: ___ | Date: ___`
- QA certifies regression tested, no blockers

### AE: Pre-Deployment Validation
- Checklist with owners
- Example: `1. Confirm image tag ✓ | 2. Seed config ✓`

### AF: Post-Deployment Validation
- Validation steps after deploy
- Example: `1. Validate in PROD | 2. Monitor logs 30min`

### AG: Deployment Plan
- Step-by-step with owner and time
- Format: `Step 1 — Action — Owner — ~X min`

### AH: Rollback Plan
- Steps to rollback with owner and ETA
- Example: `1. Revert to vX.X.X | 2. Owner: DevOps | 3. ETA: <30 min`

### AI: Dependencies
- Other teams/systems required
- Or `None`

### AJ: Configurations Pre-Deployment
- Config keys, env vars, DB seeds needed
- Or `None`

### AK: Deployment Note
- Brief note: `Backend-only. Zero downtime.`

### AL: APK/Non-APK Dependency
- `Independent` | `Depends on APK vX.X` | `Depends on Non-APK`

### AM: Backend Changes (Y/N)
- `Yes` | `No`

### AN: APK Changes (Y/N)
- `Yes` | `No`

### AO: Configurations Done (Y/N)
- `Yes` | `No`

### AP: Remarks
- Additional info, workarounds, FC communications

### AQ: Last Updated
- Format: `DD-MMM-YYYY`

## Deployment Windows

| Day | Window |
|-----|--------|
| Monday – Wednesday | 24×7 |
| Thursday | Morning only (before noon) |
| Thu afternoon – Sunday | ❌ No deployments |
| Emergency | Explicit TOPS approval required |

## Sign-Off Rules

1. Dev sign-off required before sharing with RIL
2. Explicit QA sign-off must appear in release note
3. Notes without dual sign-off will be rejected
4. Submit T-2 business days before PROD deployment

## Failed Deployment Protocol

1. Rollback immediately per plan
2. Joint RCA within 24 business hours
3. RCA covers: root cause, why testing missed it, corrective measures
4. Redeployment = fresh release (full process)
