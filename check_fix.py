import re

with open("KV_Ultimate_Guide.html", "r", encoding="utf-8") as f:
    c = f.read()

# Fix stray <code"> patterns (code blocks with extra quote)
stray = len(re.findall(r'<code">', c))
print(f"Stray <code\"> tags: {stray}")

if stray:
    # These come from my scripts that had <code"> typos
    # Fix: <div class="code-block"><code"> -> <div class="code-block"><pre>
    c = re.sub(r'(<div class="code-block[^"]*">)<code">', r'\1<pre>', c)
    # Also fix bare <code"> -> <pre>
    c = c.replace('<code">', '<pre>')
    stray_after = len(re.findall(r'<code">', c))
    print(f"Stray <code\"> after fix: {stray_after}")

# Check remaining bare pre+code
bare = len(re.findall(r'<pre><code class=', c))
print(f"Remaining bare pre+code: {bare}")

# Final counts
cb_pre = len(re.findall(r'class="code-block[^"]*"><pre>', c))
print(f"Total code-block+pre: {cb_pre}")

with open("KV_Ultimate_Guide.html", "w", encoding="utf-8") as f:
    f.write(c)

kb = len(c) / 1024
print(f"Done — {kb:.0f} KB")
