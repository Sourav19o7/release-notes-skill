---
name: release-notes-generator
description: Generate comprehensive release notes from git branches, commits, and changes. Use this skill whenever the user asks to create release notes, generate a changelog, document what's new, write release documentation, summarize changes between versions, create a release doc, or mentions "what's changed", "what's new", "release summary", "version notes", or "changelog". Also trigger when users want to document SDK changes, library updates, module modifications, or any code changes for a release. Supports both standard markdown format AND enterprise TOPS-compliant format with full deployment/rollback tracking, sign-offs, and RCA documentation.
---

# Release Notes Generator

Generate professional, categorized release notes by analyzing git history, branches, and code changes. Supports two output formats:
- **Standard Format**: Markdown (.md) and Word (.docx) - ideal for open-source projects and general releases
- **Enterprise/TOPS Format**: Comprehensive 43-column structure with deployment tracking, sign-offs, and compliance fields - ideal for enterprise clients (JioMart, RIL, etc.)

## Overview

This skill analyzes your repository to create structured release notes that include:
- Categorized changes (features, fixes, breaking changes, etc.)
- Affected SDKs, libraries, and modules
- Commit details with authors and timestamps
- Comparison between branches or tags
- **Enterprise Mode**: Full deployment planning, RCA documentation, and sign-off tracking

## Output Format Selection

Ask the user which format they need:

| Format | Best For | Output |
|--------|----------|--------|
| **Standard** | Open-source, internal teams, general releases | Markdown + Word document |
| **Enterprise/TOPS** | JioMart, RIL, enterprise clients with compliance requirements | CSV (Google Sheets compatible) + Markdown summary |

If the user mentions "TOPS", "JioMart", "RIL", "enterprise", "compliance", "sign-off", "deployment plan", or "rollback", default to Enterprise format.

## Prerequisites

Ensure you have:
- A git repository with commit history
- GitHub CLI (`gh`) installed and authenticated (for PR/issue integration)
- Python 3 with `python-docx` package (for .docx generation)

Check prerequisites:
```bash
git --version && gh auth status && python3 -c "import docx; print('python-docx OK')" 2>/dev/null || echo "Install: pip install python-docx"
```

## Workflow

### Step 1: Gather Context

Ask the user for:
1. **Version/Release name**: e.g., "v2.1.0", "March 2024 Release"
2. **Comparison range**: What to compare against
   - Between two branches: `main...feature-branch`
   - Between two tags: `v1.0.0...v2.0.0`
   - Since last tag: `$(git describe --tags --abbrev=0)...HEAD`
   - Last N commits: `HEAD~N...HEAD`
3. **Output location**: Where to save the release notes (default: `./release-notes/`)

If the user doesn't specify, suggest sensible defaults based on the repository state.

### Step 2: Analyze Git History

Run these commands to gather data:

```bash
# Get commit log with details
git log <range> --pretty=format:'%H|%an|%ae|%ad|%s' --date=short

# Get changed files summary
git diff <range> --stat

# Get list of modified directories (to identify affected modules)
git diff <range> --name-only | cut -d'/' -f1-2 | sort -u
```

### Step 3: Fetch GitHub Context (if available)

Use GitHub CLI to enrich the release notes:

```bash
# Get merged PRs in the range
gh pr list --state merged --base main --json number,title,author,labels,body --limit 100

# Get linked issues
gh issue list --state closed --json number,title,labels,body --limit 100
```

### Step 4: Categorize Changes

Organize commits and PRs into these categories based on commit message prefixes, PR labels, or content analysis:

| Category | Triggers (prefixes/labels) |
|----------|---------------------------|
| **Breaking Changes** | `BREAKING:`, `breaking-change` label, `!:` |
| **New Features** | `feat:`, `feature:`, `add:`, `enhancement` label |
| **Bug Fixes** | `fix:`, `bugfix:`, `bug` label |
| **Performance** | `perf:`, `performance:`, `optimization` |
| **Documentation** | `docs:`, `documentation` label |
| **Refactoring** | `refactor:`, `chore:` |
| **Dependencies** | `deps:`, `dependency`, changes in `package.json`, `requirements.txt`, etc. |
| **Security** | `security:`, `security` label |
| **Deprecations** | `deprecate:`, `deprecated` |

