---
spec_type: microcopy
spec_id: settings-account
created: 2026-05-06
status: draft
---

# Microcopy: Prosper Settings Page

## 1. Voice

- **Audience:** project managers (intermediate technical literacy, not developers).
- **Tone:** plain, direct, second person. Avoid jargon. Avoid the word "user" in user-facing text.
- **Verbs:** prefer "Save changes" over "Submit", "Replace" over "Upload" (when an image already exists), "Try again" over "Retry".

## 2. Page chrome

| Element                  | Copy                              |
|--------------------------|-----------------------------------|
| Browser tab title        | `Settings · Prosper`              |
| Sidebar nav: Profile     | `Profile`                         |
| Sidebar nav: Notifications | `Notifications`                 |
| Sidebar nav: Billing     | `Billing`                         |

## 3. Profile section

### Headings & labels
| Element                       | Copy                                   |
|-------------------------------|----------------------------------------|
| Section heading (`<h1>`)      | `Profile`                              |
| Display name field label      | `Display name`                         |
| Display name field placeholder| `e.g. Jane Doe`                        |
| Display name helper           | `This is how your name appears on tasks, comments, and reports.` |
| Avatar field label            | `Profile picture`                      |
| Avatar field helper           | `JPG, PNG, or GIF. 2 MB max. We'll crop it to a square.` |
| Replace button                | `Replace`                              |
| Remove button                 | `Remove`                               |

### Actions
| Element                       | Copy                                   |
|-------------------------------|----------------------------------------|
| Save button (default)         | `Save changes`                         |
| Save button (submitting)      | `Saving…`                              |
| Cancel button                 | `Cancel`                               |

### Confirmations & feedback
| Trigger                       | Copy                                   |
|-------------------------------|----------------------------------------|
| Save success toast            | `Settings updated.`                    |
| Unsaved changes dialog title  | `Discard your changes?`                |
| Unsaved changes dialog body   | `You've edited your profile but haven't saved. If you leave now, your changes will be lost.` |
| Unsaved changes confirm       | `Discard changes`                      |
| Unsaved changes cancel        | `Keep editing`                         |

### Errors
| Trigger                                | Copy                                                                |
|----------------------------------------|---------------------------------------------------------------------|
| Display name empty                     | `Add a display name so teammates can recognise you.`                |
| Display name too long (> 60 chars)     | `Keep your display name under 60 characters.`                       |
| Avatar file too large                  | `That file is over 2 MB. Try a smaller image.`                      |
| Avatar wrong file type                 | `Use a JPG, PNG, or GIF.`                                           |
| Avatar upload network failure          | `Couldn't upload that image. Check your connection and try again.`  |
| Save network failure (banner)          | `We couldn't save your changes. Try again in a moment.`             |
| Save server error 5xx (banner)         | `Something went wrong on our end. Your changes weren't saved.`      |

### Loading & empty
| Trigger                                | Copy                                                                |
|----------------------------------------|---------------------------------------------------------------------|
| Initial profile fetch failure          | `We couldn't load your settings. [Try again]`                       |

## 4. Notifications section

| Element                                    | Copy                                                                  |
|--------------------------------------------|-----------------------------------------------------------------------|
| Section heading                            | `Notifications`                                                       |
| Section description                        | `Choose what we email you about. Changes save automatically.`         |
| Toggle: daily digest                       | `Daily digest of project activity`                                    |
| Toggle: task assignment                    | `When someone assigns a task to me`                                   |
| Toggle: mention                            | `When someone @-mentions me in a comment`                             |
| Autosave inline confirmation (per toggle)  | `Saved`                                                               |
| Autosave inline failure (per toggle)       | `Couldn't save — try again`                                           |

## 5. Billing section

| Element                              | Copy                                                                          |
|--------------------------------------|-------------------------------------------------------------------------------|
| Section heading                      | `Billing`                                                                     |
| Plan label                           | `Current plan`                                                                |
| Renewal label                        | `Renews`                                                                      |
| Manage subscription button           | `Manage subscription`                                                         |
| Manage button helper                 | `Opens the Stripe Customer Portal in a new tab.`                              |
| Initial billing fetch failure        | `We couldn't load your billing details. [Try again]`                          |

## 6. Forbidden phrases

These appear nowhere in the UI. They were either generic AI defaults or violated voice guidelines:

- "Submit" (replaced with the actual outcome verb, e.g. "Save changes")
- "Loading..." with three dots and no context (replaced with a one-line skeleton on initial load, "Saving…" during submit)
- "Invalid input" (replaced with field-specific guidance)
- "Error: " prefix in any user-facing message
