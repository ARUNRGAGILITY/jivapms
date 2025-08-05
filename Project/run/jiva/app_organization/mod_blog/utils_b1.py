# utils.py - Fixed version that handles the actual content structure

import re
import markdown as md_module
from django.utils.safestring import mark_safe

def process_markdown_with_mermaid(content):
    """
    Process markdown content and handle mermaid blocks properly
    """
    if not content:
        return ""
    
    print(f"DEBUG: Original content length: {len(content)}")
    print(f"DEBUG: Original content preview: {content[:200]}...")
    
    # APPROACH: Process markdown first, then find and replace mermaid in the HTML
    
    # Step 1: Process the content with markdown first (as it currently is)
    md_processor = md_module.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.fenced_code',
        'markdown.extensions.toc',
        'markdown.extensions.tables',
        'markdown.extensions.nl2br',  # Keep this since your current setup uses it
    ])
    html_content = md_processor.convert(content)
    
    print(f"DEBUG: After markdown processing: {html_content[:500]}...")
    
    # Step 2: Find paragraphs that contain mermaid content and replace them
    def replace_mermaid_paragraphs(html):
        # Pattern to find <p> tags containing mermaid content
        def replace_mermaid_p(match):
            p_content = match.group(1)
            
            # Check if this paragraph contains mermaid content
            if '```mermaid' in p_content or 'mermaid' in p_content:
                print(f"DEBUG: Found mermaid paragraph: {p_content[:100]}...")
                
                # Clean the content
                cleaned_content = clean_mermaid_from_html(p_content)
                
                if cleaned_content:
                    print(f"DEBUG: Cleaned mermaid content: {cleaned_content[:100]}...")
                    return f'<div class="mermaid">{cleaned_content}</div>'
            
            # Return original paragraph if no mermaid content
            return match.group(0)
        
        # Replace <p> tags that might contain mermaid
        html = re.sub(r'<p>(.*?)</p>', replace_mermaid_p, html, flags=re.DOTALL)
        return html
    
    # Step 3: Apply the mermaid replacement
    processed_html = replace_mermaid_paragraphs(html_content)
    
    print(f"DEBUG: Final HTML length: {len(processed_html)}")
    print(f"DEBUG: Final HTML preview: {processed_html[:500]}...")
    
    return mark_safe(processed_html)

def clean_mermaid_from_html(html_content):
    """
    Extract and clean mermaid content from HTML paragraph content
    """
    # Remove HTML tags
    content = re.sub(r'<[^>]+>', '', html_content)
    
    # Replace HTML entities
    content = content.replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&')
    content = content.replace('&nbsp;', ' ').replace('<br />', '\n').replace('<br>', '\n')
    content = content.replace('–', '-').replace('—', '-')
    
    # Remove ```mermaid markers if present
    content = content.replace('```mermaid', '').replace('```', '')
    
    print(f"DEBUG: Cleaning content: {repr(content[:200])}")
    
    # Check if this actually contains mermaid keywords
    mermaid_keywords = ['graph TD', 'graph LR', 'pie title', 'xychart', 'erDiagram', 
                       'gitgraph', 'mindmap', 'quadrantChart', 'timeline', 
                       'sequenceDiagram', 'classDiagram', 'stateDiagram']
    
    has_mermaid = any(keyword in content for keyword in mermaid_keywords)
    
    if not has_mermaid:
        print("DEBUG: No mermaid keywords found")
        return None
    
    # Split into lines and clean
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        # Filter out obviously non-mermaid lines
        if (line and 
            not line.startswith('http') and 
            not line.startswith('localhost') and
            not 'area_id' in line and
            len(line) < 200):
            cleaned_lines.append(line)
    
    if not cleaned_lines:
        return None
    
    content = '\n'.join(cleaned_lines)
    
    # Apply specific fixes based on diagram type
    if 'pie title' in content:
        content = fix_pie_chart(content)
    elif 'xychart' in content:
        content = fix_xychart(content)
    elif 'erDiagram' in content:
        content = fix_er_diagram(content)
    elif 'gitgraph' in content:
        content = fix_gitgraph(content)
    elif 'mindmap' in content:
        content = fix_mindmap(content)
    elif 'graph TD' in content or 'graph LR' in content:
        content = fix_flowchart(content)
    elif 'quadrantChart' in content:
        content = fix_quadrant_chart(content)
    elif 'timeline' in content:
        content = fix_timeline(content)
    
    return content.strip()

