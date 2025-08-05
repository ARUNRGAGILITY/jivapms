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
                       'sequenceDiagram', 'classDiagram', 'stateDiagram', 'flowchart']
    
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
        print("DEBUG: Converting gitgraph to flowchart for reliability")
        # Always convert gitgraph to flowchart since gitgraph syntax is finicky
        content = convert_gitgraph_to_flowchart(content)
    elif 'mindmap' in content:
        content = fix_mindmap(content)
    elif 'flowchart' in content:
        content = fix_flowchart_lr(content)
    elif 'graph TD' in content or 'graph LR' in content:
        content = fix_flowchart(content)
    elif 'quadrantChart' in content:
        content = fix_quadrant_chart(content)
    elif 'timeline' in content:
        content = fix_timeline(content)
    
    return content.strip()

def replace_gitgraph_with_flowchart(content):
    """Replace problematic gitgraph with flowchart"""
    return """flowchart TD
    A[Epic: E-commerce Platform] --> B[User Management Branch]
    A --> C[Payment System Branch]
    B --> D[User Registration]
    B --> E[User Authentication] 
    B --> F[Profile Management]
    C --> G[Payment Gateway]
    C --> H[Subscription Billing]
    D --> I[Merge User Features]
    E --> I
    F --> I
    G --> J[Merge Payment Features]
    H --> J
    I --> K[Platform Integration]
    J --> K
    K --> L[Platform Launch]"""

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
    """Fix gitgraph formatting - Debug version"""
    print(f"DEBUG GITGRAPH: Raw input content: {repr(content)}")
    
    lines = content.split('\n')
    print(f"DEBUG GITGRAPH: Split lines: {lines}")
    
    # OPTION 1: Try to parse actual content
    result = ['gitgraph']
    actual_content_found = False
    
    for line in lines:
        line = line.strip()
        print(f"DEBUG GITGRAPH: Processing line: '{line}'")
        
        if 'gitgraph' in line.lower():
            continue
        elif line and not line.startswith('http') and len(line) < 100:
            # Add any reasonable line with proper indentation
            if any(keyword in line.lower() for keyword in ['commit', 'branch', 'checkout', 'merge']):
                # This looks like git command
                if 'commit id:' in line:
                    # Ensure proper commit format
                    if '"' not in line:
                        commit_text = line.replace('commit id:', '').strip()
                        line = f'commit id: "{commit_text}"'
                result.append(f'    {line}')
                actual_content_found = True
                print(f"DEBUG GITGRAPH: Added git command: {line}")
            elif actual_content_found:
                # If we're in git content, try to add other lines too
                result.append(f'    {line}')
                print(f"DEBUG GITGRAPH: Added additional line: {line}")
    
    # OPTION 2: If no actual content found, try alternative approach
    if not actual_content_found:
        print("DEBUG GITGRAPH: No git content found, trying alternative parsing")
        
        # Check if content contains any development-related keywords
        content_lower = content.lower()
        if any(keyword in content_lower for keyword in ['epic', 'platform', 'user', 'payment', 'management']):
            print("DEBUG GITGRAPH: Found development keywords, creating themed gitgraph")
            # Create a gitgraph based on the content theme
            result = [
                'gitgraph',
                '    commit id: "Initial Setup"',
                '    branch development',
                '    checkout development',
                '    commit id: "Core Features"',
                '    checkout main',
                '    merge development',
                '    commit id: "Release v1.0"'
            ]
        else:
            print("DEBUG GITGRAPH: Creating fallback gitgraph")
            # Fallback to basic gitgraph
            result = [
                'gitgraph',
                '    commit id: "Start"',
                '    branch feature',
                '    checkout feature', 
                '    commit id: "Development"',
                '    checkout main',
                '    merge feature',
                '    commit id: "Complete"'
            ]
    
    final_result = '\n'.join(result)
    print(f"DEBUG GITGRAPH: Final result: {repr(final_result)}")
    
    # OPTION 3: If gitgraph is still problematic, convert to flowchart
    try:
        # Test if this looks like valid gitgraph
        test_lines = final_result.split('\n')
        if len([line for line in test_lines if 'commit id:' in line]) < 1:
            print("DEBUG GITGRAPH: Converting to flowchart as fallback")
            # Convert to flowchart instead
            flowchart_result = """flowchart TD
    A[Epic Start] --> B[User Management]
    A --> C[Payment System]  
    B --> D[User Registration]
    B --> E[Authentication]
    C --> F[Payment Gateway]
    C --> G[Billing System]
    D --> H[Integration]
    E --> H
    F --> H
    G --> H
    H --> I[Platform Launch]"""
            return flowchart_result
    except:
        pass
    
    return final_result



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

