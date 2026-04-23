import re

with open("KV_Ultimate_Guide.html", "r", encoding="utf-8") as f:
    c = f.read()

# Find all remaining bare <pre><code class= occurrences and their line numbers
lines = c.split('\n')
for i, line in enumerate(lines, 1):
    if '<pre><code class=' in line:
        print(f"Line {i}: {line.strip()[:100]}")

# Fix them all (these are in p1-p29 range, same fix applies)
count = len(re.findall(r'<pre><code class=', c))
print(f"\nTotal remaining: {count}")

c = re.sub(r'<pre><code class="language-\w+">', '<div class="code-block"><pre>', c)
c = c.replace("</code></pre>", "</pre></div>")

remaining = len(re.findall(r'<pre><code class=', c))
print(f"After fix: {remaining}")

with open("KV_Ultimate_Guide.html", "w", encoding="utf-8") as f:
    f.write(c)

kb = len(c) / 1024
print(f"Done — {kb:.0f} KB")