def fix_pie_chart(content):
    """Fix pie chart formatting"""
    lines = content.split('\n')
    result = []
    
    title_found = False
    for line in lines:
        line = line.strip()
        if 'pie title' in line:
            # Extract title
            title_match = re.search(r'pie title\s+(.+)', line)
            if title_match:
                title = title_match.group(1).strip()
                # Remove any surrounding quotes and re-add them properly
                title = title.strip('\'"')
                result.append(f'pie title "{title}"')
                title_found = True
        elif title_found and ':' in line and any(char.isdigit() for char in line):
            # This looks like data
            # Try to extract label and value
            if '"' in line and ':' in line:
                # Already properly formatted
                result.append(f'    {line}')
            else:
                # Try to parse unformatted data
                parts = line.split(':')
                if len(parts) == 2:
                    label = parts[0].strip().strip('"\'')
                    value = parts[1].strip()
                    if value.isdigit():
                        result.append(f'    "{label}" : {value}')
    
    return '\n'.join(result) if result else content

def fix_xychart(content):
    """Fix xychart formatting"""
    lines = content.split('\n')
    result = []
    
    for line in lines:
        line = line.strip()
        if 'xychart' in line:
            result.append('xychart-beta')
        elif line.startswith('title'):
            # Ensure title is properly formatted
            title_match = re.search(r'title\s+"?([^"]+)"?', line)
            if title_match:
                result.append(f'    title "{title_match.group(1)}"')
            else:
                result.append(f'    {line}')
        elif line.startswith('x-axis') or line.startswith('y-axis') or line.startswith('line'):
            result.append(f'    {line}')
        elif line and not line.startswith(' '):
            result.append(f'    {line}')
        elif line:
            result.append(line)
    
    return '\n'.join(result)

def fix_er_diagram(content):
    """Fix ER diagram formatting"""
    lines = content.split('\n')
    result = ['erDiagram']
    
    for line in lines:
        line = line.strip()
        if 'erDiagram' in line:
            continue
        elif '||--o{' in line or '||--' in line or 'FK' in line or 'PK' in line:
            result.append(f'    {line}')
        elif line:
            result.append(f'    {line}')
    
    return '\n'.join(result)

def fix_gitgraph(content):
    """Fix gitgraph formatting"""
    lines = content.split('\n')
    result = ['gitgraph']
    
    for line in lines:
        line = line.strip()
        if 'gitgraph' in line:
            continue
        elif line:
            result.append(f'    {line}')
    
    return '\n'.join(result)

def fix_mindmap(content):
    """Fix mindmap formatting"""
    lines = content.split('\n')
    result = []
    
    for line in lines:
        line = line.strip()
        if 'mindmap' in line:
            result.append('mindmap')
        elif 'root(' in line:
            result.append(f'  {line}')
        elif line:
            # Simple heuristic for indentation
            if len(line.split()) == 1:
                result.append(f'    {line}')
            else:
                result.append(f'      {line}')
    
    return '\n'.join(result)

def fix_flowchart(content):
    """Fix basic flowchart formatting"""
    content = re.sub(r'(graph\s+(TD|LR))\s*([A-Z])', r'\1\n\3', content)
    content = content.replace('->', '-->')
    return content

def fix_quadrant_chart(content):
    """Fix quadrant chart formatting"""
    lines = content.split('\n')
    result = []
    
    for line in lines:
        line = line.strip()
        if 'quadrantChart' in line:
            result.append('quadrantChart')
        elif line.startswith(('title', 'x-axis', 'y-axis', 'quadrant-')):
            result.append(f'    {line}')
        elif line:
            result.append(f'    {line}')
    
    return '\n'.join(result)

def fix_timeline(content):
    """Fix timeline formatting"""
    lines = content.split('\n')
    result = []
    
    for line in lines:
        line = line.strip()
        if 'timeline' in line:
            result.append('timeline')
        elif line.startswith('title'):
            result.append(f'    {line}')
        elif line.startswith('section'):
            result.append(f'    {line}')
        elif ':' in line:
            result.append(f'        {line}')
        elif line:
            result.append(f'    {line}')
    
    return '\n'.join(result)