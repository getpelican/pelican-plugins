pelican-rdf plugin
==================

A plugin for rdf vocabularies providers
---------------------------------------

# Overview
 
This plugin is intended at easing the lightwheight description of vocabularies online, in the fashion of http://vocab.linkeddata.es/. It offers a new media type, the Vocabulary, and a flexible mechanism to gather metadata about said vocabulary based on sparql queries.

# How it works

## Required configuration

### Description of the variables
Your pelicanconf.py should include new options : 
- **VOC_PATHS**: A list of paths to a local folders containing vocabularies. If all your vocabularies are remote, set its value to an empty list.
- **VOC_EXCLUDES**: A list of paths to folders where you don't want vocabularies to be processed. 
- **VOC_URIS** = A list of URLs pointing to dereferencable vocabularies. Content is negociated to retrieve RDF/XML.
- **VOC_QUERIES_PATH** = Path th the folder containing the sparql queries to collect metadata about the vocabulary.
- **VOCABULARY_URL**= How the generated document URL should look like
- **VOCABULARY_SAVE_AS**= How the generated document should be named

### Default configuration
```
VOC_PATHS=['ontologies']
VOC_EXCLUDES=[]
VOC_URIS = ["https://www.irit.fr/recherches/MELODI/ontologies/IoT-O",]
VOC_QUERIES_PATH = "plugins/pelican-rdf/sparql-queries"
VOCABULARY_URL= '{slug}.html'
VOCABULARY_SAVE_AS= '{slug}.html'
```

## Accessing the vocabulary metadata

### First, a simple example...
The following snippet of code outputs a description of the vocabularies that have been processed : 
```
<h1 class="page-header">
    Ontology repository
</h1>
{% if vocabularies %}
    <table class="table table-striped">
        <thead>
          <tr>
            <th>Title</th>
            <th>Description</th>
            <th>License (if any)</th>
          </tr>
        </thead>
        <tbody>
            {% for voc in vocabularies %}
                <tr>
                    <td><a href="{{ voc.iri }}">{{ voc.title }}</a></td>
                    <td>
                        <button class="btn btn-primary" type="button" data-toggle="collapse" data-target="#{{ voc.title }}description" aria-expanded="false" aria-controls="{{ voc.title }}description">
                            {{ voc.title }} description
                        </button>
                        <div class="collapse" id="{{ voc.title }}description">
                            <div class="card card-block">
                                {{ voc.description }}
                          </div>
                        </div>
                    </td>
                    <td>{{ voc.lov_metadata.license }}</td>
                <tr>
            {% endfor %}
        </tbody>
      </table>
{% endif %}
```

### ... but how does it work ?
The required properties (iri, title, version and description) are directly available in the vocabulary metadata. Notice that the license is accessed through a compound notation, explained in the next paragraph.

### Another example...
The following snippet outputs a list of the classes defined by the ontology, as well as its superclass (limited to one for the time being) and potential description (the comment).
```
{% for class in voc.classes %}
    <div>
        <h2>{{ class.class }}</h2>
        <h3>{{ class.superclass }}</h3>
        <p>{{ class.comment }}</p>
    </div>
{% endfor %}
```

### ... with custom metadata
To understand the example, one must look at the classes.sparql (the name is important) query : 
```
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dc:  <http://purl.org/dc/elements/1.1/>
PREFIX cc:  <http://creativecommons.org/ns#>
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>

SELECT ?class ?comment ?label ?superclass
WHERE {
    ?class rdf:type owl:Class.
    OPTIONAL { ?class rdfs:comment ?comment.}
    OPTIONAL { ?label rdfs:label ?label.}
    OPTIONAL { ?class rdfs:subClassOf ?superclass.}
} GROUP BY ?class
```

Each graph binding matching this sparql query is returned as a dictionnary in the vocabulary context, with the sparql projection attributes (here, class, comment, label and superclass) as keys. Then, this list of results is stored in the vocabulary metadata under the name of the query, here "classes". 

**NOTE**: The management of multiple values such as the multiple superclasses for a class is not yet handled correctly, it is a work in progress.