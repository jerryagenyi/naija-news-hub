# Naija News Hub - Modern News Aggregation Dashboard

## Project Overview
Naija News Hub is a news aggregation platform that collects and displays news articles from various Nigerian news sources. The dashboard provides a modern, responsive interface with dark mode support, built using Tailwind CSS.

## Design System

### Color Palette
- **Primary Gradient**: 
  - From: Emerald Green (`#10B981`) 
  - To: Royal Blue (`#2563EB`)
- **Dark Mode**:
  - Background: Navy (`#1F2937`) 
  - Darker Background: (`#111827`)
- **Text Colors**:
  - Headings: White
  - Body: Light Gray (`#9CA3AF`)
- **Accent Colors**:
  - Success: Green (`#10B981`)
  - Warning: Yellow (`#FBBF24`)
  - Error: Red (`#EF4444`)
  - Info: Blue (`#3B82F6`)

### Typography
- **Font Family**: Inter or similar sans-serif
- **Sizes**:
  - Page Titles: 2xl (24px)
  - Section Headers: lg (18px)
  - Body Text: sm (14px)
  - Metadata: xs (12px)

## Layout Components

### 1. Header
- Fixed position with gradient background
- Height: 64px
- **Left Section**:
  - Logo (40x40 rounded)
  - "Naija News Hub" text
- **Right Section**:
  - Search icon
  - User profile with dropdown
  - Theme toggle

### 2. Sidebar
- Width: 256px
- Dark background (`#1F2937`)
- **Navigation Items**:
  ```
  - Dashboard (active state)
  - Articles (with "New" badge)
  - Websites
  - Jobs
  - Analytics ▾
    └─ Overview
    └─ Traffic
    └─ Content
  - System ▾
    └─ Status
    └─ Logs
    └─ Database
  - Errors (with "2" badge in red)
  - Settings
  - Help
  ```
- **System Status Widget** (bottom):
  - CPU Usage: 23%
  - Memory Usage: 45%
  - Status: "Online" badge

### 3. Main Content

#### Stats Cards Grid
- Responsive: 2x2 (mobile), 4x1 (desktop)
```
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Total Articles  │ │ Active Websites │ │   Active Jobs   │ │ Recent Errors   │
│     1,234      │ │       15        │ │        3        │ │        2        │
│    +12.5% ▲    │ │    [Globe]      │ │     -2% ▼      │ │    +50% ▼      │
│   [Document]    │ │                 │ │    [Clock]      │ │    [Alert]      │
└─────────────────┘ └─────────────────┘ └─────────────────┘ └─────────────────┘
```

#### Active Jobs Section
- Card with dark background
```
┌─ Punch News ───────────────────────┐
│ Status: Running | Time: 30 mins    │
│ [================>─────] 75%       │
├─ Vanguard News ────────────────────┤
│ Status: Paused | Time: 15 mins     │
│ [========>──────────] 45%         │
├─ ThisDay ─────────────────────────┤
│ Status: Failed | Time: 45 mins     │
│ [==================>──] 90%       │
└───────────────────────────────────┘
```

#### Recent Errors Section
- Card with dark background
```
┌─ Punch News ───────────────────────┐
│ Type: Network Error                │
│ Message: "Connection timeout"      │
│ Time: 10 minutes ago              │
├─ Vanguard News ────────────────────┤
│ Type: Parsing Error               │
│ Message: "Failed to extract..."    │
│ Time: 25 minutes ago              │
└───────────────────────────────────┘
```

#### Latest Articles Table
- Responsive with horizontal scroll on mobile
```
┌────────────────┬──────────┬─────────┬──────────┬───────────┬─────────┐
│ Title          │ Category │ Source  │ Date     │ Tags      │ Actions │
├────────────────┼──────────┼─────────┼──────────┼───────────┼─────────┤
│ Nigeria Annou..│ Politics │ Punch   │ Apr 18   │ Economy,  │ •••     │
│                │          │ News    │ 2024     │ Government│         │
├────────────────┼──────────┼─────────┼──────────┼───────────┼─────────┤
│ Tech Startups..│ Tech     │ TechCa..│ Apr 17   │ Startups, │ •••     │
│                │          │         │ 2024     │ Funding   │         │
└────────────────┴──────────┴─────────┴──────────┴───────────┴─────────┘
```

## Interactive Features

### Real-time Updates
- Job progress bars
- Error notifications
- System status metrics

### Hover States
- Navigation items: Light hover effect
- Cards: Subtle elevation
- Buttons: Opacity change
- Table rows: Background color change

### Animations
- Sidebar toggle: Smooth slide
- Progress bars: Loading animation
- Status indicators: Pulse effect
- Error count: Fade in/out

## Responsive Behavior
- **Mobile**: Single column layout, collapsible sidebar
- **Tablet**: 2-column grid for stats
- **Desktop**: Full layout with fixed sidebar

## Technical Requirements
- **Framework**: Next.js with React
- **Styling**: Tailwind CSS exclusively
- **Icons**: Feather icons (react-icons/fi)
- **State Management**: React hooks
- **Breakpoints**:
  - Mobile: < 640px
  - Tablet: 640px - 1024px
  - Desktop: > 1024px

## Additional Notes
- All metrics should be real-time updatable
- Error states should be clearly visible
- Success states should be subtle but noticeable
- Loading states for all async operations
- Accessibility features must be maintained
- Dark mode support is required
- Tooltips for icons and abbreviated information
- Empty states for all data-dependent components

---

_© 2024 Naija News Hub. All rights reserved._