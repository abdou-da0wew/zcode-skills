---
name: Version Management Skill
description: Standalone general-purpose skill: manages the full lifecycle of frontend projects. Whenever a task **may** write .html/.jsx/.tsx/.vue entry files, you must read and follow this skill **before** writing the first file (to determine the on-disk path and project directory) — not as an afterthought after output is produced; use it even if the user never mentions "project" or "version". Also handles the user's version-related operations (viewing history, restoring versions, switching projects, etc.).
---

# Version Management

> **Execution model:** Version management is implemented **entirely by this skill + `send_file`**; no Git repository or version log is maintained by any frontend/backend service. The agent executes git and file operations in the cloud-machine project directory. All git commands below are complete and executable; once they are later wrapped as tools, only the command sections get replaced — **the decision logic and process order stay unchanged**.

> **User communication rule:** The technical details of version management (git commands, meta.json updates, version number calculation, etc.) are internal execution details and must never be shown or mentioned to the user in conversation. The user only needs to see: the generated result + the version card emitted by `send_file`. If version info must be communicated, just say "Saved as V{n}" — never explain the underlying operations.

---

## ⚠️ Path Hard Rules (highest priority; execute this section before writing any file)

**This skill must kick in before the first entry file is written, not as remediation afterwards.** The first time any entry file (`.html` / `.jsx` / `.tsx` / `.vue`) is written to disk, the target path must be inside `MyProjects/{project-name}/`.

### Base path

`MyProjects` **always lives at the workspace root**, matching the `send_file` `file_path` convention `/MyProjects/{project-name}/...`. Before executing any `mkdir` / `cd` / file-writing operation, first return to the workspace root (or use a full path computed from the root); **never** use the relative path `MyProjects/...` without confirming `pwd` — this is the most common cause of the `MyProjects` folder ending up in the wrong location.

### Fixed order before writing files (do not reorder)

```bash
# 1. Determine the project name (generation rules in §1.2)
# 2. Return to the workspace root and create the project directory
cd {workspace-root}
mkdir -p "MyProjects/{project-name}/assets"
# 3. Enter the project directory; from now on all files are created [directly] inside it
cd "MyProjects/{project-name}"
# 4. Write entry files such as index.html / prototype.html and other code files
# 5. Then proceed to §1's git / meta.json / send_file flow
```

### Violation list (any of the following is a process error, even if fixed afterwards)

- Writing files to the workspace root, `~/Desktop`, `/tmp`, or any other directory first, then moving them into the project directory
- Pasting code blocks in conversation without writing to disk
- Executing file-writing commands outside the project directory

### Self-check before writing (last gate)

Before calling any file-writing command, ask yourself: **"Is the path I'm about to write to inside `MyProjects/{project-name}/`?"** If not → stop, first run the fixed order above to create the directories, then write the file.

---


## 0. Handoff with the Design Skill (required reading)

This skill works **side by side** with the Design Skill (both are carried by the same Design Agent): the Design Skill produces the design output; this skill handles persistence and version management. This section describes how the two cooperate in the HTML delivery scenario.

> **Triggering does not depend on the Design Skill.** This skill triggers by file type: whenever an entry file (.html / .jsx / .tsx / .vue) is produced **or modified**, this skill applies, regardless of whether the task went through the Design Skill routing — including cases where no design flow was involved and an existing HTML's text/colors were edited directly (in that case, skip the quality gate and go straight to asset validation → git → meta.json → send_file).

### Trigger order (when coordinating with the Design Skill)

```text
Design Skill routing → scenario skill (portfolio / deck / prototype, etc.)
→ [before writing files] follow the "Path Hard Rules" at the top of this skill to create MyProjects/{project-name}/
→ produce .html / .jsx / .tsx / .vue → files are [written directly] into MyProjects/{project-name}/ (not moved afterwards)
→ quality-gate.md passes
→ this skill (asset validation → git → meta.json → send_file)
```

