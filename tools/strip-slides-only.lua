-- Remove ::: {.slides-only} blocks. Used when building the HANDOUT.
function Div (el)
  if el.classes:includes("slides-only") then
    return {}
  end
  return el
end
