import re

with open("KV_Ultimate_Guide.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find the slice between phase 30 start and the charts-ref div
# (This is exactly the range where bare <pre><code ...> tags live)
start_marker = '<!-- ═══ DS PHASE 30'
end_marker   = '<!-- end Phase 53 -->'

idx_start = content.find(start_marker)
idx_end   = content.find(end_marker) + len(end_marker)

if idx_start == -1 or idx_end == -1:
    print("Markers not found!")
    exit(1)

segment  = content[idx_start:idx_end]
before   = content[:idx_start]
after    = content[idx_end:]

print(f"Segment length: {len(segment):,} chars")

# Count bare <pre><code> occurrences in this segment
count_before = len(re.findall(r'<pre><code class="language-\w+">', segment))
print(f"Bare <pre><code> tags to wrap: {count_before}")

# Wrap:  <pre><code class="language-XXX">  →  <div class="code-block"><pre>
# And:   </code></pre>  →  </pre></div>
segment = re.sub(
    r'<pre><code class="language-\w+">',
    '<div class="code-block"><pre>',
    segment
)
segment = segment.replace("</code></pre>", "</pre></div>")

count_after = len(re.findall(r'<pre><code class="language-\w+">', segment))
new_cb = len(re.findall(r'<div class="code-block"><pre>', segment))
print(f"Bare <pre><code> remaining: {count_after}")
print(f"<div class='code-block'><pre> in segment: {new_cb}")

content = before + segment + after

with open("KV_Ultimate_Guide.html", "w", encoding="utf-8") as f:
    f.write(content)

kb = len(content) / 1024
print(f"Done — {kb:.0f} KB")
