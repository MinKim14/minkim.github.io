import os
import re
from datetime import datetime

def convert_latex_to_html(latex_file):
    """Convert a LaTeX file to HTML format."""
    with open(latex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Basic LaTeX to HTML conversions
    html_content = content
    
    # Convert LaTeX commands to HTML
    html_content = re.sub(r'\\section\{(.*?)\}', r'<h2>\1</h2>', html_content)
    html_content = re.sub(r'\\subsection\{(.*?)\}', r'<h3>\1</h3>', html_content)
    html_content = re.sub(r'\\textbf\{(.*?)\}', r'<strong>\1</strong>', html_content)
    html_content = re.sub(r'\\textit\{(.*?)\}', r'<em>\1</em>', html_content)
    html_content = re.sub(r'\\begin\{itemize\}', r'<ul>', html_content)
    html_content = re.sub(r'\\end\{itemize\}', r'</ul>', html_content)
    html_content = re.sub(r'\\item\s*(.*?)(?=\\item|\\end\{itemize\})', r'<li>\1</li>', html_content, flags=re.DOTALL)
    html_content = re.sub(r'\\begin\{enumerate\}', r'<ol>', html_content)
    html_content = re.sub(r'\\end\{enumerate\}', r'</ol>', html_content)
    
    # Convert LaTeX math to HTML (basic support)
    html_content = re.sub(r'\$(.*?)\$', r'<span class="math">\1</span>', html_content)
    
    return html_content

def create_blog_post(html_content, title, category, date=None):
    """Create a blog post HTML file from the converted content."""
    if date is None:
        date = datetime.now().strftime("%B %d, %Y")
    
    post_template = f"""
    <article class="blog-post">
        <h2>{title}</h2>
        <div class="post-meta">
            <span class="date">{date}</span>
            <span class="category">{category}</span>
        </div>
        <div class="post-content">
            {html_content}
        </div>
    </article>
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