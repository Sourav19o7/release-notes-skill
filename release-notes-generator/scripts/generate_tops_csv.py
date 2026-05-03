#!/usr/bin/env python3
"""
Generate TOPS-compliant CSV for Google Sheets import.
Used for enterprise release notes (JioMart 3P, RIL, etc.)
"""

import csv
import json
import sys
from datetime import datetime
from pathlib import Path


HEADERS = [
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


def generate_tops_csv(changes_json_path: str, output_path: str, release_info: dict):
    """
    Generate TOPS-compliant CSV from a JSON file containing changes.

    Args:
        changes_json_path: Path to JSON file with change data
        output_path: Output CSV file path
        release_info: Dict with release metadata (name, environment, eta, dev_signoff, qa_signoff)
    """

    with open(changes_json_path, 'r') as f:
        changes = json.load(f)

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)

        for change in changes:
            change_type = change.get('type', 'Feature')
            is_bug_fix = change_type == 'Bug Fix'
            is_feature = change_type == 'Feature'

            row = [
                release_info.get('name', ''),
                change.get('title', ''),
                change.get('module', ''),
                change_type,
                change.get('category', 'Non-APK'),
                change.get('ticket_id', 'Internal'),
                change.get('pr_link', ''),
                change.get('status', 'Completed'),
                'Pending',
                release_info.get('environment', 'UAT'),
                'Pending',
                release_info.get('eta', ''),
                change.get('description', ''),
                change.get('rca', '') if is_bug_fix else 'N/A',
                change.get('solution', '') if is_bug_fix else 'N/A',
                change.get('requirement', '') if is_feature else 'N/A',
                change.get('files_changed', ''),
                change.get('components', ''),
                change.get('env_changes', 'None'),
                change.get('db_changes', 'No'),
                change.get('db_columns', 'N/A'),
                change.get('db_rollback', 'N/A'),
                change.get('config_keys', 'None'),
                change.get('api_changes', 'None'),
                '',  # Regression Testing Scope
                '',  # Regression Testing Result
                '',  # Test Evidence
                f"Inline - see column N" if is_bug_fix else 'N/A',
                f"[ ] Name: {release_info.get('dev_signoff', '___')} | Date: ___",
                f"[ ] Name: {release_info.get('qa_signoff', '___')} | Date: ___",
                '',  # Pre-Deployment Validation
                '',  # Post-Deployment Validation
                '',  # Deployment Plan
                '',  # Rollback Plan
                change.get('dependencies', 'None'),
                change.get('pre_configs', 'None'),
                change.get('deployment_note', ''),
                change.get('apk_dependency', 'Independent'),
                'Yes' if change.get('backend_change', True) else 'No',
                'Yes' if change.get('apk_change', False) else 'No',
                'No',
                change.get('remarks', ''),
                datetime.now().strftime('%d-%b-%Y')
            ]
            writer.writerow(row)

    print(f"Created TOPS-compliant CSV: {output_path}")
    print(f"Total rows: {len(changes)}")
    return output_path


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_tops_csv.py <changes.json> <output.csv> [release_info.json]")
        print("")
        print("Example changes.json format:")
        print(json.dumps([{
            "title": "Fix subscription email fallback",
            "module": "Customer",
            "type": "Bug Fix",
            "category": "Non-APK",
            "ticket_id": "ISS-286043",
            "pr_link": "https://github.com/org/repo/pull/816",
            "description": "Added email fallback for unlinked Stripe subscriptions",
            "rca": "Stripe subscriptions were not found when user ID was not linked",
            "solution": "Falls back to email-based lookup when userId lookup fails",
            "files_changed": "packages/sdk/src/customer/index.ts",
            "components": "sdk: v2.0.5",
            "db_changes": "No",
            "backend_change": True
        }], indent=2))
        print("")
        print("Example release_info.json format:")
        print(json.dumps({
            "name": "RT_2 Hot Fix - 1",
            "environment": "UAT",
            "eta": "21-Apr-2026",
            "dev_signoff": "John Doe",
            "qa_signoff": "Jane Smith"
        }, indent=2))
        sys.exit(1)

    changes_path = sys.argv[1]
    output_path = sys.argv[2]

    release_info = {}
    if len(sys.argv) > 3:
        with open(sys.argv[3], 'r') as f:
            release_info = json.load(f)
    else:
        release_info = {
            "name": "Release",
            "environment": "UAT",
            "eta": "",
            "dev_signoff": "___",
            "qa_signoff": "___"
        }

    generate_tops_csv(changes_path, output_path, release_info)


if __name__ == "__main__":
    main()