**Never** commit or `send_file` Design Skill output when the quality gate has not passed.
**Never** treat an HTML web project as delivered while this skill has not completed (pasting code blocks only, not writing to disk, or not writing into `MyProjects/` all count as not delivered).

### Design Skill owns / this skill owns

| Dimension | Design Skill | This skill |
|------|--------------|----------|
| Scenarios, styles, layout, copy language | ✅ | — |
| quality-gate, Design Compliance comments | ✅ | — |
| Project directory, assets on disk, git versions | — | ✅ |
| `meta.json`, `send_file` version cards | — | ✅ |
| User-facing wording | Design result explanation | Only "Saved as V{n}" |

### Commit message suggestions

`git commit -m` messages and the `summary` in `meta.json` may include the scenario for easier recognition, e.g.:

- `V2: Homepage hero redesign (portfolio)`
- `V3: Based on V1: switch to International Typographic Style (landing-page)`

### Entry point for reading

The Design-side handoff notes are in: `SKILL.md` § Version Management Handoff. For persistence, git, `meta.json`, `send_file`, and similar mechanics, this skill is the source of truth (design only hands off; it does not redefine them).

---

## 0.1 Preview status quo (known limitations, kept as-is)

| Symptom | Cause | Current handling |
|------|------|----------|
| Multi-file HTML projects (multi-page, several html files) cannot navigate between pages | Preview goes through OSS links; this round only processed HTML and image assets, but the whole bundle was not uploaded to OSS, so other html files still reference relative paths that the frontend cannot load | **Not handled for now**, keep as-is |
| Clicking some historical version previews may still show the latest version | Preview scans the workspace path and generates OSS links on the fly, without tag isolation | **Not handled for now**, keep as-is |
| Single-file HTML with `.js`/`.css`/`assets/` (images) can generally be previewed | The backend replaces relative asset paths inside the HTML with OSS links | Normal |

**Agent note:** these limitations do not affect version commits or `send_file` output; do not inline all resources or force single-file output because a preview failed.

---

## 1. Project Creation

### 1.1 Decision rules

If the output includes these frontend file types: `.html`, `.jsx`, `.tsx`, `.vue` → **must** create/update a project and go through the version flow (regardless of which caller skill was used).
If the output is an image, doc, ppt, JSON, design spec, plain text, etc. → ordinary file; no project is created.

**Common misjudgments (forbidden):** assuming "just paste code blocks" or "writing to Desktop is fine" because the task was routed to a caller scenario; whenever an entry HTML/frontend file is written, deliver it as a project.

### 1.2 Mandatory path check (critical rule)

**All web_project files must be saved under `MyProjects/{project-name}/`. Saving to the workspace root, Desktop, temp directories, or only pasting code blocks is forbidden.**

The preferred approach is **prevention** rather than remediation: per the "⚠️ Path Hard Rules" at the top, create the project directory and write directly into the correct location before the first file is written. The following checks are the **final gate** before commit / `send_file`:

1. **Before writing**: per the hard rules at the top, create the directories first and write directly into the correct location
2. **Before commit / send_file**: run the gate script below; if stray files are found → **must `mv` them into the project directory first** and re-validate before continuing
3. **Project name generation rule**: auto-generate a semantic project name from the user's intent and content theme (e.g. `beijing-travel-site`, `enterprise-crm-admin`)

```bash
# Path gate before commit (run at the workspace root)
cd {workspace-root}

# (a) The project directory must contain at least one entry file (not limited to index.html; prototype.html etc. are equally valid)
ls "MyProjects/{project-name}/"*.html "MyProjects/{project-name}/"*.jsx \
   "MyProjects/{project-name}/"*.tsx "MyProjects/{project-name}/"*.vue 2>/dev/null | grep -q . \
  || { echo "ERROR: no entry file inside MyProjects/{project-name}/ — commit / send_file forbidden"; }

# (b) No entry files may be scattered in the workspace root or anywhere else
find . -maxdepth 2 -not -path "./MyProjects/*" \
  \( -name '*.html' -o -name '*.jsx' -o -name '*.tsx' -o -name '*.vue' \) \
  | while read -r f; do
      echo "STRAY: $f → must run mv \"$f\" \"MyProjects/{project-name}/\" and re-validate"
    done
```

