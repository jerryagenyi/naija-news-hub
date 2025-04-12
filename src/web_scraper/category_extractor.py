"""
Category extraction module for Naija News Hub.

This module provides functions to extract categories from article content.
"""

import re
import json
import logging
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def extract_categories_from_html(html: str) -> List[str]:
    """
    Extract categories from HTML content.

    Args:
        html: HTML content

    Returns:
        List of categories
    """
    categories = []

    # Try article:section meta tag
    section_match = re.search(r'<meta\s+property=["\']article:section["\']\s+content=["\']([^"\']*)["\']/>', html, re.IGNORECASE | re.DOTALL)
    if section_match and section_match.group(1).strip():
        categories.append(section_match.group(1).strip())

    # Try og:article:section meta tag
    og_section_match = re.search(r'<meta\s+property=["\']og:article:section["\']\s+content=["\']([^"\']*)["\']/>', html, re.IGNORECASE | re.DOTALL)
    if og_section_match and og_section_match.group(1).strip():
        categories.append(og_section_match.group(1).strip())

    # Try article:section:secondary meta tag
    secondary_section_match = re.search(r'<meta\s+property=["\']article:section:secondary["\']\s+content=["\']([^"\']*)["\']/>', html, re.IGNORECASE | re.DOTALL)
    if secondary_section_match and secondary_section_match.group(1).strip():
        categories.append(secondary_section_match.group(1).strip())

    # Try DublinCore subject meta tag
    dc_subject_match = re.search(r'<meta\s+name=["\']DC.subject["\']\s+content=["\']([^"\']*)["\']/>', html, re.IGNORECASE | re.DOTALL)
    if dc_subject_match and dc_subject_match.group(1).strip():
        categories.extend([subj.strip() for subj in dc_subject_match.group(1).split(',') if subj.strip()])

    # Try to extract categories from breadcrumbs
    breadcrumb_matches = re.findall(r'<li\s+class=["\']breadcrumb-item["\'][^>]*>\s*<a[^>]*>([^<]+)</a>', html, re.IGNORECASE)
    if breadcrumb_matches:
        categories.extend([crumb.strip() for crumb in breadcrumb_matches if crumb.strip()])

    # Try to extract from JSON-LD
    json_ld_match = re.search(r'<script\s+type=["\']application/ld\+json["\'][^>]*>([^<]+)</script>', html, re.IGNORECASE | re.DOTALL)
    if json_ld_match:
        try:
            json_data = json.loads(json_ld_match.group(1))
            if isinstance(json_data, dict):
                # Check for articleSection
                if 'articleSection' in json_data:
                    if isinstance(json_data['articleSection'], list):
                        categories.extend([section.strip() for section in json_data['articleSection'] if section.strip()])
                    elif isinstance(json_data['articleSection'], str) and json_data['articleSection'].strip():
                        categories.append(json_data['articleSection'].strip())

                # Check for breadcrumb
                if 'breadcrumb' in json_data and 'itemListElement' in json_data['breadcrumb']:
                    for item in json_data['breadcrumb']['itemListElement']:
                        if 'name' in item and item['name'].strip():
                            categories.append(item['name'].strip())
        except (json.JSONDecodeError, AttributeError, KeyError):
            pass

    # Try to extract from schema.org markup
    schema_match = re.search(r'<div\s+itemscope\s+itemtype=["\']http://schema.org/Article["\'][^>]*>(.*?)</div>', html, re.IGNORECASE | re.DOTALL)
    if schema_match:
        # Look for articleSection
        section_matches = re.findall(r'<meta\s+itemprop=["\']articleSection["\']\s+content=["\']([^"\']*)["\']/>', schema_match.group(1), re.IGNORECASE)
        categories.extend([section.strip() for section in section_matches if section.strip()])

    # Try to extract from navigation menu
    nav_matches = re.findall(r'<li\s+class=["\'].*?current.*?["\']\s*>.*?<a[^>]*>([^<]+)</a>', html, re.IGNORECASE | re.DOTALL)
    if nav_matches:
        categories.extend([nav.strip() for nav in nav_matches if nav.strip()])

    # Try to extract from URL path
    url_match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']*)["\']/>', html, re.IGNORECASE)
    if url_match:
        url = url_match.group(1)
        path = urlparse(url).path.strip('/')
        path_parts = path.split('/')

        # Common category indicators in URLs
        category_indicators = ['category', 'section', 'topic', 'cat', 'dept', 'channel']

        for i, part in enumerate(path_parts):
            if part.lower() in category_indicators and i + 1 < len(path_parts):
                # The next part is likely a category
                category = path_parts[i + 1].replace('-', ' ').replace('_', ' ').title()
                categories.append(category)

    # Remove duplicates and ensure we have at least one category
    categories = list(dict.fromkeys([cat for cat in categories if cat]))

    return categories