### Step 5: Identify Affected Components

Analyze changed file paths to determine affected:

- **SDKs**: Look for `/sdk/`, `/client/`, language-specific directories (`/python/`, `/js/`, `/go/`)
- **Libraries**: Check `/lib/`, `/packages/`, dependency files
- **Modules**: Top-level directories, `/src/modules/`, `/components/`
- **APIs**: `/api/`, `/routes/`, `/endpoints/`
- **Infrastructure**: `/infra/`, `/deploy/`, `/ci/`, `.github/`

Create a summary table of affected components.

### Step 6: Generate Release Notes

Create the release notes with this structure:

```markdown
# Release Notes: [Version/Name]

**Release Date:** [Date]
**Comparison:** [range]

## Summary

[2-3 sentence overview of the release highlights]

## Affected Components

| Component | Type | Changes |
|-----------|------|---------|
| [name] | SDK/Library/Module | [brief description] |

## Breaking Changes

> **Action Required:** Review these changes before upgrading.

- [Change description] ([#PR](link)) - @author

## New Features

- [Feature description] ([#PR](link)) - @author

## Bug Fixes

- [Fix description] ([#PR](link)) - @author

## Performance Improvements

- [Improvement description] ([#PR](link)) - @author

## Documentation

- [Doc change description] ([#PR](link)) - @author

## Dependencies

- [Dependency update] ([#PR](link))

## Other Changes

- [Other change] ([#PR](link)) - @author

## Contributors

Thank you to all contributors for this release:
- @contributor1
- @contributor2

## Full Changelog

[Link to compare view on GitHub]
```

### Step 7: Generate Output Files

#### Markdown Output

Save the release notes to `release-notes-[version].md`.

#### Word Document Output

Create a Python script to convert Markdown to .docx:

```python
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re

def create_release_notes_docx(markdown_content, output_path):
    doc = Document()

    # Set up styles
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)

    lines = markdown_content.split('\n')

    for line in lines:
        if line.startswith('# '):
            p = doc.add_heading(line[2:], level=0)
        elif line.startswith('## '):
            doc.add_heading(line[3:], level=1)
        elif line.startswith('### '):
            doc.add_heading(line[4:], level=2)
        elif line.startswith('- '):
            doc.add_paragraph(line[2:], style='List Bullet')
        elif line.startswith('> '):
            p = doc.add_paragraph(line[2:])
            p.style = 'Intense Quote'
        elif line.startswith('|'):
            # Handle tables - simplified
            continue
        elif line.strip():
            doc.add_paragraph(line)

    doc.save(output_path)
    print(f"Created: {output_path}")

# Usage
create_release_notes_docx(markdown_content, "release-notes.docx")
```

Save this script and run it to generate the .docx file.

### Step 8: Present to User

After generating both files:
1. Show a preview of the release notes in the conversation
2. Provide the file paths
3. Ask if any adjustments are needed (tone, categorization, missing items)

## Tips for Best Results

- **Conventional Commits**: If the repo uses conventional commits (`feat:`, `fix:`, etc.), categorization will be more accurate
- **PR Labels**: GitHub labels help with categorization - encourage teams to use them
- **Scope in commits**: `feat(sdk):` helps identify affected components
- **Link PRs to issues**: Makes the changelog more meaningful

## Customization Options

Ask users if they want to customize:
- Category names or groupings
- Output template/format
- Level of detail (summary vs. detailed)
- Whether to include contributor list
- Company branding or headers

## Error Handling

- **No git repo**: Prompt user to navigate to a git repository
- **No commits in range**: Suggest a different comparison range
- **GitHub CLI not authenticated**: Guide through `gh auth login`
- **python-docx not installed**: Offer to install with `pip install python-docx`

---

# Enterprise/TOPS Format (JioMart 3P Compliant)

When generating release notes for enterprise clients with compliance requirements, use this comprehensive format based on the TOPS directive.

