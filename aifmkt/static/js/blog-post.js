(function () {
  "use strict";

  var progressEl = document.getElementById("reading-progress");
  if (progressEl) {
    var onScroll = function () {
      var h = document.documentElement;
      var scrollable = h.scrollHeight - h.clientHeight;
      var pct = scrollable > 0 ? (h.scrollTop || document.body.scrollTop) / scrollable : 0;
      progressEl.style.width = (pct * 100).toFixed(2) + "%";
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    onScroll();
  }

  var content = document.querySelector(".ckeditor-content");
  var tocList = document.getElementById("toc-list");
  var tocEmpty = document.getElementById("toc-empty");
  var tocNav = document.getElementById("toc");
  if (content && tocList) {
    var headings = content.querySelectorAll("h2, h3");
    var fragment = document.createDocumentFragment();
    var idCounter = {};
    headings.forEach(function (h, i) {
      var text = (h.textContent || "").trim();
      if (!text) return;
      var baseId = (h.getAttribute("id") || ("sec-" + i + "-" + text.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, ""))).slice(0, 50);
      if (idCounter[baseId]) {
        idCounter[baseId] += 1;
        baseId = baseId + "-" + idCounter[baseId];
      } else {
        idCounter[baseId] = 1;
      }
      if (!h.getAttribute("id")) h.setAttribute("id", baseId);

      var li = document.createElement("li");
      var a = document.createElement("a");
      a.setAttribute("href", "#" + baseId);
      a.textContent = text;
      a.className = "block py-1 pl-3 border-l-2 border-transparent text-gray-500 hover:text-red-600 hover:border-red-600 transition " + (h.tagName === "H3" ? "pl-6 text-xs" : "");
      a.setAttribute("data-toc-target", baseId);
      li.appendChild(a);
      fragment.appendChild(li);
    });
    tocList.appendChild(fragment);
    if (headings.length === 0) {
      if (tocEmpty) tocEmpty.classList.remove("hidden");
      if (tocNav) tocNav.classList.add("hidden");
    }
  }

  var copyBtn = document.getElementById("copy-link-btn");
  if (copyBtn) {
    copyBtn.addEventListener("click", function () {
      var url = copyBtn.getAttribute("data-url") || window.location.href;
      var done = function () {
        var original = copyBtn.getAttribute("title");
        copyBtn.setAttribute("title", "Copied!");
        copyBtn.classList.add("bg-red-600", "text-white", "border-red-600");
        setTimeout(function () {
          copyBtn.setAttribute("title", original);
          copyBtn.classList.remove("bg-red-600", "text-white", "border-red-600");
        }, 1800);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(done).catch(function () {});
      } else {
        var tmp = document.createElement("textarea");
        tmp.value = url;
        document.body.appendChild(tmp);
        tmp.select();
        try { document.execCommand("copy"); } catch (e) {}
        document.body.removeChild(tmp);
        done();
      }
    });
  }
})();
