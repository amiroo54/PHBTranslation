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
  background: image("data/background.jpg", width: 110%),
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

#let level2-counter = counter("level2-count")

// Chapter headings
#show heading.where(level: 1): it => [

  #pagebreak()

  #place(
    top + center, 
    float: true,
    scope: "parent",
    clearance: 2em
  )[
    #text(
      size: 2.5em,
      weight: "black",
      fill: rgb("#7a1f1f")
    )[
      #it.body
    ]
    #line(length: 100%)
  ]

]


// Section headings
#show heading.where(level: 2): it => [

  #(if it.outlined { colbreak() })

  #v(1.5em)

  #align(center)[
    #text(
      size: 2.3em,
      weight: "bold",
      fill: rgb("#7a1f1f"),
    )[
      #it.body
    ]
  ]

  #line(length: 100%)
  #v(0.8em)
]


// Subsections
#show heading.where(level: 3): it => block[
  #v(0.8em)

  #text(
    size: 1.7em,
    weight: "bold",
    fill: rgb("#7a1f1f"),
  )[
    #it.body
  ]

  #line(length: 100%)

  #v(0.4em)
]


#show heading.where(level: 4): it => block[
  #v(0.5em)

  #text(
    size: 1.4em,
    weight: "bold",
  )[
    #it.body
  ]

  #v(0.3em)
]

// ---------- TABLES ----------

// Automatic table styling
#set table(
  fill: (_, y) => if y == 0 { none } else if calc.odd(y) { rgb("E9FFFD") } else { rgb("#D6F2EE") }, 
  stroke: none
)

// Table header
#show table.cell.where(y: 0): set text(
  weight: "bold",
) 

#show table: it => block(
  inset: 0.4em,
  radius: 4pt,
)[
  #it
]

#show table: it => context layout(parent-size => {
  //Avoid recursion which would occur since there is a call to #table later
  if it.has("label") and it.label == <already-processed> { return it }
  
  //Choose column type based on whether the table fills the width already
  let table-width = measure(it).width
  let already-fills-width = table-width >= parent-size.width * 0.9
  let col-type = if already-fills-width {(auto, )} else {(1fr, )}
  
  //Get how many columns there are in this table
  let num-col = it.fields().at("columns").len()
  
  //Extract the children (cells) and keep all the rest of the table arguments
  let (children, ..rest) = it.fields()
  //[Fills width: #already-fills-width, column type: #col-type\ Parent width: #parent-size.width, table width (theoretical): #table-width]
  [#table(
    ..children,
    ..rest,
    columns: col-type * num-col,
  )#label("already-processed")]
})

#show figure.where(
  kind: table
): set figure.caption(position: top)


// Automatic captions
#show figure.caption: set text(
  size: 9pt,
  style: "italic",
)

// ---------- QUOTES / FLAVOR TEXT ----------

#show quote: it => block(
  inset: 1em,
  fill: rgb("#eae3d7"),
  stroke: (
    right: 3pt + rgb("#7a1f1f"),
  ),
  radius: 3pt,
)[

  #it.body
]

// ---------- CODE ----------

#show raw: set text(
  font: "Vazirmatn",
  size: 8.5pt,
)

// ---------- OUTLINE ----------

#show outline.entry.where(
  level: 1
): set text(
  fill: rgb("#7a1f1f"),
  weight: "bold",
  )

#set page(columns: 3)
#heading(level: 2, outlined: false)[فهرست]
#outline(depth: 2, title: none)
 
// ---------- IMPORT MARKDOWN ----------

#import "@preview/cmarker:0.1.8"

#let column-count = int(sys.inputs.column-count)
#let text = sys.inputs.text

#set page(columns: column-count)

#cmarker.render(
  text,
  scope: (
    image: (source, alt: none, format: auto) => image(source, alt: alt, format: format),
    column-count: column-count,
    ),
)