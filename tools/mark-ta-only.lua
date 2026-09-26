-- TAs' edition only: set each ::: {.ta-only} block in a shaded "For the TA" box,
-- so a TA reading aloud from the manual can see at a glance what students do not have.
function Div (el)
  if el.classes:includes("ta-only") and FORMAT:match("latex") then
    local out = { pandoc.RawBlock("latex", "\\begin{tanote}") }
    for _, b in ipairs(el.content) do table.insert(out, b) end
    table.insert(out, pandoc.RawBlock("latex", "\\end{tanote}"))
    return out
  end
  return el
end
