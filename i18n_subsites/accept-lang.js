// name   : accept-lang.js
// author : Simon Descarpentries, simon /\ acoeuro [] com
// date   : 2018-01
// licence: GPLv3
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
