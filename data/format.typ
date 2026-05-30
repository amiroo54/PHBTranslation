// ---------- PAGE SETUP ----------

#set page(
  paper: "a4",
  margin: (
    top: 1.6cm,
    bottom: 1.8cm,
    inside: 1.5cm,
    outside: 1.5cm,
  ),
  numbering: "۱",
)

// ---------- TEXT ----------

#set text(
  font: "Vazirmatn",
  size: 10pt,
  lang: "fa",
  dir: rtl,
)

// Better paragraph spacing
#set par(
  justify: true,
  leading: 0.65em,
)

// ---------- HEADINGS ----------

// Chapter headings
#show heading.where(level: 1): it => [

  #colbreak()

  #v(1.5em)

  #align(center)[
    #text(
      size: 26pt,
      weight: "bold",
      fill: rgb("#7a1f1f"),
    )[
      #it.body
    ]
  ]

  //#v(0.5em)

  #line(length: 100%)

  //#v(1em)
]

// Section headings
#show heading.where(level: 2): it => [
  #v(0.8em)

  #text(
    size: 16pt,
    weight: "bold",
    fill: rgb("#7a1f1f"),
  )[
    #it.body
  ]

  #line(length: 100%)

  #v(0.4em)
]

// Subsections
#show heading.where(level: 3): it => [
  #v(0.5em)

  #text(
    size: 13pt,
    weight: "bold",
  )[
    #it.body
  ]

  #v(0.3em)
]

// ---------- TABLES ----------

// Automatic table styling
#show table: it => block(
  inset: 0.4em,
  stroke: 0.6pt + gray,
  radius: 4pt,
  fill: luma(245),
  width: 100%,
)[
  #it
]

#show table: it => {
  if it.has("label") and it.label == <already-processed> { return it }
  
  let num-col = it.fields().at("columns").len()
  let num-col-auto = num-col - 1
  
  [#table(
    columns: (1fr, ) * num-col ,
    ..it.children
  )#label("already-processed")]
}

// Automatic captions
#show figure.caption: set text(
  size: 9pt,
  style: "italic",
)

// ---------- QUOTES / FLAVOR TEXT ----------

#show quote: it => block(
  inset: 1em,
  fill: rgb("#f8f1e5"),
  stroke: (
    left: 3pt + rgb("#7a1f1f"),
  ),
  radius: 3pt,
)[
  #set text(size: 9pt)

  #it.body
]

// ---------- CODE ----------

#show raw: set text(
  font: "Vazirmatn",
  size: 8.5pt,
)

#set page(columns: 3)
#outline(depth: 1)
#set page(columns: 2)

// ---------- IMPORT MARKDOWN ----------

#import "@preview/cmarker:0.1.8"

#let text = sys.inputs.text
//#cmarker.render(text)

#figure()