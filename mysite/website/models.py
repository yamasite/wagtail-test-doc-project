"""
Createable pages used in CodeRed CMS.
"""

from coderedcms.blocks import ReusableContentBlock
from modelcluster.fields import ParentalKey
from coderedcms.forms import CoderedFormField
from coderedcms.models import (
    CoderedArticlePage,
    CoderedArticleIndexPage,
    CoderedEmail,
    CoderedFormPage,
    CoderedWebPage, ReusableContent)


from wagtail.core.blocks import StreamBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtailmarkdown.blocks import MarkdownBlock
from wagtail.core.fields import StreamField, RichTextField

from django.utils.translation import gettext_lazy as _
from django.forms.utils import flatatt
from django.utils.html import format_html, format_html_join

from wagtail.snippets.models import register_snippet
from django.db import models
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel)

from wagtailmedia.blocks import AbstractMediaChooserBlock

from wagtailmenus.models import MenuPageMixin
from wagtailmenus.panels import menupage_panel

from django.utils import translation
from django.http import HttpResponseRedirect

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import MultiFieldPanel, PageChooserPanel

class MyStreamBlock(StreamBlock):
    markdown = MarkdownBlock(icon="code")


class ArticlePage(CoderedArticlePage):
    """
    Article, suitable for news or blog content.
    """
    class Meta:
        verbose_name = 'Article'
        ordering = ['-first_published_at']

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ['website.ArticleIndexPage']

    template = 'coderedcms/pages/article_page.html'
    amp_template = 'coderedcms/pages/article_page.amp.html'
    search_template = 'coderedcms/pages/article_page.search.html'


class ArticleIndexPage(CoderedArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """
    class Meta:
        verbose_name = 'Article Landing Page'

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'website.ArticlePage'

    # Only allow ArticlePages beneath this page.
    subpage_types = ['website.ArticlePage', 'website.DocPage', 'website.DocPageWithReuseSupport', 'DocPageWithMediaAndReuseSupport', 'DocPageWithMediaAndReuseSupportAndMenu','DocPageWithMediaAndReuseSupportAndMultilanguage']

    template = 'coderedcms/pages/article_index_page.html'


class FormPage(CoderedFormPage):
    """
    A page with an html <form>.
    """
    class Meta:
        verbose_name = 'Form'

    template = 'coderedcms/pages/form_page.html'


class FormPageField(CoderedFormField):
    """
    A field that links to a FormPage.
    """
    class Meta:
        ordering = ['sort_order']

    page = ParentalKey('FormPage', related_name='form_fields')


class FormConfirmEmail(CoderedEmail):
    """
    Sends a confirmation email after submitting a FormPage.
    """
    page = ParentalKey('FormPage', related_name='confirmation_emails')


class WebPage(CoderedWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    Template renders all Navbar and Footer snippets in existance.
    """
    class Meta:
        verbose_name = 'Web Page'

    template = 'coderedcms/pages/web_page.html'


class AgoraMediaBlock(AbstractMediaChooserBlock):
    def render_basic(self, value, context=None):
        if not value:
            return ''

        if value.type == 'video':
            player_code = '''
            <div>
                <video width="320" height="240" controls>
                    {0}
                    Your browser does not support the video tag.
                </video>
            </div>
            '''
        else:
            player_code = '''
            <div>
                <audio controls>
                    {0}
                    Your browser does not support the audio element.
                </audio>
            </div>
            '''

        return format_html(player_code, format_html_join(
            '\n', "<source{0}>",
            [[flatatt(s)] for s in value.sources]
        ))


class DocPage(CoderedWebPage):
    """
    DocPage implements CoderedWebPage, with markdown editor integrated
    """
    class Meta:
        verbose_name = 'Doc page'

    body = StreamField(MyStreamBlock, null=True, blank=True)

    # Panels
    body_content_panels = [
        StreamFieldPanel('body'),
    ]

    template = 'coderedcms/pages/doc_page.html'


MARKDOWN_STREAMBLOCK = [
    ('markdown', MyStreamBlock())
]

@register_snippet
class ReusableMarkdownContent(models.Model):
    """
    Snippet for resusable markdown content in streamfields.
    """
    class Meta:
        verbose_name = _('Reusable Markdown Content')
        verbose_name_plural = _('Reusable Markdown Content')

    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )

    content = StreamField(MARKDOWN_STREAMBLOCK, blank=True, verbose_name='content')

    panels = [
        FieldPanel('name'),
        StreamFieldPanel('content')
    ]

    def __str__(self):
        return self.name


