# coding: utf-8
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang=None):
        inlinestyles = self.options.get('inlinestyles')
        linenos = self.options.get('linenos')

        if not lang:
            text = code.strip()
            return u'<pre><code>%s</code></pre>\n' % mistune.escape(text)

        try:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = HtmlFormatter(
                noclasses=inlinestyles, linenos=linenos
            )
            code = highlight(code, lexer, formatter)
            if linenos:
                return '<div class="highlight-wrapper">%s</div>\n' % code
            return code
        except:
            return '<pre class="%s"><code>%s</code></pre>\n' % (
                lang, mistune.escape(code)
            )