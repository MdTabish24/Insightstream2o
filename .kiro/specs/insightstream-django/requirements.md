# Requirements Document

## Introduction

InsightStream is a comprehensive YouTube analytics and content creation platform being rebuilt with Django. The platform provides AI-powered tools for YouTube creators to optimize their content, analyze performance, and grow their channels. This migration from Next.js to Django will maintain all existing functionality while leveraging Django's robust backend capabilities, admin interface, and Python ecosystem for AI/ML integrations.

## Glossary

- **InsightStream**: The YouTube analytics and content creation platform
- **Thumbnail**: A preview image for YouTube videos (16:9 aspect ratio)
- **Outlier**: A video that performs significantly above or below the channel average
- **SmartScore**: A weighted algorithm combining views, velocity, and engagement metrics
- **IQR (Interquartile Range)**: Statistical method for detecting outliers
- **Upload Streak**: Consistency pattern of video uploads over time
- **Algorithm Score**: A 0-100 rating based on YouTube ranking factors
- **Long-tail Keywords**: Specific, low-competition search phrases
- **FLUX Model**: AI image generation model via Replicate API
- **Gemini AI**: Google's AI model for content generation and analysis

## Requirements

### Requirement 1: User Authentication and Management

**User Story:** As a YouTube creator, I want to securely register and login to InsightStream, so that I can access personalized analytics and save my generated content.

#### Acceptance Criteria

1. WHEN a user submits valid registration credentials THEN the InsightStream system SHALL create a new user account and store the user in the database
2. WHEN a user submits valid login credentials THEN the InsightStream system SHALL authenticate the user and create a session
3. WHEN an unauthenticated user attempts to access protected routes THEN the InsightStream system SHALL redirect the user to the login page
4. WHEN a user logs out THEN the InsightStream system SHALL invalidate the session and redirect to the home page
5. WHEN a user registers THEN the InsightStream system SHALL validate email uniqueness and password strength

### Requirement 2: AI Thumbnail Generator

**User Story:** As a YouTube creator, I want to generate professional thumbnails using AI, so that I can create eye-catching visuals without graphic design skills.

#### Acceptance Criteria

1. WHEN a user submits a text prompt for thumbnail generation THEN the InsightStream system SHALL send the request to the FLUX AI model and return a generated image
2. WHEN the primary AI provider (Replicate) fails THEN the InsightStream system SHALL fallback to Pollinations AI and complete the generation
3. WHEN a thumbnail is successfully generated THEN the InsightStream system SHALL upload the image to ImageKit CDN and store the URL in the database
4. WHEN a user provides a reference image THEN the InsightStream system SHALL incorporate the reference style into the generated thumbnail
5. WHEN a user requests their thumbnail history THEN the InsightStream system SHALL return all thumbnails associated with the user's email
6. WHEN generating a thumbnail THEN the InsightStream system SHALL produce an image with 16:9 aspect ratio in PNG format

### Requirement 3: AI Content Generator

**User Story:** As a YouTube creator, I want AI-generated video concepts with optimized titles and descriptions, so that I can create content that performs well in search.

#### Acceptance Criteria

1. WHEN a user submits a topic for content generation THEN the InsightStream system SHALL return 3 unique video concepts with titles, descriptions, and tags
2. WHEN generating content THEN the InsightStream system SHALL include an SEO score (0-100) for each title based on keyword optimization
3. WHEN generating descriptions THEN the InsightStream system SHALL include hooks, main content sections, and calls-to-action
4. WHEN the AI generation fails THEN the InsightStream system SHALL return a basic fallback content structure
5. WHEN content is generated THEN the InsightStream system SHALL store the content as JSON in the database with user association

### Requirement 4: Keyword Research Tool

**User Story:** As a YouTube creator, I want to research keywords for my videos, so that I can optimize my content for discoverability.

#### Acceptance Criteria

1. WHEN a user submits a topic for keyword research THEN the InsightStream system SHALL return primary keywords with search volume analysis
2. WHEN performing keyword research THEN the InsightStream system SHALL return long-tail keywords for niche targeting
3. WHEN performing keyword research THEN the InsightStream system SHALL return trending keywords based on current YouTube data
4. WHEN performing keyword research THEN the InsightStream system SHALL return related topics for content expansion
5. WHEN returning keywords THEN the InsightStream system SHALL include metadata for search volume, competition level, and relevance score

### Requirement 5: Trending Hashtags Generator

**User Story:** As a YouTube creator, I want to discover trending hashtags for my niche, so that I can increase my video visibility.

#### Acceptance Criteria

1. WHEN a user requests trending hashtags for a topic THEN the InsightStream system SHALL extract real hashtags from trending YouTube videos
2. WHEN extracting hashtags THEN the InsightStream system SHALL use regex pattern matching on video descriptions
3. WHEN generating hashtags THEN the InsightStream system SHALL combine real extracted hashtags with AI-generated suggestions
4. WHEN returning hashtags THEN the InsightStream system SHALL include usage count and engagement metrics
5. WHEN a user clicks a hashtag THEN the InsightStream system SHALL copy the hashtag to clipboard