@register_snippet
class ReusableMarkdownCodeEntityContent(models.Model):
    """
    Snippet for resusable markdown content in streamfields.
    """
    class Meta:
        verbose_name = _('Reusable Code Entity Content')
        verbose_name_plural = _('Reusable Code Entity Content')

    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )

    content = StreamField(MARKDOWN_STREAMBLOCK, blank=True, verbose_name='content')

    panels = [
        FieldPanel('name'),
        StreamFieldPanel('content')
    ]

    def __str__(self):
        return self.name


class MarkdownContentBlock(ReusableContentBlock):
    """
    Enables choosing a ResusableContent snippet.
    """
    content = SnippetChooserBlock(ReusableMarkdownContent)

    class Meta:
        icon = 'fa-recycle'
        label = _('Reusable Markdown Content')
        template = 'coderedcms/blocks/reusable_markdown_content_block.html'


class DocPageWithReuseSupport(CoderedWebPage):
    """
    DocPage implements CoderedWebPage, with markdown editor integrated
    """
    class Meta:
        verbose_name = 'Doc page with reuse support'

    search_filterable = True
    search_db_include = True
    search_db_boost = 10

    REUSABLE_MARKDOWN_STREAMBLOCK = [
        ('markdown', MyStreamBlock()),
        ('reuse', MarkdownContentBlock())
    ]

    body = StreamField(REUSABLE_MARKDOWN_STREAMBLOCK, null=True, blank=True)

    # Panels
    body_content_panels = [
        StreamFieldPanel('body'),
    ]

    template = 'coderedcms/pages/doc_page_md_reuse.html'


class DocPageWithMediaAndReuseSupport(CoderedWebPage):
    """
    DocPage implements CoderedWebPage, with markdown editor integrated
    """
    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ['website.ArticleIndexPage']

    search_filterable = True
    search_db_include = True
    search_db_boost = 9

    template = 'coderedcms/pages/article_page.html'
    amp_template = 'coderedcms/pages/article_page.amp.html'
    search_template = 'coderedcms/pages/article_page.search.html'

    class Meta:
        verbose_name = 'Doc page with media and reuse support'
        ordering = ['-first_published_at']

    REUSABLE_MEDIA_MARKDOWN_STREAMBLOCK = [
        ('markdown', MyStreamBlock()),
        ('reuse', MarkdownContentBlock()),
        ('media', AgoraMediaBlock(icon='media')),
    ]

    body = StreamField(REUSABLE_MEDIA_MARKDOWN_STREAMBLOCK, null=True, blank=True)

    # Panels
    body_content_panels = [
        StreamFieldPanel('body'),
    ]


    template = 'coderedcms/pages/doc_page_md_media_reuse.html'


class DocPageWithMediaAndReuseSupportAndMenu(CoderedWebPage, MenuPageMixin):
    """
    DocPage implements CoderedWebPage, with markdown editor integrated @deprecated
    """

    add_submenu_item_for_news = models.BooleanField(default=False)

    search_filterable = True
    search_db_include = True
    search_db_boost = 8

    def modify_submenu_items(
            self, menu_items, current_page, current_ancestor_ids, current_site,
            allow_repeating_parents, apply_active_classes, original_menu_tag,
            menu_instance, request, use_absolute_page_urls
    ):
        menu_items = super(DocPageWithMediaAndReuseSupportAndMenu, self).modify_menu_items(
            menu_items, current_page, current_ancestor_ids,
            current_site, allow_repeating_parents, apply_active_classes,
            original_menu_tag, menu_instance, request, use_absolute_page_urls)

        if self.add_submenu_item_for_news:
            menu_items.append({
                'href': '/news/',
                'text': 'Read the news',
                'active_class': 'news-link',
            })
        return menu_items

    def has_submenu_items(
            self, current_page, allow_repeating_parents, original_menu_tag,
            menu_instance, request
    ):

        if self.add_submenu_item_for_news:
            return True
        return super(DocPageWithMediaAndReuseSupportAndMenu, self).has_submenu_items(
            current_page, allow_repeating_parents, original_menu_tag,
            menu_instance, request)

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ['website.ArticleIndexPage']

    template = 'coderedcms/pages/article_page.html'
    amp_template = 'coderedcms/pages/article_page.amp.html'
    search_template = 'coderedcms/pages/article_page.search.html'

    class Meta:
        verbose_name = '(DO NOT USE) Doc page with media and reuse , menu support'
        ordering = ['-first_published_at']

    REUSABLE_MEDIA_MARKDOWN_STREAMBLOCK = [
        ('markdown', MyStreamBlock()),
        ('reuse', MarkdownContentBlock()),
        ('media', AgoraMediaBlock(icon='media')),
    ]

    body = StreamField(REUSABLE_MEDIA_MARKDOWN_STREAMBLOCK, null=True, blank=True)

    # Panels
    body_content_panels = [
        StreamFieldPanel('body'),
    ]

    # wagtail-menus cannot be rendered, use coderedcms menu instead
    settings_panels = CoderedWebPage.settings_panels + [menupage_panel]

    template = 'coderedcms/pages/doc_page_md_media_reuse_menu.html'


