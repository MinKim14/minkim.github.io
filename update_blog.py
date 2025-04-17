import os
import glob
from datetime import datetime
import re

def get_post_metadata(post_file):
    """Extract metadata from post filename."""
    filename = os.path.basename(post_file)
    parts = filename[:-5].split('-')  # Remove .html and split
    if len(parts) >= 4:
        date = datetime.strptime('-'.join(parts[:3]), '%Y-%m-%d')
        title = ' '.join(parts[3:-1])
        category = parts[-1]
        return {
            'date': date,
            'title': title,
            'category': category,
            'filename': filename
        }
    return None

def update_section_page(category, posts):
    """Update a section page with new posts."""
    template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{category.title()} - Code Blog</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <nav>
            <div class="logo">Code Blog</div>
            <ul>
                <li><a href="index.html">Home</a></li>
                <li><a href="web-development.html">Web Development</a></li>
                <li><a href="algorithms.html">Algorithms</a></li>
                <li><a href="projects.html">Projects</a></li>
                <li><a href="about.html">About</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <section class="section-header">
            <h1>{category.title()}</h1>
            <p>Explore our collection of {category.lower()} articles and tutorials</p>
        </section>

        <section class="content-section">
            {posts}
        </section>
    </main>

    <footer>
        <p>&copy; 2024 Code Blog. All rights reserved.</p>
    </footer>
</body>
</html>"""
    
    with open(f"{category.lower()}.html", 'w', encoding='utf-8') as f:
        f.write(template)

def update_index_page(posts):
    """Update the index page with latest posts."""
    latest_posts = sorted(posts, key=lambda x: x['date'], reverse=True)[:3]
    
    posts_html = ""
    for post in latest_posts:
        posts_html += f"""
            <article class="post-card">
                <h3>{post['title']}</h3>
                <p>{post['date'].strftime("%B %d, %Y")} - {post['category']}</p>
                <a href="posts/{post['filename']}" class="read-more">Read More</a>
            </article>
        """
    
    # Read the current index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the post-grid section
    new_content = re.sub(
        r'<div class="post-grid">.*?</div>',
        f'<div class="post-grid">{posts_html}</div>',
        content,
        flags=re.DOTALL
    )
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)

def main():
    # Get all posts
    posts = []
    for post_file in glob.glob('posts/*.html'):
        metadata = get_post_metadata(post_file)
        if metadata:
            posts.append(metadata)
    
    # Group posts by category
    categories = {}
    for post in posts:
        if post['category'] not in categories:
            categories[post['category']] = []
        categories[post['category']].append(post)
    
    # Update section pages
    for category, category_posts in categories.items():
        posts_html = ""
        for post in sorted(category_posts, key=lambda x: x['date'], reverse=True):
            with open(f"posts/{post['filename']}", 'r', encoding='utf-8') as f:
                post_content = f.read()
            posts_html += post_content
        update_section_page(category, posts_html)
    
    # Update index page
    update_index_page(posts)

if __name__ == "__main__":
    main() 