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

#let red = rgb("#7a1f1f")

// Chapter headings
#show heading.where(level: 1): it => [

  #pagebreak()

  #place(
    top + center, 
    float: true,
    scope: "parent",
    clearance: 2em
  )[
    
    #set text(size: 2.5em, weight: "black", fill: red)
    #it
    
    #line(length: 100%)
  ]

]


// Section headings
#show heading.where(level: 2): it => [

  #(if it.outlined { colbreak() })

  #v(1.5em)

  #set text(size: 2.3em, weight: "bold", fill: red)
  #align(center)[
    #it
  ]

  #line(length: 100%)
  #v(0.8em)
]


// Subsections
#show heading.where(level: 3): it => block[
  #v(0.8em)

  #set text(size: 1.7em, weight: "bold", fill: red)
  #it

  #line(length: 100%)

  #v(0.4em)
]


#show heading.where(level: 4): it => block[
  #v(0.5em)

  #set text(size: 1.4em, weight: "bold")
  #it

  #v(0.3em)
]

#let to-string(it) = {
  if it == none {
    none
  }
  else if type(it) == str {
    it
  } else if type(it) != content {
    str(it)
  } else if it.has("text") {
    it.text
  } else if it.has("children") {
    it.children.map(to-string).join()
  } else if it.has("body") {
    to-string(it.body)
  } else if it == [ ] {
    ""
  }
}


#show heading.where(level: 6): it => {
  let match = to-string(it).match(regex(`^([^.]*)\.`.text)).text
  show match: text.with(fill: red)
  text(weight: "medium")[#it]
}


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

#set figure.caption(position: top)

#show figure.caption: it => [
  #align(right)[
    #text(size: 1.1em, weight: "extrabold", it.body)
  ]
]


#let figure = (attrs, body) => {
  
  show figure: set block(breakable: "breakable" in attrs.keys())
  
  let fig-class = attrs.at("class", default: "")

  if fig-class == "fr" {
    figure(caption: body.children.at(2))[
      #let (children, ..rest) = body.children.at(1).fields()
      #let len = rest.at("columns").len()
      #table(..children, ..rest, columns: (1fr, ) * len)
    ]
  }
  else if fig-class == "auto" {
    figure(caption: body.children.at(2))[
      #let (children, ..rest) = body.children.at(1).fields()
      #let len = rest.at("columns").len()
      #table(..children, ..rest, columns: (auto, ) * len)
    ]
  }
  else if fig-class == "multitable" {
    let table-count = body.children.len() - 3 // Two empties for the head and tail and the caption
    let multitable-counter = counter("multitable")
    multitable-counter.update(0)

    show table: it => {
      if it.has("label") and it.label == <already-processed> { return it }
      
      multitable-counter.step()
            
      let num-col = it.fields().at("columns").len()
      
      let (children, ..rest) = it.fields()
      [#table(
        ..children,
        ..rest,
        columns: (1fr, ) * num-col,
      )#label("already-processed")]

      context if multitable-counter.get().first() < table-count {
        colbreak()
      } 
    }

    figure(caption: body.children.at(table-count + 1))[
      #columns(table-count, gutter: 2pt)[
        #body.children.slice(1, table-count + 1).join()
      ]
    ]
  }
  else if fig-class == "spell-list" {
    figure(caption: body.children.at(2), body.children.at(1))  
  }
  else if fig-class == "wide" {
    show figure.where(kind: table): set figure(
      placement: auto,
      scope: "parent" 
    )
    figure(caption: body.children.at(2), body.children.at(1))
  }
  else {
    body
  }
}

// ---------- STAT BLOCKS ----------

#let stat-block = (attrs, body) => {
  let beige = rgb("#BDB1B1")
  let gray = rgb("#555555")
  
  block(
    stroke: 2pt + beige,
    radius: 10pt,
    inset: (top: 0.5em, left: 0.5em, right: 0.5em, bottom: 1em,),
    breakable: false
  )[
    #let color-state = state("color", false)
    #let header-state = state("header", false)

    #show par: it => {
      context {
        let is-action = color-state.at(it.location())
        let is-header = not header-state.at(it.location())
        let txt-color = if is-action and is-header { black } else { red } 
        let blk-spacing = if is-action { 1em } else { 0.7em }

        set text(fill: txt-color)
        set block(spacing: blk-spacing)

        block(it)

      }
    }

    #show heading.where(level: 3): it => block[
      #color-state.update(false)
      
      #set text(size: 1.9em, fill: red)
      #it.body
      #v(-0.8em)
      #line(length: 100%, stroke: 1pt + red)
    ]


    #show heading.where(level: 4): it => block[
      #header-state.update(true)

      #text(it.body, size: 1.3em, fill: red, weight: "extralight")
      #v(-0.5em)
      #line(length: 100%, stroke: 1pt + red)

      #header-state.update(false)
      #color-state.update(true)
    ]



    #show table.cell: set text(
      fill: red
    )

    #show table.cell.where(y: 0): it => {
      set text(
        size: 0.5em,
        fill: gray
      )
      set table.cell(
        inset: (top: 0pt, bottom: 0pt)
      )

      it
    }

    #set table(
      fill: (x, y) => if y == 0 { rgb(0,0, 0, 0%) } else if x >= 2 { rgb("#DAC8C8") } else { rgb("#E1D9D6") },
      stroke: none
    )


    #body
  ]
}

// ---------- QUOTES / FLAVOR TEXT ----------

#show quote: it => block(
  inset: 1em,
  fill: rgb("#eae3d7"),
  stroke: (
    right: 3pt + red,
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
  fill: red,
  weight: "bold",
  )

#set page(columns: 3)
#heading(level: 2, outlined: false)[فهرست]
#outline(depth: 2, title: none)
 
// ---------- IMPORT MARKDOWN ----------

#import "@preview/cmarker:0.1.10"

#let column-count = int(sys.inputs.column-count)
#let text = sys.inputs.text

#set page(columns: column-count)

#let html-dict = (
  figure: ("normal", (attrs, body) => figure(attrs, body)),
  statblock: ("normal", (attrs, body) => stat-block(attrs, body))
)

#cmarker.render(
  text,
  scope: (
    image: (source, alt: none, format: auto) => image(source, alt: alt, format: format),
    column-count: column-count,
    ),
  html: html-dict,
  // show-source: true,
)