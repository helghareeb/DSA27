-- Remove ::: {.handout-only} blocks. Used when building the SLIDE deck.
function Div (el)
  if el.classes:includes("handout-only") then
    return {}
  end
  return el
end