If any ERROR / STRAY is reported → commit and `send_file` are **forbidden**; fix the paths first, then re-run the gate.

### 1.3 File structure rules

**Core principle: the project directory is self-contained, and all files (code + assets + export artifacts) are tracked in Git.**

- **Single file vs multi-file:** neither force single-file (inlined JS/CSS) nor encourage always-multi-file. Judge by project complexity:
  - Simple landing page, H5, single-page showcase → single-file `index.html` is fine
  - Reusable styles/scripts, many components → multi-file (e.g. `index.html` + `style.css` + `main.js`)
- **User upload destination:** `upload/`; the only directory for in-project assets: `MyProjects/{project-name}/assets/`
- Reference assets in code via **relative paths**: `assets/{file-name}`; referencing `upload/` paths is forbidden (at preview time the backend replaces relative paths with OSS links; the agent never writes OSS URLs by hand)
- Name assets with semantic English names (e.g. `hero-banner.png`); avoid non-ASCII characters and spaces
- `assets/` **is tracked in Git** — every version's snapshot includes all assets at that time, so restoring a historical version rolls code and assets back together and any historical version can be fully previewed

#### Handling assets (upload → assets, mandatory)

**Never** let the HTML reference `assets/xxx` with no corresponding file on disk (the most common cause of broken images: the path was written but nothing was copied from `upload/`).

1. Locate the source file in `upload/` (message attachment path, `find upload`, `ls -lt upload` for the most recent uploads)
2. `mkdir -p MyProjects/{project-name}/assets`
3. `cp upload/{source} MyProjects/{project-name}/assets/{name}` — `{name}` must **exactly match** `assets/{name}` in the HTML (if the HTML is already written, copy and rename to match the reference)
4. Then write/modify the HTML references; `cp` images one by one
5. **Validate before commit** (any MISSING means no commit / send_file):

```bash
cd MyProjects/{project-name}
grep -ohE 'assets/[a-zA-Z0-9_.-]+' index.html 2>/dev/null | sort -u | while read -r ref; do
  [ -f "$ref" ] || echo "MISSING: $ref"
done
```

6. Once there is no MISSING, create the version per §3 and `send_file`

#### Asset sources (three kinds; the on-disk rules are identical)

| Source | Typical order | Agent action | New version? |
|------|----------|------------|------------|
| **User upload** | HTML first then images / images first then HTML | `cp` from `upload/` to `assets/`, reference matches file name; when images arrive later, name them after the existing HTML references | cp only, no code change → ❌; HTML reference changed → ✅ |
| **Agent image search** | User wants images, agent finds them online | Download into `assets/{name}` (writing only an external URL is forbidden); then write/modify the HTML references | ✅ |
| **Agent image generation** | User wants images, agent generates them | Write into `assets/{name}` (writing `assets/xxx` without persisting the file is forbidden); then write the HTML | ✅ |

**Shared rule:** whenever the HTML contains `assets/` references, the validation above is mandatory before commit; if a file is missing, persist it or change the reference — never commit with MISSING.
**HTML first without images:** placeholder text/styles are fine, but **do not** write nonexistent `assets/xxx`; once the user uploads or the agent produces the image, write the real reference and `cp` it.

#### Preserving user images across versions (important)

For images the user has already uploaded and referenced in `assets/`, when a new version is produced by **natural-language / comment / parameter-editor** edits:

- If the user did **not** ask to remove that module and did **not** ask to swap the image → **must preserve** the original `assets/` files and the `assets/...` references in the HTML; do not delete, do not change paths, do not ask the user to re-upload
- Style/copy/layout-only changes → only touch code files, leave `assets/` alone (unless the user explicitly asked to replace the asset)
- `git add .` automatically includes unchanged `assets/` files in the new version snapshot (Git reuses unchanged files without storing them twice); no manual handling needed

