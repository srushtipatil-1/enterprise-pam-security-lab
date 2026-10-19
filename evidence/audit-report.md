# Vault Audit Evidence Report

Source log: `C:\vault\audit.log`  
Window: 2026-09-17T12:07:37.67466Z to 2026-10-19T06:26:43.0354696Z

## Summary

- Requests: **42**
- Allowed: **36**
- Denied: **6**
- Requests made with the root token: **27**  <- review: day-to-day work should use named identities

## Activity by identity (WHO)

| Identity | Policies | Allowed | Denied |
|---|---|---|---|
| (unauthenticated) |  | 0 | 1 |
| approle | default,rotation-service | 4 | 1 |
| root | root | 2 | 0 |
| token | root | 25 | 0 |
| userpass-analyst1 | analyst,default | 2 | 2 |
| userpass-pamadmin1 | default,pam-admin | 3 | 2 |

## Denied requests

| Time | Who | Operation | Path | Error |
|---|---|---|---|---|
| 2026-10-19T06:24:05.3982095Z | (unauthenticated) | update | auth/userpass/login/analyst1 | invalid credentials |
| 2026-10-19T06:25:10.2634332Z | userpass-analyst1 | create | secret/data/privileged/test-account | 1 error occurred: * permission denied |
| 2026-10-19T06:25:31.498507Z | userpass-analyst1 | read | sys/policies/acl/analyst | 1 error occurred: * permission denied |
| 2026-10-19T06:25:34.0046669Z | userpass-pamadmin1 | delete | sys/audit/file | 1 error occurred: * permission denied |
| 2026-10-19T06:25:34.1769738Z | userpass-pamadmin1 | update | sys/policies/acl/analyst | 1 error occurred: * permission denied |
| 2026-10-19T06:26:20.2930259Z | approle | read | secret/data/privileged/linux-admin | 1 error occurred: * permission denied |

## Full trail (WHO / WHAT / WHEN / RESULT)

| Time | Who | Operation | Path | Result |
|---|---|---|---|---|
| 2026-09-17T12:07:37.67466Z | root | update | sys/audit/file | ALLOWED |
| 2026-09-17T12:07:50.5447086Z | root | read | secret/data/privileged/linux-admin | ALLOWED |
| 2026-10-19T06:18:23.6329834Z | token | update | sys/audit/file | ALLOWED |
| 2026-10-19T06:18:23.890803Z | token | update | sys/policies/acl/analyst | ALLOWED |
| 2026-10-19T06:18:24.0805097Z | token | update | sys/policies/acl/pam-admin | ALLOWED |
| 2026-10-19T06:18:24.3219791Z | token | update | sys/policies/acl/rotation-service | ALLOWED |
| 2026-10-19T06:22:10.0485952Z | token | read | sys/mounts | ALLOWED |
| 2026-10-19T06:22:10.2718158Z | token | read | sys/audit | ALLOWED |
| 2026-10-19T06:22:10.4369554Z | token | update | sys/policies/acl/analyst | ALLOWED |
| 2026-10-19T06:22:10.6401098Z | token | update | sys/policies/acl/pam-admin | ALLOWED |
| 2026-10-19T06:22:10.8460345Z | token | update | sys/policies/acl/rotation-service | ALLOWED |
| 2026-10-19T06:22:11.0483051Z | token | read | sys/auth | ALLOWED |
| 2026-10-19T06:22:11.5057075Z | token | update | sys/auth/userpass | ALLOWED |
| 2026-10-19T06:22:43.4259669Z | token | create | auth/userpass/users/analyst1 | ALLOWED |
| 2026-10-19T06:22:58.4880768Z | token | create | auth/userpass/users/pamadmin1 | ALLOWED |
| 2026-10-19T06:22:58.7531299Z | token | update | sys/auth/approle | ALLOWED |
| 2026-10-19T06:22:58.9366685Z | token | create | auth/approle/role/rotation-service | ALLOWED |
| 2026-10-19T06:22:59.175191Z | token | read | auth/approle/role/rotation-service/role-id | ALLOWED |
| 2026-10-19T06:22:59.4090043Z | token | update | auth/approle/role/rotation-service/secret-id | ALLOWED |
| 2026-10-19T06:22:59.6468125Z | token | read | secret/data/privileged/linux-admin | ALLOWED |
| 2026-10-19T06:23:35.7901816Z | token | create | secret/data/privileged/linux-admin | ALLOWED |
| 2026-10-19T06:23:36.0070757Z | token | list | sys/policies/acl/ | ALLOWED |
| 2026-10-19T06:23:36.2739914Z | token | read | sys/auth | ALLOWED |
| 2026-10-19T06:23:36.4752388Z | token | read | sys/audit | ALLOWED |
| 2026-10-19T06:24:05.3982095Z | (unauthenticated) | update | auth/userpass/login/analyst1 | DENIED |
| 2026-10-19T06:24:37.7714209Z | token | read | auth/token/lookup-self | ALLOWED |
| 2026-10-19T06:24:38.1724102Z | token | update | auth/userpass/users/analyst1/password | ALLOWED |
| 2026-10-19T06:24:38.6111056Z | token | update | auth/userpass/users/pamadmin1/password | ALLOWED |
| 2026-10-19T06:25:00.1628349Z | userpass-analyst1 | update | auth/userpass/login/analyst1 | ALLOWED |
| 2026-10-19T06:25:10.0273833Z | userpass-analyst1 | read | secret/data/privileged/linux-admin | ALLOWED |
| 2026-10-19T06:25:10.2634332Z | userpass-analyst1 | create | secret/data/privileged/test-account | DENIED |
| 2026-10-19T06:25:31.498507Z | userpass-analyst1 | read | sys/policies/acl/analyst | DENIED |
| 2026-10-19T06:25:33.7007033Z | userpass-pamadmin1 | update | auth/userpass/login/pamadmin1 | ALLOWED |
| 2026-10-19T06:25:33.8627679Z | userpass-pamadmin1 | create | secret/data/privileged/svc-backup | ALLOWED |
| 2026-10-19T06:25:34.0046669Z | userpass-pamadmin1 | delete | sys/audit/file | DENIED |
| 2026-10-19T06:25:34.1769738Z | userpass-pamadmin1 | update | sys/policies/acl/analyst | DENIED |
| 2026-10-19T06:26:03.6356329Z | approle | update | auth/approle/login | ALLOWED |
| 2026-10-19T06:26:03.7860491Z | approle | update | secret/data/privileged/linux-admin | ALLOWED |
| 2026-10-19T06:26:03.909188Z | approle | update | secret/data/privileged/svc-backup | ALLOWED |
| 2026-10-19T06:26:20.0972294Z | approle | update | auth/approle/login | ALLOWED |
| 2026-10-19T06:26:20.2930259Z | approle | read | secret/data/privileged/linux-admin | DENIED |
| 2026-10-19T06:26:43.0354696Z | userpass-pamadmin1 | read | secret/metadata/privileged/linux-admin | ALLOWED |