## TOPS Format Overview

The enterprise format uses 43 columns organized into 5 sections. Each fix/feature/config change gets one row.

### Section 1: Core Metadata (Columns A-L)

| Column | Field | How to Populate |
|--------|-------|-----------------|
| A | Release | Release name and version from user input (e.g., `RT_2 Hot Fix - 1`) |
| B | Feature/Fix Title | One-line title from commit message or PR title |
| C | Module | Extract from file paths: `Inbound`, `Outbound`, `Order Management`, etc. |
| D | Type | `Bug Fix` / `Feature` / `Config` / `Env` / `DB` - determine from commit prefix |
| E | Category | `APK` / `Non-APK` / `Independent` - based on changed files |
| F | Source/Ticket ID | Extract from commit message (e.g., `ISS-286043`) or PR body |
| G | PR Link | Full GitHub PR URL from `gh pr list` |
| H | Development Status | `Completed` for merged PRs, `In Progress` for open |
| I | Sanity Testing Status | Default `Pending` - user fills in |
| J | Deployment Environment | `SIT` / `UAT` / `Production` - user fills in |
| K | Deployment Status | `Pending` / `Deployed` / `Rolled Back` - user fills in |
| L | ETA | Target date - user fills in |

### Section 2: Change Description & Business Justification (Columns M-P)

| Column | Field | How to Populate |
|--------|-------|-----------------|
| M | Change Description & Business Justification | Expand PR description or commit body - explain WHY this change is needed |
| N | Root Cause Analysis (Bug Fix only) | For bug fixes: what was broken, which workflow/users affected. Plain language, no code. |
| O | Solution Provided (Bug Fix only) | What was fixed, correct behavior post-fix. Plain language, no code. |
| P | Requirement Description (Feature only) | Feature capability, who requested, expected outcome |

### Section 3: Technical Change Details (Columns Q-X)

| Column | Field | How to Populate |
|--------|-------|-----------------|
| Q | Files/Services Changed | From `git diff --name-only`, group by service/module |
| R | Impacted Components/Image Tags | Service name + image tag (extract from deployment files if available) |
| S | Env Variable Changes | Scan for `.env` changes or config updates. Format: `VAR | Before: old | After: new` |
| T | DB Changes (Y/N) | Check for migration files, SQL scripts, schema changes |
| U | DB Column Affected | Table.column names from migration files |
| V | DB Rollback Script Available | `Yes` / `No` / `N/A` |
| W | New Config/Feature Flag Keys | Extract from config files. Format: `Key | Type | Default | Effect` |
| X | API Contract Changes | Check for route/endpoint changes, OpenAPI spec updates |

### Section 4: Testing & Sign-Off (Columns Y-AD)

| Column | Field | How to Populate |
|--------|-------|-----------------|
| Y | Regression Testing Scope | List test scenarios - user fills in |
| Z | Regression Testing Result | `PASS` / `FAIL` / `PARTIAL` - user fills in |
| AA | Test Evidence | Environment, date, tester, evidence link - user fills in |
| AB | RCA Document Reference | For bug fixes: link to RCA or `Inline - see column N` |
| AC | **DEV SIGN-OFF** | `[ ] Name: ___ | Date: ___` - **MANDATORY** |
| AD | **QA SIGN-OFF** | `[ ] Name: ___ | Date: ___` - **MANDATORY** |

⚠️ **TOPS will reject release notes without both Dev and QA sign-off.**

### Section 5: Deployment & Rollback (Columns AE-AQ)

