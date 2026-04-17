# Standardise Logging Usage Across Modules

## Summary
Logging system exists but usage is inconsistent across modules.

## Problem
- Mixed structured and unstructured logs
- Some UI output still logged
- Inconsistent use of log levels

## Desired Behaviour
- Use structured logging everywhere
- Separate UI output from logs
- Consistent log levels

## Proposed Solution
- Audit all log calls
- Replace legacy logs with structured events
- Ensure print() does not log

## Acceptance Criteria
- [ ] All logs follow structured format
- [ ] No UI text appears in logs
- [ ] Consistent log levels used
