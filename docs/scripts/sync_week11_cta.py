# -*- coding: utf-8 -*-
from pathlib import Path
import re

docs = Path(__file__).resolve().parents[1]
idx = (docs / "index.html").read_text(encoding="utf-8")

css_m = re.search(
    r"  \.wk-visual > \* \{ flex: 1; min-height: 200px; \}\n  \.wk-visual\.has-cta \{.*?\n  \}\n",
    idx,
    re.S,
)
block_m = re.search(
    r"    <!-- 11 → separate page security.html -->.*?    <!-- 12 shop page style",
    idx,
    re.S,
)
if not css_m or not block_m:
    raise SystemExit("markers not found in index.html")

css = css_m.group(0)
block = block_m.group(0)

targets = [
    "test-dynamic.html",
    "kp/demo/test-dynamic.html",
    "kp/_template/test-dynamic.html",
]
for rel in targets:
    p = docs / rel
    if not p.exists():
        print("skip", rel)
        continue
    t = p.read_text(encoding="utf-8")
    if ".wk-visual.has-cta" not in t:
        t = t.replace(
            "  .wk-visual > * { flex: 1; min-height: 200px; }\n",
            css,
            1,
        )
    if "<!-- 11 → separate page security.html -->" in t:
        t = re.sub(
            r"    <!-- 11 → separate page security.html -->.*?    <!-- 12 shop page style",
            block,
            t,
            count=1,
            flags=re.S,
        )
    p.write_text(t, encoding="utf-8")
    print("ok", rel)

# test-dynamic should match index for this product page
(docs / "test-dynamic.html").write_text(idx, encoding="utf-8")
print("ok test-dynamic.html = index")