| Column | Field | How to Populate |
|--------|-------|-----------------|
| AE | Pre-Deployment Validation | Checklist of pre-deployment tasks with owners |
| AF | Post-Deployment Validation | Checklist of validations after deployment |
| AG | Deployment Plan | Step-by-step with owner and time estimate per step |
| AH | Rollback Plan | Steps to rollback, owner, ETA |
| AI | Dependencies | Other teams/systems this depends on |
| AJ | Configurations Pre-Deployment | Config keys, env vars, DB seeds needed before deploy |
| AK | Deployment Note | e.g., `Backend-only. Zero downtime. Rollback available.` |
| AL | APK/Non-APK Dependency | `Independent` / `Depends on APK vX.X` / `Depends on Non-APK` |
| AM | Backend Changes (Y/N) | Check if backend code changed |
| AN | APK Changes (Y/N) | Check if APK-related code changed |
| AO | Configurations Done (Y/N) | User fills in |
| AP | Remarks | Additional notes, workarounds, FC communications |
| AQ | Last Updated | Auto-generate: `DD-MMM-YYYY` |

## Enterprise Workflow

### Step 1: Gather Enterprise Context

In addition to standard context, ask for:
1. **Release Name**: e.g., `RT_2 Hot Fix - 1`
2. **Client/Project**: e.g., `JioMart 3P`
3. **Target Environment**: SIT, UAT, or Production
4. **Deployment Window**: Confirm timing (Mon-Wed 24x7, Thu morning only)
5. **Dev Sign-off Contact**: Name for column AC
6. **QA Sign-off Contact**: Name for column AD

### Step 2: Analyze with Enterprise Detail

Run additional analysis for enterprise fields:

```bash
# Check for database migrations
find . -name "*.sql" -newer $(git log -1 --format=%cd --date=short <range>^)
git diff <range> --name-only | grep -E "(migration|schema|sql)"

# Check for environment variable changes
git diff <range> -- "*.env*" ".env*" "*config*"

# Check for API changes
git diff <range> -- "*route*" "*endpoint*" "*api*" "*.yaml" "*.json" | head -100

# Identify APK vs Non-APK changes
git diff <range> --name-only | grep -E "(android|ios|mobile|app)" && echo "APK" || echo "Non-APK"
```

### Step 3: Generate CSV Output

Create a CSV file that can be directly imported to Google Sheets:

```python
import csv
from datetime import datetime

def generate_tops_csv(changes, output_path, release_info):
    """Generate TOPS-compliant CSV for Google Sheets import."""

    headers = [
        'Release', 'Feature/Fix Title', 'Module', 'Type', 'Category',
        'Source/Ticket ID', 'PR Link', 'Development Status', 'Sanity Testing Status',
        'Deployment Environment', 'Deployment Status', 'ETA',
        'Change Description & Business Justification',
        'Root Cause Analysis', 'Solution Provided', 'Requirement Description',
        'Files/Services Changed', 'Impacted Components', 'Env Variable Changes',
        'DB Changes (Y/N)', 'DB Column Affected', 'DB Rollback Script Available',
        'New Config Keys', 'API Contract Changes',
        'Regression Testing Scope', 'Regression Testing Result', 'Test Evidence',
        'RCA Document Reference', 'DEV SIGN-OFF', 'QA SIGN-OFF',
        'Pre-Deployment Validation', 'Post-Deployment Validation',
        'Deployment Plan', 'Rollback Plan', 'Dependencies',
        'Configurations Pre-Deployment', 'Deployment Note',
        'APK/Non-APK Dependency', 'Backend Changes (Y/N)', 'APK Changes (Y/N)',
        'Configurations Done (Y/N)', 'Remarks', 'Last Updated'
    ]

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for change in changes:
            row = [
                release_info['name'],
                change.get('title', ''),
                change.get('module', ''),
                change.get('type', ''),
                change.get('category', 'Non-APK'),
                change.get('ticket_id', 'Internal'),
                change.get('pr_link', ''),
                'Completed',
                'Pending',
                release_info.get('environment', 'UAT'),
                'Pending',
                release_info.get('eta', ''),
                change.get('description', ''),
                change.get('rca', 'N/A') if change.get('type') == 'Bug Fix' else 'N/A',
                change.get('solution', 'N/A') if change.get('type') == 'Bug Fix' else 'N/A',
                change.get('requirement', 'N/A') if change.get('type') == 'Feature' else 'N/A',
                change.get('files_changed', ''),
                change.get('components', ''),
                change.get('env_changes', 'None'),
                change.get('db_changes', 'No'),
                change.get('db_columns', 'N/A'),
                change.get('db_rollback', 'N/A'),
                change.get('config_keys', 'None'),
                change.get('api_changes', 'None'),
                '', '', '', '',  # Testing fields - user fills
                f"[ ] Name: {release_info.get('dev_signoff', '___')} | Date: ___",
                f"[ ] Name: {release_info.get('qa_signoff', '___')} | Date: ___",
                '', '', '', '',  # Deployment fields - user fills
                change.get('dependencies', 'None'),
                change.get('pre_configs', 'None'),
                change.get('deployment_note', ''),
                change.get('apk_dependency', 'Independent'),
                'Yes' if change.get('backend_change') else 'No',
                'Yes' if change.get('apk_change') else 'No',
                'No',
                '',
                datetime.now().strftime('%d-%b-%Y')
            ]
            writer.writerow(row)

    print(f"Created TOPS-compliant CSV: {output_path}")
```

