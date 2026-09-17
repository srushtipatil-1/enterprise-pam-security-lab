# Active Directory & LDAP — Core Concepts

This document covers foundational Active Directory (AD) and LDAP 
concepts relevant to PAM operations, even though a full AD lab was 
not built for this project (noted as a "plus" rather than a 
requirement for this role).

## Active Directory Basics

- Domain: A logical grouping of users, computers, and resources 
  managed centrally (e.g. corp.local)
- Domain Controller (DC): The server that hosts AD and handles 
  authentication requests
- Organizational Unit (OU): A container used to organize users/
  computers/groups within a domain for easier policy management
- Group Policy (GPO): Rules applied to users/computers in an OU 
  (e.g. password complexity requirements, login restrictions)
- Domain Admin: The highest-privilege account type in AD — 
  equivalent conceptually to a "root" or "Administrator" account, 
  and a prime target for PAM vaulting
- **Service Account**: A non-human account used by applications/
  services to authenticate — commonly onboarded into PAM platforms 
  since they often have elevated, long-lived privileges

## LDAP Basics

- LDAP (Lightweight Directory Access Protocol): The protocol 
  used to query and modify directory services like Active Directory
- Distinguished Name (DN): The full path identifying an object 
  in the directory (e.g. CN=srushti,OU=Users,DC=corp,DC=local)
- Bind: The authentication step where a client connects to the 
  LDAP directory using credentials

## Relevance to PAM / CyberArk

- CyberArk (and other PAM platforms) commonly integrate with AD/LDAP to:
  - Onboard Domain Admin and service accounts into the vault
  - Authenticate PAM platform users against existing AD credentials 
    (rather than maintaining separate local accounts)
  - Apply least-privilege by mapping AD security groups to PAM roles 
    (e.g. an AD group "PAM-Analysts" mapped to read-only vault access)

## Why this matters

Even without a full AD lab, understanding these concepts is important 
for a PAM Operations role because privileged account onboarding often 
starts with identifying AD-based accounts (Domain Admins, service 
accounts) that need to be brought under vault control.