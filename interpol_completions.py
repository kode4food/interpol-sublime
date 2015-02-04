import sublime, sublime_plugin

class InterpolCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if not view.match_selector(locations[0], "source.interpol"):
            return []

        pt = locations[0] - len(prefix) - 1
        ch = view.substr(sublime.Region(pt, pt + 1))
        if ch != '<':
            return []

        return ([
            ("a\tTag", "a href=\"$1\">$2</a>"),
            ("iframe\tTag", "iframe src=\"$1\"></iframe>"),
            ("link\tTag", "link rel=\"stylesheet\" type=\"text/css\" href=\"$1\">"),
            ("script\tTag", "script type=\"${1:text/javascript}\">$0</script>"),
            ("style\tTag", "style type=\"${1:text/css}\">$0</style>"),

            ("img\tTag", "img src=\"$1\">"),
            ("param\tTag", "param name=\"$1\" value=\"$2\">"),

            (prefix + "\tTag", prefix + ">$1</" + prefix + ">")
        ], sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)
