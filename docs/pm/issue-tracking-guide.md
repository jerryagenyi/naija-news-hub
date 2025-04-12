# Naija News Hub - Issue Tracking Guide

## Overview

GitHub Issues is a powerful tool for tracking tasks, bugs, and feature requests. This guide explains how to use GitHub Issues effectively for the Naija News Hub project.

## Issue Types

### 1. Epics (Large Features)
- Use the `epic` label
- Example: "Implement Core Scraping Functionality"
- Should be broken down into smaller stories and tasks
- Include acceptance criteria and dependencies

### 2. Stories (User-Facing Features)
- Use the `story` label
- Example: "As a user, I want to add a new news source"
- Should be testable and have clear acceptance criteria
- May be part of an epic

### 3. Tasks (Technical Implementation)
- Use the `task` label
- Example: "Implement database schema for news sources"
- Should be specific and actionable
- May be part of a story

### 4. Bugs
- Use the `bug` label
- Example: "Fix rate limiting not working for specific news source"
- Should include steps to reproduce
- Should be prioritized based on severity

### 5. Documentation
- Use the `documentation` label
- Example: "Update API documentation for new endpoints"
- Should reference the relevant code or feature
- Should specify the documentation type (user guide, API docs, etc.)

## Issue Structure

### Title
- Clear and descriptive
- Use present tense
- Example: "Implement user authentication system"

### Description
- Problem statement or feature description
- Acceptance criteria
- Technical details
- Dependencies
- Related issues

### Labels
- Type: `epic`, `story`, `task`, `bug`, `documentation`
- Priority: `priority: critical`, `priority: high`, `priority: medium`, `priority: low`
- Component: `component: api`, `component: scraper`, `component: database`, `component: frontend`
- Status: `status: in-progress`, `status: review`, `status: blocked`

### Assignees
- Assign to specific team members
- Use @mentions for discussions
- Update when reassigned

### Milestones
- Link to project milestones
- Use for tracking progress
- Example: "M1: Initial Setup"

## Workflow

### 1. Creating Issues
1. Click "New Issue" in GitHub
2. Select appropriate template
3. Fill in all required fields
4. Add relevant labels
5. Assign to milestone
6. Submit issue

### 2. Issue Lifecycle
1. **Backlog**: New issues start here
2. **To Do**: Issues ready for implementation
3. **In Progress**: Currently being worked on
4. **Review**: Ready for review
5. **Done**: Completed and verified

### 3. Updating Issues
- Update status regularly
- Add comments for progress
- Link related issues
- Update labels as needed
- Close when complete

## Best Practices

### Writing Good Issues
- Be specific and detailed
- Include acceptance criteria
- Add screenshots when relevant
- Reference related code or documentation
- Use markdown formatting

### Managing Issues
- Regular triage meetings
- Update status daily
- Close completed issues
- Archive old issues
- Use project boards for visualization

### Issue Templates

#### Epic Template
```markdown
## Description
[Detailed description of the epic]

## Goals
- [ ] Goal 1
- [ ] Goal 2
- [ ] Goal 3

## Stories
- [ ] Story 1
- [ ] Story 2
- [ ] Story 3

## Dependencies
- Dependency 1
- Dependency 2

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
```

#### Story Template
```markdown
## User Story
As a [type of user], I want [goal] so that [benefit]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Details
[Relevant technical information]

## Dependencies
- Dependency 1
- Dependency 2
```

#### Task Template
```markdown
## Description
[Detailed description of the task]

## Implementation Steps
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Testing
- [ ] Test case 1
- [ ] Test case 2

## Dependencies
- Dependency 1
- Dependency 2
```

#### Bug Template
```markdown
## Description
[Description of the bug]

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- OS: [Operating System]
- Browser: [Browser and Version]
- Other relevant details

## Screenshots
[If applicable]
```

## Project Board Setup

### Columns
1. **Backlog**
   - New issues
   - Future work
   - Low priority items

2. **To Do**
   - Ready for implementation
   - Prioritized items
   - Next sprint items

3. **In Progress**
   - Currently being worked on
   - Blocked items
   - Need help items

4. **Review**
   - Ready for review
   - Testing needed
   - Documentation needed

5. **Done**
   - Completed items
   - Verified items
   - Deployed items

### Automation
- Use GitHub Actions for automation
- Auto-assign reviewers
- Auto-label based on content
- Auto-close stale issues
- Auto-update status

## Regular Maintenance

### Daily
- Update issue status
- Respond to comments
- Review new issues
- Update project board

### Weekly
- Triage meeting
- Priority review
- Progress review
- Clean up old issues

### Monthly
- Milestone review
- Issue cleanup
- Process improvement
- Documentation update

## Version History

### 1.0.0 - March 2024
- Initial creation of issue tracking guide
- Definition of issue types and templates
- Establishment of workflow
- Setup of project board structure 