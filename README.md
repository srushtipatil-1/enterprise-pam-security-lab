# Enterprise PAM Security Lab

A hands-on Privileged Access Management (PAM) lab demonstrating core enterprise security operations concepts using free, open-source, and native tools — built as a practical companion to CyberArk PAM platform knowledge.

## Overview

This project simulates real-world PAM workflows: privileged account management, least-privilege enforcement, credential vaulting, password rotation, RBAC, audit logging, and incident troubleshooting. Every concept is mapped back to its CyberArk equivalent in `documentation/cyberark-mapping.md`.

## What this demonstrates

- Privileged Access Management (PAM) concepts and workflows
- Identity & Access Management (IAM) / Role-Based Access Control (RBAC)
- Least-privilege enforcement (Linux sudo, Windows UAC)
- Secrets management and credential vaulting (HashiCorp Vault)
- Automated password rotation (Python)
- Audit logging and evidence collection
- Incident troubleshooting runbooks / SOPs
- Privileged account onboarding workflow

## Tech stack

HashiCorp Vault, Python, PowerShell, Windows, Linux (Ubuntu), Git/GitHub

## Project structure

- `linux/` — Linux privileged account tests
- `windows/` — Windows privileged account tests (UAC elevation)
- `vault/` — Vault setup, secrets, RBAC policies
- `scripts/` — Password rotation automation
- `runbooks/` — Troubleshooting guides (credential access, rotation, SSH, RDP)
- `documentation/` — Onboarding workflow, audit evidence, CyberArk concept mapping
- `screenshots/` — Evidence for every test performed

## Key evidence

- Least privilege enforcement tested on both Linux and Windows
- Vault RBAC policy tested: read allowed, write denied for restricted role
- Password rotation script verified end-to-end (Vault version increment confirmed)
- Full audit trail captured via Vault's file audit device

## Note

This lab uses open-source and native OS tools to simulate PAM operational concepts for learning and demonstration purposes. It is not affiliated with or a substitute for a production CyberArk deployment. See `documentation/cyberark-mapping.md` for the full concept-to-implementation mapping.