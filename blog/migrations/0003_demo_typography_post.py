from django.db import migrations
from django.utils import timezone


def add_demo_post(apps, schema_editor):
    Post = apps.get_model('blog', 'Post')
    Category = apps.get_model('blog', 'Category')
    Tag = apps.get_model('blog', 'Tag')
    User = apps.get_model('auth', 'User')

    user = User.objects.filter(is_superuser=True).first()
    if not user:
        return

    cat, _ = Category.objects.get_or_create(name='Design', defaults={'slug': 'design'})
    tag_demo, _ = Tag.objects.get_or_create(name='Typography', defaults={'slug': 'typography'})
    tag_design, _ = Tag.objects.get_or_create(name='Design', defaults={'slug': 'design'})

    post = Post.objects.create(
        title='Complete Typography Demo — See Every Style in Action',
        slug='typography-demo',
        author=user,
        category=cat,
        status='PB',
        publish_date=timezone.now(),
        short_answer='A comprehensive showcase of all typography elements: headings, paragraphs, blockquotes, lists, code blocks, tables, images, and more.',
        body="""
<h2>Heading Level 2 — The Main Section Title</h2>
<p>This is a standard paragraph. It demonstrates the base body text styling with <strong>bold text</strong>, <em>italic text</em>, <b>bold using the b tag</b>, and <i>italic using the i tag</i>. You can also have <code>inline code snippets</code> for technical terms. Here is a <a href="#">sample hyperlink</a> showing link styling with underline offset.</p>
<p>This second paragraph shows how paragraphs stack vertically. The spacing between consecutive paragraphs should be consistent and comfortable for reading. Long blocks of text like this help evaluate the line-height (leading) and overall readability of the content area. The goal is to make sure readers can scan through without fatigue.</p>

<h2>Heading Level 2 Again</h2>
<h3>Heading Level 3 — Subsection</h3>
<p>Level 3 headings are used for subsections. They should be visually distinct from H2 but still clearly part of the hierarchy. Notice the margin spacing above and below each heading level.</p>
<h4>Heading Level 4</h4>
<p>Level 4 headings are great for minor subsections within an H3 block. They use a lighter font weight and smaller size.</p>
<h5>Heading Level 5</h5>
<p>Level 5 is even smaller, used for very granular groupings.</p>
<h6>Heading Level 6</h6>
<p>Level 6 is the smallest heading — typically uppercase with letter spacing for labels or side notes.</p>

<hr />

<h2>Blockquotes</h2>
<p>Blockquotes are used to highlight quotes or call out important text. Here is what they look like:</p>
<blockquote>
<p>"Good typography is not just about choosing pretty fonts. It is about making your design easy and comfortable to read for your audience. The smallest detail can make the biggest difference."</p>
<cite>— A wise designer</cite>
</blockquote>
<p>A blockquote should stand out from the surrounding text with its left border accent, background color, and slightly larger italic text. The cite element at the bottom attributes the quote.</p>

<hr />

<h2>Lists</h2>
<h3>Unordered List (Bullets)</h3>
<ul>
<li>First item in an unordered list</li>
<li>Second item with more text to show line wrapping behavior and how list items stack vertically</li>
<li>Third item
<ul>
<li>Nested item at level 2</li>
<li>Another nested item</li>
</ul>
</li>
<li>Fourth item back at root level</li>
</ul>

<h3>Ordered List (Numbered)</h3>
<ol>
<li>Step one in a numbered procedure</li>
<li>Step two with additional explanation text that wraps to show proper indentation and alignment</li>
<li>Step three</li>
</ol>

<hr />

<h2>Code Blocks</h2>
<p>For longer code snippets, use the preformatted text block. It has a dark background and monospace font.</p>
<pre><code>// A sample JavaScript function
function greet(name) {
    const message = `Hello, ${name}!`;
    console.log(message);
    return message;
}

// Call the function
greet('World');</code></pre>
<p>Inline code like <code>npm install</code> or <code>git commit -m "message"</code> uses a different styling — light gray background with red text, suitable for short technical references.</p>

<hr />

<h2>Tables</h2>
<p>Data tables display structured information with clear headers and alternating row styling.</p>
<table>
<thead>
<tr>
<th>Feature</th>
<th>Free Plan</th>
<th>Pro Plan</th>
<th>Enterprise</th>
</tr>
</thead>
<tbody>
<tr>
<td>Users</td>
<td>1</td>
<td>10</td>
<td>Unlimited</td>
</tr>
<tr>
<td>Storage</td>
<td>5 GB</td>
<td>50 GB</td>
<td>1 TB</td>
</tr>
<tr>
<td>Support</td>
<td>Email</td>
<td>Priority</td>
<td>24/7 Dedicated</td>
</tr>
<tr>
<td>API Access</td>
<td>—</td>
<td>✓</td>
<td>✓</td>
</tr>
</tbody>
</table>

<hr />

<h2>Images &amp; Figures</h2>
<p>Images use the figure element with an optional caption for proper semantic markup.</p>
<figure>
<img src="https://picsum.photos/seed/typo-demo/1200/600" alt="Typography demo image" />
<figcaption>An example image showing proper figure and figcaption styling with rounded corners and shadow.</figcaption>
</figure>
<p>Images should be responsive, have rounded corners, and a subtle shadow. The caption is centered below in a smaller italic font.</p>

<hr />

<h2>Horizontal Rules</h2>
<p>Horizontal rules separate major sections with a subtle gradient line.</p>
<p>This is the paragraph above the rule.</p>
<hr />
<p>And this is the paragraph below it. The horizontal rule should have generous margin above and below.</p>
""",
    )
    post.tags.add(tag_demo, tag_design)


def remove_demo_post(apps, schema_editor):
    Post = apps.get_model('blog', 'Post')
    Post.objects.filter(slug='typography-demo').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_seed_demo_data'),
    ]

    operations = [
        migrations.RunPython(add_demo_post, remove_demo_post),
    ]