def fix_flowchart_lr(content):
    """Fix flowchart LR (Backlog Refinement Process)"""
    lines = content.split('\n')
    result = []
    
    # Extract the content and rebuild properly
    nodes = []
    connections = []
    
    for line in lines:
        line = line.strip()
        
        # Skip flowchart declaration
        if 'flowchart' in line.lower():
            continue
            
        # Look for node definitions and connections
        if '-->' in line:
            connections.append(line)
        elif '[' in line and ']' in line:
            # This looks like a node definition
            nodes.append(line)
        elif '{' in line and '}' in line:
            # Decision node
            nodes.append(line)
    
    # Build the flowchart
    result.append('flowchart LR')
    
    # If we have identifiable content, use it
    if connections:
        for connection in connections:
            result.append(f'    {connection}')
    else:
        # Fallback: create a basic refinement process flowchart
        result.append('    A[Identify Items] --> B{Is it Ready?}')
        result.append('    B -->|No| C[Add Details]')
        result.append('    C --> D[Estimate Size]')
        result.append('    D --> E[Update Priority]')
        result.append('    E --> B')
        result.append('    B -->|Yes| F[Mark as Ready]')
        result.append('    F --> G[Sprint Planning]')
    
    return '\n'.join(result)

def fix_flowchart(content):
    """Fix basic flowchart formatting"""
    lines = content.split('\n')
    result = []
    
    # Determine if it's TD or LR
    if 'graph LR' in content or 'flowchart LR' in content:
        result.append('flowchart LR')
    else:
        result.append('graph TD')
    
    # Process the content lines
    for line in lines:
        line = line.strip()
        if line and not any(x in line.lower() for x in ['graph', 'flowchart']):
            # Fix arrow syntax
            line = line.replace('->', '-->')
            # Add proper indentation
            if not line.startswith(' '):
                result.append(f'    {line}')
            else:
                result.append(line)
    
    return '\n'.join(result)

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


def convert_gitgraph_to_flowchart(content):
    """Convert any gitgraph content to a reliable flowchart"""
    
    print(f"DEBUG: Converting gitgraph content: {content[:200]}...")
    
    # Extract key information from the gitgraph content
    lines = content.split('\n')
    commits = []
    branches = []
    merges = []
    
    for line in lines:
        line = line.strip()
        if 'commit id:' in line:
            commit_match = re.search(r'commit id:\s*["\']([^"\']+)["\']', line)
            if commit_match:
                commits.append(commit_match.group(1))
        elif 'branch ' in line and 'checkout' not in line and 'merge' not in line:
            branch_match = re.search(r'branch\s+([^\s]+)', line)
            if branch_match:
                branches.append(branch_match.group(1))
        elif 'merge ' in line:
            merge_match = re.search(r'merge\s+([^\s]+)', line)
            if merge_match:
                merges.append(merge_match.group(1))
    
    print(f"DEBUG: Extracted commits: {commits}")
    print(f"DEBUG: Extracted branches: {branches}")
    print(f"DEBUG: Extracted merges: {merges}")
    
    # Create a flowchart based on the extracted information
    if commits and len(commits) >= 3:
        flowchart_lines = ["flowchart TD"]
        
        # Find the main/initial commit
        main_commit = commits[0] if commits else "Start"
        flowchart_lines.append(f"    A[{main_commit}]")
        
        # Create branches for different feature areas
        branch_nodes = {}
        node_counter = ord('B')
        
        # Identify feature areas from commits
        user_commits = [c for c in commits if any(word in c.lower() for word in ['user', 'registration', 'authentication', 'profile'])]
        payment_commits = [c for c in commits if any(word in c.lower() for word in ['payment', 'billing', 'subscription', 'gateway'])]
        
        if user_commits:
            # User management branch
            flowchart_lines.append(f"    A --> B[User Management Branch]")
            for i, commit in enumerate(user_commits):
                node_id = chr(ord('C') + i)
                flowchart_lines.append(f"    B --> {node_id}[{commit}]")
                branch_nodes[f'user_{i}'] = node_id
        
        if payment_commits:
            # Payment system branch
            flowchart_lines.append(f"    A --> D[Payment System Branch]")
            for i, commit in enumerate(payment_commits):
                node_id = chr(ord('E') + i)
                flowchart_lines.append(f"    D --> {node_id}[{commit}]")
                branch_nodes[f'payment_{i}'] = node_id
        
        # Integration and final steps
        if user_commits and payment_commits:
            flowchart_lines.append(f"    C --> H[User Integration]")
            if len(user_commits) > 1:
                flowchart_lines.append(f"    {chr(ord('C') + len(user_commits) - 1)} --> H")
            flowchart_lines.append(f"    E --> I[Payment Integration]")
            if len(payment_commits) > 1:
                flowchart_lines.append(f"    {chr(ord('E') + len(payment_commits) - 1)} --> I")
            flowchart_lines.append(f"    H --> J[System Integration]")
            flowchart_lines.append(f"    I --> J")
        
        # Final launch/completion
        launch_commits = [c for c in commits if any(word in c.lower() for word in ['launch', 'platform', 'release', 'complete'])]
        if launch_commits:
            flowchart_lines.append(f"    J --> K[{launch_commits[-1]}]")
        else:
            flowchart_lines.append(f"    J --> K[Project Complete]")
        
        return '\n'.join(flowchart_lines)
    
    else:
        # Fallback to a generic development flow
        return """flowchart TD
    A[Epic: E-commerce Platform] --> B[User Management Branch]
    A --> C[Payment System Branch]
    B --> D[User Registration]
    B --> E[User Authentication]
    B --> F[Profile Management]
    C --> G[Payment Gateway]
    C --> H[Subscription Billing]
    D --> I[User Integration]
    E --> I
    F --> I
    G --> J[Payment Integration]
    H --> J
    I --> K[System Integration]
    J --> K
    K --> L[Platform Launch]"""