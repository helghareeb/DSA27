-- Set Arabic runs right-to-left for LaTeX output.
--
-- XeTeX does not reorder bidirectional text on its own, so an Arabic phrase in
-- an otherwise English document comes out with its words in reverse order, and
-- Arabic inside a code span is set in a monospace font with no Arabic glyphs at
-- all (XeLaTeX reports "Missing character" and drops it).
--
-- This filter finds each maximal run of consecutive Arabic words and wraps the
-- WHOLE run in one \textarabic{...}. Wrapping word by word is not enough: each
-- word would be reversed correctly but the words themselves would still be laid
-- out left to right, so the phrase would read backwards.
--
-- No-op for any output format that is not LaTeX or Beamer.

local function is_latex ()
  return FORMAT:match("latex") ~= nil or FORMAT:match("beamer") ~= nil
end

-- UTF-8 lead bytes for the Arabic blocks:
--   U+0600-U+06FF -> 0xD8..0xDB   U+0750-U+077F -> 0xDD
--   U+FB50-U+FEFF -> 0xEF (Arabic Presentation Forms)
local function has_arabic (s)
  return s:find("[\216\217\218\219\221]") ~= nil
end

-- ASCII punctuation at either edge of a run -- "(", ")", ".", ",", ";", quotes --
-- is kept OUT of the Arabic font. Noto Sans Arabic has no Latin punctuation, so
-- inside \textarabic it printed as an empty box; outside, it is set in the text
-- font, and in an English sentence "(" + Arabic + ")" reads correctly.
local function arabic (text)
  local pre, core, post = text:match("^([%p%s]*)(.-)([%p%s]*)$")
  if core == "" then return pandoc.Str(text) end
  local out = pandoc.Inlines{}
  if pre ~= "" then out:insert(pandoc.Str(pre)) end
  out:insert(pandoc.RawInline("latex", "\\textarabic{" .. core .. "}"))
  if post ~= "" then out:insert(pandoc.Str(post)) end
  return out
end

-- Only Inlines is defined, deliberately. Pandoc applies element filters (Str,
-- Code) before the surrounding list filter, so a Str filter here would have
-- already replaced the words with RawInline and there would be nothing left to
-- merge into a run.
function Inlines (inlines)
  if not is_latex() then return nil end

  local out = pandoc.Inlines{}
  local run = nil

  local function flush ()
    if run then
      out:extend(arabic(run))
      run = nil
    end
  end

  for i, el in ipairs(inlines) do
    if el.t == "Str" and has_arabic(el.text) then
      run = run and (run .. " " .. el.text) or el.text
    elseif el.t == "Space" and run then
      -- Hold the space back: it is re-added above if the run continues.
      local nxt = inlines[i + 1]
      if not (nxt and nxt.t == "Str" and has_arabic(nxt.text)) then
        flush()
        out:insert(el)
      end
    elseif el.t == "Code" and has_arabic(el.text) then
      -- A code span holding Arabic cannot stay monospace.
      flush()
      out:extend(arabic(el.text))
    else
      flush()
      out:insert(el)
    end
  end

  flush()
  return out
end