def extract_tags_from_html(html: str) -> List[str]:
    """
    Extract tags from HTML content.

    Args:
        html: HTML content

    Returns:
        List of tags
    """
    tags = []

    # Try article:tag meta tag
    tags_match = re.search(r'<meta\s+property=["\']article:tag["\']\s+content=["\']([^"\']*)["\']/>', html, re.IGNORECASE | re.DOTALL)
    if tags_match and tags_match.group(1).strip():
        tags.extend([tag.strip() for tag in tags_match.group(1).split(',') if tag.strip()])

    # Try keywords meta tag
    keywords_match = re.search(r'<meta\s+name=["\']keywords["\']\s+content=["\']([^"\']*)["\']/>', html, re.IGNORECASE | re.DOTALL)
    if keywords_match and keywords_match.group(1).strip():
        tags.extend([tag.strip() for tag in keywords_match.group(1).split(',') if tag.strip()])

    # Try to extract from JSON-LD
    json_ld_match = re.search(r'<script\s+type=["\']application/ld\+json["\'][^>]*>([^<]+)</script>', html, re.IGNORECASE | re.DOTALL)
    if json_ld_match:
        try:
            json_data = json.loads(json_ld_match.group(1))
            if isinstance(json_data, dict):
                # Check for keywords
                if 'keywords' in json_data:
                    if isinstance(json_data['keywords'], list):
                        tags.extend([keyword.strip() for keyword in json_data['keywords'] if keyword.strip()])
                    elif isinstance(json_data['keywords'], str) and json_data['keywords'].strip():
                        tags.extend([tag.strip() for tag in json_data['keywords'].split(',') if tag.strip()])
        except (json.JSONDecodeError, AttributeError, KeyError):
            pass

    # Try to extract from tag links
    tag_matches = re.findall(r'<a\s+[^>]*?(?:class=["\'].*?tag.*?["\']|href=["\'].*?/tag/.*?["\'])[^>]*>([^<]+)</a>', html, re.IGNORECASE | re.DOTALL)
    if tag_matches:
        tags.extend([tag.strip() for tag in tag_matches if tag.strip()])

    # Remove duplicates
    tags = list(dict.fromkeys([tag for tag in tags if tag]))

    return tags

def normalize_category_name(name: str) -> str:
    """
    Normalize a category name.

    Args:
        name: Category name

    Returns:
        Normalized category name
    """
    # Convert to title case
    normalized = name.title()

    # Replace common abbreviations
    abbreviations = {
        'Ai': 'AI',
        'Ml': 'ML',
        'Iot': 'IoT',
        'Nft': 'NFT',
        'Vr': 'VR',
        'Ar': 'AR',
        'Ui': 'UI',
        'Ux': 'UX',
        'Api': 'API',
        'Seo': 'SEO',
        'Ceo': 'CEO',
        'Cto': 'CTO',
        'Cfo': 'CFO',
        'Hr': 'HR',
        'Pr': 'PR',
        'Tv': 'TV',
        'Usa': 'USA',
        'Uk': 'UK',
        'Eu': 'EU',
        'Un': 'UN',
        'Us': 'US',
    }

    for abbr, replacement in abbreviations.items():
        normalized = normalized.replace(abbr, replacement)

    # Replace special characters with spaces
    normalized = re.sub(r'[^\w\s]', ' ', normalized)

    # Remove extra whitespace
    normalized = re.sub(r'\s+', ' ', normalized).strip()

    return normalized

