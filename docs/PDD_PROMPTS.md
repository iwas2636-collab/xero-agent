# PDD Developer Prompts Guide

This guide provides specific prompts for each stage of Prompt-Driven Development.

## Phase 1: Architect (Design & Planning)

```
Design [FEATURE] as a minimal, testable slice:

**Requirements:**
- [Specific requirement 1]
- [Specific requirement 2]

**Scope:**
- Files to create/modify: [specific paths]
- Public interface + request/response payloads

**Acceptance Criteria:**
- Given: [initial state]
- When: [user action]
- Then: [expected outcome]

Output: Detailed plan + file structure outline (no code yet)
```

## Phase 2: Red (Failing Tests)

```
Create failing tests for [BEHAVIOR]:

**Test Requirements:**
- Unit tests for core logic
- Integration tests for external dependencies
- Edge cases and negative scenarios

**Constraints:**
- No production code changes
- Tests should fail initially
- Use existing project structure

Output: Test files only, no implementation code
```

## Phase 3: Green (Minimal Implementation)

```
Implement minimal code to make tests pass:

**Guidelines:**
- Simplest possible solution
- No premature optimization
- No unrelated refactoring
- Preserve existing public APIs

Output: Minimal implementation diff only
```

## Phase 4: Refactor (Code Improvement)

```
Refactor implementation while keeping all tests green:

**Goals:**
- Improve code clarity and readability
- Extract common patterns
- Reduce duplication

**Constraints:**
- All existing tests must pass
- Preserve public API contracts

Output: Refactored code with explanation
```

## AI Agent Specific Prompts

### Agent Development
```
Build an AI agent component:
- Agent role: [CustomerAgent/ResearchAgent]
- Core tools: [built-in and custom tools]
- Safety guardrails: [input validation, output filtering]
- Session management: [memory and context handling]

Include streaming response support and error handling.
```

### Security Testing
```
Add security tests for the AI agent:
- Prompt injection prevention
- PII data handling validation
- Input sanitization testing
- Response content filtering

Tests should cover malicious input scenarios and error handling.
```