#### Style-sample file retention rules

If there is a style-sample stage before the formal build (the model first generates an HTML containing several numbered design directions for the user to choose from), the sample HTML must be moved into `MyProjects/{project-name}/` and named `style-samples.html`; if the user is unsatisfied and asks for new directions, subsequent rounds increment to `style-samples-2.html`, `style-samples-3.html`; overwriting an existing sample file is forbidden. Sample files must never be named `index.html` or any other entry-file name. Samples are emitted via `send_file` for the user to preview and choose. `style-samples*.html` is wildcard-excluded in `.gitignore`; it never enters Git history or counts toward the project version number. Do not delete the sample source files/folders before the sample files have been persisted into the project directory.

### 1.4 Creation flow

The first time an entry file is produced for the user (**steps 1-3 must happen before any code file is written**, see the "⚠️ Path Hard Rules" at the top):

1. Generate a project name from the user's intent
2. Return to the workspace root; if `MyProjects` does not exist: `mkdir -p MyProjects/`
3. Create the project directory and assets: `mkdir -p MyProjects/{project-name}/assets`, then `cd` into it and **write all files directly inside this directory**
4. Copy user images from `upload/` to `assets/` first, then write the HTML; writing only `assets/` paths without persisting files is forbidden
5. Git initialization and first commit:

```bash
cd MyProjects/{project-name}
git init
echo -e "meta.json\nstyle-samples*.html" > .gitignore
git add .
git commit -m "V1: {one-sentence summary}"
git tag v1
# ↑ all of the above must complete, then create meta.json, and finally call send_file to emit V1
```

6. Create `meta.json` (structure in §5)
7. Call `send_file` to emit the version (see §3.4), `title` = project name (e.g. `beijing-travel-site`)

### 1.5 Project directory structure

```
upload/                  ← user upload destination (not in project Git)

MyProjects/
└── {project-name}/
    ├── .git/
    ├── .gitignore       ← excludes meta.json and style-samples*.html
    ├── meta.json        ← version metadata (not in Git)
    ├── style-samples*.html ← design direction samples, several numbered directions for the user to choose from (not in Git; optional; multiple rounds allowed)
    ├── index.html       ← main entry (in Git; path varies by project)
    ├── ...              ← other code files (in Git)
    ├── assets/          ← asset files (in Git; tracked as part of the version snapshot)
    └── export/          ← export artifacts (in Git; for fixed-image projects)
```

---

## 2. Multi-Project Management

### 2.1 Identifying the current project

Judge by priority:

1. The project name explicitly mentioned in the user's natural language
2. The project corresponding to the current tab passed in by the frontend (only used to identify the project; does not decide which version to edit)
3. The most recently operated project in this session
4. If none of the above works → scan the `MyProjects/` subdirectories, read each project's `meta.json`, list the projects, and ask the user

### 2.2 Switching projects

Read the target project's `meta.json` and tell the user: "Switched to project: {project-name}, current version V{n}"

### 2.3 Non-project tasks

Tasks that do not produce entry files trigger no project or version operations.

---

## 3. Version Management

### 3.1 Edit entry point and version determination

| Edit entry | Project | Version |
|---------|------|------|
| Comment feature (select an element in the preview area and write an instruction) | MD instruction contains the project name | MD instruction contains the version number (the version shown in the preview) |
| Parameter editor (edit button in the preview area) | MD instruction contains the project name | MD instruction contains the version number (the version shown in the preview) |
| Natural language (chat box input) | See rules below | See rules below |
| Chat card "Edit based on this version" | The card's project | The card's version (goes through the §4 merge flow) |

**Natural language default: edit the latest version of the latest project.**

Determining the project: per §2 priority (user-specified > frontend context > most recent > ask).

Determining the version:

| Scenario | Handling |
|------|----------|
| User explicitly specifies a version (e.g. "change the title based on V2", or the input box is prefilled with "Edit based on '{project-name}' V2") | Use the specified version → §4 merge flow |
| User specifies the project but not the version | That project's latest version |
| Anything else | Latest version of the latest project by default |

