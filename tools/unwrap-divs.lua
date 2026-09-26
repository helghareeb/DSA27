-- Replace any surviving handout-only / slides-only Div with its own children,
-- so pandoc does not emit an empty LaTeX environment around them.
function Div (el)
  if el.classes:includes("handout-only") or el.classes:includes("slides-only")
     or el.classes:includes("ta-only") then
    return el.content
  end
  return el
end
