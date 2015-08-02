# Org Reader

Publish Emacs Org files alongside the rest of your website or blag.

- `ORG_READER_EMACS_LOCATION`: Required. Location of Emacs binary.

- `ORG_READER_EMACS_SETTINGS`: Optional. An absolute path to an Elisp file, to
  run per invocation. Useful for initializing the `package` Emacs library if
  that's where your Org mode comes from, or any modifications to Org Export-
  related variables. If you want to use your standard emacs init file, you 
  can ignore this variable.

- `ORG_READER_BACKEND`: Optional. A custom backend to provide to Org. Defaults
  to 'html.

To provide metadata to Pelican, provide the following header in your Org file:

	#+TITLE: The Title Of This BlogPost
	#+DATE: <2001-01-01>
	#+CATEGORY: comma, separated, list, of, tags

The slug is automatically the filename of the Org file.
