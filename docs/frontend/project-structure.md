# Naija News Hub Frontend - Project Structure

## Directory Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js app directory
│   │   ├── (auth)/            # Authentication routes
│   │   │   ├── login/
│   │   │   └── register/
│   │   ├── (dashboard)/       # Dashboard routes
│   │   │   ├── articles/
│   │   │   ├── websites/
│   │   │   ├── jobs/
│   │   │   ├── errors/
│   │   │   └── settings/
│   │   ├── layout.tsx         # Root layout
│   │   └── page.tsx           # Home page
│   ├── components/            # Reusable components
│   │   ├── layout/           # Layout components
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Footer.tsx
│   │   ├── dashboard/        # Dashboard components
│   │   │   ├── StatsCard.tsx
│   │   │   ├── JobStatus.tsx
│   │   │   └── ErrorSummary.tsx
│   │   ├── articles/         # Article components
│   │   │   ├── ArticleCard.tsx
│   │   │   ├── ArticleGrid.tsx
│   │   │   └── ArticleFilters.tsx
│   │   └── common/           # Common components
│   │       ├── Button.tsx
│   │       ├── Input.tsx
│   │       └── Loading.tsx
│   ├── lib/                  # Utility functions
│   │   ├── api/             # API client
│   │   │   ├── client.ts
│   │   │   ├── articles.ts
│   │   │   ├── websites.ts
│   │   │   └── jobs.ts
│   │   ├── auth/            # Authentication
│   │   │   ├── auth.ts
│   │   │   └── middleware.ts
│   │   └── utils/           # Utility functions
│   │       ├── date.ts
│   │       └── format.ts
│   ├── hooks/               # Custom hooks
│   │   ├── useWebSocket.ts
│   │   ├── useArticles.ts
│   │   └── useJobs.ts
│   ├── types/              # TypeScript types
│   │   ├── article.ts
│   │   ├── website.ts
│   │   └── job.ts
│   └── styles/             # Global styles
│       └── globals.css
├── public/                 # Static assets
├── package.json
└── tsconfig.json
```

## Core Components

### Layout Components

1. **Header** ✅
   - Logo
   - Navigation
   - User menu
   - Theme toggle
   - Search bar
   - Mobile responsive design

2. **Sidebar** ✅
   - Navigation links
   - Collapsible sections
   - Active state indicators
   - Mobile responsive design

3. **Footer** ✅
   - Copyright
   - Links
   - Version info
   - Mobile responsive design

### Dashboard Components

1. **StatsCard** ✅
   - Title
   - Value
   - Icon
   - Trend indicator
   - Responsive design

2. **JobStatus** ✅
   - Progress bar
   - Status text
   - Time elapsed
   - Action buttons
   - Real-time updates

3. **ErrorSummary** ✅
   - Error count
   - Error types
   - Recent errors
   - Resolution status
   - Real-time updates

### Article Components

1. **ArticleCard** (In Progress)
   - Title
   - Excerpt
   - Image
   - Metadata
   - Action buttons

2. **ArticleGrid** (In Progress)
   - Responsive grid layout
   - Pagination
   - Loading states
   - Empty state

3. **ArticleFilters** (In Progress)
   - Search
   - Date range
   - Website filter
   - Category filter

## Features

### Real-time Updates (In Progress)

1. **WebSocket Integration**
   - Connection management
   - Event handling
   - Reconnection logic
   - Error handling

2. **Data Synchronization**
   - Job status updates
   - Article updates
   - Error notifications
   - User notifications

### Authentication (Planned)

1. **User Management**
   - Login/Register
   - Password reset
   - Profile management
   - Session handling

2. **Authorization**
   - Role-based access
   - Route protection
   - API token management
   - Permission checks

### UI/UX

1. **Responsive Design** ✅
   - Mobile-first approach
   - Breakpoint handling
   - Responsive layouts
   - Touch interactions

2. **Theme Support** ✅
   - Light/Dark mode
   - Theme persistence
   - Custom themes
   - Color schemes

3. **Loading States** ✅
   - Skeleton loading
   - Progress indicators
   - Error states
   - Empty states

## API Integration

### API Client ✅

1. **Base Client**
   - Axios configuration
   - Error handling
   - Request/Response interceptors
   - Authentication headers
   - TypeScript types

2. **Resource Clients**
   - Articles API
   - Websites API
   - Jobs API
   - Users API

### Data Management (In Progress)

1. **State Management**
   - React Query setup
   - Cache configuration
   - Mutation handling
   - Optimistic updates

2. **Data Fetching**
   - Pagination
   - Infinite scroll
   - Search
   - Filtering

## Development Guidelines

1. **Code Style** ✅
   - ESLint configuration
   - Prettier setup
   - TypeScript strict mode
   - Component patterns

2. **Testing** (In Progress)
   - Jest setup
   - React Testing Library
   - Component tests
   - Integration tests

3. **Performance** (In Progress)
   - Code splitting
   - Image optimization
   - Bundle analysis
   - Performance monitoring

4. **Documentation** ✅
   - Component documentation
   - API documentation
   - Usage examples
   - Development guides

## Services Directory
The `services` directory contains API-related services and utilities:

- `api.ts`: Main API client implementation
- `mockApi.ts`: Mock API service for development and testing
  - Simulates API endpoints with realistic delays
  - Provides mock data for articles, categories, and sources
  - Supports filtering, pagination, and search

## Data Directory
The `data` directory contains mock data and type definitions:

- `mockData.ts`: Mock data for development
  - Articles with metadata
  - Categories and sources
  - Consistent data structure for testing 