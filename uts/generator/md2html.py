import re, html as _h


def _inl(t):
    t = _h.escape(t).replace("&lt;br&gt;", "<br>")
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)


CSS = ("body{font:15px/1.55 Segoe UI,Arial,sans-serif;max-width:900px;margin:24px auto;padding:0 16px;color:#1b1f24}"
       "h1{border-bottom:3px solid #0b5a7a;padding-bottom:6px}h2{color:#0b5a7a;margin-top:28px}h3{margin-top:20px}"
       "table{border-collapse:collapse;width:100%;margin:10px 0}th,td{border:1px solid #c9d1d9;padding:6px 9px;text-align:left;vertical-align:top}"
       "th{background:#0b5a7a;color:#fff}table.kv td:first-child{background:#eef3f6;font-weight:600;width:22%}"
       "code{background:#eef3f6;padding:1px 5px;border-radius:3px;font-size:.92em}hr{border:0;border-top:1px solid #c9d1d9;margin:24px 0}"
       "@media print{body{max-width:none;margin:0}h2{page-break-after:avoid}table{page-break-inside:avoid}}")


def md2html(md, title):
    o, L, i, lst = [], md.split("\n"), 0, None

    def close():
        nonlocal lst
        if lst:
            o.append(f"</{lst}>"); lst = None
    while i < len(L):
        ln = L[i]
        if ln.startswith("|"):
            close(); rows = []
            while i < len(L) and L[i].startswith("|"):
                rows.append([c.strip() for c in L[i].strip().strip("|").split("|")]); i += 1
            hdr, body = rows[0], rows[2:]
            tr = lambda r, t: "<tr>" + "".join(f"<{t}>{_inl(c)}</{t}>" for c in r) + "</tr>"
            if all(not h for h in hdr):
                o.append("<table class='kv'>" + "".join(tr(r, "td") for r in body) + "</table>")
            else:
                o.append("<table><thead>" + tr(hdr, "th") + "</thead><tbody>" + "".join(tr(r, "td") for r in body) + "</tbody></table>")
            continue
        m = re.match(r"^(#{1,3}) (.*)", ln)
        if m:
            close(); n = len(m.group(1)); o.append(f"<h{n}>{_inl(m.group(2))}</h{n}>")
        elif ln.strip() == "---": close(); o.append("<hr>")
        elif ln.startswith("- "):
            if lst != "ul": close(); o.append("<ul>"); lst = "ul"
            o.append(f"<li>{_inl(ln[2:])}</li>")
        elif re.match(r"^\d+\. ", ln):
            if lst != "ol": close(); o.append("<ol>"); lst = "ol"
            o.append(f"<li>{_inl(re.sub(r'^\d+\. ', '', ln))}</li>")
        elif ln.strip() == "": close()
        else: close(); o.append(f"<p>{_inl(ln)}</p>")
        i += 1
    close()
    return f"<!doctype html><html lang='id'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{_h.escape(title)}</title><style>{CSS}</style></head><body>" + "\n".join(o) + "</body></html>"
