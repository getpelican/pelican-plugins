# Comment Form (aka: never gather Metadata)
Add a form, which allows your visitors to easily write comments.

But more importantly, on submit the form generates a mailto-link.
The resulting email contains a valid markdown block. Now you only have to copy this block in a new file. And therefore there is no need to gather the metadata (like date, author, replyto) yourself.

#### Reply button
Add this in the "comment for loop" in your article theme, so your visitors can reply to a comment.

```html
<button onclick="reply('{{comment.slug | urlencode}}');">Reply</button>
```

#### Form
A basic form so your visitors can write comments.

```html
<form role="form" id="commentForm" action="#">
	<input name="Name" type="text" id="commentForm_inputName" placeholder="Enter your name or synonym">
	<textarea name="Text" id="commentForm_inputText" rows="10" style="resize:vertical;" placeholder="Your comment"></textarea>
	<button type="submit" id="commentForm_button">Post via email</button>
	<input name="replyto" type="hidden" id="commentForm_replyto">
</form>
```
You may want to add a button to reset the `replyto` field.

#### Javascript
To generate the mailto-Link and set the `replyto` field there is some javascript required.

```javascript
<script type="text/javascript">
	function reply(id)
	{
		id = decodeURIComponent(id);
		$('#commentForm_replyto').val(id);
	}

	$(document).ready(function() {
		function generateMailToLink()
		{
			var user = 'your_user_name'; //user@domain = your email address
			var domain = 'your_email_provider';
			var subject = 'Comment for \'{{ article.slug }}\'' ;

			var d = new Date();
			var body = ''
				+ 'Hey,\nI posted a new comment on ' + document.URL + '\n\nGreetings ' + $("#commentForm_inputName").val() + '\n\n\n'
				+ 'Raw comment data:\n'
				+ '----------------------------------------\n'
				+ 'date: ' + d.getFullYear() + '-' + (d.getMonth()+1) + '-' + d.getDate() + ' ' + d.getHours() + ':' + d.getMinutes() + '\n'
				+ 'author: ' + $("#commentForm_inputName").val() + '\n';

			var replyto = $('#commentForm_replyto').val();
			if (replyto.length != 0)
			{
				body += 'replyto: ' + replyto + '\n'
			}

			body += '\n'
				+ $("#commentForm_inputText").val() + '\n'
				+ '----------------------------------------\n';

			var link = 'mailto:' + user + '@' + domain + '?subject='
				+ encodeURIComponent(subject)
				+ "&body="
				+ encodeURIComponent(body);
			return link;
		}


		$('#commentForm').on("submit",
			function( event )
			{
				event.preventDefault();
				$(location).attr('href', generateMailToLink());
			}
		);
	});
</script>
```
(jQuery is required for this script)

Don't forget to set the Variables `user` and `domain`.
