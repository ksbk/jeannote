# Jat21 — Access Stabilization Checklist

**Status:** Pre-upgrade — do not migrate, push, or deploy until this is complete  
**Date:** 2026-04-19  
**Infrastructure model:** Client-owned — Jat21 owns GitHub org, Railway, Cloudinary, DNS  
**Purpose:** Stabilize and document Kusse Studio operator access before any upgrade or change

---

## Context

Phase 0 ownership verification is complete. The current model is client-owned
infrastructure, not Kusse Studio-managed. Kusse Studio has operator access
across all layers but does not own the accounts.

Before any upgrade to v1.4.2 or any production change, confirm that Kusse
Studio access is stable, documented, and not dependent on shared client
credentials or informal access.

---

## Checklist

### 1. GitHub

- [ ] Confirm Kusse Studio / personal GitHub account is added as a collaborator
      or admin on `jat21architect-sys/jat21`
- [ ] Do not rely on shared client login or informal access
- [ ] Confirm branch protection or "Wait for CI" status on `main`
- [ ] Record: who can push to `main`, who can approve PRs

**Note:** If access is currently informal (e.g. client shared credentials),
request a named collaborator invite before any code changes.

---

### 2. Railway

- [ ] Confirm Kusse Studio account has team member or operator access to the
      Jat21 Railway project — not just a shared login
- [ ] Confirm access to: deployments, environment variables, logs, Postgres
      database
- [ ] Confirm Postgres connection details are accessible (for backup/restore)
- [ ] Confirm Railway account recovery path — who controls the Railway account
      email?
- [ ] Record: Railway project name, service names, Postgres service name

**Note:** Do not rotate or change any Railway environment variables yet.
Document current access only.

---

### 3. Cloudinary

- [ ] Confirm access to the Jat21 Cloudinary account (cloud name, API key)
- [ ] Confirm recovery path — who controls the Cloudinary account email?
- [ ] Record: `CLOUDINARY_CLOUD_NAME` and whether credentials are in Railway
      env vars
- [ ] Do not rotate Cloudinary credentials yet

**Note:** If Cloudinary credentials are only in Railway env vars and not
documented elsewhere, note this as a recovery risk.

---

### 4. Domain / DNS

- [ ] Confirm who controls the `jat21.com` domain registrar account
- [ ] Document current DNS records: A/CNAME for root and www, any MX records
- [ ] Confirm registrar and account recovery path
- [ ] Client remains DNS/domain owner — document only, do not change

---

### 5. Email / SMTP

- [ ] Confirm current SMTP provider: Gmail
- [ ] Document: which Gmail account, what app password is in use
- [ ] Confirm recovery path — who controls the Gmail account?
- [ ] Record: `EMAIL_HOST_USER` value in Railway env vars (do not share
      plaintext)
- [ ] Note: Gmail SMTP has sending limits — flag as a future improvement if
      volume grows

---

### 6. Django admin

- [ ] Confirm Kusse Studio has a named superuser/admin account under a studio
      email address — not a shared client account
- [ ] Confirm client has their own named admin account
- [ ] Neither account should be the only recovery path
- [ ] Record: how many superuser accounts exist, what emails

**Note:** If only one superuser account exists, create a second named account
before any upgrade work begins.

---

### 7. Database backups

- [ ] Document the current Postgres backup process — is Railway auto-backup
      enabled? What is the retention period?
- [ ] Confirm a manual backup can be taken before any upgrade
- [ ] Record: how to trigger a manual backup, where to store it
- [ ] Confirm media files (Cloudinary) are not at risk during an upgrade

**Backup must be confirmed before any migration or upgrade is run on
production.**

---

## What this checklist does not cover

- Migrating Jat21 to Kusse Studio-managed infrastructure — deferred
- Upgrading `jat21architect-sys/jat21` to v1.4.2 — deferred until access is stable
- Changing any production environment variables — deferred
- DNS changes — not required for upgrade

---

## After completing this checklist

When all items above are confirmed and documented:

1. Take a manual database backup
2. Proceed to `jat21-managed-transition-checklist.md` Phase 1 (verification)
   for the v1.4.2 upgrade
