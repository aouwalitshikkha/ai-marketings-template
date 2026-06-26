(function () {
  "use strict";

  var INACTIVE = ["bg-red-100", "text-red-800", "hover:bg-red-200"];
  var ACTIVE = ["bg-red-700", "text-white", "hover:bg-red-800"];
  var BADGE_INACTIVE = ["bg-red-200", "text-red-800"];
  var BADGE_ACTIVE = ["bg-red-800", "text-red-100"];

  var filterInput = document.getElementById("glossary-filter");
  var filterClear = document.getElementById("glossary-filter-clear");
  var groups = document.querySelectorAll(".glossary-group");
  var noMatch = document.getElementById("no-term-match");
  var noMatchQuery = document.getElementById("no-term-query");
  var navLinks = document.querySelectorAll(".group-link");
  var backBtn = document.getElementById("back-to-top");

  function applyLinkState(link, active) {
    link.dataset.active = active ? "true" : "false";
    var add = active ? ACTIVE : INACTIVE;
    var remove = active ? INACTIVE : ACTIVE;
    add.forEach(function (c) { link.classList.add(c); });
    remove.forEach(function (c) { link.classList.remove(c); });
    var badge = link.querySelector(".group-count-badge");
    if (badge) {
      var bAdd = active ? BADGE_ACTIVE : BADGE_INACTIVE;
      var bRemove = active ? BADGE_INACTIVE : BADGE_ACTIVE;
      bAdd.forEach(function (c) { badge.classList.add(c); });
      bRemove.forEach(function (c) { badge.classList.remove(c); });
    }
  }

  navLinks.forEach(function (link) { applyLinkState(link, false); });

  var debounceTimer;
  function runFilter() {
    var q = (filterInput.value || "").toLowerCase().trim();
    if (filterClear) filterClear.classList.toggle("hidden", !q);
    var anyVisible = false;

    groups.forEach(function (group) {
      var items = group.querySelectorAll(".term-item");
      var groupVisible = false;
      items.forEach(function (item) {
        var text = item.textContent.toLowerCase();
        var match = !q || text.indexOf(q) !== -1;
        item.style.display = match ? "" : "none";
        if (match) groupVisible = true;
      });
      group.style.display = groupVisible ? "" : "none";
      if (groupVisible) anyVisible = true;
    });

    if (noMatch) {
      noMatch.classList.toggle("hidden", anyVisible);
      if (noMatchQuery) noMatchQuery.textContent = q ? 'No terms match "' + q + '".' : "Try a different search term.";
    }
  }

  if (filterInput) {
    filterInput.addEventListener("input", function () {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(runFilter, 120);
    });
  }

  if (filterClear && filterInput) {
    filterClear.addEventListener("click", function () {
      filterInput.value = "";
      filterInput.focus();
      runFilter();
    });
  }

  if ("IntersectionObserver" in window && navLinks.length) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var id = entry.target.id;
          navLinks.forEach(function (link) {
            applyLinkState(link, link.getAttribute("data-target") === id);
          });
        }
      });
    }, { rootMargin: "-50% 0px -50% 0px" });
    groups.forEach(function (g) { observer.observe(g); });
  }

  var scrollTicking = false;
  if (backBtn) {
    window.addEventListener("scroll", function () {
      if (!scrollTicking) {
        window.requestAnimationFrame(function () {
          if (window.scrollY > 400) {
            backBtn.classList.remove("translate-y-20", "opacity-0", "pointer-events-none");
            backBtn.classList.add("translate-y-0", "opacity-100", "pointer-events-auto");
          } else {
            backBtn.classList.add("translate-y-20", "opacity-0", "pointer-events-none");
            backBtn.classList.remove("translate-y-0", "opacity-100", "pointer-events-auto");
          }
          scrollTicking = false;
        });
        scrollTicking = true;
      }
    }, { passive: true });
    backBtn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  var termLinks = document.querySelectorAll(".term-link");
  termLinks.forEach(function (link) {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      var termId = link.getAttribute("data-term");
      var url = window.location.origin + window.location.pathname + "#term-" + termId;
      var done = function () {
        var original = link.getAttribute("title");
        link.setAttribute("title", "Copied!");
        link.classList.add("text-red-600", "bg-red-50");
        setTimeout(function () {
          link.setAttribute("title", original);
          link.classList.remove("text-red-600", "bg-red-50");
        }, 1800);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(done).catch(function () {
          window.location.hash = "term-" + termId;
        });
      } else {
        var tmp = document.createElement("textarea");
        tmp.value = url;
        document.body.appendChild(tmp);
        tmp.select();
        try { document.execCommand("copy"); done(); } catch (err) { window.location.hash = "term-" + termId; }
        document.body.removeChild(tmp);
      }
    });
  });
})();