### Step 4: Generate Summary Markdown

Also create a markdown summary for quick review:

```markdown
# Release Notes Summary: [Release Name]

**Client:** [Client Name]
**Release:** [Release Name]
**Target Environment:** [SIT/UAT/Production]
**Prepared by:** [Team Name]

## ⚠️ Pre-Release Checklist

- [ ] Dev Sign-Off obtained
- [ ] QA Sign-Off obtained
- [ ] Regression testing completed
- [ ] Deployment plan reviewed
- [ ] Rollback plan documented
- [ ] TOPS submission T-2 business days before deployment

## Change Summary

| Type | Count |
|------|-------|
| Bug Fixes | X |
| Features | X |
| Config Changes | X |

## Detailed Changes

[Include standard release notes sections here]

## Deployment Window Compliance

| Day | Window | Status |
|-----|--------|--------|
| Monday - Wednesday | 24x7 | ✓ OK |
| Thursday | Morning only | ⚠️ Check timing |
| Fri - Sun | ❌ No deployments | |

## Sign-Off Status

| Role | Name | Date | Status |
|------|------|------|--------|
| Dev Lead | [Name] | | ⬜ Pending |
| QA Lead | [Name] | | ⬜ Pending |

---

*Full details available in the Google Sheet: [Link]*
```

## Color Coding Reference (for Google Sheets)

When importing to Google Sheets, apply these colors:

### Header Row Colors

| Section | Columns | Color | Hex |
|---------|---------|-------|-----|
| Core Metadata | A-L | Deep Navy | `#1F3864` |
| Change Description | M-P | Navy Blue | `#2F5496` |
| Technical Details | Q-X | Dark Brown | `#7B3F00` |
| Testing & Sign-Off | Y-AD | Forest Green | `#375623` |
| Deployment & Rollback | AE-AQ | Dark Orange | `#C55A11` |

### Data Row Colors

| Condition | Color | Hex |
|-----------|-------|-----|
| Bug Fix row | Light Orange tint | `#FCE4D6` |
| Feature row | Light Blue tint | `#D6E4F7` |
| Config/DB row | Light Yellow tint | `#FFF2CC` |
| Sign-Off Completed | Light Green | `#E2EFDA` |
| Sign-Off Pending | Light Orange | `#FCE4D6` |
| Deployed | Light Green | `#E2EFDA` |
| Rolled Back | Light Orange | `#FCE4D6` |

## TOPS Deployment Rules

**Deployment Windows:**
- Monday - Wednesday: 24×7
- Thursday: Morning only (preferably before noon)
- Thursday afternoon - Sunday: ❌ No deployments
- Emergency: Explicit written approval from TOPS required

**Sign-Off Rules:**
- Dev sign-off is mandatory before sharing any release note
- QA sign-off must explicitly appear in the release note
- Release notes without dual sign-off will be rejected
- Submit minimum 2 business days before intended production deployment

**Failed Deployment Protocol:**
1. Rollback immediately as per rollback plan
2. Joint RCA submitted within 24 business hours
3. RCA must cover: root cause, why testing didn't catch it, corrective measures
4. Redeployment treated as fresh release - full process required