### Requirement 6: Thumbnail Search Engine

**User Story:** As a YouTube creator, I want to search for video thumbnails by text or similar images, so that I can find inspiration and analyze successful thumbnails.

#### Acceptance Criteria

1. WHEN a user submits a text search query THEN the InsightStream system SHALL return matching videos from YouTube Data API
2. WHEN returning search results THEN the InsightStream system SHALL include video statistics (views, likes, comments, publish date)
3. WHEN a user uploads an image for similarity search THEN the InsightStream system SHALL generate AI tags and find similar thumbnails
4. WHEN displaying thumbnails THEN the InsightStream system SHALL show high-quality preview images
5. WHEN analyzing thumbnails THEN the InsightStream system SHALL generate AI-powered tags describing the thumbnail content

### Requirement 7: Outlier Detection System

**User Story:** As a YouTube creator, I want to identify my best and worst performing videos, so that I can understand what content resonates with my audience.

#### Acceptance Criteria

1. WHEN a user submits a channel for outlier analysis THEN the InsightStream system SHALL calculate statistical outliers using the IQR method
2. WHEN calculating outliers THEN the InsightStream system SHALL use SmartScore algorithm (50% views, 30% velocity, 20% engagement)
3. WHEN calculating metrics THEN the InsightStream system SHALL normalize values to a 0-1 scale for fair comparison
4. WHEN detecting outliers THEN the InsightStream system SHALL identify both high outliers (above Q3 + 1.5×IQR) and low outliers (below Q1 - 1.5×IQR)
5. WHEN returning results THEN the InsightStream system SHALL include age-adjusted metrics (views per day)

### Requirement 8: Upload Streak Analyzer

**User Story:** As a YouTube creator, I want to analyze my upload consistency, so that I can optimize my posting schedule for the YouTube algorithm.

#### Acceptance Criteria

1. WHEN a user submits a channel for streak analysis THEN the InsightStream system SHALL calculate an algorithm score (0-100)
2. WHEN analyzing uploads THEN the InsightStream system SHALL retrieve the last 50 videos from the channel's uploads playlist
3. WHEN analyzing content THEN the InsightStream system SHALL distinguish between Shorts and regular videos
4. WHEN returning analysis THEN the InsightStream system SHALL include view predictions for upcoming videos
5. WHEN returning analysis THEN the InsightStream system SHALL recommend optimal upload schedules based on current patterns
6. WHEN returning analysis THEN the InsightStream system SHALL include AI-powered growth suggestions

### Requirement 9: Admin Dashboard

**User Story:** As a platform administrator, I want to view platform statistics and manage users, so that I can monitor platform health and usage.

#### Acceptance Criteria

1. WHEN an admin logs in with valid credentials THEN the InsightStream system SHALL grant access to the admin dashboard
2. WHEN viewing the dashboard THEN the InsightStream system SHALL display total users, thumbnails generated, and content created
3. WHEN viewing the dashboard THEN the InsightStream system SHALL identify and display the most active users
4. WHEN viewing the dashboard THEN the InsightStream system SHALL show recent user registrations
5. WHEN invalid admin credentials are submitted THEN the InsightStream system SHALL deny access and display an error message

### Requirement 10: API Key Management and Rate Limiting

**User Story:** As a system administrator, I want the platform to handle API rate limits gracefully, so that the service remains reliable under high load.

#### Acceptance Criteria

1. WHEN an API key reaches its rate limit THEN the InsightStream system SHALL rotate to the next available API key
2. WHEN all API keys are exhausted THEN the InsightStream system SHALL return a user-friendly error message
3. WHEN making external API calls THEN the InsightStream system SHALL implement retry logic with exponential backoff
4. WHEN caching is applicable THEN the InsightStream system SHALL cache responses to reduce API calls

### Requirement 11: Data Persistence and Storage

**User Story:** As a user, I want my generated content to be saved and retrievable, so that I can access my work across sessions.

#### Acceptance Criteria

1. WHEN a thumbnail is generated THEN the InsightStream system SHALL persist the thumbnail URL, user input, and creation timestamp
2. WHEN content is generated THEN the InsightStream system SHALL persist the content JSON, user input, and creation timestamp
3. WHEN a user requests their history THEN the InsightStream system SHALL return items ordered by creation date descending
4. WHEN storing data THEN the InsightStream system SHALL associate all records with the user's email address

### Requirement 12: Django REST API

**User Story:** As a frontend developer, I want well-structured REST API endpoints, so that I can build responsive user interfaces.

#### Acceptance Criteria

1. WHEN an API request is made THEN the InsightStream system SHALL return JSON-formatted responses
2. WHEN an API error occurs THEN the InsightStream system SHALL return appropriate HTTP status codes with error details
3. WHEN processing requests THEN the InsightStream system SHALL validate input data and return validation errors
4. WHEN returning lists THEN the InsightStream system SHALL support pagination for large result sets
5. WHEN an authenticated endpoint is accessed without valid credentials THEN the InsightStream system SHALL return a 401 Unauthorized response
