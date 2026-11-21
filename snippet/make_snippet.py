# Builds the "ELI for Harvey" Script Lab snippet from the published ELI snippet (the gist ELI users import).
# Changes: own name/label, own storage (localStorage prefix + own IndexedDB), tools from apndrewn/eli-lite-data,
# templates still from apndrewn/eli-data, no credentials step on first run. Usage: python make_snippet.py <eli.yaml> <out.yaml>
import sys, yaml
src, out = sys.argv[1], sys.argv[2]
lines = open(src, encoding="utf-8").read().split("\n")

PRELUDE = r'''(function () {
  // ELI for Harvey: keep this snippet's settings apart from ELI's (Script Lab shares storage between snippets).
  var P = "eliH:", real = window.localStorage;
  function keys() { var a = []; try { for (var i = 0; i < real.length; i++) { var k = real.key(i); if (k && k.indexOf(P) === 0) a.push(k.slice(P.length)); } } catch (e) { } return a; }
  var shim = {
    getItem: function (k) { try { return real.getItem(P + k); } catch (e) { return null; } },
    setItem: function (k, v) { real.setItem(P + k, String(v)); },
    removeItem: function (k) { try { real.removeItem(P + k); } catch (e) { } },
    clear: function () { keys().forEach(function (k) { try { real.removeItem(P + k); } catch (e) { } }); },
    key: function (i) { return keys()[i] || null; }
  };
  Object.defineProperty(shim, "length", { get: function () { return keys().length; } });
  try { Object.defineProperty(window, "localStorage", { configurable: true, get: function () { return shim; } }); } catch (e) { }
  if (window.localStorage !== shim) {
    document.body && (document.body.innerHTML = "<p style='font:14px Arial;padding:16px'>ELI for Harvey could not keep its settings separate from ELI in this Script Lab, so it has stopped to protect ELI. Please tell Andrew.</p>");
    throw new Error("ELI for Harvey: storage separation unavailable");
  }
  if (!shim.getItem("eli_github_repo")) shim.setItem("eli_github_repo", "apndrewn/eli-data");
  if (!shim.getItem("eli_github_branch")) shim.setItem("eli_github_branch", "main");
  window.ELI_PROFILE = { id: "harvey", name: "ELI for Harvey", toolsRepo: "apndrewn/eli-lite-data" };
})();'''

def sub(old, new, count=1):
    global lines
    txt = "\n".join(lines); n = txt.count(old)
    assert n == count, (n, old[:60]); lines = txt.replace(old, new).split("\n")

sub("name: ELI 3.8", "name: ELI for Harvey")
sub("description: Creates a new snippet from a blank template.", "description: ELI's program tools (no AI) that complement Harvey. Tools from apndrewn/eli-lite-data.")
i = lines.index("  content: >+")
assert lines[i + 1] == ""
ins = []
for l in PRELUDE.split("\n"):
    ins += ["    " + l, ""]   # folded block scalar: a blank line between lines keeps each line break
lines[i + 2:i + 2] = ins
sub('const FEATURE_DB_NAME = "ELI_FeatureDB";', 'const FEATURE_DB_NAME = "ELI_FeatureDB_Harvey";')
sub('function _activeRepo() { try { return window.eli.compat.lsGet("eli_github_repo") || null; } catch (e) { return null; } }',
    'function _activeRepo() { return (window.ELI_PROFILE && window.ELI_PROFILE.toolsRepo) || null; }')
sub("            return importToken({\n              firstRun: true,\n              suppressSync: true,\n            }).then(function (result) {",
    '            return Promise.resolve({ kind: "envelope" }).then(function (result) {')
sub('label.innerHTML = "ELI<sup>AI</sup>";', 'label.innerHTML = "ELI<sup>for Harvey</sup>";')
sub('<span class=\\"app-label\\">ELI<sup>AI</sup></span>', '<span class=\\"app-label\\">ELI<sup>for Harvey</sup></span>')
open(out, "w", encoding="utf-8").write("\n".join(lines))

a = yaml.safe_load(open(src, encoding="utf-8")); b = yaml.safe_load(open(out, encoding="utf-8"))
assert set(a) == set(b) and b["name"] == "ELI for Harvey"
sa, sb = a["script"]["content"], b["script"]["content"]
assert sb.count("ELI_FeatureDB_Harvey") == 1 and "eliH:" in sb and "eli-lite-data" in sb
assert a["style"] == b["style"] and a["libraries"] == b["libraries"]
open(out + ".js", "w", encoding="utf-8").write(sb)
print("ok: script", len(sa), "->", len(sb), "chars")
