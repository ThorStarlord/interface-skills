# Execution Modes

The `workflow-orchestrator` supports five distinct execution modes, each with different safety boundaries and user involvement.

| Mode | Allowed | Description | Approval Gates | Safety Requirements |
| :--- | :--- | :--- | :--- | :--- |
| `plan_only` | Yes | Generate plan only. No execution. | N/A | None |
| `prompt_chain` | Yes | Generate copy/paste prompts for specialized skills. | N/A | None |
| `guided_execution` | Yes | Execute one step at a time with user approval. | Mandatory | None |
| `autonomous_execution` | Yes | Execute full chain automatically with approval gates. | Mandatory | High-risk opt-in |
| `yolo_execution` | Yes | Full automation of local steps without intermediate gates. | Bypassed | Explicit YOLO opt-in, Feature Branch, Run Log |

---

### 1. `plan_only` (Default)
The safest mode. The orchestrator analyzes the brief, selects a workflow, and explains the sequence without touching the repository.

### 2. `prompt_chain`
Produces a series of prompts that the user can manually copy and paste into other agent sessions. Useful when the user wants full control over the execution context.

### 3. `guided_execution`
The orchestrator executes steps one by one. After each step, it must present the artifact produced and wait for user approval before proceeding to the next step.

### 4. `autonomous_execution`
The orchestrator executes the full chain but **MUST stop at every defined [Approval Gate](approval-gates.md)**.
- **Requirement**: User must provide the opt-in string: `"I accept the risks of autonomous execution."`
- **Safety**: Cannot commit to `main`, cannot delete core files.
- **Scope**: Can execute `local` and `local_command` skills.

### 5. `yolo_execution`
Maximum automation for local sensemaking and assumed-installed implementation skills. All approval gates are bypassed for eligible skills.
- **Requirement**: User must provide the exact opt-in string: 
  `"I choose yolo_execution and accept automated repository changes, feature-branch commits, bypassed gates, and recovery risk."`
- **Requirement**: Every step must be `availability.type: local` or `local_command`. Skills marked as `external`, `external_required`, or `prompt_only` are NOT permitted in YOLO mode.
- **Requirement**: Must use a **feature branch**. Direct commits to `main` or `master` are strictly prohibited.
- **Requirement**: Must write a [Run Log](run-log-template.md) before and after mutation.
- **Requirement**: Must follow the [Git Safety Policy](git-safety-policy.md) and [Recovery Policy](recovery-policy.md).
