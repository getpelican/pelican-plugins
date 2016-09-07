//requires jquery
var CommentSystem = {
	email_user:   "not set",
	email_domain: "not set",
	display_replyto_html: function(comment_content, article_slug, author) {return ''},

	cancelReply: function() {
		$('#commentForm_replyto').val("");
		$('#pcs-comment-form-display-replyto').hide();
	},

	setReply: function(slug, author) {
		slug   = decodeURIComponent(slug);
		author = decodeURIComponent(author);

		$('html, body').animate({ scrollTop: $("#pcs-comment-form").offset().top }, 1000);

		$('#pcs-comment-form-input-replyto').val(slug);

		var jquery_escaped_id = slug.replace('.', '\\.')
		var commentContent = $('#comment-' + jquery_escaped_id + ' .pcs-comment-content:first').text().trim()

		$('#pcs-comment-form-display-replyto').html(this.display_replyto_html(commentContent, slug, author));
		$('#pcs-comment-form-display-replyto').show();
	},

	getMailtoLink: function(slug) {
		var subject = 'Comment for \'' + slug + '\'' ;

		var now = new Date();
		tzo = -now.getTimezoneOffset(),
		dif = tzo >= 0 ? '+' : '-',
		pad = function(num) {
			norm = Math.abs(Math.floor(num));
			return (norm < 10 ? '0' : '') + norm;
		};
		var body = ''
			+ 'Hey,\nI posted a new comment on ' + document.URL + '\n\nGreetings ' + $("#pcs-comment-form-input-name").val() + '\n\n\n'
			+ 'Raw comment data:\n'
			+ '----------------------------------------\n'
			+ 'email: \n' // just that I don't forget to write it down
			+ 'date: ' + now.getFullYear()
					+ '-' + pad(now.getMonth()+1)
					+ '-' + pad(now.getDate())
					+ 'T' + pad(now.getHours())
					+ ':' + pad(now.getMinutes())
					+ dif + pad(tzo / 60)
					+ ':' + pad(tzo % 60) +'\n'
			+ 'author: ' + $("#pcs-comment-form-input-name").val() + '\n';

		var replyto = $('#pcs-comment-form-input-replyto').val();
		if (replyto.length != 0)
		{
			body += 'replyto: ' + replyto + '\n'
		}

		var url = $("#pcs-comment-form-input-website").val();
		if (url.length != 0)
		{
			if(url.substr(0,7) != 'http://' && url.substr(0,8) != 'https://'){
				url = 'http://' + url;
			}
			body += 'website: ' + url + '\n';
		}
		body += '\n'
			+ $("#pcs-comment-form-input-textarea").val() + '\n'
			+ '----------------------------------------\n';

		var link = 'mailto:' + this.email_user + '@' + this.email_domain + '?subject='
			+ encodeURIComponent(subject)
			+ "&body="
			+ encodeURIComponent(body.replace(/\r?\n/g, "\r\n"));
		console.log(link)
		return link;
	}
}