def generate_category_url(base_url: str, category_name: str) -> str:
    """
    Generate a URL for a category.

    Args:
        base_url: Base URL of the website
        category_name: Category name

    Returns:
        Category URL
    """
    # Normalize the category name
    normalized = normalize_category_name(category_name)

    # Convert to URL-friendly format
    slug = normalized.lower().replace(' ', '-')

    # Remove any remaining special characters
    slug = re.sub(r'[^\w\-]', '', slug)

    # Ensure base_url ends with a slash
    if not base_url.endswith('/'):
        base_url += '/'

    # Generate the URL
    return f"{base_url}category/{slug}"

def categorize_article(article_data: Dict[str, Any], base_url: str) -> Dict[str, Any]:
    """
    Categorize an article based on its content.

    Args:
        article_data: Article data
        base_url: Base URL of the website

    Returns:
        Updated article data with categories
    """
    # Get HTML content
    html = article_data.get("content_html", "")

    # Extract categories
    categories = extract_categories_from_html(html)

    # If no categories found, try to infer from title and content
    if not categories:
        title = article_data.get("title", "")
        content = article_data.get("content", "")

        # Common news categories
        category_keywords = {
            "Politics": ["politics", "government", "election", "vote", "president", "minister", "parliament", "senate", "congress", "democrat", "republican"],
            "Business": ["business", "economy", "market", "stock", "finance", "investment", "company", "corporate", "entrepreneur", "startup"],
            "Technology": ["technology", "tech", "software", "hardware", "app", "digital", "internet", "web", "online", "cyber", "ai", "artificial intelligence", "machine learning", "blockchain", "crypto"],
            "Entertainment": ["entertainment", "celebrity", "movie", "film", "music", "album", "song", "artist", "actor", "actress", "tv", "television", "show", "series"],
            "Sports": ["sports", "football", "soccer", "basketball", "tennis", "golf", "cricket", "rugby", "athlete", "tournament", "championship", "league", "match", "game", "player", "team"],
            "Health": ["health", "medical", "medicine", "doctor", "hospital", "disease", "virus", "pandemic", "vaccine", "treatment", "wellness", "fitness"],
            "Science": ["science", "research", "study", "scientist", "discovery", "space", "astronomy", "physics", "chemistry", "biology", "environment", "climate"],
            "Education": ["education", "school", "university", "college", "student", "teacher", "professor", "academic", "learning", "course", "degree", "curriculum"],
            "Travel": ["travel", "tourism", "tourist", "destination", "vacation", "holiday", "trip", "tour", "hotel", "resort", "flight", "airline"],
            "Food": ["food", "recipe", "cooking", "chef", "restaurant", "cuisine", "meal", "dish", "ingredient", "diet", "nutrition"],
            "Fashion": ["fashion", "style", "clothing", "dress", "outfit", "designer", "model", "trend", "collection", "runway", "brand"],
            "Lifestyle": ["lifestyle", "living", "home", "family", "relationship", "marriage", "wedding", "parenting", "child", "baby"],
            "Opinion": ["opinion", "editorial", "column", "commentary", "perspective", "viewpoint", "analysis"],
            "World": ["world", "international", "global", "foreign", "country", "nation", "continent", "region"],
            "Local": ["local", "community", "neighborhood", "city", "town", "municipal", "regional", "state", "provincial"]
        }

        # Count keyword occurrences
        category_scores = {category: 0 for category in category_keywords}

        # Check title (higher weight)
        title_lower = title.lower()
        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in title_lower:
                    category_scores[category] += 3

        # Check content
        content_lower = content.lower()
        for category, keywords in category_keywords.items():
            for keyword in keywords:
                category_scores[category] += content_lower.count(keyword)

        # Get top categories
        top_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)

        # Add top categories if they have a score > 0
        for category, score in top_categories[:3]:
            if score > 0:
                categories.append(category)

    # Ensure we have at least one category
    if not categories:
        categories = ["News"]

    # Normalize category names
    categories = [normalize_category_name(category) for category in categories]

    # Remove duplicates
    categories = list(dict.fromkeys(categories))

    # Extract tags
    tags = extract_tags_from_html(html)

    # Update article data
    article_data["categories"] = categories
    article_data["tags"] = tags

    # Generate category URLs
    article_data["category_urls"] = [generate_category_url(base_url, category) for category in categories]

    return article_data
