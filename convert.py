import os
import re
from datetime import datetime

def convert_latex_to_html(latex_file):
    """Convert a LaTeX file to HTML format with blog styling."""
    with open(latex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove LaTeX document class and packages
    content = re.sub(r'\\documentclass\{.*?\}', '', content)
    content = re.sub(r'\\usepackage\{.*?\}', '', content)
    content = re.sub(r'\\geometry\{.*?\}', '', content)
    content = re.sub(r'\\definecolor\{.*?\}', '', content)
    content = re.sub(r'\\lstset\{.*?\}', '', content)
    content = re.sub(r'\\title\{.*?\}', '', content)
    content = re.sub(r'\\author\{.*?\}', '', content)
    content = re.sub(r'\\date\{.*?\}', '', content)
    content = re.sub(r'\\begin\{document\}', '', content)
    content = re.sub(r'\\end\{document\}', '', content)
    content = re.sub(r'\\maketitle', '', content)
    
    # Convert LaTeX commands to HTML with blog-specific classes
    html_content = content
    
    # Convert section* to h2
    html_content = re.sub(r'\\section\*\{(.*?)\}', r'<h2 class="post-section">\1</h2>', html_content)
    html_content = re.sub(r'\\subsection\*\{(.*?)\}', r'<h3 class="post-subsection">\1</h3>', html_content)
    
    # Convert texttt to code
    html_content = re.sub(r'\\texttt\{(.*?)\}', r'<code class="post-code-inline">\1</code>', html_content)
    
    # Convert textbf to strong
    html_content = re.sub(r'\\textbf\{(.*?)\}', r'<strong class="post-bold">\1</strong>', html_content)
    
    # Convert itemize with blog styling
    html_content = re.sub(r'\\begin\{itemize\}', r'<ul class="post-list">', html_content)
    html_content = re.sub(r'\\end\{itemize\}', r'</ul>', html_content)
    html_content = re.sub(r'\\item\s*(.*?)(?=\\item|\\end\{itemize\})', r'<li class="post-list-item">\1</li>', html_content, flags=re.DOTALL)
    
    # Convert lstlisting to pre and code
    def process_listing(match):
        language = re.search(r'\[language=(.*?)\]', match.group(0))
        lang_class = f'language-{language.group(1).lower()}' if language else ''
        code = re.search(r'\\begin\{lstlisting\}.*?\n(.*?)\\end\{lstlisting\}', match.group(0), re.DOTALL)
        if code:
            return f'<pre class="post-code-block {lang_class}"><code>{code.group(1).strip()}</code></pre>'
        return match.group(0)
    
    html_content = re.sub(r'\\begin\{lstlisting\}.*?\\end\{lstlisting\}', process_listing, html_content, flags=re.DOTALL)
    
    # Convert math to HTML (basic support)
    html_content = re.sub(r'\$(.*?)\$', r'<span class="post-math">\1</span>', html_content)
    
    # Add paragraph styling
    html_content = re.sub(r'\n\n', r'</p>\n<p class="post-paragraph">', html_content)
    html_content = '<p class="post-paragraph">' + html_content + '</p>'
    
    # Clean up multiple newlines
    html_content = re.sub(r'\n{3,}', '\n\n', html_content)
    
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
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/default.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
        <script>hljs.highlightAll();</script>
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