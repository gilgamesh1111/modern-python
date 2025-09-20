# {py:mod}`modern_python.wikipedia`

```{py:module} modern_python.wikipedia
```

```{autodoc2-docstring} modern_python.wikipedia
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Page <modern_python.wikipedia.Page>`
  - ```{autodoc2-docstring} modern_python.wikipedia.Page
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`random_page <modern_python.wikipedia.random_page>`
  - ```{autodoc2-docstring} modern_python.wikipedia.random_page
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`API_URL <modern_python.wikipedia.API_URL>`
  - ```{autodoc2-docstring} modern_python.wikipedia.API_URL
    :summary:
    ```
* - {py:obj}`headers <modern_python.wikipedia.headers>`
  - ```{autodoc2-docstring} modern_python.wikipedia.headers
    :summary:
    ```
````

### API

````{py:data} API_URL
:canonical: modern_python.wikipedia.API_URL
:value: >
   'https://{language}.wikipedia.org/api/rest_v1/page/random/summary'

```{autodoc2-docstring} modern_python.wikipedia.API_URL
```

````

````{py:data} headers
:canonical: modern_python.wikipedia.headers
:value: >
   None

```{autodoc2-docstring} modern_python.wikipedia.headers
```

````

`````{py:class} Page(/, **data: typing.Any)
:canonical: modern_python.wikipedia.Page

Bases: {py:obj}`pydantic.BaseModel`

```{autodoc2-docstring} modern_python.wikipedia.Page
```

```{rubric} Initialization
```

```{autodoc2-docstring} modern_python.wikipedia.Page.__init__
```

````{py:attribute} title
:canonical: modern_python.wikipedia.Page.title
:type: str
:value: >
   None

```{autodoc2-docstring} modern_python.wikipedia.Page.title
```

````

````{py:attribute} extract
:canonical: modern_python.wikipedia.Page.extract
:type: str
:value: >
   None

```{autodoc2-docstring} modern_python.wikipedia.Page.extract
```

````

`````

````{py:function} random_page(language: str = 'en') -> modern_python.wikipedia.Page
:canonical: modern_python.wikipedia.random_page

```{autodoc2-docstring} modern_python.wikipedia.random_page
```
````
