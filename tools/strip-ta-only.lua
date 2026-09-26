-- Remove ::: {.ta-only} blocks. Used for everything students receive: the
-- per-lab PDFs and the students' edition of the lab manual. The TAs' edition is
-- built without this filter, and unwrap-divs.lua then unwraps the block.
function Div (el)
  if el.classes:includes("ta-only") then
    return {}
  end
  return el
end
