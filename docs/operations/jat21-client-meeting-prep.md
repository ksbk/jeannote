# Jat21 — Client Meeting Prep

**Date:** 2026-04-19  
**Purpose:** Prepare for an in-person or video meeting with the Jat21 client  
**Tone:** Friendly, practical, non-technical — this is a trusted working relationship

---

## Purpose of the meeting

The goal is to make sure we both have proper, stable access to your website
before any updates are made. Nothing changes during or after this meeting
without your agreement. This is about getting things properly set up so the
site can be updated, backed up, and fixed cleanly — without either of us
being stuck if something goes wrong.

---

## Plain-language explanation for the client

*Say something like this at the start of the meeting:*

> "Your website belongs to you. Your domain, your content, your brand, your
> business data — all of that stays yours. I manage the technical side so the
> site gets updated properly, stays backed up, and gets fixed quickly when
> something breaks. Before I make any changes, I just want to make sure we
> both have proper access and that nothing is sitting in one person's account
> that we can't get to if needed."

This framing works well because it:
- Reassures the client that they are not giving anything up
- Explains the practical reason without technical jargon
- Sets expectations before any work begins

---

## What to confirm in the meeting

Work through these as a conversation, not a form. Most of these are just
a quick "yes, you can do that" or "let me check."

### GitHub

**What to ask:**
> "Can you add me as a collaborator on the website repo so I can push
> updates directly? It's on GitHub under your account."

**What you need:** Named collaborator access (not shared login)  
**What to avoid:** Do not ask for their GitHub password or take over the org

---

### Railway (hosting/deployment)

**What to ask:**
> "Can you add me as a team member on the Railway project so I can check
> deployments, view logs, and manage environment settings?"

**What you need:** Team member access with access to deployments, environment
variables, logs, and the Postgres database  
**What to avoid:** Do not ask to own the Railway account

---

### Cloudinary (images/media)

**What to ask:**
> "Is the Cloudinary account for the site connected to your email?
> Can you confirm I have access, or add me as a team member?"

**What you need:** Confirm access to the account. If you already have it
through Railway env vars, just confirm the account is recoverable.  
**What to avoid:** Do not rotate or change credentials during the meeting

---

### Domain / DNS (jat21.com)

**What to ask:**
> "Who manages the jat21.com domain? Is it through a registrar like
> Namecheap, GoDaddy, or somewhere else? I don't need access to it —
> I just want to know who to contact if a DNS change is ever needed."

**What you need:** Know the registrar name and who has the account  
**What to avoid:** Do not ask for registrar login. Client keeps DNS ownership.

---

### Gmail SMTP (email sending)

**What to ask:**
> "The site sends emails through a Gmail account — do you know which
> one? And is there an app password set up for it?"

**What you need:** Confirm the Gmail account email and whether an app
password exists and is stored somewhere recoverable  
**What to avoid:** Do not ask for the main Gmail password. App passwords
are separate and safer.

---

### Django admin accounts

**What to ask:**
> "On the website admin panel — do you have your own login? I want to
> make sure you always have full access independent of me."

**What you need:** Client has their own named admin account. You have your
own separate named admin account. Neither is the only recovery path.  
**What to avoid:** Do not use a single shared admin login for both of you.

---

### Backups

**What to ask:**
> "Before I make any updates to the site, I want to take a backup of
> the database. Railway should do this automatically — do you know if
> it's set up?"

**What you need:** Confirm Railway Postgres auto-backup is enabled and what
the retention period is. Confirm you can trigger a manual backup.  
**What to avoid:** Do not run any backup or migration during the meeting.

---

## What to ask for vs. what not to ask for

| Ask for | Do not ask for |
|---|---|
| Named GitHub collaborator invite | Shared GitHub password |
| Railway team member access | Railway account ownership |
| Cloudinary team member or confirm access | Cloudinary password |
| Name of DNS registrar | Registrar login or domain transfer |
| Gmail account name + app password confirmation | Main Gmail password |
| Separate named Django admin accounts | Shared admin login |

---

## What access you need as Kusse Studio operator

By the end of the meeting, you should be able to:

- Push code to `jat21architect-sys/jat21` via a named GitHub collaborator role
- View deployments, logs, and env vars in Railway as a named team member
- Access or recover Cloudinary credentials
- Know the DNS registrar (no login required)
- Confirm the Gmail SMTP setup and app password
- Log in to the Django admin with your own named superuser account
- Trigger or confirm a database backup before any upgrade

---

## How to explain ongoing maintenance simply

*If the client asks what you'll actually be doing:*

> "Mostly it's invisible to you. I keep the site software up to date,
> make sure backups are running, and fix anything that breaks. If you
> want to add or change content, you can do that yourself through the
> admin panel — or I can do it for you. Before any bigger change,
> I'll always let you know what I'm doing and why."

---

## Follow-up actions after the meeting

- [ ] Accept any GitHub collaborator invite
- [ ] Confirm Railway team member access is working
- [ ] Note Cloudinary account name and recovery path
- [ ] Note DNS registrar name
- [ ] Note Gmail account and confirm app password is stored somewhere safe
- [ ] Confirm both admin accounts exist in Django admin
- [ ] Confirm Railway Postgres auto-backup is enabled
- [ ] Take a manual database backup before any upgrade begins
- [ ] Update `jat21-access-stabilization.md` with confirmed answers

---

## What comes after

Once access is stabilized and documented:

1. Take a manual database backup
2. Begin the v1.4.2 upgrade using `jat21-managed-transition-checklist.md`
3. Run health gate on a test branch before touching production