class LanguageRedirectionPage(CoderedWebPage):

    def serve(self, request):
        # This will only return a language that is in the LANGUAGES Django setting
        language = translation.get_language_from_request(request)

        return HttpResponseRedirect(self.url + language + '/')


class TranslatablePageMixin(models.Model):
    # One link for each alternative language
    # These should only be used on the main language page (english)
    chinese_link = models.ForeignKey(Page, null=True, on_delete=models.SET_NULL, blank=True, related_name='+')
    japanese_link = models.ForeignKey(Page, null=True, on_delete=models.SET_NULL, blank=True, related_name='+')

    panels = [
        PageChooserPanel('chinese_link'),
        PageChooserPanel('japanese_link'),
    ]

    def get_language(self):
        """
        This returns the language code for this page.
        """
        # Look through ancestors of this page for its language homepage
        # The language homepage is located at depth 3
        language_homepage = self.get_ancestors(inclusive=True).get(depth=3)

        # The slug of language homepages should always be set to the language code
        return language_homepage.slug


    # Method to find the main language version of this page
    # This works by reversing the above links

    def english_page(self):
        """
        This finds the english version of this page
        """
        language = self.get_language()

        if language == 'en-us':
            return self
        elif language == 'zh-Hans':
            return type(self).objects.filter(chinese_link=self).first().specific
        elif language == 'ja':
            return type(self).objects.filter(japanese_link=self).first().specific

        # We need a method to find a version of this page for each alternative language.
        # These all work the same way. They firstly find the main version of the page
        # (english), then from there they can just follow the link to the correct page.

        def chinese_page(self):
            """
            This finds the chinese version of this page
            """
            english_page = self.english_page()

            if english_page and english_page.chinese_link:
                return english_page.chinese_link.specific

        def spanish_page(self):
            """
            This finds the japanese version of this page
            """
            english_page = self.english_page()

            if english_page and english_page.japanese_link:
                return english_page.japanese_link.specific

    class Meta:
            abstract = True


class DocPageWithMediaAndReuseSupportAndMultilanguage(CoderedWebPage, TranslatablePageMixin):
    """
    DocPage implements CoderedWebPage, with markdown editor integrated and multilanguage
    """
    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ['website.ArticleIndexPage']

    search_filterable = True
    search_db_include = True
    search_db_boost = 9

    template = 'coderedcms/pages/article_page.html'
    amp_template = 'coderedcms/pages/article_page.amp.html'
    search_template = 'coderedcms/pages/article_page.search.html'

    class Meta:
        verbose_name = 'Doc page with media and reuse support with multilan'
        ordering = ['-first_published_at']

    REUSABLE_MEDIA_MARKDOWN_STREAMBLOCK = [
        ('markdown', MyStreamBlock()),
        ('reuse', MarkdownContentBlock()),
        ('media', AgoraMediaBlock(icon='media')),
    ]

    body = StreamField(REUSABLE_MEDIA_MARKDOWN_STREAMBLOCK, null=True, blank=True)

    # Panels
    body_content_panels = [
        StreamFieldPanel('body'),
        MultiFieldPanel(TranslatablePageMixin.panels, 'Language links'),
    ]


    template = 'coderedcms/pages/doc_page_md_media_reuse.html'