/**
 *
 * @source: https://github.com/getpelican/pelican-plugins/raw/master/i18n_subsites/accept-lang.js
 *
 * @licstart  The following is the entire license notice for the
 *  JavaScript code in this page.
 *
 * Copyright (C) 2018  Simon Descarpentries
 *
 *
 * The JavaScript code in this page is free software: you can
 * redistribute it and/or modify it under the terms of the GNU
 * General Public License (GNU GPL) as published by the Free Software
 * Foundation, either version 3 of the License, or (at your option)
 * any later version.  The code is distributed WITHOUT ANY WARRANTY;
 * without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.  See the GNU GPL for more details.
 *
 * As additional permission under GNU GPL version 3 section 7, you
 * may distribute non-source (e.g., minimized or compacted) forms of
 * that code without the copy of the GNU GPL normally required by
 * section 4, provided you include this license notice and a URL
 * through which recipients can access the Corresponding Source.
 *
 * @licend  The above is the entire license notice
 * for the JavaScript code in this page.
 *
 */

//
// jshint -W097
//

;(function (){
	'use strict'

	const FOUND = 0;
	var default_lang = default_lang || 'en';
	var page_lang = document.documentElement.lang;
	var nav_lang = navigator.language.slice(0,2);
	var domain_part = document.URL.split('/').slice(0,3).join('/');

	if (document.referrer.indexOf(domain_part) == FOUND || page_lang == nav_lang) {
		console.log('No need to change lang');
		return;
	}

	console.log('should change lang from '+page_lang+' to '+nav_lang);
	var slice_nb = page_lang != default_lang ? 4 : 3;  // default_lang has no lang prefix
	var page_part = document.URL.split('/').slice(slice_nb).join('/');
	var lang_link = domain_part;
	lang_link += nav_lang != default_lang ? '/'+nav_lang : '';
	lang_link += page_part ? '/'+page_part : '';  // avoid slash if index/no page_part
	var lang_sel = 'a[href="'+lang_link+'"]';
	console.log('search for '+lang_sel);
	var lang_node = document.querySelector(lang_sel);

	if (lang_node)
		lang_node.click();
}())