Do not ask follow-up questions. All versions can be restored; editing an unintended version can be rolled back via restore.

#### Handling rules for comment edits and parameter edits

After the user uses comment editing or parameter editing in the preview area (including historical version previews), the frontend generates an MD instruction and sends it to the agent. The MD instruction contains the **project name** and **version number**; the agent processes it as follows:

1. Parse the project name from the MD instruction → locate `MyProjects/{project-name}/`
2. Parse the version number from the MD instruction → get `V{n}`
3. Read the project's `latest_version` from `meta.json` and determine the version relationship:
   - **Specified version = latest version** → edit directly in the current workspace → create a new version per §3.3
   - **Specified version ≠ latest version (historical version)** → **must** run the §4.4 merge flow (first `git checkout v{n} -- .` to restore the specified version, then apply the edit, and finally commit once as a new version). **Skipping the restore step is forbidden**; no matter how small the agent believes the difference is, it must restore strictly before editing.
4. Search all HTML files in the project directory for matches by anchor, locate the target element, and apply the modification
5. When done, create the version + update `meta.json` + `send_file` per the git instructions in §3.3 / §4.4

> **The MD template is maintained by the frontend.** This skill does not define the exact MD format; as long as it contains the project name, version number, anchor, and the modification, the agent can parse it.

### 3.2 When to create a version

| Trigger | New version? | Notes |
|--------|-------------|------|
| First generation | ✅ V1 | Project creation |
| Natural-language edit | ✅ | Version number increments |
| Comment-feature edit | ✅ | Version number increments |
| Parameter editor save | ✅ | Text changes, style parameters, and image replacements all count as a new version |
| Version restore | ✅ | See §4 |
| Editing based on a historical version | ✅ | §4 merge; produces one version |
| User only uploads assets, no code change | ❌ | Only writes `assets/`; no commit |
| User uploads assets and the agent updates code references | ✅ | Requires commit + `send_file` |
| Adding an entry file to an existing project (e.g. new `light.html`) | ✅ | New file is committed together with existing files as a new version |
| Style-sample stage produces `style-samples*.html` | ❌ | Not in Git, not version-numbered; only `send_file` output for user selection |

### 3.3 Git commands for creating a version

After the modification is complete, run in the project directory:

```bash
cd MyProjects/{project-name}
LATEST_TAG=$(git tag --sort=-v:refname | head -n 1)
NEXT_NUM=$((${LATEST_TAG#v} + 1))
NEXT_TAG="v${NEXT_NUM}"
git add .
git commit -m "V${NEXT_NUM}: {one-sentence summary}"
git tag $NEXT_TAG
# ↑ all of the above must complete, then update meta.json, and finally call send_file to emit the new version
```

### 3.4 Chat output (send_file)

Every new version must be emitted via `send_file`.

#### 3.4.1 Default rule: single-entry-file projects

| Parameter | Value |
|------|-----|
| `ext` | Always `web_project` |
| `title` | Project name, e.g. `beijing-travel-site`; **do not** include the version number (the frontend concatenates the `version` field); must never be a specific file name (like index, main, etc.) |
| `file_path` | Full path of the project's main entry file, e.g. `/MyProjects/beijing-travel-site/index.html` |
| `project_name` | Same as `project_name` in `meta.json` |
| `version` | This version number, e.g. `V3` |

Call example:
```json
{"title": "beijing-travel-site", "ext": "web_project", "file_path": "/MyProjects/beijing-travel-site/index.html", "project_name": "beijing-travel-site", "version": "V3"}
```

#### 3.4.2 Multi-entry-file projects (new rule)

When the project contains **multiple independent entry HTML files** (e.g. `index.html` + `light.html`, or multiple pages):

