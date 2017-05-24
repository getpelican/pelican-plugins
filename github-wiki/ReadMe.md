# GitHub Wiki
A plugin to convert a flat GitHub wiki into a structured 'read-only' wiki on your pelican site.

## Usage

The plugin looks for a GitHub style wiki (flat collection of md files) at `content\wiki`. You can clone a wiki with:

    git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.wiki.git

And you can also do clever things to set this up as a submodule of your main pelican site repo.

The plugin needs a `wikiarticle.html` template in your theme templates folder. An example template file is provided. 

The resulting wiki will be available at `output\wiki`. 

## Structure

By default the generated wiki will also be flat with no heirarchy to the pages. This plugin allows you to automatically generate a virtual file structure.

In order to provide a structure to the wiki each page can be given the `Path:` metadata.

    Path: foo/bar/baz

This will allow a correctly set up template to generate breadcrumbs and a structured menu where this page will be under the `foo/bar/baz`. Note: The plugin does not actually make this folder structure in the output (this is to make is easier to associate the 
generated pages with their original wiki pages). 

If a page has the same name and location in the structure as a virtual folder (i.e For the path given above, a file called `bar.md` with the path `Path: foo`) then the breadcrumbs and menu can link to that page as though it were the index of that vritual folder.

## Template

The template is given the following variables.

- `content`: The template has the usual `content` variable available for the converted html of the wiki page. 
- `breadcrumbs`: A list of tuples describing a 'path' to the current wiki page. The first value is the name of a parent page (in order). The second value is either 'a' or 'p'. 'a' means that the parent page exists and can be linked to, 'p' means the parent page 
doesn't 
exist and is just there for descriptibe purposes.
- `links`: A list of tuples describing a site map of the wiki. The first value is the name of the page, the second value is either 'indexdir' or 'noindexdir' if the page has or does not have subpages respectively, and the third value is the level of the page 
within the wiki (how many parents it has).

Also provided is a simple javascript file to make the structured menu in the example template openable/closable. 

Though you cannot edit this 'wiki' directly from your site an example of how to emulate wiki editing behaviour is shown in the example template. You can link directly to the github edit page for the wiki page you're on allowing your Github contributers to very 
easily edit pages. Combined with hooks to redeploy your wiki this can emulate a real wiki quite well.
