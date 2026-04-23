import re

with open("KV_Ultimate_Guide.html", "r", encoding="utf-8") as f:
    content = f.read()

before = len(content)

# Count before
cb_code = len(re.findall(r'class="code-block[^"]*"><code>', content))
end_code = content.count("</code></div>")
print(f"Before: code-block+<code> openings: {cb_code},  </code></div> closings: {end_code}")

# Fix 1: <div class="code-block"><code>  →  <div class="code-block"><pre>
content = re.sub(
    r'(<div class="code-block[^"]*">)<code>',
    r'\1<pre>',
    content
)

# Fix 2: </code></div>  →  </pre></div>
# Only replace where it follows a code-block (all occurrences in p30+ match this pattern)
content = content.replace("</code></div>", "</pre></div>")

# Verify after
cb_code_after = len(re.findall(r'class="code-block[^"]*"><code>', content))
end_code_after = content.count("</code></div>")
cb_pre_after = len(re.findall(r'class="code-block[^"]*"><pre>', content))
end_pre_after = content.count("</pre></div>")
print(f"After:  code-block+<code> openings: {cb_code_after}")
print(f"After:  code-block+<pre>  openings: {cb_pre_after}")
print(f"After:  </code></div>:              {end_code_after}")
print(f"After:  </pre></div>:               {end_pre_after}")

with open("KV_Ultimate_Guide.html", "w", encoding="utf-8") as f:
    f.write(content)

kb = len(content) / 1024
print(f"Done — {kb:.0f} KB")