1. **All entry files must be committed in the same commit** (`git add .` naturally includes everything)
2. **send_file strategy:**
   - If there is only one **main entry** (the rest are auxiliary), emit only the main entry by default
   - If the caller skill explicitly requires emitting multiple files (e.g. the prototype's two files), follow the caller's requirement
   - Nothing may be missed: every HTML file must be tracked by git
3. Calling `ext=directory` on the project directory to emit the folder is **forbidden**

Example (`index.html` is the main entry, `light.html` is a new variant):
```bash
# One commit containing both files
git add index.html light.html assets/
git commit -m "V4: add light theme variant"
git tag v4
```

send_file emits only the main entry:
```json
{"title": "beijing-travel-site", "ext": "web_project", "file_path": "/MyProjects/beijing-travel-site/index.html", "project_name": "beijing-travel-site", "version": "V4"}
```

#### 3.4.3 Prototype two-file delivery (stable rule)

When the caller skill is `prototype.md` and the version includes a two-file delivery (interactive prototype + flow doc):

1. **Version inclusion scope (mandatory)**
   This version must include and commit both HTML files (usually `prototype.html` and `flow.html`); committing only one of them is forbidden.
2. **Chat output (mandatory)**
   Call `send_file` **twice** for the same version number, emitting each single file:
   - First: `prototype.html`
   - Second: `flow.html`
3. **Card naming suggestion**
   Mark the file's role in `title` so the user can tell them apart (title contains no version number):
   - `{project-name}-prototype`
   - `{project-name}-flow`
4. **Prohibitions**
   - Packing `prototype.html + flow.html` into a directory and emitting it in one shot is forbidden
   - Emitting only one of the files and claiming the prototype two-file delivery is complete is forbidden

Example (same version V4, two consecutive calls):
```json
{"title":"enterprise-crm-admin-prototype","ext":"web_project","file_path":"/MyProjects/enterprise-crm-admin/prototype.html","project_name":"enterprise-crm-admin","version":"V4"}
{"title":"enterprise-crm-admin-flow","ext":"web_project","file_path":"/MyProjects/enterprise-crm-admin/flow.html","project_name":"enterprise-crm-admin","version":"V4"}
```

#### 3.4.4 Fixed-image export projects (social cards, etc.; new rule)

For scenarios with a `fixed-image` output target (e.g. social media cards, cover images, long images), the typical flow is:

1. **Generate the HTML first** (design-stage artifact) → save it as usual under `MyProjects/{project-name}/`
2. **Then run export** to produce images → save artifacts to `MyProjects/{project-name}/export/`
3. **Version management:** both the HTML and `export/` are tracked in Git, in the same commit
4. **send_file strategy (mandatory):**
   - **First call:** emit the HTML file (`ext: web_project`)
   - **Second call:** emit the export artifact
     - Single exported image: `ext: <specific extension>` (e.g. `png`, `jpg`), `file_path: /MyProjects/{project-name}/export/xxx.png`
     - Exported folder (multiple images): `ext: directory`, `file_path: /MyProjects/{project-name}/export/`

**Key rules:**
- The HTML and the export artifacts **must live under the same project directory**
- Both **must be in the same version (commit)**
- Export artifacts scattered outside the project directory are forbidden

Example (social long-image project, V2):
```bash
# Project directory structure
cd MyProjects/social-travel-guide
git add .
git commit -m "V2: refine cover colors and layout"
git tag v2
```

send_file calls (two in a row):
```json
{"title":"social-travel-guide","ext":"web_project","file_path":"/MyProjects/social-travel-guide/index.html","project_name":"social-travel-guide","version":"V2"}
{"title":"social-travel-guide-export","ext":"directory","file_path":"/MyProjects/social-travel-guide/export/"}
```

### 3.5 Chat cards and "Edit based on this version"

- **Historical versions and the latest version** display consistently at the top of the preview area (exact UI is implemented by the frontend); the agent does not distinguish between two preview protocols
- **Every** version card produced by `send_file` in the chat carries an "Edit based on this version" button (frontend-implemented)
- When the user clicks it, the input box is prefilled with: **"Edit based on '{project-name}' V{n}"** (e.g. `Edit based on 'beijing-travel-site' V2`; version number uses capital `V` + digits, matching `send_file.version`)
- When the agent receives that phrasing → handle it via the §4 **merge flow** (the `V{n}` in the text becomes `TARGET_TAG=v{n}`)
- **Both latest-version and historical-version cards** show the button; the preview top bar styling is identical (frontend-implemented; no extra agent action)

> **Note:** there is no separate "version list" capability; users specify versions via chat history cards or natural language.

---

## 4. Version Restore

### 4.1 Restore scope

A restore restores the **entire project directory state** (code files + `assets/` assets + `export/` artifacts). `git checkout` restores the target version's complete working tree, ensuring the restored version can be fully previewed.

### 4.2 Restore entry points

There is no dedicated frontend "restore" button. Restores are triggered by:

| Entry | Description |
|------|------|
| Natural language "restore to V2" | Agent runs the standard §4.3 restore directly |
| Natural language "restyle based on V2" | Agent runs the §4.4 merge flow (restore + edit = one version) |
| Chat card "Edit based on this version" button | Input box prefilled with "Edit based on '{project-name}' V{n}" → user sends → agent runs the §4.4 merge flow |
| Comment / parameter edit (in a historical version preview) | MD instruction contains a historical version number → agent runs the §4.4 merge flow |

### 4.3 Standard restore (restore only, no edits attached)

Restore = checkout + commit a new version + send_file; all three steps are required. A checkout alone does not count as a completed restore.
Commands:

```bash
cd MyProjects/{project-name}
TARGET_TAG="v{version number specified by the user}"
LATEST_TAG=$(git tag --sort=-v:refname | head -n 1)
NEXT_NUM=$((${LATEST_TAG#v} + 1))
NEXT_TAG="v${NEXT_NUM}"
git checkout $TARGET_TAG -- .
git add .
git commit -m "V${NEXT_NUM}: restore to V{target version}"
git tag $NEXT_TAG
# ↑ all of the above must complete, then update meta.json, and finally call send_file to emit the new version
```

**Understanding post-restore state:** the workspace files (code + `assets/` + `export/`) + `meta.json` are the source of truth; do not rely on a backend version service or replaying past conversations.

After restoring, the agent confirms with the user:
- The current project name and new version number
- Which files/pages are included
- The differences versus before the restore (e.g. "the food recommendations section is not included; that feature was added in V3")
- Call `send_file` to emit the new version's main entry (parameters same as §3.4).

Version numbers always increment (restoring V4 to V2 → produces V5). Original versions are preserved.

### 4.4 Restore + edit merge flow (produces exactly one version)

Applies when: the user asked to edit based on a historical version (including "Edit based on '{project-name}' V{n}").

**Version number rule:** no matter which historical version the edit is based on, the new version number **must** be plain numeric increment of the current latest version + 1 (e.g. current V8 → new version V9). Suffixed version numbers (like `V4-light`, `V4-dark`, `V2-new`) are **forbidden**, and naming with the base version as a prefix is forbidden. Overwriting, moving, or deleting existing version tags is **forbidden** — existing versions are always preserved; new versions can only be appended.

Commands:
```bash
cd MyProjects/{project-name}
TARGET_TAG="v{target version}"
git checkout $TARGET_TAG -- .
# ↓ apply the user-requested edits on this basis (modify file contents); no intermediate commit
LATEST_TAG=$(git tag --sort=-v:refname | head -n 1)
NEXT_NUM=$((${LATEST_TAG#v} + 1))
NEXT_TAG="v${NEXT_NUM}"
git add .
git commit -m "V${NEXT_NUM}: based on V{target version}: {edit summary}"
git tag $NEXT_TAG
# ↑ all of the above must complete, then update meta.json, and finally call send_file to emit the new version
```

---

## 5. meta.json Structure

One per project, recording the project's overall state. Excluded via `.gitignore`; never enters version history.

```json
{
  "project_name": "beijing-travel-site",
  "latest_version": "v3",
  "is_published": false,
  "published_version": null,
  "domain": null,
  "versions": [
    {
      "id": "v1",
      "timestamp": "2026-05-01T14:30:00+08:00",
      "based_on": null,
      "summary": "Homepage + attractions list"
    },
    {
      "id": "v2",
      "timestamp": "2026-05-05T10:30:00+08:00",
      "based_on": null,
      "summary": "Style switched to International Typographic Style"
    },
    {
      "id": "v3",
      "timestamp": "2026-05-06T14:30:00+08:00",
      "based_on": "v1",
      "summary": "Based on V1: redesigned page layout"
    }
  ]
}
```

| Field | Type | Description |
|------|------|------|
| project_name | string | Project name, auto-generated by the agent, user-modifiable |
| latest_version | string | Current latest version number (e.g. "v5") |
| is_published / published_version / domain | — | Default false / null in phase 1 |
| versions[].id | string | Version number (e.g. "v1") |
| versions[].timestamp | string | Creation time (ISO 8601 with timezone) |
| versions[].based_on | string \| null | Only set for restores or edits based on a historical version; points at the base version; null for normal edits |
| versions[].summary | string | One-sentence change summary auto-generated by the agent |

---

## 6. Operation Quick Reference

| User action | Agent action |
|--------|--------|
| "Build me a XX website" | **Create** `MyProjects/{project-name}/` first → generate files inside it → §1 create (git init + V1) → `send_file` |
| "Build a product prototype (prototype)" | **Create** the project directory first → generate `prototype.html` + `flow.html` inside it → same-version commit (both files in Git) → two consecutive `send_file` calls per §3.4.3 |
| "Make the title bigger" (no special context) | Edit latest version of latest project → §3.3 version commands → `send_file` |
| "Add a light theme to the existing project" | Generate `light.html` → same commit as existing files → `send_file` emits the main entry |
| "Change the title based on V2" / prefilled "Edit based on '{project-name}' V2" | §4 merge flow → `send_file` |
| Comment / parameter edit | Parse project name + version from the MD instruction → decide §3.3 or §4.4 per §3.1 rules → `send_file` |
| User uploads an image (`upload/`) | `cp` → `assets/` → align with HTML → §1 validation → §3.3 if code changed |
| HTML first, images later | `cp` using the HTML reference names; no commit if code unchanged, new version if references changed |
| Agent searches/generates images for the site | Download or write into `assets/` → write references → §1 validation → §3.3 |
| User only uploads, no code change | Only write `assets/`; no commit |
| Style change without image swap/module removal | Change code, **preserve assets references and files** → §3.3 → `send_file` |
| "Restore to V2" | §4 standard restore (code + assets roll back together) → `send_file` |
| Card "Edit based on this version" clicked | User sends the prefilled text → §4 merge → `send_file` |
| Natural language says "publish" / "unpublish" | Guide the user to the frontend publish button (not implemented in phase 1) |
| "Write me a proposal" | No version management triggered |
| Ambiguous reference | Scan `MyProjects/` → ask the user |
| Social card / cover image | Generate HTML → save into the project → export into `export/` → same commit → HTML `send_file` + export `send_file` |
| Style-sample stage ("show me a few directions first") | Generate `style-samples.html` → save to `MyProjects/{project-name}/` → `send_file` → wait for the user to pick a direction → no commit, no version number |

---

## 7. Appendix: Preview and Paths (agent reference)

- **Inside the workspace:** HTML uses relative paths like `assets/xxx.png`; in multi-file projects, `link` / `script` use relative paths to reference code files in the same or sub directories
- **During user preview:** the backend resolves absolute paths on the cloud machine and replaces them with OSS links; the agent must **never** write OSS URLs in source code
- **Git tracking scope:** code files + `assets/` assets + `export/` artifacts all go into Git; `meta.json` and `style-samples*.html` are excluded by `.gitignore`
- **Known limitations:** multi-file project JS/CSS preview and historical-version preview inconsistencies — see §0.1; not fixed this phase
