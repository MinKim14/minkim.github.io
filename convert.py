import os
import re
from datetime import datetime

def convert_latex_to_html(latex_file):
    """Convert a LaTeX file to HTML format with blog styling."""
    with open(latex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Basic LaTeX to HTML conversions with blog styling
    html_content = content
    
    # Convert LaTeX commands to HTML with blog-specific classes
    html_content = re.sub(r'\\section\{(.*?)\}', r'<h2 class="post-section">\1</h2>', html_content)
    html_content = re.sub(r'\\subsection\{(.*?)\}', r'<h3 class="post-subsection">\1</h3>', html_content)
    html_content = re.sub(r'\\textbf\{(.*?)\}', r'<strong class="post-bold">\1</strong>', html_content)
    html_content = re.sub(r'\\textit\{(.*?)\}', r'<em class="post-italic">\1</em>', html_content)
    
    # Convert itemize with blog styling
    html_content = re.sub(r'\\begin\{itemize\}', r'<ul class="post-list">', html_content)
    html_content = re.sub(r'\\end\{itemize\}', r'</ul>', html_content)
    html_content = re.sub(r'\\item\s*(.*?)(?=\\item|\\end\{itemize\})', r'<li class="post-list-item">\1</li>', html_content, flags=re.DOTALL)
    
    # Convert enumerate with blog styling
    html_content = re.sub(r'\\begin\{enumerate\}', r'<ol class="post-ordered-list">', html_content)
    html_content = re.sub(r'\\end\{enumerate\}', r'</ol>', html_content)
    html_content = re.sub(r'\\item\s*(.*?)(?=\\item|\\end\{enumerate\})', r'<li class="post-ordered-item">\1</li>', html_content, flags=re.DOTALL)
    
    # Convert math with blog styling
    html_content = re.sub(r'\$(.*?)\$', r'<span class="post-math">\1</span>', html_content)
    
    # Add paragraph styling
    html_content = re.sub(r'\n\n', r'</p>\n<p class="post-paragraph">', html_content)
    html_content = '<p class="post-paragraph">' + html_content + '</p>'
    
    return html_content

def create_blog_post(html_content, title, category, date=None):
    """Create a blog post HTML file with blog styling."""
    if date is None:
        date = datetime.now().strftime("%B %d, %Y")
    
    post_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} - Code Blog</title>
        <link rel="stylesheet" href="../styles.css">
    </head>
    <body>
        <header>
            <nav>
                <div class="logo">Code Blog</div>
                <ul>
                    <li><a href="../index.html">Home</a></li>
                    <li><a href="../web-development.html">Web Development</a></li>
                    <li><a href="../algorithms.html">Algorithms</a></li>
                    <li><a href="../projects.html">Projects</a></li>
                    <li><a href="../about.html">About</a></li>
                </ul>
            </nav>
        </header>

        <main>
            <div class="color-bar top"></div>
            <article class="blog-post">
                <div class="post-header">
                    <h2 class="post-title">{title}</h2>
                    <div class="post-meta">
                        <span class="post-date">{date}</span>
                        <span class="post-category">{category}</span>
                    </div>
                </div>
                <div class="post-content">
                    {html_content}
                </div>
                <div class="post-navigation">
                    <a href="../{category.lower()}.html" class="back-button">← Back to {category.title()}</a>
                    <a href="../index.html" class="home-button">Home</a>
                </div>
            </article>
            <div class="color-bar bottom"></div>
        </main>

        <footer>
            <p>&copy; 2024 Code Blog. All rights reserved.</p>
        </footer>
    </body>
    </html>
    """
    
    return post_template

def process_latex_directory():
    """Process all LaTeX files in the latex directory."""
    latex_dir = os.path.join(os.path.dirname(__file__), 'latex')
    posts_dir = os.path.join(os.path.dirname(__file__), 'posts')
    
    # Create posts directory if it doesn't exist
    if not os.path.exists(posts_dir):
        os.makedirs(posts_dir)
    
    # Process each LaTeX file
    for filename in os.listdir(latex_dir):
        if filename.endswith('.tex'):
            latex_file = os.path.join(latex_dir, filename)
            html_content = convert_latex_to_html(latex_file)
            
            # Extract metadata from filename (format: YYYY-MM-DD-title-category.tex)
            parts = filename[:-4].split('-')
            if len(parts) >= 4:
                date = datetime.strptime('-'.join(parts[:3]), '%Y-%m-%d').strftime("%B %d, %Y")
                title = ' '.join(parts[3:-1])
                category = parts[-1]
            else:
                date = datetime.now().strftime("%B %d, %Y")
                title = filename[:-4]
                category = "Uncategorized"
            
            # Create blog post
            post_html = create_blog_post(html_content, title, category, date)
            
            # Save the post
            post_filename = f"{filename[:-4]}.html"
            with open(os.path.join(posts_dir, post_filename), 'w', encoding='utf-8') as f:
                f.write(post_html)
            
            print(f"Processed {filename} -> {post_filename}")

if __name__ == "__main__":
    process_latex_directory() 