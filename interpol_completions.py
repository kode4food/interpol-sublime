import sublime, sublime_plugin


interpol_simple_tags = [
    "abbr", "address", "area", "article", "aside", "audio", "base", "bdi", 
    "bdo", "blockquote", "body", "br", "button", "canvas", "caption", "cite", 
    "code", "col", "colgroup", "datalist", "dd", "del", "details", "dfn", 
    "dialog", "div", "dl", "dt", "em", "embed", "fieldset", "figcaption", 
    "figure", "font", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", 
    "hgroup", "hr", "html", "input", "ins", "kbd", "keygen", "label", "legend", 
    "li", "main", "map", "mark", "menu", "menuitem", "meta", "meter", "nav", 
    "noscript", "object", "ol", "optgroup", "option", "output", "pre", 
    "progress", "rp", "rt", "ruby", "samp", "section", "select", "small", 
    "source", "span", "strong", "sub", "summary", "sup", "table", "tbody", 
    "td", "textarea", "tfoot", "th", "thead", "time", "title", "tr", "track", 
    "ul", "var", "video", "wbr"
]

interpol_completion_items = [
    ("a", "a href=\"$1\">$2</a>"),
    ("iframe", "iframe src=\"$1\"></iframe>"),
    ("img", "img src=\"$1\">"),
    ("link", "link rel=\"stylesheet\" type=\"text/css\" href=\"$1\">"),
    ("param", "param name=\"$1\" value=\"$2\">"),
    ("script", "script type=\"${1:text/javascript}\">$0</script>"),
    ("style", "style type=\"${1:text/css}\">$0</style>")
]

interpol_completion_items += [(item, item + ">$1<" + item + ">") for item in interpol_simple_tags]
interpol_completion_items = sorted(interpol_completion_items, key=lambda item: item[0])

interpol_completion_tags = set([item[0] for item in interpol_completion_items])
interpol_completion_list = [(item[0] + "\tTag", item[1]) for item in interpol_completion_items]

class InterpolCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if not view.match_selector(locations[0], "source.interpol"):
            return None

        pt = locations[0] - len(prefix) - 1
        ch = view.substr(sublime.Region(pt, pt + 1))
        if ch != '<':
            return None

        result = list(interpol_completion_list)
        if prefix not in interpol_completion_tags:
            result.append(            
                (prefix + "\tTag", prefix + ">$1</" + prefix + ">")
            )

        return (
            result, 
            sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS
        )
